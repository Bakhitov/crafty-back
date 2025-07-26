from datetime import datetime
from typing import Dict, Any, Optional, List, Union, Callable
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from pydantic import BaseModel, Field, validator, model_validator
try:
    # Для тестов - используем JSON вместо JSONB в SQLite
    from sqlalchemy.types import JSON
    # В тестовом окружении JSONB будет переопределен на JSON
except ImportError:
    # В продакшене используем JSONB
    pass

Base = declarative_base()


# === PYDANTIC МОДЕЛИ ДЛЯ КОНФИГУРАЦИЙ (идентичные полям Agno Agent) ===

class ModelConfig(BaseModel):
    """Конфигурация модели (идентична Agno Model параметрам)"""
    id: Optional[str] = Field(default="gpt-4.1", description="ID модели")
    name: Optional[str] = Field(default=None, description="Имя модели")
    provider: Optional[str] = Field(default=None, description="Провайдер модели")
    
    # === OPENAI ПАРАМЕТРЫ ===
    temperature: Optional[float] = Field(
        default=None, 
        ge=0.0, 
        le=2.0, 
        description="Рандомизация вывода (0.0-2.0)"
    )
    max_tokens: Optional[int] = Field(
        default=None, 
        gt=0, 
        le=200000, 
        description="Максимальное количество токенов (1-200000)"
    )
    max_completion_tokens: Optional[int] = Field(
        default=None, 
        gt=0, 
        description="Максимум токенов в completion"
    )
    top_p: Optional[float] = Field(
        default=None, 
        ge=0.0, 
        le=1.0, 
        description="Nucleus sampling (0.0-1.0)"
    )
    frequency_penalty: Optional[float] = Field(
        default=None, 
        ge=-2.0, 
        le=2.0, 
        description="Штраф за повторение токенов (-2.0 до 2.0)"
    )
    presence_penalty: Optional[float] = Field(
        default=None, 
        ge=-2.0, 
        le=2.0, 
        description="Штраф за присутствие токенов (-2.0 до 2.0)"
    )
    stop: Optional[Union[str, List[str]]] = Field(default=None, description="Стоп-секвенции")
    seed: Optional[int] = Field(
        default=None, 
        ge=0, 
        description="Сид для детерминизма (неотрицательное число)"
    )
    logit_bias: Optional[Dict[str, Any]] = Field(default=None, description="Изменение вероятности токенов")
    logprobs: Optional[bool] = Field(default=None, description="Включить логарифмы вероятностей")
    top_logprobs: Optional[int] = Field(default=None, description="Логпробы на токен")
    user: Optional[str] = Field(default=None, description="ID конечного пользователя")
    store: Optional[bool] = Field(default=None, description="Сохранять ли вывод запроса")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные метаданные")
    modalities: Optional[List[str]] = Field(default=None, description="Список поддерживаемых модальностей")
    audio: Optional[Dict[str, Any]] = Field(default=None, description="Параметры аудио")
    response_format: Optional[Dict[str, Any]] = Field(default=None, description="Формат ответа")
    
    # === НОВЫЕ ПАРАМЕТРЫ O3 И АУДИО (Agno 1.7.0) ===
    reasoning_effort: Optional[str] = Field(
        default=None, 
        description="Уровень усилий для рассуждения o3 (low, medium, high)"
    )
    
    # === CLAUDE (ANTHROPIC) ПАРАМЕТРЫ ===
    stop_sequences: Optional[List[str]] = Field(
        default=None, 
        max_items=4, 
        description="Стоп-секвенции Claude (максимум 4)"
    )
    top_k: Optional[int] = Field(
        default=None, 
        ge=1, 
        le=500, 
        description="Top-k sampling (1-500)"
    )
    
    # === GEMINI (GOOGLE) ПАРАМЕТРЫ ===
    generation_config: Optional[Dict[str, Any]] = Field(default=None, description="Конфигурация генерации Gemini")
    safety_settings: Optional[Dict[str, Any]] = Field(default=None, description="Настройки безопасности Gemini")
    function_declarations: Optional[List[Dict[str, Any]]] = Field(default=None, description="Объявления функций Gemini")
    generative_model_kwargs: Optional[Dict[str, Any]] = Field(default=None, description="Доп. аргументы Gemini")
    grounding: Optional[bool] = Field(default=False, description="Включить grounding")
    search: Optional[bool] = Field(default=False, description="Включить поиск")
    grounding_dynamic_threshold: Optional[float] = Field(default=None, description="Порог grounding")
    vertexai: Optional[bool] = Field(default=False, description="Использовать Vertex AI")
    project_id: Optional[str] = Field(default=None, description="Google Cloud проект")
    location: Optional[str] = Field(default=None, description="Регион GCP")
    max_output_tokens: Optional[int] = Field(default=None, description="Максимум токенов Gemini")
    
    # === ОБЩИЕ ПАРАМЕТРЫ ===
    structured_outputs: Optional[bool] = Field(default=None, description="Использовать ли структурированный вывод")
    override_system_role: Optional[bool] = Field(default=None, description="Переопределять ли роль system-пользователя")
    system_message_role: Optional[str] = Field(default="system", description="Роль для system-сообщений")
    add_images_to_message_content: Optional[bool] = Field(default=True, description="Добавлять ли изображения в сообщения")
    
    # === API ПАРАМЕТРЫ ===
    api_key: Optional[str] = Field(default=None, description="API ключ")
    organization: Optional[str] = Field(default=None, description="Организация OpenAI")
    base_url: Optional[str] = Field(default=None, description="Базовый URL запроса")
    timeout: Optional[float] = Field(default=None, description="Таймаут запроса")
    max_retries: Optional[int] = Field(default=None, description="Максимум повторов")
    extra_headers: Optional[Dict[str, Any]] = Field(default=None, description="Заголовки запроса")
    extra_query: Optional[Dict[str, Any]] = Field(default=None, description="Доп. параметры запроса")
    request_params: Optional[Dict[str, Any]] = Field(default=None, description="Доп. параметры запроса")
    default_headers: Optional[Dict[str, Any]] = Field(default=None, description="Заголовки по умолчанию")
    default_query: Optional[Dict[str, Any]] = Field(default=None, description="Параметры по умолчанию")
    client_params: Optional[Dict[str, Any]] = Field(default=None, description="Параметры клиента")

    @validator('id')
    def validate_model_id(cls, v):
        """Упрощенная валидация - позволяем любые модели"""
        if v is None:
            return v
        
        # Базовая проверка формата
        if not isinstance(v, str) or len(v.strip()) == 0:
            raise ValueError("ID модели должен быть непустой строкой")
        
        return v.strip()

    @validator('stop')
    def validate_stop_sequences(cls, v):
        """Валидация стоп-секвенций"""
        if v is None:
            return v
        
        if isinstance(v, str):
            if len(v) > 100:
                raise ValueError("Стоп-секвенция не может быть длиннее 100 символов")
            return v
        
        if isinstance(v, list):
            if len(v) > 4:
                raise ValueError("Максимум 4 стоп-секвенции")
            for seq in v:
                if not isinstance(seq, str):
                    raise ValueError("Все стоп-секвенции должны быть строками")
                if len(seq) > 100:
                    raise ValueError("Стоп-секвенция не может быть длиннее 100 символов")
            return v
        
        raise ValueError("stop должно быть строкой или списком строк")

    @validator('reasoning_effort')
    def validate_reasoning_effort(cls, v):
        """Валидация уровня усилий для рассуждения o3"""
        if v is None:
            return v
        
        valid_levels = {"low", "medium", "high"}
        if v not in valid_levels:
            raise ValueError(f"reasoning_effort должен быть одним из: {', '.join(valid_levels)}")
        
        return v

    @model_validator(mode='before')
    @classmethod
    def validate_model_specific_params(cls, values):
        """Кросс-валидация параметров в зависимости от модели"""
        if isinstance(values, dict):
            model_id = values.get('id')
            if not model_id:
                return values
            
            # Валидация параметров для разных провайдеров
            if model_id.startswith('gpt-') or model_id.startswith('o'):
                # OpenAI модели
                if values.get('top_k') is not None:
                    raise ValueError("top_k не поддерживается для OpenAI моделей")
                if values.get('stop_sequences') is not None:
                    raise ValueError("Используйте 'stop' вместо 'stop_sequences' для OpenAI")
                
                # reasoning_effort только для o3 моделей
                if values.get('reasoning_effort') is not None and not model_id.startswith('o3'):
                    raise ValueError("reasoning_effort поддерживается только для o3 моделей")
                    
            elif model_id.startswith('claude-'):
                # Claude модели
                if values.get('seed') is not None:
                    raise ValueError("seed не поддерживается для Claude моделей")
                if values.get('stop') is not None and values.get('stop_sequences') is not None:
                    raise ValueError("Используйте либо 'stop', либо 'stop_sequences', но не оба")
                    
            elif model_id.startswith('gemini-'):
                # Gemini модели
                if values.get('frequency_penalty') is not None:
                    raise ValueError("frequency_penalty не поддерживается для Gemini")
                if values.get('presence_penalty') is not None:
                    raise ValueError("presence_penalty не поддерживается для Gemini")
        
        return values


