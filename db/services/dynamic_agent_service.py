"""
Упрощенный сервис для работы с динамическими агентами.
Прямая интеграция с Agno без избыточных абстракций.
Лаконичная и легковесная реализация.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union, AsyncGenerator, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import ValidationError

logger = logging.getLogger(__name__)

from db.models import (
    DynamicAgent, ModelConfig, ToolsConfig, MemoryConfig, KnowledgeConfig, 
    StorageConfig, ReasoningConfig, TeamConfig, AgentSettings,
    AgnoAgentSettings, AgnoKnowledgeParams, AgnoReasoningParams, AgnoStorageParams
)
from db.session import SessionLocal
from db.services.dynamic_tool_service import dynamic_tool_service
from db.url import get_db_url

# Прямой импорт Agno (изолированный в одном месте)
try:
    from agno.agent import Agent
    from agno.models.base import Model
    from agno.memory.v2.db.postgres import PostgresMemoryDb
    from agno.storage.agent.postgres import PostgresAgentStorage
    from agno.knowledge import AgentKnowledge
    from agno.media import Audio, File as FileMedia, Image, Video
    AGNO_AVAILABLE = True
    print("Agno успешно импортирован")
except ImportError as e:
    AGNO_AVAILABLE = False
    print(f"Agno недоступен: {e}")


class AgentCache:
    """Простой кэш для агентов с TTL"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 минут по умолчанию
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[DynamicAgent, datetime]] = {}
        self._list_cache: Optional[Tuple[List[DynamicAgent], datetime]] = None
    
    def get(self, agent_id: str) -> Optional[DynamicAgent]:
        """Получить агента из кэша"""
        if agent_id not in self._cache:
            return None
        
        agent, cached_time = self._cache[agent_id]
        if self._is_expired(cached_time):
            del self._cache[agent_id]
            return None
        
        return agent
    
    def set(self, agent_id: str, agent: DynamicAgent):
        """Сохранить агента в кэш"""
        self._cache[agent_id] = (agent, datetime.utcnow())
    
    def get_list(self) -> Optional[List[DynamicAgent]]:
        """Получить список агентов из кэша"""
        if self._list_cache is None:
            return None
        
        agents, cached_time = self._list_cache
        if self._is_expired(cached_time):
            self._list_cache = None
            return None
        
        return agents
    
    def set_list(self, agents: List[DynamicAgent]):
        """Сохранить список агентов в кэш"""
        self._list_cache = (agents, datetime.utcnow())
    
    def invalidate(self, agent_id: str):
        """Сбросить кэш для агента"""
        self._cache.pop(agent_id, None)
        self._list_cache = None
    
    def invalidate_all(self):
        """Сбросить весь кэш"""
        self._cache.clear()
        self._list_cache = None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Получить статистику кэша"""
        now = datetime.utcnow()
        active_entries = sum(1 for _, (_, time) in self._cache.items() if not self._is_expired(time))
        expired_entries = len(self._cache) - active_entries
        
        list_cache_status = "active" if self._list_cache and not self._is_expired(self._list_cache[1]) else "expired"
        
        return {
            "ttl_seconds": self.ttl_seconds,
            "active_entries": active_entries,
            "expired_entries": expired_entries,
            "total_entries": len(self._cache),
            "list_cache_status": list_cache_status,
        }
    
    def cleanup_expired(self) -> int:
        """Очистить истекшие записи"""
        expired_keys = [k for k, (_, time) in self._cache.items() if self._is_expired(time)]
        for key in expired_keys:
            del self._cache[key]
        
        if self._list_cache and self._is_expired(self._list_cache[1]):
            self._list_cache = None
        
        return len(expired_keys)
    
    def _is_expired(self, cached_time: datetime) -> bool:
        """Проверить, истек ли кэш"""
        return (datetime.utcnow() - cached_time).total_seconds() > self.ttl_seconds


class DynamicAgentService:
    """
    Упрощенный сервис для работы с динамическими агентами.
    Прямая интеграция с Agno, минимум абстракций.
    """
    
    def __init__(self, cache_ttl: int = 300):
        self.db_session = SessionLocal
        self.db_url = get_db_url()
        self.cache = AgentCache(ttl_seconds=cache_ttl)
    
    # === CRUD операции с кэшированием ===
    
    def get_all_active_agents(self) -> List[DynamicAgent]:
        """Получить все активные агенты"""
        cached_agents = self.cache.get_list()
        if cached_agents is not None:
            return cached_agents
        
        with self.db_session() as session:
            agents = session.query(DynamicAgent).filter(
                DynamicAgent.is_active == True
            ).order_by(DynamicAgent.created_at.desc()).all()
            
            self.cache.set_list(agents)
            for agent in agents:
                self.cache.set(agent.agent_id, agent)
            
            return agents
    
    def get_agent_by_id(self, agent_id: str) -> Optional[DynamicAgent]:
        """Получить агента по ID"""
        cached_agent = self.cache.get(agent_id)
        if cached_agent is not None:
            return cached_agent
        
        with self.db_session() as session:
            agent = session.query(DynamicAgent).filter(
                and_(
                    DynamicAgent.agent_id == agent_id,
                    DynamicAgent.is_active == True
                )
            ).first()
            
            if agent:
                self.cache.set(agent_id, agent)
            
            return agent
    
    def create_agent(self, agent_data: Dict[str, Any]) -> DynamicAgent:
        """Создать нового агента с Pydantic валидацией"""
        
        # Валидация через Pydantic
        self._validate_agent_data(agent_data)
        
        with self.db_session() as session:
            # Создаем агента
            agent = DynamicAgent(
                name=agent_data['name'],
                agent_id=agent_data['agent_id'],
                description=agent_data.get('description'),
                instructions=agent_data.get('instructions'),
                model_configuration=agent_data.get('model_configuration'),
                tools_config=agent_data.get('tools_config'),
                knowledge_config=agent_data.get('knowledge_config'),
                memory_config=agent_data.get('memory_config'),
                storage_config=agent_data.get('storage_config'),
                reasoning_config=agent_data.get('reasoning_config'),
                team_config=agent_data.get('team_config'),
                settings=agent_data.get('settings'),
                is_active=agent_data.get('is_active', True),
                is_active_api=agent_data.get('is_active_api', True)
            )
            
            session.add(agent)
            session.commit()
            session.refresh(agent)
            
            # Обновляем кэш
            self.cache.set(agent.agent_id, agent)
            self.cache.invalidate_all()
            
            return agent
    
    def update_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> Optional[DynamicAgent]:
        """Обновить агента"""
        
        # Валидация через Pydantic (только для переданных данных)
        self._validate_agent_data(agent_data, partial=True)
        
        with self.db_session() as session:
            agent = session.query(DynamicAgent).filter(
                and_(
                    DynamicAgent.agent_id == agent_id,
                    DynamicAgent.is_active == True
                )
            ).first()
            
            if not agent:
                return None
            
            # Обновляем поля
            for key, value in agent_data.items():
                if hasattr(agent, key):
                    setattr(agent, key, value)
            
            session.commit()
            session.refresh(agent)
            
            # Обновляем кэш
            self.cache.set(agent_id, agent)
            self.cache.invalidate_all()
            
            return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """Удалить агента (soft delete)"""
        with self.db_session() as session:
            agent = session.query(DynamicAgent).filter(
                and_(
                    DynamicAgent.agent_id == agent_id,
                    DynamicAgent.is_active == True
                )
            ).first()
            
            if not agent:
                return False
            
            agent.is_active = False
            session.commit()
            
            # Обновляем кэш
            self.cache.invalidate(agent_id)
            self.cache.invalidate_all()
            
            return True
    
    def get_available_agent_ids(self) -> List[str]:
        """Получить список доступных ID агентов"""
        agents = self.get_all_active_agents()
        return [agent.agent_id for agent in agents]
    
    def get_agent_instance(self, agent_id: str, **kwargs) -> Optional[Any]:
        """⚠️ УСТАРЕВШИЙ синхронный метод получения Agno Agent (без MCP поддержки)"""
        
        if not AGNO_AVAILABLE:
            raise RuntimeError("Agno недоступен. Проверьте установку.")
        
        # Получаем динамического агента
        dynamic_agent = self.get_agent_by_id(agent_id)
        if not dynamic_agent:
            return None
        
        # ⚠️ Используем синхронный метод - MCP инструменты будут пропущены
        print(f"⚠️ get_agent_instance: используется синхронный режим для агента '{agent_id}' - MCP инструменты пропущены")
        return self._build_agno_agent(dynamic_agent, **kwargs)

    async def get_agent_instance_async(self, agent_id: str, **kwargs) -> Optional[Any]:
        """✅ ПРАВИЛЬНЫЙ асинхронный метод получения Agno Agent (с MCP поддержкой)"""
        
        if not AGNO_AVAILABLE:
            raise RuntimeError("Agno недоступен. Проверьте установку.")
        
        # Получаем динамического агента
        dynamic_agent = self.get_agent_by_id(agent_id)
        if not dynamic_agent:
            return None
        
        # ✅ Используем асинхронный метод с полной поддержкой MCP
        return await self._build_agno_agent_async(dynamic_agent, **kwargs)
    
    def _validate_agent_data(self, agent_data: Dict[str, Any], partial: bool = False):
        """Валидация данных агента через Pydantic модели"""
        
        # Валидация обязательных полей (только для создания)
        if not partial:
            required_fields = ['name', 'agent_id']
            for field in required_fields:
                if field not in agent_data:
                    raise ValueError(f"Обязательное поле '{field}' отсутствует")
        
        # Валидация конфигураций через Pydantic
        config_mappings = {
            'model_configuration': ModelConfig,
            'tools_config': ToolsConfig,
            'memory_config': MemoryConfig,
            'knowledge_config': KnowledgeConfig,
            'storage_config': StorageConfig,
            'reasoning_config': ReasoningConfig,
            'team_config': TeamConfig,
            'settings': AgentSettings,
        }
        
        for config_key, config_class in config_mappings.items():
            if config_key in agent_data and agent_data[config_key] is not None:
                try:
                    # Проверяем валидность через создание экземпляра Pydantic модели
                    config_instance = config_class(**agent_data[config_key])
                    # ✅ ИСПРАВЛЕНИЕ: Используем by_alias=True, чтобы в БД сохранялись
                    # имена полей, как в API (например, 'schema' вместо 'db_schema').
                    agent_data[config_key] = config_instance.dict(
                        by_alias=True, exclude_unset=True, exclude_none=True
                    )
                except ValidationError as e:
                    raise ValueError(f"Ошибка валидации {config_key}: {e}")
                except Exception as e:
                    raise ValueError(f"Ошибка обработки {config_key}: {e}")
    
    # === Выполнение агентов ===
    
    async def run_agent(self, agent_id: str, message: str, **kwargs) -> Union[str, AsyncGenerator[str, None]]:
        """Запустить агента с сообщением"""
        
        if not AGNO_AVAILABLE:
            raise RuntimeError("Agno недоступен. Проверьте установку.")
        
        # Получаем агента
        dynamic_agent = self.get_agent_by_id(agent_id)
        if not dynamic_agent:
            raise ValueError(f"Агент {agent_id} не найден")
        
        # Валидация параметров выполнения
        self._validate_agent_runtime_config(dynamic_agent, **kwargs)
        
        # ✅ ИСПРАВЛЕНО: Используем async версию для создания агента с MCP
        agno_agent = await self._build_agno_agent_async(dynamic_agent, **kwargs)
        
        # Обрабатываем файлы (если есть)
        files = kwargs.get('files', [])
        file_result = await self._process_files_for_agent(message, files)
        
        # Если файлы были обработаны, получаем сообщение и медиа объекты
        if isinstance(file_result, tuple):
            processed_message, media_dict = file_result
        else:
            processed_message = file_result
            media_dict = {}
        
        # Запускаем агента
        try:
            run_kwargs = {'stream': kwargs.get('stream', False)}
            
            # Добавляем изображения и файлы если есть (Agno нативно поддерживает раздельную передачу)
            if media_dict.get('images'):
                run_kwargs['images'] = media_dict['images']
                print(f"✅ Передаем {len(media_dict['images'])} изображений в Agent.run()")
            if media_dict.get('files'):
                run_kwargs['files'] = media_dict['files']
                print(f"✅ Передаем {len(media_dict['files'])} файлов в Agent.run()")
            
            # Добавляем user_id и session_id для памяти
            if 'user_id' in kwargs and kwargs['user_id']:
                run_kwargs['user_id'] = kwargs['user_id']
            
            if 'session_id' in kwargs and kwargs['session_id']:
                run_kwargs['session_id'] = kwargs['session_id']

            # Передаём флаг остановки после вызова инструмента, если указан
            if 'stop_after_tool_call' in kwargs:
                run_kwargs['stop_after_tool_call'] = kwargs['stop_after_tool_call']
            
            if kwargs.get('stream', False):
                # Потоковый режим
                return agno_agent.run(processed_message, **run_kwargs)
            else:
                # Обычный режим
                response = agno_agent.run(processed_message, **run_kwargs)
                # Возвращаем полный RunResponse объект для получения run_id
                if hasattr(response, 'to_dict'):
                    return response.to_dict()
                elif hasattr(response, 'content'):
                    return {"content": response.content, "run_id": getattr(response, 'run_id', None)}
                else:
                    return {"content": str(response), "run_id": None}
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения агента: {str(e)}")
    
    def _validate_agent_runtime_config(self, agent: DynamicAgent, **kwargs):
        """Валидация конфигурации для выполнения агента"""
        
        # Проверяем обязательные поля
        if not agent.instructions and not kwargs.get('instructions'):
            raise ValueError("У агента должны быть инструкции")
        
        # Валидация переопределений модели
        model_override = kwargs.get('model_override')
        if model_override:
            if not isinstance(model_override, str):
                raise ValueError("model_override должен быть строкой")
        
        # Валидация температуры
        temperature = kwargs.get('temperature')
        if temperature is not None:
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 2:
                raise ValueError("temperature должна быть числом от 0 до 2")
        
        # Валидация max_tokens
        max_tokens = kwargs.get('max_tokens')
        if max_tokens is not None:
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                raise ValueError("max_tokens должен быть положительным числом")
        
        # Валидация tool_call_limit
        tool_call_limit = kwargs.get('tool_call_limit')
        if tool_call_limit is not None:
            if not isinstance(tool_call_limit, int) or tool_call_limit <= 0 or tool_call_limit > 100:
                raise ValueError("tool_call_limit должен быть числом от 1 до 100")
    
    def _create_model_instance(self, model_config: ModelConfig) -> Any:
        """Создать экземпляр модели Agno с правильной фильтрацией параметров"""
        model_id = model_config.id or "gpt-4.1"
        model_params = model_config.dict(exclude_none=True)
        model_params.pop('id', None)
        
        # ✅ Фильтрация на основе реального кода Agno
        if model_id.startswith('gpt-') or model_id.startswith('o'):
            from agno.models.openai import OpenAIChat
            # OpenAI НЕ поддерживает: stop_sequences, top_k, grounding, search, mcp_servers, thinking, system_message_role
            unsupported = {'stop_sequences', 'top_k', 'grounding', 'search', 'mcp_servers', 'thinking', 
                          'max_output_tokens', 'generation_config', 'safety_settings', 'vertexai', 
                          'project_id', 'location', 'cache_system_prompt', 'extended_cache_time',
                          'system_message_role', 'add_images_to_message_content'}
            
            # reasoning_effort поддерживается только для o3 моделей
            if not model_id.startswith('o3') and 'reasoning_effort' in model_params:
                unsupported.add('reasoning_effort')
            
            filtered_params = {k: v for k, v in model_params.items() if k not in unsupported}
            return OpenAIChat(id=model_id, **filtered_params)
            
        elif model_id.startswith('claude-'):
            from agno.models.anthropic import Claude
            # Claude НЕ поддерживает: logprobs, top_logprobs, frequency_penalty, presence_penalty, user, seed, grounding, search, reasoning_effort, system_message_role
            unsupported = {'logprobs', 'top_logprobs', 'frequency_penalty', 'presence_penalty', 
                          'user', 'seed', 'grounding', 'search', 'max_completion_tokens', 'reasoning_effort',
                          'generation_config', 'safety_settings', 'vertexai', 'project_id', 'location',
                          'system_message_role', 'add_images_to_message_content'}
            filtered_params = {k: v for k, v in model_params.items() if k not in unsupported}
            return Claude(id=model_id, **filtered_params)
            
        elif model_id.startswith('gemini-'):
            from agno.models.google import Gemini
            # Gemini НЕ поддерживает: max_tokens (заменяется на max_output_tokens), user, organization, base_url, timeout, max_retries, stop заменяется на stop_sequences, reasoning_effort
            unsupported = {'max_tokens', 'user', 'organization', 'base_url', 'timeout', 
                          'max_retries', 'stop', 'logit_bias', 'top_logprobs', 'modalities', 'audio', 
                          'extra_headers', 'extra_query', 'thinking', 'mcp_servers', 'reasoning_effort',
                          'system_message_role', 'add_images_to_message_content'}
            filtered_params = {k: v for k, v in model_params.items() if k not in unsupported}
            # Заменяем max_tokens на max_output_tokens для Gemini
            if 'max_completion_tokens' in filtered_params:
                filtered_params['max_output_tokens'] = filtered_params.pop('max_completion_tokens')
            return Gemini(id=model_id, **filtered_params)
            
        else:
            # Fallback - пробуем OpenAI
            from agno.models.openai import OpenAIChat
            unsupported = {'stop_sequences', 'top_k', 'grounding', 'search', 'mcp_servers', 'thinking',
                          'reasoning_effort', 'system_message_role', 'add_images_to_message_content'}
            filtered_params = {k: v for k, v in model_params.items() if k not in unsupported}
            return OpenAIChat(id=model_id, **filtered_params)

    async def _build_agno_agent_async(self, dynamic_agent: DynamicAgent, **kwargs) -> Agent:
        """✅ ПРАВИЛЬНЫЙ асинхронный метод создания Agno Agent с MCP поддержкой"""
        
        # === БАЗОВЫЕ ПАРАМЕТРЫ ===
        agent_params = {
            'name': dynamic_agent.name,
            'agent_id': dynamic_agent.agent_id,
            'description': dynamic_agent.description,
            'instructions': dynamic_agent.instructions,
        }
        
        # === МОДЕЛЬ ===
        model_config = dynamic_agent.get_model_config()
        if model_config:
            agent_params['model'] = self._create_model_instance(model_config)
        
        # === ИНСТРУМЕНТЫ ===
        tools_config = dynamic_agent.get_tools_config()
        if tools_config:
            all_tools = []
            
            # Статические инструменты (синхронные)
            if tools_config.tools:
                all_tools.extend(self._create_static_tool_instances(tools_config.tools))
            
            # Динамические инструменты (синхронные)
            if tools_config.dynamic_tools:
                all_tools.extend(self._create_dynamic_tool_instances(tools_config.dynamic_tools))
            
            # Кастомные инструменты (синхронные)
            if tools_config.custom_tools:
                all_tools.extend(self._create_custom_tool_instances(tools_config.custom_tools))
            
            # ✅ MCP инструменты (АСИНХРОННЫЕ) - правильная обработка
            if tools_config.mcp_servers:
                try:
                    mcp_tools = await self._create_mcp_tools_async(tools_config.mcp_servers)
                    if mcp_tools:
                        all_tools.extend(mcp_tools)
                        print(f"✅ Подключено {len(mcp_tools)} MCP инструментов: {tools_config.mcp_servers}")
                except Exception as e:
                    print(f"⚠️ Ошибка подключения MCP серверов {tools_config.mcp_servers}: {e}")
            
            if all_tools:
                agent_params['tools'] = all_tools
            
            # Остальные параметры инструментов
            if tools_config.show_tool_calls is not None:
                agent_params['show_tool_calls'] = tools_config.show_tool_calls
            if tools_config.tool_call_limit is not None:
                agent_params['tool_call_limit'] = tools_config.tool_call_limit
            if tools_config.tool_choice is not None:
                agent_params['tool_choice'] = tools_config.tool_choice
        
            # --- РЕАЛИЗОВАННЫЕ ПОЛЯ ---
            if tools_config.function_declarations:
                agent_params['function_declarations'] = tools_config.function_declarations
            # --- КОНЕЦ ---
        
        # === ПАМЯТЬ ===
        memory_config = dynamic_agent.get_memory_config()
        if memory_config and memory_config.enable_agentic_memory:
            from agno.memory.v2.memory import Memory
            from agno.memory.v2.db.postgres import PostgresMemoryDb
            
            memory_db = PostgresMemoryDb(
                db_url=memory_config.db_url or self.db_url,
                table_name=memory_config.table_name or "user_memories",
                schema=memory_config.db_schema or "ai"
            )
            agent_params['memory'] = Memory(db=memory_db)
            
            if memory_config.enable_user_memories:
                agent_params['enable_user_memories'] = True
        
            # --- РЕАЛИЗОВАННЫЕ ПОЛЯ ---
            if memory_config.enable_session_summaries:
                agent_params['enable_session_summaries'] = memory_config.enable_session_summaries
            
            if memory_config.add_memory_references is not None:
                agent_params['add_memory_references'] = memory_config.add_memory_references
            
            if memory_config.add_session_summary_references is not None:
                agent_params['add_session_summary_references'] = memory_config.add_session_summary_references

            if memory_config.memory_filters:
                agent_params['memory_filters'] = memory_config.memory_filters
            # --- КОНЕЦ ---
        
        # 6. Конфигурация хранилища (Storage)
        storage = self._create_storage_instance(dynamic_agent.storage_config)
        if storage:
            agent_params['storage'] = storage

        # 7. Конфигурация знаний (Knowledge) - RAG
        knowledge = self._create_knowledge_instance(dynamic_agent.knowledge_config)
        if knowledge:
            agent_params['knowledge'] = knowledge
        
        # 8. Конфигурация рассуждений (Reasoning)
        reasoning = self._create_reasoning_config(dynamic_agent.reasoning_config)
        if reasoning:
            agent_params['reasoning'] = reasoning
        
        # === НАСТРОЙКИ (из AgentSettings) ===
        settings = dynamic_agent.get_settings()
        if settings:
            # 🛡️ Системное решение: используем безопасную модель для фильтрации
            safe_settings = AgnoAgentSettings(**settings.dict(exclude_none=True))
            agent_params.update(safe_settings.dict(exclude_none=True))
        
        # === ПЕРЕОПРЕДЕЛЕНИЯ ===
        excluded_params = {'model_override', 'files', 'stream', 'user_id', 'session_id', 'stop_after_tool_call'}
        overrides = {k: v for k, v in kwargs.items() if v is not None and k not in excluded_params}
        agent_params.update(overrides)
        
        # Обрабатываем model_override отдельно и мультимодальность
        model_override = kwargs.get('model_override')
        has_images = kwargs.get('images') is not None
        
        # Автоматически используем gpt-4.1 для мультимодальных запросов
        if has_images and not model_override:
            model_override = 'gpt-4.1'
            print(f"🖼️ Обнаружены изображения, автоматически используем gpt-4.1 для мультимодальности")
        
        if model_override:
            # Переопределяем модель если указано или для мультимодальности
            if model_config:
                # Клонируем существующую конфигурацию и изменяем только ID
                model_config_dict = model_config.dict()
                model_config_dict['id'] = model_override
                
                # Для мультимодальности добавляем поддержку изображений
                if has_images:
                    model_config_dict['temperature'] = model_config_dict.get('temperature', 0.7)
                    
                new_model_config = ModelConfig(**model_config_dict)
            else:
                # Создаем новую конфигурацию с параметрами для мультимодальности
                model_params = {'id': model_override}
                if has_images:
                    model_params['temperature'] = 0.7
                    
                new_model_config = ModelConfig(**model_params)
            
            agent_params['model'] = self._create_model_instance(new_model_config)
        
        # === СОЗДАНИЕ AGENT ===
        return Agent(**agent_params)

    # === ✅ FALLBACK синхронный метод (без MCP) ===
    def _build_agno_agent(self, dynamic_agent: DynamicAgent, **kwargs) -> Agent:
        """УСТАРЕВШИЙ синхронный метод создания Agno Agent (без MCP поддержки)"""
        print("⚠️ Используется синхронный метод создания агента - MCP инструменты будут пропущены")

        agent_params = {
            'name': dynamic_agent.name,
            'agent_id': dynamic_agent.agent_id,
            'description': dynamic_agent.description,
            'instructions': dynamic_agent.instructions,
            'is_active': dynamic_agent.is_active,
            'is_active_api': dynamic_agent.is_active_api,
            'created_at': dynamic_agent.created_at,
            'updated_at': dynamic_agent.updated_at,
        }

        model_config = dynamic_agent.get_model_config()
        if model_config:
            agent_params['model'] = self._create_model_instance(model_config)

        tools_config = dynamic_agent.get_tools_config()
        all_tools = []
        if tools_config:
            if tools_config.tools:
                all_tools.extend(self._create_static_tool_instances(tools_config.tools))
            if tools_config.dynamic_tools:
                all_tools.extend(self._create_dynamic_tool_instances(tools_config.dynamic_tools))
            if tools_config.custom_tools:
                all_tools.extend(self._create_custom_tool_instances(tools_config.custom_tools))
            
            agent_params['tools'] = all_tools
            if tools_config.show_tool_calls is not None:
                agent_params['show_tool_calls'] = tools_config.show_tool_calls
            if tools_config.tool_call_limit is not None:
                agent_params['tool_call_limit'] = tools_config.tool_call_limit
            if tools_config.tool_choice is not None:
                agent_params['tool_choice'] = tools_config.tool_choice
            if tools_config.function_declarations:
                agent_params['function_declarations'] = tools_config.function_declarations

        agent_params['memory'] = None

        storage = self._create_storage_instance(dynamic_agent.storage_config)
        if storage:
            agent_params['storage'] = storage

        knowledge = self._create_knowledge_instance(dynamic_agent.knowledge_config)
        if knowledge:
            agent_params['knowledge'] = knowledge

        reasoning = self._create_reasoning_config(dynamic_agent.reasoning_config)
        if reasoning:
            agent_params['reasoning'] = reasoning

        settings = dynamic_agent.get_settings()
        if settings:
            # 🛡️ Системное решение: используем безопасную модель для фильтрации
            safe_settings = AgnoAgentSettings(**settings.dict(exclude_none=True))
            agent_params.update(safe_settings.dict(exclude_none=True))

        overrides = {k: v for k, v in kwargs.items() if v is not None}
        agent_params.update(overrides)

        try:
            agent = Agent(**agent_params)
        except Exception as e:
            logger.error(f"Failed to build Agno agent '{dynamic_agent.agent_id}': {e}")
            raise ValueError(f"Не удалось собрать агента: {e}")

        return agent
    
    def _create_storage_instance(self, storage_config: Optional[Dict[str, Any]]) -> Optional[Any]:
        if not storage_config or not storage_config.get('enabled', False):
            return None
        
        storage_conf = StorageConfig(**storage_config)
        if storage_conf.storage_type in {"postgres", "postgresql"}:
            try:
                # 🛡️ Системное решение: используем безопасную модель для фильтрации
                safe_params = AgnoStorageParams(**storage_conf.dict(by_alias=True))
                # ✅ Используем by_alias=True, чтобы получить 'schema', а не 'db_schema'
                storage_params = safe_params.dict(exclude_none=True, by_alias=True)

                if 'db_url' not in storage_params or storage_params.get('db_url') is None:
                    storage_params['db_url'] = self.db_url
                
                # Заполняем schema, если она не была передана
                if 'schema' not in storage_params or storage_params.get('schema') is None:
                    storage_params['schema'] = 'ai' # значение по-умолчанию

                logger.debug(f"Creating PostgresAgentStorage with params: {storage_params}")
                return PostgresAgentStorage(**storage_params)
            except Exception as e:
                logger.error(f"Failed to initialize PostgresAgentStorage: {e}")
                raise ValueError(f"Ошибка конфигурации хранилища: {e}")
        else:
            logger.warning(f"Unsupported storage type: {storage_conf.storage_type}")
        return None

    def _create_knowledge_instance(self, knowledge_config: Optional[Dict[str, Any]]) -> Optional[Any]:
        if not knowledge_config or not knowledge_config.get('add_references', False):
            return None
        try:
            # 🛡️ Системное решение: используем безопасную модель для фильтрации
            knowledge_conf = KnowledgeConfig(**knowledge_config)
            safe_params = AgnoKnowledgeParams(**knowledge_conf.dict())
            knowledge_params = safe_params.dict(exclude_none=True)
            
            logger.debug(f"Creating AgentKnowledge with params: {knowledge_params}")
            return AgentKnowledge(**knowledge_params)
        except Exception as e:
            logger.error(f"Failed to initialize AgentKnowledge: {e}")
            raise ValueError(f"Ошибка конфигурации знаний: {e}")

    def _create_reasoning_config(self, reasoning_config: Optional[Dict[str, Any]]) -> Optional[Dict]:
        if not reasoning_config or not reasoning_config.get('reasoning', False):
            return None
        try:
            # 🛡️ Системное решение: используем безопасную модель для фильтрации
            reasoning_conf = ReasoningConfig(**reasoning_config)
            safe_params = AgnoReasoningParams(**reasoning_conf.dict())
            reasoning_params = safe_params.dict(exclude_none=True)

            logger.debug(f"Creating ReasoningConfig with params: {reasoning_params}")
            return reasoning_params
        except Exception as e:
            logger.error(f"Failed to initialize ReasoningConfig: {e}")
            raise ValueError(f"Ошибка конфигурации рассуждений: {e}")

    def _create_static_tool_instances(self, tools_config: List[Dict[str, Any]]) -> List[Any]:
        """Создать экземпляры статических инструментов из конфигурации"""
        if not AGNO_AVAILABLE:
            return []
        
        tool_instances = []
        
        for tool_config in tools_config:
            try:
                if isinstance(tool_config, dict):
                    # Формат: {"type": "CalculatorTools", "config": {...}}
                    tool_type = tool_config.get('type')
                    config = tool_config.get('config', {})
                    
                    if tool_type:
                        # Используем DynamicToolService
                        from db.services.dynamic_tool_service import dynamic_tool_service
                        tool_instance = dynamic_tool_service.create_tool_instance(tool_type, config)
                        
                        if tool_instance:
                            tool_instances.append(tool_instance)
                            print(f"✅ Создан статический инструмент: {tool_type}")
                            
                elif isinstance(tool_config, str):
                    # Формат: "CalculatorTools"
                    from db.services.dynamic_tool_service import dynamic_tool_service
                    tool_instance = dynamic_tool_service.create_tool_instance(tool_config, {})
                    
                    if tool_instance:
                        tool_instances.append(tool_instance)
                        print(f"✅ Создан статический инструмент: {tool_config}")
                else:
                    print(f"❌ Неподдерживаемый формат инструмента: {tool_config}")
                    
            except Exception as e:
                print(f"❌ Ошибка создания статического инструмента {tool_config}: {e}")
                continue
        
        return tool_instances

    def _create_dynamic_tool_instances(self, tool_ids: List[str]) -> List[Any]:
        """Создать экземпляры динамических инструментов"""
        if not AGNO_AVAILABLE:
            return []
        
        tool_instances = []
        
        for tool_id in tool_ids:
            try:
                # Используем DynamicToolService для создания инструментов
                from db.services.dynamic_tool_service import dynamic_tool_service
                
                tool_instance = dynamic_tool_service.create_tool_instance(tool_id, {})
                
                if tool_instance:
                    tool_instances.append(tool_instance)
                    print(f"✅ Создан динамический инструмент: {tool_id}")
                
            except Exception as e:
                print(f"❌ Ошибка создания инструмента {tool_id}: {e}")
                continue
        
        return tool_instances
    
    def _create_custom_tool_instances(self, tool_ids: List[str]) -> List[Any]:
        """Создать экземпляры кастомных Python инструментов"""
        if not AGNO_AVAILABLE:
            return []
        
        tool_instances = []
        
        for tool_id in tool_ids:
            try:
                # Используем CustomToolService для создания инструментов
                from db.services.custom_tool_service import custom_tool_service
                
                tool_instance = custom_tool_service.create_tool_instance(tool_id, {})
                
                if tool_instance:
                    tool_instances.append(tool_instance)
                    print(f"✅ Создан кастомный инструмент: {tool_id}")
                
            except Exception as e:
                print(f"❌ Ошибка создания кастомного инструмента {tool_id}: {e}")
                continue
        
        return tool_instances
    
    async def _create_mcp_tools_async(self, server_ids: List[str]) -> List[Any]:
        """✅ ПРАВИЛЬНЫЙ асинхронный метод создания MCP инструментов"""
        if not AGNO_AVAILABLE:
            return []
        
        tool_instances = []
        
        import anyio
        from db.services.mcp_service import mcp_service

        for server_id in server_ids:
            try:
                # Пытаемся создать MCP-инструмент, но не более 3 сек, иначе пропускаем
                async with anyio.fail_after(10):
                    mcp_tools = await mcp_service.create_tool_instance_async(server_id)
                if mcp_tools:
                    tool_instances.append(mcp_tools)
                    print(f"✅ Создан MCP инструмент (async): {server_id}")
                else:
                    print(f"⚠️ MCP инструмент '{server_id}' пропущен (не удалось инициализировать)")
            except (anyio.exceptions.TimeoutError, Exception) as e:
                print(f"⚠️ MCP '{server_id}' отключён: {e}")
                continue
        
        return tool_instances
    
    def _create_agno_tool_instance(self, tool_id: str, config: Dict[str, Any]) -> Optional[Any]:
        """Создать экземпляр Agno инструмента по ID"""
        if not AGNO_AVAILABLE:
            return None

    def _get_tool_module_mapping(self) -> Dict[str, str]:
        """
        DEPRECATED: Удален хардкод маппинг.
        Теперь используется динамический импорт из БД через module_path.
        """
        # Возвращаем пустой словарь для обратной совместимости
        return {}
    
    async def _process_files_for_agent(self, message: str, files: List) -> Union[str, Tuple[str, Dict[str, List]]]:
        """Обработка файлов для агента с разделением на изображения и документы"""
        if not files:
            return message
        
        if not AGNO_AVAILABLE:
            return message + "\n\n[ФАЙЛЫ НЕ ПОДДЕРЖИВАЮТСЯ: Agno недоступен]"
        
        from agno.media import File, Image
        
        agno_images = []  # Для Message.images
        agno_files = []   # Для Message.files
        file_descriptions = []
        text_files_content = []  # Для текстовых файлов, которые добавляются к сообщению
        
        for file in files:
            try:
                # Читаем содержимое файла
                content = await file.read()
                filename = getattr(file, 'filename', 'unknown_file')
                content_type = getattr(file, 'content_type', 'application/octet-stream')
                
                # Проверяем тип файла и создаем соответствующий объект
                if content_type.startswith('image/'):
                    # Для изображений используем Image класс (идет в Message.images)
                    agno_image = Image(
                        content=content,
                        filename=filename
                    )
                    agno_images.append(agno_image)
                    file_descriptions.append(f"- 🖼️ {filename} ({content_type}, {len(content)} байт)")
                    
                else:
                    # Для документов используем File класс (идет в Message.files)
                    # OpenAI поддерживает только PDF файлы, остальные пропускаем с предупреждением
                    if content_type == 'application/pdf':
                        agno_file = File(
                            content=content,
                            mime_type=content_type,
                            filename=filename
                        )
                        agno_files.append(agno_file)
                        file_descriptions.append(f"- 📄 {filename} ({content_type}, {len(content)} байт)")
                    else:
                        # Добавляем текстовое содержимое к сообщению для других типов файлов
                        try:
                            text_content = content.decode('utf-8') if isinstance(content, bytes) else str(content)
                            text_files_content.append(f"\n\n--- Содержимое файла {filename} ---\n{text_content}\n--- Конец файла {filename} ---")
                            file_descriptions.append(f"- 📝 {filename} (содержимое добавлено в сообщение, {len(content)} байт)")
                        except Exception as e:
                            file_descriptions.append(f"- ❌ {filename} (ошибка декодирования: {str(e)})")
                
            except Exception as e:
                logger.error(f"Ошибка обработки файла: {e}")
                file_descriptions.append(f"- ❌ Ошибка обработки файла: {str(e)}")
        
        # Обновляем сообщение с информацией о файлах и текстовым содержимым
        updated_message = message
        if file_descriptions:
            updated_message += f"\n\nЗагруженные файлы:\n" + "\n".join(file_descriptions)
        if text_files_content:
            updated_message += "\n".join(text_files_content)
        
        # Возвращаем словарь с разделенными типами файлов
        media_dict = {}
        if agno_images:
            media_dict['images'] = agno_images
        if agno_files:
            media_dict['files'] = agno_files
            
        return updated_message, media_dict
    
    # === Управление кэшем ===
    
    def invalidate_agent_cache(self, agent_id: str):
        """Сбросить кэш агента"""
        self.cache.invalidate(agent_id)
    
    def invalidate_all_cache(self):
        """Сбросить весь кэш"""
        self.cache.invalidate_all()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Получить статистику кэша"""
        return self.cache.get_cache_stats()
    
    def cleanup_expired_cache(self) -> int:
        """Очистить истекшие записи кэша"""
        return self.cache.cleanup_expired()
    
    def refresh_agent_cache(self, agent_id: str) -> Optional[DynamicAgent]:
        """Обновить кэш агента"""
        self.cache.invalidate(agent_id)
        return self.get_agent_by_id(agent_id)
    
    def refresh_all_cache(self) -> List[DynamicAgent]:
        """Обновить весь кэш"""
        self.cache.invalidate_all()
        return self.get_all_active_agents()
    
    # === Дополнительные методы ===
    
    def clone_agent(self, source_agent_id: str, new_agent_id: str, new_name: str) -> Optional[DynamicAgent]:
        """Клонировать агента"""
        source_agent = self.get_agent_by_id(source_agent_id)
        if not source_agent:
            return None
        
        agent_data = source_agent.to_dict()
        agent_data.pop('id', None)
        agent_data.pop('created_at', None)
        agent_data.pop('updated_at', None)
        agent_data['agent_id'] = new_agent_id
        agent_data['name'] = new_name
        
        return self.create_agent(agent_data)
    
    def search_agents(self, query: Optional[str] = None, tags: Optional[List[str]] = None) -> List[DynamicAgent]:
        """Поиск агентов"""
        with self.db_session() as session:
            query_obj = session.query(DynamicAgent).filter(DynamicAgent.is_active == True)
            
            if query:
                query_obj = query_obj.filter(
                    or_(
                        DynamicAgent.name.ilike(f'%{query}%'),
                        DynamicAgent.description.ilike(f'%{query}%'),
                        DynamicAgent.agent_id.ilike(f'%{query}%')
                    )
                )
            
            return query_obj.order_by(DynamicAgent.created_at.desc()).all()


# Глобальный экземпляр сервиса
dynamic_agent_service = DynamicAgentService() 