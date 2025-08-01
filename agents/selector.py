from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Session

# Существующие статические агенты (не трогаем)
from agents.agno_assist import get_agno_assist
from agents.finance_agent import get_finance_agent
from agents.web_agent import get_web_agent

# Новая функциональность для динамических агентов
from agents.tools_loader import load_tools_for_agent
from agents.agent_cache import agent_cache  # ← КЭШ С УЧЕТОМ КОНФИГУРАЦИЙ
from agents.tool_hooks import get_tool_hooks
from agents.response_models import get_response_model
from agents.team_manager import get_team_manager
from db.models.agent import DynamicAgent
from db.session import get_db

# Нативные agno классы
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from db.session import db_url

# Простой кэш для списка агентов (TTL 5 минут)
_available_agents_cache = {"data": None, "expires_at": 0}


def invalidate_available_agents_cache():
    """Принудительная инвалидация кэша списка агентов (для CREATE/DELETE операций)"""
    global _available_agents_cache
    _available_agents_cache["data"] = None
    _available_agents_cache["expires_at"] = 0


class AgentType(Enum):
    WEB_AGENT = "web_agent"
    AGNO_ASSIST = "agno_assist"
    FINANCE_AGENT = "finance_agent"


def get_available_agents(db: Optional[Session] = None) -> List[str]:
    """Возвращает список всех доступных агентов (статических + динамических)"""
    import time
    
    # Проверяем кэш (TTL 5 минут для списка агентов)
    now = time.time()
    if _available_agents_cache["data"] and now < _available_agents_cache["expires_at"]:
        return _available_agents_cache["data"]
    
    # Статические агенты
    static_agents = [agent.value for agent in AgentType]
    
    # Динамические агенты из БД
    if db is None:
        db = next(get_db())
    
    try:
        dynamic_agents = db.query(DynamicAgent.agent_id).filter(
            DynamicAgent.is_active == True
        ).all()
        dynamic_agent_ids = [agent.agent_id for agent in dynamic_agents]
        
        result = static_agents + dynamic_agent_ids
        
        # Кэшируем результат на 5 минут
        _available_agents_cache["data"] = result
        _available_agents_cache["expires_at"] = now + 300  # 5 минут
        
        return result
    except Exception:
        # Если БД недоступна, возвращаем только статические
        return static_agents