class ToolsConfig(BaseModel):
    """Конфигурация инструментов (идентична Agno Agent параметрам)"""
    tools: Optional[List[Dict[str, Any]]] = Field(default=None, description="Список статических инструментов")
    show_tool_calls: Optional[bool] = Field(default=None, description="Показывать ли вызовы инструментов")
    tool_call_limit: Optional[int] = Field(default=None, description="Лимит вызовов инструментов")
    tool_choice: Optional[Union[str, Dict]] = Field(default=None, description="Управление выбором инструмента")
    
    # === НОВЫЙ ПАРАМЕТР: TOOL HOOKS ===
    tool_hooks: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        description="Хуки до/после вызова инструмента (ссылки на функции)"
    )
    
    # === ДИНАМИЧЕСКИЕ ИНСТРУМЕНТЫ ===
    dynamic_tools: Optional[List[str]] = Field(default=None, description="Список ID динамических инструментов из БД")
    custom_tools: Optional[List[str]] = Field(default=None, description="Список ID кастомных Python инструментов")
    mcp_servers: Optional[List[str]] = Field(default=None, description="Список ID MCP серверов")
    
    # === ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ===
    function_declarations: Optional[List[Dict[str, Any]]] = Field(default=None, description="Объявления функций")

    @validator('tool_choice')
    def validate_tool_choice(cls, v):
        """Валидация выбора инструмента"""
        if v is None:
            return v
        
        if isinstance(v, str):
            # Поддерживаемые строковые значения
            if v not in {"auto", "none", "required"}:
                raise ValueError("tool_choice должен быть 'auto', 'none', 'required' или объектом")
        elif isinstance(v, dict):
            # Формат принудительного выбора инструмента
            if v['type'] not in {'function', 'tool'}:
                raise ValueError("tool_choice type должен быть 'function' или 'tool'")
        else:
            raise ValueError("tool_choice должен быть строкой или объектом")
        
        return v
    
    @validator('tool_hooks')
    def validate_tool_hooks(cls, v):
        """Валидация хуков инструментов"""
        if v is None:
            return v
        
        if not isinstance(v, list):
            raise ValueError("tool_hooks должен быть списком")
        
        for hook in v:
            if not isinstance(hook, dict):
                raise ValueError("Каждый хук должен быть объектом")
            
            required_fields = {'hook_type', 'module_path', 'function_name'}
            if not all(field in hook for field in required_fields):
                raise ValueError(f"Хук должен содержать поля: {required_fields}")
            
            # Валидация типа хука
            if hook['hook_type'] not in {'before_tool_call', 'after_tool_call', 'on_tool_error'}:
                raise ValueError("hook_type должен быть 'before_tool_call', 'after_tool_call' или 'on_tool_error'")


