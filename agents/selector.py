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
    model = OpenAIChat(id=final_model_id)
    
    # Инструменты из БД с кэшированием
    tools = load_tools_for_agent(db, dynamic_agent.tool_ids or [])
    
    # Получаем конфигурацию агента
    agent_config = dynamic_agent.agent_config or {}
    
    # Storage (как в существующих агентах)
    storage_config = agent_config.get("storage", {})
    storage_table = storage_config.get("table_name", "sessions")  # Используем общую таблицу sessions
    storage = PostgresAgentStorage(
        table_name=storage_table, 
        db_url=db_url,
        schema="public"  # Явно указываем схему public
    )
    
    # Memory (КРИТИЧНО для continue endpoint!)
    memory = None
    enable_agentic_memory = False
    
    memory_config = agent_config.get("memory", {})
    if memory_config.get("enabled", False):
        from agno.memory.v2.db.postgres import PostgresMemoryDb
        from agno.memory.v2.memory import Memory
        
        memory_table = memory_config.get("table_name", "user_memories")  # Используем общую таблицу памяти
        memory = Memory(
            model=OpenAIChat(id=final_model_id),
            db=PostgresMemoryDb(
                table_name=memory_table, 
                db_url=db_url,
                schema="public"  # Явно указываем схему public
            ),
            delete_memories=memory_config.get("delete_memories", True),
            clear_memories=memory_config.get("clear_memories", True),
        )
        enable_agentic_memory = agent_config.get("enable_agentic_memory", True)
    
    # History настройки
    history_config = agent_config.get("history", {})
    add_history_to_messages = history_config.get("add_history_to_messages", True)
    num_history_runs = history_config.get("num_history_runs", 3)
    read_chat_history = history_config.get("read_chat_history", True)
    
    # Инструкции
    instructions = dynamic_agent.system_instructions or []
    if isinstance(instructions, list):
        instructions = "\n".join(instructions)
    
    # Другие настройки
    add_state_in_messages = agent_config.get("add_state_in_messages", True)
    markdown = agent_config.get("markdown", True)
    add_datetime_to_instructions = agent_config.get("add_datetime_to_instructions", True)
    debug_mode = agent_config.get("debug_mode", debug_mode)
    
    # Создаем нативный agno Agent с полными конфигурациями
    return Agent(
        name=dynamic_agent.name,
        agent_id=dynamic_agent.agent_id,
        user_id=user_id,
        session_id=session_id,
        model=model,
        tools=tools,  # Нативные agno инструменты
        description=dynamic_agent.description,
        instructions=instructions,
        storage=storage,
        # -*- Memory (критично для continue endpoint) -*-
        memory=memory,
        enable_agentic_memory=enable_agentic_memory,
        # -*- History -*-
        add_history_to_messages=add_history_to_messages,
        num_history_runs=num_history_runs,
        read_chat_history=read_chat_history,
        # -*- Other settings -*-
        add_state_in_messages=add_state_in_messages,
        markdown=markdown,
        add_datetime_to_instructions=add_datetime_to_instructions,
        debug_mode=debug_mode
    )