def get_agent(
    model_id: str = "gpt-4.1-mini-2025-04-14",
    agent_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
    db: Optional[Session] = None
):
    """Получает агента любого типа с кэшем, учитывающим конфигурации"""
    
    # 1. Сначала проверяем статические агенты (не трогаем, без кэша)
    if agent_id == AgentType.WEB_AGENT.value:
        return get_web_agent(model_id=model_id, user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    elif agent_id == AgentType.AGNO_ASSIST.value:
        return get_agno_assist(model_id=model_id, user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    elif agent_id == AgentType.FINANCE_AGENT.value:
        return get_finance_agent(model_id=model_id, user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    
    # 2. Динамические агенты - получаем конфигурацию из БД
    if db is None:
        db = next(get_db())
    
    # Ищем динамического агента (сначала пользовательского, потом глобального)
    dynamic_agent = db.query(DynamicAgent).filter(
        DynamicAgent.agent_id == agent_id,
        DynamicAgent.is_active == True
    ).order_by(
        DynamicAgent.user_id == user_id,  # Пользовательские агенты приоритетнее
        DynamicAgent.user_id.is_(None)    # Потом глобальные
    ).first()
    
    if not dynamic_agent:
        raise ValueError(f"Agent: {agent_id} not found")
    
    # 3. Проверяем кэш с учетом конфигурации ⚡
    cached_agent = agent_cache.get(agent_id, model_id, user_id, debug_mode, dynamic_agent)
    if cached_agent:
        # Обновляем только session_id (может меняться между запросами)
        cached_agent.session_id = session_id
        return cached_agent
    
    # 4. Создаем агента и кэшируем с конфигурацией
    agent = _create_agent_from_db(dynamic_agent, model_id, user_id, session_id, debug_mode, db)
    # Кэшируем созданного агента с текущей конфигурацией
    agent_cache.set(agent, model_id, user_id, debug_mode, dynamic_agent)
    return agent


def _create_agent_from_db(
    dynamic_agent: DynamicAgent, 
    model_id: str,
    user_id: Optional[str], 
    session_id: Optional[str],
    debug_mode: bool,
    db: Session
) -> Agent:
    """Создает нативный agno Agent из данных БД с полными конфигурациями"""
    
    # Модель (как в существующих агентах)
    model_config = dynamic_agent.model_config or {}
    final_model_id = model_id or model_config.get("id", "gpt-4.1-mini-2025-04-14")
    
    # Создаем основную модель с полными настройками
    model_params = {
        "id": final_model_id,
        "temperature": model_config.get("temperature"),
        "max_tokens": model_config.get("max_tokens"),
        "max_completion_tokens": model_config.get("max_completion_tokens"),
        "top_p": model_config.get("top_p"),
        "frequency_penalty": model_config.get("frequency_penalty"),
        "presence_penalty": model_config.get("presence_penalty"),
        "seed": model_config.get("seed"),
        "stop": model_config.get("stop"),
        "reasoning_effort": model_config.get("reasoning_effort"),
        "store": model_config.get("store"),
        "metadata": model_config.get("metadata"),
        "modalities": model_config.get("modalities"),
        "audio": model_config.get("audio"),
        "api_key": model_config.get("api_key"),
        "organization": model_config.get("organization"),
        "base_url": model_config.get("base_url"),
        "timeout": model_config.get("timeout"),
        "max_retries": model_config.get("max_retries"),
    }
    # Убираем None значения
    model_params = {k: v for k, v in model_params.items() if v is not None}
    model = OpenAIChat(**model_params)
    
    # Инструменты из БД с кэшированием
    tools = load_tools_for_agent(db, dynamic_agent.tool_ids or [])
    
    # Получаем конфигурацию агента
    agent_config = dynamic_agent.agent_config or {}
    
    # Storage (опционально, как Memory и Knowledge)
    storage = None
    storage_config = agent_config.get("storage")
    if storage_config is not None:  # Секция storage есть в конфиге
        if storage_config.get("enabled", True):  # enabled по умолчанию True ТОЛЬКО если секция storage указана
            storage_table = storage_config.get("table_name", "sessions")
            storage = PostgresAgentStorage(
                table_name=storage_table, 
                db_url=db_url,
                schema="public"
            )
    
    # Memory (КРИТИЧНО для continue endpoint!)
    memory = None
    memory_config = agent_config.get("memory", {})
    if memory_config.get("enabled", False):
        from agno.memory.v2.db.postgres import PostgresMemoryDb
        from agno.memory.v2.memory import Memory
        
        memory_table = memory_config.get("table_name", "user_memories")
        memory = Memory(
            model=OpenAIChat(id=final_model_id),
            db=PostgresMemoryDb(
                table_name=memory_table, 
                db_url=db_url,
                schema="public"
            ),
            delete_memories=memory_config.get("delete_memories", True),
            clear_memories=memory_config.get("clear_memories", True),
        )
    
    # Knowledge (RAG система)
    knowledge = None
    knowledge_config = agent_config.get("knowledge", {})
    if knowledge_config.get("enabled", False):
        # Поддержка различных типов знаний
        knowledge_type = knowledge_config.get("type", "url")
        if knowledge_type == "url" and knowledge_config.get("urls"):
            from agno.knowledge.url import UrlKnowledge
            from agno.vectordb.pgvector import PgVector
            
            knowledge = UrlKnowledge(
                urls=knowledge_config["urls"],
                vector_db=PgVector(
                    db_url=db_url,
                    table_name=knowledge_config.get("table_name", "knowledge"),
                    schema="public"
                )
            )
        elif knowledge_type == "pdf" and knowledge_config.get("pdf_paths"):
            from agno.knowledge.pdf import PDFKnowledge
            from agno.vectordb.pgvector import PgVector
            
            knowledge = PDFKnowledge(
                path=knowledge_config["pdf_paths"],
                vector_db=PgVector(
                    db_url=db_url,
                    table_name=knowledge_config.get("table_name", "knowledge"),
                    schema="public"
                )
            )
    
    # Reasoning модель (для сложных рассуждений)
    reasoning_model = None
    reasoning_config = agent_config.get("reasoning", {})
    if reasoning_config.get("enabled", False):
        reasoning_model_id = reasoning_config.get("model_id", final_model_id)
        reasoning_model = OpenAIChat(id=reasoning_model_id)
    
    # Parser модель (для парсинга ответов)
    parser_model = None
    parser_config = agent_config.get("parser", {})
    if parser_config.get("enabled", False):
        parser_model_id = parser_config.get("model_id", final_model_id)
        parser_model = OpenAIChat(id=parser_model_id)
    
    # History настройки
    history_config = agent_config.get("history", {})
    
    # Инструкции
    instructions = dynamic_agent.system_instructions or []
    if isinstance(instructions, list):
        instructions = "\n".join(instructions)
    
    # Создаем нативный agno Agent с ПОЛНЫМИ конфигурациями
    agent_params = {
        # 1. Основные настройки агента
        "name": dynamic_agent.name,
        "agent_id": dynamic_agent.agent_id,
        "model": model,
        "introduction": agent_config.get("introduction"),
        
        # 2. Пользовательские настройки
        "user_id": user_id,
        
        # 3. Настройки сессии
        "session_id": session_id,
        "session_name": agent_config.get("session_name"),
        "session_state": agent_config.get("session_state"),
        "search_previous_sessions_history": agent_config.get("search_previous_sessions_history", False),
        "num_history_sessions": agent_config.get("num_history_sessions"),
        "cache_session": agent_config.get("cache_session", True),
        
        # 4. Контекст агента
        "context": agent_config.get("context"),
        "add_context": agent_config.get("add_context", False),
        "resolve_context": agent_config.get("resolve_context", True),
        
        # 5. Память агента
        "memory": memory,
        "enable_agentic_memory": agent_config.get("enable_agentic_memory", False),
        "enable_user_memories": agent_config.get("enable_user_memories", False),
        "add_memory_references": agent_config.get("add_memory_references"),
        "enable_session_summaries": agent_config.get("enable_session_summaries", False),
        "add_session_summary_references": agent_config.get("add_session_summary_references"),
        
        # 6. История агента
        "add_history_to_messages": history_config.get("add_history_to_messages", True),
        "num_history_responses": history_config.get("num_history_responses"),
        "num_history_runs": history_config.get("num_history_runs", 3),
        
        # 7. Знания агента
        "knowledge": knowledge,
        "knowledge_filters": agent_config.get("knowledge_filters"),
        "enable_agentic_knowledge_filters": agent_config.get("enable_agentic_knowledge_filters", False),
        "add_references": agent_config.get("add_references", False),
        "retriever": agent_config.get("retriever"),
        "references_format": agent_config.get("references_format", "json"),
        
        # 8. Хранилище агента
        "storage": storage,
        "extra_data": agent_config.get("extra_data"),
        
        # 9. Инструменты агента
        "tools": tools,
        "show_tool_calls": agent_config.get("show_tool_calls", True),
        "tool_call_limit": agent_config.get("tool_call_limit"),
        "tool_choice": agent_config.get("tool_choice"),
        "tool_hooks": _get_tool_hooks_from_config(agent_config.get("tool_hooks")),
        
        # 9.2 Стандартные инструменты
        "read_chat_history": history_config.get("read_chat_history", True),
        "search_knowledge": agent_config.get("search_knowledge", True),
        "update_knowledge": agent_config.get("update_knowledge", False),
        "read_tool_call_history": agent_config.get("read_tool_call_history", False),
        
        # 10. Рассуждения агента
        "reasoning": reasoning_config.get("enabled", False),
        "reasoning_model": reasoning_model,
        "reasoning_agent": agent_config.get("reasoning_agent"),
        "reasoning_min_steps": reasoning_config.get("min_steps", 1),
        "reasoning_max_steps": reasoning_config.get("max_steps", 10),
        
        # 11. Системные сообщения
        "system_message": agent_config.get("system_message"),
        "system_message_role": agent_config.get("system_message_role", "system"),
        "create_default_system_message": agent_config.get("create_default_system_message", True),
        
        # 11.2 Построение системного сообщения
        "description": dynamic_agent.description,
        "goal": dynamic_agent.goal or agent_config.get("goal"),  # Приоритет: DB поле -> agent_config
        "instructions": instructions,
        "expected_output": dynamic_agent.expected_output or agent_config.get("expected_output"),  # Приоритет: DB поле -> agent_config
        "additional_context": agent_config.get("additional_context"),
        "markdown": agent_config.get("markdown", True),
        "add_name_to_instructions": agent_config.get("add_name_to_instructions", False),
        "add_datetime_to_instructions": agent_config.get("add_datetime_to_instructions", True),
        "add_location_to_instructions": agent_config.get("add_location_to_instructions", False),
        "timezone_identifier": agent_config.get("timezone_identifier"),
        "add_state_in_messages": agent_config.get("add_state_in_messages", True),
        
        # 12. Дополнительные сообщения
        "add_messages": agent_config.get("add_messages"),
        "success_criteria": agent_config.get("success_criteria"),
        
        # 13. Пользовательские сообщения
        "user_message": agent_config.get("user_message"),
        "user_message_role": agent_config.get("user_message_role", "user"),
        "create_default_user_message": agent_config.get("create_default_user_message", True),
        
        # 14. Настройки ответа агента
        "retries": agent_config.get("retries", 0),
        "delay_between_retries": agent_config.get("delay_between_retries", 1),
        "exponential_backoff": agent_config.get("exponential_backoff", False),
        
        # 14.2 Модель ответа и парсинг
        "response_model": _get_response_model_from_config(agent_config.get("response_model")),
        "parser_model": parser_model,
        "parser_model_prompt": parser_config.get("prompt"),
        "parse_response": agent_config.get("parse_response", True),
        "structured_outputs": agent_config.get("structured_outputs"),
        "use_json_mode": agent_config.get("use_json_mode", False),
        "save_response_to_file": agent_config.get("save_response_to_file"),
        
        # 15. Потоковая передача
        "stream": agent_config.get("stream"),
        "stream_intermediate_steps": agent_config.get("stream_intermediate_steps", False),
        "store_events": agent_config.get("store_events", False),
        "events_to_skip": agent_config.get("events_to_skip"),
        
        # 16. Команда агентов
        "team": _get_team_from_config(agent_config.get("team"), db, user_id, debug_mode),
        "team_data": agent_config.get("team_data"),
        "role": dynamic_agent.role or agent_config.get("role"),  # Приоритет: DB поле -> agent_config
        "respond_directly": agent_config.get("respond_directly", False),
        "add_transfer_instructions": agent_config.get("add_transfer_instructions", True),
        "team_response_separator": agent_config.get("team_response_separator", "\n"),
        "team_session_id": agent_config.get("team_session_id"),
        "team_id": agent_config.get("team_id"),
        "team_session_state": agent_config.get("team_session_state"),
        
        # 17. Приложение и Workflow
        "app_id": agent_config.get("app_id"),
        "workflow_id": agent_config.get("workflow_id"),
        "workflow_session_id": agent_config.get("workflow_session_id"),
        "workflow_session_state": agent_config.get("workflow_session_state"),
        
        # 18. Отладка и мониторинг
        "debug_mode": agent_config.get("debug_mode", debug_mode),
        "debug_level": agent_config.get("debug_level", 1),
        "monitoring": agent_config.get("monitoring", False),
        "telemetry": agent_config.get("telemetry", True),
    }
    
    # Убираем None значения для чистоты
    agent_params = {k: v for k, v in agent_params.items() if v is not None}
    
    return Agent(**agent_params)


def _get_tool_hooks_from_config(tool_hooks_config):
    """
    Обработка tool_hooks конфигурации - поддержка имен и объектов
    
    Args:
        tool_hooks_config: Конфигурация из agent_config.tool_hooks
        
    Returns:
        Список hook функций или None
    """
    if not tool_hooks_config:
        return None
        
    if isinstance(tool_hooks_config, list):
        if all(isinstance(h, str) for h in tool_hooks_config):
            # Список имен hook'ов - загружаем из реестра
            return get_tool_hooks(tool_hooks_config)
        else:
            # Уже список функций (для совместимости)
            return tool_hooks_config
    
    return None


def _get_response_model_from_config(response_model_config):
    """
    Обработка response_model конфигурации - поддержка имен моделей
    
    Args:
        response_model_config: Конфигурация из agent_config.response_model
        
    Returns:
        Pydantic модель или None
    """
    if not response_model_config:
        return None
    
    if isinstance(response_model_config, str):
        # Имя модели - загружаем из реестра
        model_class = get_response_model(response_model_config)
        if not model_class:
            from agno.utils.log import log_warning
            log_warning(f"Response model '{response_model_config}' not found in registry")
        return model_class
    else:
        # Уже объект класса (для совместимости)
        return response_model_config


def _get_team_from_config(team_config, db, user_id, debug_mode):
    """
    Обработка team конфигурации - поддержка agent_id ссылок
    
    Args:
        team_config: Конфигурация из agent_config.team 
        db: Сессия базы данных
        user_id: ID пользователя для контекста
        debug_mode: Режим отладки
        
    Returns:
        Список Agent объектов или None
    """
    if not team_config:
        return None
    
    if isinstance(team_config, list):
        if all(isinstance(agent_id, str) for agent_id in team_config):
            # Список agent_id - создаем команду через TeamManager
            team_manager = get_team_manager(db)
            team_agents = team_manager.build_team(
                team_config, 
                user_id=user_id, 
                debug_mode=debug_mode
            )
            return team_agents if team_agents else None
        else:
            # Уже список Agent объектов (для совместимости)
            return team_config
    
    return None