class MemoryConfig(BaseModel):
    """Конфигурация памяти (идентична Agno Agent параметрам)"""
    memory_type: Optional[str] = Field(default="postgres", description="Тип памяти")
    enable_agentic_memory: Optional[bool] = Field(default=False, description="Агент управляет памятью")
    enable_user_memories: Optional[bool] = Field(default=False, description="Сохранять память о пользователе")
    add_memory_references: Optional[bool] = Field(default=None, description="Добавлять ссылки на память")
    user_data: Optional[Dict[str, Any]] = Field(default=None, description="Метаданные пользователя")
    agent_data: Optional[Dict[str, Any]] = Field(default=None, description="Метаданные агента")
    
    # === ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ПАМЯТИ ===
    enable_session_summaries: Optional[bool] = Field(default=False, description="Сохранять резюме сессии")
    add_session_summary_references: Optional[bool] = Field(default=None, description="Добавлять ссылки на резюме")
    memory_filters: Optional[Dict[str, Any]] = Field(default=None, description="Фильтры для памяти")
    
    # === POSTGRES MEMORY ПАРАМЕТРЫ ===
    db_url: Optional[str] = Field(default=None, description="URL базы данных для памяти")
    table_name: Optional[str] = Field(default="agent_memory", description="Название таблицы памяти")
    db_schema: Optional[str] = Field(default="ai", description="Схема базы данных", alias="schema")
    auto_upgrade_schema: Optional[bool] = Field(default=False, description="Автоматическое обновление схемы")
    
    # === DEPRECATED ПАРАМЕТРЫ (но всё ещё есть в agno) ===
    num_history_responses: Optional[int] = Field(default=None, description="Количество исторических ответов (deprecated)")

    @validator('memory_type')
    def validate_memory_type(cls, v):
        """Валидация типа памяти"""
        if v is None:
            return v
        
        # Поддерживаем только PostgreSQL (Supabase)
        supported_types = {"postgres", "postgresql"}
        if v not in supported_types:
            raise ValueError(f"Неподдерживаемый тип памяти: {v}. Доступные: {', '.join(supported_types)} (только PostgreSQL/Supabase)")
        
        return v

    @model_validator(mode='before')
    @classmethod
    def validate_memory_config(cls, values):
        """Кросс-валидация конфигурации памяти"""
        memory_type = values.get('memory_type')
        enable_agentic = values.get('enable_agentic_memory', False)
        enable_user = values.get('enable_user_memories', False)
        
        # Проверяем совместимость agentic memory с типом памяти
        if enable_agentic and memory_type not in {'postgres', 'postgresql'}:
            raise ValueError("Agentic memory поддерживается только с postgres (Supabase)")
        
        # Проверяем совместимость user memories
        if enable_user and memory_type not in {'postgres', 'postgresql'}:
            raise ValueError("User memories поддерживаются только с postgres (Supabase)")
        
        return values


class KnowledgeConfig(BaseModel):
    """Конфигурация базы знаний (идентична Agno Agent параметрам)"""
    knowledge_filters: Optional[Dict[str, Any]] = Field(default=None, description="Фильтры для базы знаний")
    enable_agentic_knowledge_filters: Optional[bool] = Field(default=False, description="Агент может выбирать фильтры")
    add_references: Optional[bool] = Field(default=False, description="Включить RAG")
    references_format: Optional[str] = Field(default="json", description="Формат ссылок")
    search_knowledge: Optional[bool] = Field(default=True, description="Включить поиск по базе знаний")
    update_knowledge: Optional[bool] = Field(default=False, description="Разрешить обновление знаний")
    
    # === ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ЗНАНИЙ ===
    retriever: Optional[Dict[str, Any]] = Field(default=None, description="Функция для получения ссылок")
    knowledge_base: Optional[str] = Field(default=None, description="ID базы знаний")
    max_references: Optional[int] = Field(default=10, description="Максимальное количество ссылок")
    similarity_threshold: Optional[float] = Field(default=0.7, description="Порог схожести для поиска")
    
    # === VECTOR DATABASE ПАРАМЕТРЫ ===
    vector_db_url: Optional[str] = Field(default=None, description="URL векторной базы данных")
    embedding_model: Optional[str] = Field(default=None, description="Модель для эмбеддингов")
    chunk_size: Optional[int] = Field(default=1000, description="Размер чанков для индексации")
    chunk_overlap: Optional[int] = Field(default=200, description="Перекрытие между чанками")
    
    # === DEFAULT TOOLS ПАРАМЕТРЫ (из Agent) ===
    read_chat_history: Optional[bool] = Field(default=False, description="Инструмент чтения истории чата")
    read_tool_call_history: Optional[bool] = Field(default=False, description="Инструмент истории вызовов инструментов")

    @validator('references_format')
    def validate_references_format(cls, v):
        """Валидация формата ссылок"""
        if v is None:
            return v
        
        supported_formats = {"json", "markdown", "text", "xml"}
        if v not in supported_formats:
            raise ValueError(f"Неподдерживаемый формат ссылок: {v}. Доступные: {', '.join(supported_formats)}")
        
        return v


class StorageConfig(BaseModel):
    """Конфигурация хранилища (идентична Agno Agent параметрам)"""
    storage_type: Optional[str] = Field(default="postgres", description="Тип хранилища")
    db_url: Optional[str] = Field(default=None, description="URL базы данных")
    enabled: Optional[bool] = Field(default=True, description="Включено ли хранилище")
    table_name: Optional[str] = Field(default="sessions", description="Название таблицы для сессий")
    db_schema: Optional[str] = Field(default="ai", description="Схема базы данных", alias="schema")
    store_events: Optional[bool] = Field(default=False, description="Сохранять события выполнения")
    extra_data: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные данные")

    @validator('storage_type')
    def validate_storage_type(cls, v):
        """Валидация типа хранилища"""
        if v is None:
            return v
        
        # Поддерживаем только PostgreSQL (Supabase)
        supported_types = {"postgres", "postgresql"}
        if v not in supported_types:
            raise ValueError(f"Неподдерживаемый тип хранилища: {v}. Доступные: {', '.join(supported_types)} (только PostgreSQL/Supabase)")
        
        return v

    @validator('db_url')
    def validate_db_url(cls, v):
        """Валидация URL базы данных"""
        if v is None:
            return v
        
        # Базовая проверка формата URL
        if not v.startswith(('postgresql://', 'sqlite://', 'redis://', 'mysql://')):
            raise ValueError("db_url должен начинаться с поддерживаемого протокола (postgresql://, sqlite://, redis://, mysql://)")
        
        return v

    @model_validator(mode='before')
    @classmethod
    def validate_storage_config(cls, values):
        """Кросс-валидация конфигурации хранилища"""
        if isinstance(values, dict):
            storage_type = values.get('storage_type')
            db_url = values.get('db_url')
            enabled = values.get('enabled', True)
            
            # Если хранилище включено и требует БД, проверяем URL
            if enabled and storage_type in {'postgres', 'postgresql'}:
                if not db_url:
                    raise ValueError(f"db_url обязателен для типа хранилища: {storage_type}")
        
        return values


class ReasoningConfig(BaseModel):
    """Конфигурация reasoning (идентична Agno Agent параметрам)"""
    reasoning: Optional[bool] = Field(default=False, description="Включить пошаговое рассуждение")
    
    # === СЛОЖНЫЕ ОБЪЕКТЫ ЧЕРЕЗ ССЫЛКИ ===
    reasoning_model: Optional[Union[ModelConfig, str]] = Field(
        default=None, 
        description="Модель для reasoning: ModelConfig объект или ID модели из реестра"
    )
    reasoning_agent: Optional[Union[Dict[str, Any], str]] = Field(
        default=None, 
        description="Агент для reasoning: конфигурация или agent_id для ссылки"
    )
    
    # === ОСНОВНЫЕ ПАРАМЕТРЫ ===
    reasoning_min_steps: Optional[int] = Field(default=1, description="Минимальное количество шагов")
    reasoning_max_steps: Optional[int] = Field(default=10, description="Максимальное количество шагов")
    goal: Optional[str] = Field(default=None, description="Цель задачи")
    success_criteria: Optional[str] = Field(default=None, description="Критерии успешности")
    expected_output: Optional[str] = Field(default=None, description="Ожидаемый результат")
    
    # === ДОПОЛНИТЕЛЬНЫЕ REASONING ПАРАМЕТРЫ ===
    reasoning_prompt: Optional[str] = Field(default=None, description="Промпт для reasoning")
    reasoning_instructions: Optional[List[str]] = Field(default=None, description="Инструкции для reasoning")
    stream_reasoning: Optional[bool] = Field(default=False, description="Стримить шаги рассуждения")
    save_reasoning_steps: Optional[bool] = Field(default=True, description="Сохранять шаги рассуждения")
    show_full_reasoning: Optional[bool] = Field(
        default=False, 
        description="Показывать полный процесс рассуждения в ответе"
    )
    
    @validator('reasoning_model')
    def validate_reasoning_model(cls, v):
        """Валидация модели для reasoning"""
        if v is None:
            return v
        
        if isinstance(v, str):
            # ID модели - будет загружаться из реестра моделей
            if len(v.strip()) == 0:
                raise ValueError("ID модели не может быть пустым")
            if len(v) > 100:
                raise ValueError("ID модели не может быть длиннее 100 символов")
        elif isinstance(v, dict):
            # Встроенная конфигурация модели - валидируется ModelConfig
            try:
                ModelConfig(**v)
            except Exception as e:
                raise ValueError(f"Некорректная конфигурация модели: {e}")
        else:
            raise ValueError("reasoning_model должен быть строкой (ID) или объектом (ModelConfig)")
        
        return v
    
    @validator('reasoning_agent')
    def validate_reasoning_agent(cls, v):
        """Валидация агента для reasoning"""
        if v is None:
            return v
        
        if isinstance(v, str):
            # agent_id - ссылка на другого агента
            if len(v.strip()) == 0:
                raise ValueError("agent_id не может быть пустым")
            if len(v) > 100:
                raise ValueError("agent_id не может быть длиннее 100 символов")
        elif isinstance(v, dict):
            # Встроенная конфигурация агента
            required_fields = {'name', 'model', 'instructions'}
            if not any(field in v for field in required_fields):
                raise ValueError(f"Конфигурация агента должна содержать хотя бы одно из полей: {required_fields}")
        else:
            raise ValueError("reasoning_agent должен быть строкой (agent_id) или объектом (конфигурация)")
        
        return v


class TeamConfig(BaseModel):
    """Конфигурация команды (идентична Agno Team параметрам)"""
    # === ОСНОВНЫЕ ПАРАМЕТРЫ КОМАНДЫ ===
    team_mode: Optional[str] = Field(default="coordinate", description="Режим работы команды")
    role: Optional[str] = Field(default=None, description="Роль агента в команде")
    respond_directly: Optional[bool] = Field(default=False, description="Отвечать напрямую")
    add_transfer_instructions: Optional[bool] = Field(default=True, description="Добавить инструкции по передаче")
    team_response_separator: Optional[str] = Field(default="\n", description="Разделитель ответов команды")
    workflow_id: Optional[str] = Field(default=None, description="ID рабочего процесса")
    parent_team_id: Optional[str] = Field(default=None, description="ID родительской команды")
    
    # === СЛОЖНЫЕ ОБЪЕКТЫ ЧЕРЕЗ ССЫЛКИ ===
    team: Optional[List[Union[str, Dict[str, Any]]]] = Field(
        default=None,
        description="Команда агентов: список agent_id или встроенных конфигураций"
    )
    
    # === ДОПОЛНИТЕЛЬНЫЕ TEAM ПАРАМЕТРЫ ===
    team_id: Optional[str] = Field(default=None, description="UUID команды")
    team_session_id: Optional[str] = Field(default=None, description="ID сессии команды")
    team_session_state: Optional[Dict[str, Any]] = Field(default=None, description="Состояние сессии команды")
    members: Optional[List[Dict[str, Any]]] = Field(default=None, description="Участники команды")
    add_member_tools_to_system_message: Optional[bool] = Field(default=True, description="Добавить инструменты участников")
    show_members_responses: Optional[bool] = Field(default=False, description="Показывать ответы участников")
    stream_member_events: Optional[bool] = Field(default=True, description="Стриминг событий участников")
    share_member_interactions: Optional[bool] = Field(default=False, description="Делиться логами участников")
    get_member_information_tool: Optional[bool] = Field(default=False, description="Инструмент для получения инфо об участниках")
    
    @validator('team')
    def validate_team(cls, v):
        """Валидация команды агентов"""
        if v is None:
            return v
        
        if not isinstance(v, list):
            raise ValueError("team должен быть списком")
        
        if len(v) > 10:
            raise ValueError("Максимум 10 агентов в команде")
        
        for member in v:
            if isinstance(member, str):
                # agent_id - ссылка на агента
                if len(member.strip()) == 0:
                    raise ValueError("agent_id не может быть пустым")
                if len(member) > 100:
                    raise ValueError("agent_id не может быть длиннее 100 символов")
            elif isinstance(member, dict):
                # Встроенная конфигурация агента
                required_fields = {'name', 'model'}
                if not any(field in member for field in required_fields):
                    raise ValueError(f"Конфигурация агента должна содержать хотя бы одно из полей: {required_fields}")
            else:
                raise ValueError("Каждый участник команды должен быть строкой (agent_id) или объектом (конфигурация)")
        
        return v


class AgentSettings(BaseModel):
    """Дополнительные настройки агента (идентичные Agno Agent параметрам)"""
    
    # === ОСНОВНЫЕ ПАРАМЕТРЫ АГЕНТА ===
    introduction: Optional[str] = Field(default=None, description="Введение, добавляемое в начало чата")
    user_id: Optional[str] = Field(default=None, description="ID пользователя")
    session_id: Optional[str] = Field(default=None, description="UUID сессии")
    session_name: Optional[str] = Field(default=None, description="Название сессии")
    session_state: Optional[Dict[str, Any]] = Field(default=None, description="Состояние сессии")
    extra_data: Optional[Dict[str, Any]] = Field(default=None, description="Доп. данные агента")
    
    # === СИСТЕМНЫЕ СООБЩЕНИЯ ===
    system_message: Optional[str] = Field(default=None, description="Системное сообщение")
    system_message_role: Optional[str] = Field(default="system", description="Роль системного сообщения")
    create_default_system_message: Optional[bool] = Field(default=True, description="Создавать системное сообщение")
    system_prompt: Optional[str] = Field(default=None, description="Системный промпт")
    instructions: Optional[Union[str, List[str]]] = Field(default=None, description="Инструкции")
    
    # === ПОЛЬЗОВАТЕЛЬСКИЕ СООБЩЕНИЯ ===
    user_message: Optional[str] = Field(default=None, description="Сообщение пользователя")
    user_message_role: Optional[str] = Field(default="user", description="Роль пользователя")
    create_default_user_message: Optional[bool] = Field(default=True, description="Создавать сообщение пользователя")
    add_messages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Дополнительные сообщения")
    
    # === КОНТЕКСТ ===
    context: Optional[Dict[str, Any]] = Field(default=None, description="Контекст для инструментов")
    add_context: Optional[bool] = Field(default=False, description="Добавлять контекст к сообщению")
    resolve_context: Optional[bool] = Field(default=True, description="Выполнить функции в контексте")
    additional_context: Optional[str] = Field(default=None, description="Дополнительный контекст")
    add_state_in_messages: Optional[bool] = Field(default=False, description="Включить состояние в сообщения")
    
    # === ИСТОРИЯ ===
    add_history_to_messages: Optional[bool] = Field(default=False, description="Добавить историю в сообщения")
    num_history_runs: Optional[int] = Field(default=3, description="Количество предыдущих запусков")
    search_previous_sessions_history: Optional[bool] = Field(default=False, description="Поиск по предыдущим сессиям")
    num_history_sessions: Optional[int] = Field(default=2, description="Количество сессий в истории")
    read_chat_history: Optional[bool] = Field(default=False, description="Инструмент чтения истории")
    read_tool_call_history: Optional[bool] = Field(default=False, description="Инструмент истории вызовов")
    
    # === ФОРМАТИРОВАНИЕ ОТВЕТОВ ===
    markdown: Optional[bool] = Field(default=False, description="Форматировать как Markdown")
    add_name_to_instructions: Optional[bool] = Field(default=False, description="Добавить имя к инструкциям")
    add_datetime_to_instructions: Optional[bool] = Field(default=False, description="Добавить дату/время к системному сообщению")
    add_location_to_instructions: Optional[bool] = Field(default=False, description="Добавить локацию к системному сообщению")
    timezone_identifier: Optional[str] = Field(default=None, description="Идентификатор временной зоны (TZ Database format)")
    save_response_to_file: Optional[str] = Field(default=None, description="Сохранение ответа в файл")
    
    # === ПОТОКОВАЯ ПЕРЕДАЧА ===
    stream: Optional[bool] = Field(default=None, description="Стриминг ответа")
    stream_intermediate_steps: Optional[bool] = Field(default=False, description="Стримить промежуточные шаги")
    
    # === ОТЛАДКА И МОНИТОРИНГ ===
    debug_mode: Optional[bool] = Field(default=False, description="Режим отладки")
    monitoring: Optional[bool] = Field(default=False, description="Логирование в agno.com")
    telemetry: Optional[bool] = Field(default=True, description="Минимальное логирование")
    
    # === RETRY ЛОГИКА ===
    retries: Optional[int] = Field(default=0, description="Количество попыток при ошибке")
    delay_between_retries: Optional[int] = Field(default=1, description="Задержка между попытками")
    exponential_backoff: Optional[bool] = Field(default=False, description="Удвоение задержки")
    
    # === ПАРСИНГ И ОТВЕТЫ ===
    response_model: Optional[Dict[str, Any]] = Field(default=None, description="Модель ответа (BaseModel)")
    parse_response: Optional[bool] = Field(default=True, description="Преобразовать ответ в модель")
    use_json_mode: Optional[bool] = Field(default=False, description="Ответ в JSON формате")
    parser_model: Optional[Union[ModelConfig, str]] = Field(
        default=None, 
        description="Модель для парсинга: ModelConfig объект или ID модели из реестра"
    )
    parser_model_prompt: Optional[str] = Field(default=None, description="Промпт для парсинга")
    
    # === СОБЫТИЯ ===
    store_events: Optional[bool] = Field(default=False, description="Сохранять события выполнения")
    events_to_skip: Optional[List[str]] = Field(default=None, description="Пропускать указанные события")
    
    # === КОМАНДА (TEAM) ===
    team_data: Optional[Dict[str, Any]] = Field(default=None, description="Общие данные команды")
    team_session_id: Optional[str] = Field(default=None, description="ID командной сессии")
    
    # === ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ===
    config_version: Optional[str] = Field(default="1.0", description="Версия конфигурации")
    tags: Optional[List[str]] = Field(default=None, description="Теги для поиска")
    app_id: Optional[str] = Field(default=None, description="ID приложения")


class DynamicAgent(Base):
    """
    Упрощенная модель для динамических агентов с Pydantic валидацией.
    Лаконичная структура с прямой интеграцией Agno параметров.
    """
    __tablename__ = 'dynamic_agents'
    __table_args__ = {'schema': 'ai'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # Имя агента
    agent_id = Column(String(100), nullable=False, unique=True)  # UUID агента
    description = Column(Text, nullable=True)  # Описание агента
    instructions = Column(Text, nullable=True)  # Инструкции для агента
    
    # === КОНФИГУРАЦИИ С PYDANTIC ВАЛИДАЦИЕЙ ===
    
    # Основные конфигурации (Pydantic модели сериализуются в JSONB)
    model_configuration = Column(JSONB, nullable=True)  # ModelConfig
    tools_config = Column(JSONB, nullable=True)  # ToolsConfig
    knowledge_config = Column(JSONB, nullable=True)  # KnowledgeConfig
    memory_config = Column(JSONB, nullable=True)  # MemoryConfig
    storage_config = Column(JSONB, nullable=True)  # StorageConfig
    reasoning_config = Column(JSONB, nullable=True)  # ReasoningConfig
    team_config = Column(JSONB, nullable=True)  # TeamConfig
    settings = Column(JSONB, nullable=True)  # AgentSettings
    
    # Мета-информация
    is_active = Column(Boolean, nullable=True, default=True)
    is_active_api = Column(Boolean, nullable=True, default=True)
    is_public = Column(Boolean, nullable=True, default=False)  # Публичность агента
    company_id = Column(Text, nullable=True)  # ID компании
    photo = Column(Text, nullable=True)  # Фото агента
    created_at = Column(DateTime, nullable=True, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=True, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        """Валидация agent_id"""
        if not agent_id or len(agent_id.strip()) == 0:
            raise ValueError("agent_id не может быть пустым")
        if len(agent_id) > 100:
            raise ValueError("agent_id не может быть длиннее 100 символов")
        return agent_id.strip()

    @validates('name')
    def validate_name(self, key, name):
        """Валидация имени агента"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Имя агента не может быть пустым")
        if len(name) > 255:
            raise ValueError("Имя агента не может быть длиннее 255 символов")
        return name.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект агента в словарь, включая все конфигурации."""
        return {
            "id": self.id,
            "name": self.name,
            "agent_id": self.agent_id,
            "description": self.description,
            "instructions": self.instructions,
            "model_configuration": self.model_configuration,
            "tools_config": self.tools_config,
            "knowledge_config": self.knowledge_config,
            "memory_config": self.memory_config,
            "storage_config": self.storage_config,
            "reasoning_config": self.reasoning_config,
            "team_config": self.team_config,
            "settings": self.settings,
            "is_active": self.is_active,
            "is_active_api": self.is_active_api,
            "is_public": self.is_public,
            "company_id": self.company_id,
            "photo": self.photo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    # === Методы для работы с Pydantic моделями ===
    
    def get_model_config(self) -> Optional[ModelConfig]:
        """Get model configuration as ModelConfig object"""
        if not self.model_configuration:
            return None
        return ModelConfig(**self.model_configuration)
    
    def set_model_config(self, config: ModelConfig):
        """Set model configuration from ModelConfig object"""
        self.model_configuration = config.dict(exclude_none=True)
    
    def get_tools_config(self) -> Optional[ToolsConfig]:
        """Получить типизированную конфигурацию инструментов"""
        if not self.tools_config:
            return None
        return ToolsConfig(**self.tools_config)
    
    def set_tools_config(self, config: ToolsConfig):
        """Установить конфигурацию инструментов"""
        self.tools_config = config.dict(exclude_none=True)
    
    def get_memory_config(self) -> Optional[MemoryConfig]:
        """Получить типизированную конфигурацию памяти"""
        if not self.memory_config:
            return None
        return MemoryConfig(**self.memory_config)
    
    def set_memory_config(self, config: MemoryConfig):
        """Установить конфигурацию памяти"""
        self.memory_config = config.dict(exclude_none=True)
    
    def get_knowledge_config(self) -> Optional[KnowledgeConfig]:
        """Получить типизированную конфигурацию знаний"""
        if not self.knowledge_config:
            return None
        return KnowledgeConfig(**self.knowledge_config)
    
    def set_knowledge_config(self, config: KnowledgeConfig):
        """Установить конфигурацию знаний"""
        self.knowledge_config = config.dict(exclude_none=True)
    
    def get_storage_config(self) -> Optional[StorageConfig]:
        """Получить типизированную конфигурацию хранилища"""
        if not self.storage_config:
            return None
        return StorageConfig(**self.storage_config)
    
    def set_storage_config(self, config: StorageConfig):
        """Установить конфигурацию хранилища"""
        self.storage_config = config.dict(exclude_none=True)
    
    def get_reasoning_config(self) -> Optional[ReasoningConfig]:
        """Получить типизированную конфигурацию reasoning"""
        if not self.reasoning_config:
            return None
        return ReasoningConfig(**self.reasoning_config)
    
    def set_reasoning_config(self, config: ReasoningConfig):
        """Установить конфигурацию reasoning"""
        self.reasoning_config = config.dict(exclude_none=True)
    
    def get_team_config(self) -> Optional[TeamConfig]:
        """Получить типизированную конфигурацию команды"""
        if not self.team_config:
            return None
        return TeamConfig(**self.team_config)
    
    def set_team_config(self, config: TeamConfig):
        """Установить конфигурацию команды"""
        self.team_config = config.dict(exclude_none=True)
    
    def get_settings(self) -> Optional[AgentSettings]:
        """Получить настройки агента"""
        if self.settings is None:
            return None
        return AgentSettings(**self.settings)
    
    def set_settings(self, settings: AgentSettings):
        """Установить настройки агента"""
        self.settings = settings.dict(exclude_none=True)
    

    


    def __repr__(self):
        return f"<DynamicAgent(id={self.id}, agent_id='{self.agent_id}', name='{self.name}', active={self.is_active})>" 


# === НОВАЯ МОДЕЛЬ ДЛЯ ДИНАМИЧЕСКИХ ИНСТРУМЕНТОВ ===
class DynamicTool(Base):
    """Конфигурация динамического инструмента"""
    __tablename__ = 'dynamic_tools'
    __table_args__ = {'schema': 'ai'}
    
    id = Column(Integer, primary_key=True)
    tool_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)  # Альтернативное название
    agno_class = Column(String(255), nullable=False)  # DuckDuckGoTools, YFinanceTools, etc.
    module_path = Column(String(500), nullable=False)  # agno.tools.duckduckgo, agno.tools.yfinance, etc.
    config = Column(JSONB, nullable=True, default={})
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # Категория для группировки
    icon = Column(String(255), nullable=True)  # Иконка для фронтенда
    company_id = Column(Text, nullable=True)  # ID компании
    is_public = Column(Boolean, nullable=True, default=False)  # Публичность инструмента
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @validates('tool_id')
    def validate_tool_id(self, key, tool_id):
        """Валидация ID инструмента"""
        if not tool_id or len(tool_id.strip()) < 3:
            raise ValueError("ID инструмента должен содержать минимум 3 символа")
        if len(tool_id) > 100:
            raise ValueError("ID инструмента не может быть длиннее 100 символов")
        return tool_id.strip()

    @validates('name')
    def validate_name(self, key, name):
        """Валидация названия инструмента"""
        if not name or len(name.strip()) < 3:
            raise ValueError("Название инструмента должно содержать минимум 3 символа")
        if len(name) > 255:
            raise ValueError("Название инструмента не может быть длиннее 255 символов")
        return name.strip()

    @validates('agno_class')
    def validate_agno_class(self, key, agno_class):
        """Валидация класса Agno"""
        if not agno_class or not agno_class.strip():
            raise ValueError("Класс Agno обязателен")
        if len(agno_class) > 255:
            raise ValueError("Класс Agno не может быть длиннее 255 символов")
        return agno_class.strip()

    @validates('module_path')
    def validate_module_path(self, key, module_path):
        """Валидация пути к модулю"""
        if not module_path or not module_path.strip():
            raise ValueError("Путь к модулю обязателен")
        if len(module_path) > 500:
            raise ValueError("Путь к модулю не может быть длиннее 500 символов")
        if not module_path.startswith('agno.tools.'):
            raise ValueError("Путь к модулю должен начинаться с 'agno.tools.'")
        return module_path.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'tool_id': self.tool_id,
            'name': self.name,
            'display_name': self.display_name,
            'agno_class': self.agno_class,
            'module_path': self.module_path,
            'config': self.config,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'company_id': self.company_id,
            'is_public': self.is_public,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<DynamicTool(tool_id='{self.tool_id}', name='{self.name}', agno_class='{self.agno_class}', module='{self.module_path}')>" 


# === МОДЕЛИ ДЛЯ КАСТОМНЫХ ИНСТРУМЕНТОВ И MCP ===

class CustomTool(Base):
    """Модель для кастомных Python инструментов"""
    __tablename__ = 'custom_tools'
    __table_args__ = {'schema': 'ai'}
    
    id = Column(Integer, primary_key=True)
    tool_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_code = Column(Text, nullable=False)
    config = Column(JSONB, nullable=True, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    @validates('tool_id')
    def validate_tool_id(self, key, tool_id):
        """Валидация ID инструмента"""
        if not tool_id or len(tool_id.strip()) < 3:
            raise ValueError("ID инструмента должен содержать минимум 3 символа")
        if len(tool_id) > 100:
            raise ValueError("ID инструмента не может быть длиннее 100 символов")
        # Проверка на корректный идентификатор Python
        if not tool_id.replace('_', '').isalnum():
            raise ValueError("ID инструмента должен содержать только буквы, цифры и подчеркивания")
        return tool_id.strip()
    
    @validates('source_code')
    def validate_source_code(self, key, source_code):
        """Базовая валидация кода"""
        if not source_code or len(source_code.strip()) < 10:
            raise ValueError("Исходный код должен содержать минимум 10 символов")
        
        # Простая проверка на опасные конструкции
        dangerous = ['import os', 'import sys', 'import subprocess', 
                    'exec(', 'eval(', '__import__', 'open(', 'compile(']
        for pattern in dangerous:
            if pattern in source_code:
                raise ValueError(f"Код содержит небезопасную конструкцию: {pattern}")
        
        # Проверка синтаксиса
        try:
            compile(source_code, '<string>', 'exec')
        except SyntaxError as e:
            raise ValueError(f"Синтаксическая ошибка в коде: {e}")
        
        return source_code
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'tool_id': self.tool_id,
            'name': self.name,
            'description': self.description,
            'source_code': self.source_code,
            'config': self.config,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<CustomTool(tool_id='{self.tool_id}', name='{self.name}', active={self.is_active})>"


class MCPServer(Base):
    """Модель для MCP серверов"""
    __tablename__ = 'mcp_servers'
    __table_args__ = {'schema': 'ai'}
    
    id = Column(Integer, primary_key=True)
    server_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    command = Column(Text, nullable=True)  # Для stdio transport
    url = Column(String(500), nullable=True)  # Для sse/http transport
    transport = Column(String(20), default='stdio')
    env_config = Column(JSONB, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    @validates('server_id')
    def validate_server_id(self, key, server_id):
        """Валидация ID сервера"""
        if not server_id or len(server_id.strip()) < 3:
            raise ValueError("ID сервера должен содержать минимум 3 символа")
        if len(server_id) > 100:
            raise ValueError("ID сервера не может быть длиннее 100 символов")
        if not server_id.replace('_', '').replace('-', '').isalnum():
            raise ValueError("ID сервера должен содержать только буквы, цифры, подчеркивания и дефисы")
        return server_id.strip()
    
    @validates('transport')
    def validate_transport(self, key, transport):
        """Валидация типа транспорта"""
        valid_transports = ['stdio', 'sse', 'streamable-http']
        if transport not in valid_transports:
            raise ValueError(f"Транспорт должен быть одним из: {', '.join(valid_transports)}")
        return transport
    
    @validates('command', 'url')
    def validate_connection_params(self, key, value):
        """Валидация параметров подключения"""
        if key == 'command' and self.transport == 'stdio' and not value:
            raise ValueError("Для stdio транспорта требуется команда")
        if key == 'url' and self.transport in ['sse', 'streamable-http'] and not value:
            raise ValueError(f"Для {self.transport} транспорта требуется URL")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'description': self.description,
            'command': self.command,
            'url': self.url,
            'transport': self.transport,
            'env_config': self.env_config,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<MCPServer(server_id='{self.server_id}', name='{self.name}', transport='{self.transport}')" 

# ==============================================================================
# === 🛡️ Безопасные модели для прямой передачи в Agno (системное решение) ===
# ==============================================================================

class AgnoBaseModel(BaseModel):
    """Базовая модель с общей конфигурацией для безопасной передачи в Agno."""
    class Config:
        extra = 'ignore'  # Игнорировать любые поля, не определенные в этой модели

# ------------------------------------------------------------------------------
# --- 1. Безопасные параметры для agno.storage.agent.postgres.PostgresAgentStorage ---
# ------------------------------------------------------------------------------

class AgnoStorageParams(AgnoBaseModel):
    """
    Содержит только те поля, которые принимает конструктор PostgresAgentStorage.
    """
    db_url: Optional[str] = None
    table_name: Optional[str] = "sessions"
    # ❗️ Поле переименовано в db_schema во избежание конфликта с BaseModel.schema()
    db_schema: Optional[str] = Field(default=None, alias="schema") 
    auto_upgrade_schema: Optional[bool] = False

# ------------------------------------------------------------------------------
# --- 2. Безопасные параметры для agno.knowledge.AgentKnowledge ---
# ------------------------------------------------------------------------------

class AgnoKnowledgeParams(AgnoBaseModel):
    """
    Содержит только те поля, которые принимает конструктор AgentKnowledge.
    """
    add_references: Optional[bool] = None
    references_format: Optional[str] = None
    search_knowledge: Optional[bool] = None
    update_knowledge: Optional[bool] = None
    max_references: Optional[int] = None
    similarity_threshold: Optional[float] = None
    
# ------------------------------------------------------------------------------
# --- 3. Безопасные параметры для agno.agent.Agent (в части Reasoning) ---
# ------------------------------------------------------------------------------

class AgnoReasoningParams(AgnoBaseModel):
    """
    Содержит только те поля, которые используются для конфигурации Reasoning в Agent.
    """
    reasoning: Optional[bool] = None
    max_steps: Optional[int] = None
    max_tokens_per_step: Optional[int] = None
    stop_on_observation: Optional[bool] = None

# ------------------------------------------------------------------------------
# --- 4. Безопасные параметры для agno.agent.Agent (общие настройки) ---
# ------------------------------------------------------------------------------

class AgnoAgentSettings(AgnoBaseModel):
    """
    Содержит только те общие поля из AgentSettings, которые принимает Agno Agent.
    Исключает наши кастомные поля типа 'config_version', 'store_events'.
    """
    # Общие
    introduction: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Системные и пользовательские сообщения
    system_message: Optional[str] = None
    system_message_role: Optional[str] = None
    create_default_system_message: Optional[bool] = None
    user_message: Optional[str] = None
    user_message_role: Optional[str] = None
    create_default_user_message: Optional[bool] = None
    
    # Контекст и состояние
    context: Optional[Dict[str, Any]] = None
    add_context: Optional[bool] = None
    resolve_context: Optional[bool] = None
    add_state_to_instructions: Optional[bool] = None
    add_state_in_messages: Optional[bool] = None
    add_datetime_to_instructions: Optional[bool] = None
    
    # История
    add_history_to_messages: Optional[bool] = None
    num_history_runs: Optional[int] = None
    search_previous_sessions_history: Optional[bool] = None
    num_history_sessions: Optional[int] = None
    read_chat_history: Optional[bool] = None
    
    # Форматирование и вывод
    markdown: Optional[bool] = None
    stream: Optional[bool] = None
    json_output: Optional[bool] = None
    
    # Память
    enable_agentic_memory: Optional[bool] = None
    enable_user_memories: Optional[bool] = None
    add_memory_references: Optional[bool] = None
    
    # Дополнительные возможности
    retriever: Optional[Dict[str, Any]] = None  # Callable сериализуется как Dict
    
    # Отладка
    debug_mode: Optional[bool] = None

    # === НЕДОСТАЮЩИЕ ПАРАМЕТРЫ ИЗ AGNO.AGENT ===

    # Системные и промпты
    session_name: Optional[str] = None
    session_state: Optional[Dict[str, Any]] = None
    goal: Optional[str] = None
    success_criteria: Optional[str] = None
    expected_output: Optional[str] = None
    additional_context: Optional[str] = None
    timezone_identifier: Optional[str] = None

    # Сообщения и инструкции
    add_name_to_instructions: Optional[bool] = None
    add_location_to_instructions: Optional[bool] = None
    add_messages: Optional[List[Dict[str, Any]]] = None

    # История
    num_history_responses: Optional[int] = None

    # Знания
    knowledge_filters: Optional[Dict[str, Any]] = None
    enable_agentic_knowledge_filters: Optional[bool] = None
    add_references: Optional[bool] = None
    references_format: Optional[str] = None
    search_knowledge: Optional[bool] = None
    update_knowledge: Optional[bool] = None

    # Инструменты
    show_tool_calls: Optional[bool] = None
    tool_call_limit: Optional[int] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    read_tool_call_history: Optional[bool] = None

    # Reasoning
    reasoning: Optional[bool] = None
    reasoning_min_steps: Optional[int] = None
    reasoning_max_steps: Optional[int] = None

    # Парсинг и ответы
    parser_model_prompt: Optional[str] = None
    response_model: Optional[Dict[str, Any]] = None  # Type[BaseModel] -> Dict
    parse_response: Optional[bool] = None
    structured_outputs: Optional[bool] = None
    use_json_mode: Optional[bool] = None
    save_response_to_file: Optional[str] = None

    # Стриминг и события
    stream_intermediate_steps: Optional[bool] = None
    store_events: Optional[bool] = None
    events_to_skip: Optional[List[str]] = None  # List[RunEvent] -> List[str]

    # Retry логика
    retries: Optional[int] = None
    delay_between_retries: Optional[int] = None
    exponential_backoff: Optional[bool] = None

    # Команда
    team_data: Optional[Dict[str, Any]] = None
    role: Optional[str] = None
    respond_directly: Optional[bool] = None
    add_transfer_instructions: Optional[bool] = None
    team_response_separator: Optional[str] = None

    # Дополнительные системные
    debug_level: Optional[int] = None  # Literal[1, 2] -> int
    monitoring: Optional[bool] = None
    telemetry: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None 

# === ПРИМЕЧАНИЕ: Pydantic модели реестров находятся в db/registry_models.py === 

# === SQL ТАБЛИЦЫ ДЛЯ РЕЕСТРОВ ===

class ModelRegistryTable(Base):
    """SQL таблица для реестра моделей"""
    __tablename__ = 'model_registry'
    __table_args__ = {'schema': 'ai'}

    id = Column(Integer, primary_key=True)
    registry_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    model_config = Column(JSONB, nullable=False)  # ModelConfig в JSON
    is_active = Column(Boolean, nullable=False, default=True)
    tags = Column(JSONB, nullable=True)  # Массив строк
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def get_model_config(self) -> Optional[ModelConfig]:
        """Получить Pydantic модель из JSON"""
        if self.model_config:
            try:
                return ModelConfig(**self.model_config)
            except Exception as e:
                print(f"Ошибка парсинга model_config для {self.registry_id}: {e}")
                return None
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            'registry_id': self.registry_id,
            'name': self.name,
            'description': self.description,
            'model_config': self.model_config,
            'is_active': self.is_active,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class AgentRegistryTable(Base):
    """SQL таблица для реестра агентов"""
    __tablename__ = 'agent_registry'
    __table_args__ = {'schema': 'ai'}

    id = Column(Integer, primary_key=True)
    registry_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    agent_config = Column(JSONB, nullable=False)  # Упрощенная конфигурация агента
    is_active = Column(Boolean, nullable=False, default=True)
    tags = Column(JSONB, nullable=True)  # Массив строк
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            'registry_id': self.registry_id,
            'name': self.name,
            'description': self.description,
            'agent_config': self.agent_config,
            'is_active': self.is_active,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class HookRegistryTable(Base):
    """SQL таблица для реестра хуков"""
    __tablename__ = 'hook_registry'
    __table_args__ = {'schema': 'ai'}

    id = Column(Integer, primary_key=True)
    registry_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    hook_type = Column(String(50), nullable=False)  # before_tool_call, after_tool_call, on_tool_error
    module_path = Column(String(500), nullable=False)
    function_name = Column(String(255), nullable=False)
    config = Column(JSONB, nullable=True)  # Конфигурация хука
    is_active = Column(Boolean, nullable=False, default=True)
    tags = Column(JSONB, nullable=True)  # Массив строк
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def get_hook_config(self) -> Optional[Any]:
        """Получить Pydantic модель из данных таблицы"""
        try:
            from db.registry_models import HookRegistry
            return HookRegistry(
                registry_id=self.registry_id,
                name=self.name,
                description=self.description,
                hook_type=self.hook_type,
                module_path=self.module_path,
                function_name=self.function_name,
                config=self.config,
                is_active=self.is_active,
                tags=self.tags,
                created_at=self.created_at,
                updated_at=self.updated_at,
            )
        except Exception as e:
            print(f"Ошибка создания HookRegistry для {self.registry_id}: {e}")
            return None

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            'registry_id': self.registry_id,
            'name': self.name,
            'description': self.description,
            'hook_type': self.hook_type,
            'module_path': self.module_path,
            'function_name': self.function_name,
            'config': self.config,
            'is_active': self.is_active,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }