# 🚀 РЕАЛИЗОВАННЫЕ КОНФИГУРАЦИИ ДИНАМИЧЕСКИХ СУЩНОСТЕЙ

> ✅ **ПОЛНОЕ ПОКРЫТИЕ:** Все 8 основных конфигураций агентов реализованы на 100%  
> 📊 **Основано на:** Agno 1.7.0 с полной поддержкой всех Agent параметров  
> 🎯 **Статус:** Готово к использованию в продакшене

## 📋 СОДЕРЖАНИЕ РЕАЛИЗОВАННЫХ КОНФИГУРАЦИЙ

### 🤖 ОСНОВНЫЕ КОНФИГУРАЦИИ АГЕНТОВ (8/8 ✅)
- [1. ModelConfig - Конфигурация моделей](#1-modelconfig---конфигурация-моделей-✅)
- [2. ToolsConfig - Конфигурация инструментов](#2-toolsconfig---конфигурация-инструментов-✅)
- [3. MemoryConfig - Конфигурация памяти](#3-memoryconfig---конфигурация-памяти-✅)
- [4. KnowledgeConfig - Конфигурация базы знаний](#4-knowledgeconfig---конфигурация-базы-знаний-✅)
- [5. StorageConfig - Конфигурация хранилища](#5-storageconfig---конфигурация-хранилища-✅)
- [6. ReasoningConfig - Конфигурация reasoning](#6-reasoningconfig---конфигурация-reasoning-✅)
- [7. TeamConfig - Конфигурация команды](#7-teamconfig---конфигурация-команды-✅)
- [8. AgentSettings - Дополнительные настройки](#8-agentsettings---дополнительные-настройки-✅)

### 🔧 ДОПОЛНИТЕЛЬНЫЕ СУЩНОСТИ
- [9. DynamicTool - Динамические инструменты](#9-dynamictool---динамические-инструменты)
- [10. CustomTool - Кастомные инструменты](#10-customtool---кастомные-инструменты)
- [11. MCPServer - MCP серверы](#11-mcpserver---mcp-серверы)

---

## 🎯 КРАТКИЙ ОБЗОР АРХИТЕКТУРЫ

### Как это работает:
```
📊 JSON Config (БД) → 🔍 Pydantic Validation → 🔄 Service Layer → 🤖 agno.Agent
```

1. **Конфигурации сохраняются в PostgreSQL** как JSONB поля
2. **Pydantic модели валидируют** все параметры на соответствие agno
3. **Service слой превращает** JSON в живые объекты agno
4. **Готовый Agent** можно использовать как обычный agno.Agent

### Преимущества:
- ✅ **100% совместимость** с agno.Agent
- ✅ **Динамическое создание** агентов без перезапуска
- ✅ **Полная валидация** всех параметров
- ✅ **Типобезопасность** через Pydantic
- ✅ **Кэширование** для производительности

---

## 1. ModelConfig - Конфигурация моделей ✅

### 🎯 Описание
**ModelConfig** - это сердце агента, определяющее какую языковую модель использовать и как она будет работать. Поддерживает **ВСЕ** провайдеры и параметры из agno.

### 🔧 Как это работает
1. **Pydantic валидация** проверяет все параметры на соответствие API провайдера
2. **Service слой** создает нужный объект модели (OpenAIChat, Claude, Gemini)
3. **Agent** использует модель для генерации ответов

### 💡 Поддерживаемые провайдеры
- **OpenAI:** GPT-4o, GPT-4, GPT-3.5, o1, o3 (+ новые параметры reasoning_effort)
- **Anthropic:** Claude 3.5, Claude 3 (+ Claude-специфичные параметры)
- **Google:** Gemini 1.5, Gemini 2.0 (+ Vertex AI поддержка)
- **Azure OpenAI:** Все модели OpenAI через Azure
- **Остальные:** Groq, Cohere, Together AI, Ollama, и др.

### 📝 Структура конфигурации

#### 🔑 Основные параметры
```json
{
  "id": "gpt-4o",                    // ✅ ID модели - главный параметр
  "name": "GPT-4 Omni",              // ✅ Человекочитаемое имя
  "provider": "openai"                // ✅ Провайдер (auto-detect по id)
}
```

#### 🤖 OpenAI параметры (GPT-4, GPT-3.5, o1, o3)
```json
{
  // 🎛️ Базовые параметры генерации
  "temperature": 0.7,                 // Креативность (0.0=детерминизм, 2.0=хаос)
  "max_tokens": 4000,                 // Лимит токенов ответа (1-200000)
  "max_completion_tokens": 2000,      // Альтернативный лимит для completion
  "top_p": 0.9,                       // Nucleus sampling (0.0-1.0)
  "frequency_penalty": 0.0,           // Штраф за повторения (-2.0 до 2.0)
  "presence_penalty": 0.0,            // Штраф за упоминания (-2.0 до 2.0)
  
  // 🛑 Управление остановкой
  "stop": ["END", "STOP"],            // Стоп-слова (строка или массив)
  "seed": 42,                         // Сид для детерминизма
  
  // 📊 Продвинутые параметры
  "logit_bias": {"50256": -100},      // Принудительное изменение вероятностей
  "logprobs": true,                   // Получать логарифмы вероятностей
  "top_logprobs": 5,                  // Количество топ логпробов на токен
  
  // 🆔 Идентификация
  "user": "user_123",                 // ID пользователя для трекинга
  "store": false,                     // Сохранять ли разговор в OpenAI
  "metadata": {"session": "chat_1"},  // Произвольные метаданные
  
  // 🎵 Мультимодальность (GPT-4o, GPT-4o-mini)
  "modalities": ["text", "audio"],    // Поддерживаемые типы контента
  "audio": {"voice": "alloy", "format": "wav"}, // Настройки аудио
  
  // 📋 Форматирование ответа
  "response_format": {"type": "json_object"}, // Принудительный JSON
  
  // 🧠 O3 НОВАЯ ФИЧА! (только для o3-модели)
  "reasoning_effort": "medium"        // Уровень рассуждений: low/medium/high
}
```

#### 🎭 Claude (Anthropic) параметры
```json
{
  // 🛑 Остановка генерации (Claude-специфично)
  "stop_sequences": ["Human:", "AI:"], // Максимум 4 стоп-фразы
  "top_k": 40,                        // Top-k sampling (1-500, Claude-только)
  "max_tokens": 4000,                 // У Claude только max_tokens (не max_completion_tokens)
  
  // ⚠️ ВАЖНО: Claude НЕ поддерживает seed, frequency_penalty, presence_penalty
}
```

#### 🔍 Gemini (Google) параметры
```json
{
  // 📊 Генерация
  "max_output_tokens": 2000,          // Gemini использует max_output_tokens
  "generation_config": {              // Детальная конфигурация генерации
    "candidate_count": 1,             // Количество вариантов ответа
    "stop_sequences": ["END"],        // Стоп-слова для Gemini
    "max_output_tokens": 2000,        // Дублирование для совместимости
    "temperature": 0.7,               // Можно дублировать основные параметры
    "top_p": 0.9,
    "top_k": 40
  },
  
  // 🛡️ Безопасность
  "safety_settings": {                // Настройки фильтрации контента
    "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE"
  },
  
  // 🔧 Функциональность
  "function_declarations": [],        // Объявления функций (альтернатива tools)
  "grounding": true,                  // Поиск в реальном времени
  "search": true,                     // Веб-поиск
  "grounding_dynamic_threshold": 0.7, // Порог релевантности поиска
  
  // ☁️ Google Cloud
  "vertexai": false,                  // Использовать Vertex AI вместо Studio
  "project_id": "my-gcp-project",     // GCP проект (для Vertex AI)
  "location": "us-central1"           // Регион GCP
}
```

#### 🌐 API параметры (универсальные)
```json
{
  // 🔐 Аутентификация
  "api_key": "sk-proj-...",           // API ключ провайдера
  "organization": "org-...",          // Организация (OpenAI only)
  
  // 🔗 Подключение
  "base_url": "https://api.openai.com/v1", // Альтернативный endpoint
  "timeout": 60.0,                    // Таймаут запроса в секундах
  "max_retries": 3,                   // Количество повторов при ошибке
  
  // 📡 HTTP настройки
  "extra_headers": {                  // Дополнительные HTTP заголовки
    "X-Custom-Header": "value",
    "Authorization-Custom": "Bearer token"
  },
  "extra_query": {"version": "2024-01"}, // URL параметры
  "request_params": {"verify": true}, // Параметры requests библиотеки
  "default_headers": {},              // Заголовки по умолчанию
  "default_query": {},                // URL параметры по умолчанию
  "client_params": {"http2": true}    // Параметры HTTP клиента
}
```

### ⚠️ Важные особенности валидации

1. **Автоматическая детекция провайдера** по model ID:
   - `gpt-*` → OpenAI
   - `claude-*` → Anthropic  
   - `gemini-*` → Google
   
2. **Кросс-валидация параметров**:
   - `reasoning_effort` только для o3 моделей
   - `top_k` не работает с OpenAI
   - `seed` не поддерживается Claude

3. **Умные дефолты**:
   - Если не указан `temperature`, используется дефолт провайдера
   - Автоматическое определение `max_tokens` vs `max_output_tokens`

---

## 2. ToolsConfig - Конфигурация инструментов ✅

### 🎯 Описание
**ToolsConfig** управляет "суперсилами" агента - всеми инструментами, которые он может использовать. Поддерживает **101+ классов** agno инструментов + наши динамические расширения.

### 🔧 Как это работает
1. **Статические инструменты** - прямые объекты agno (DuckDuckGoTools, CalculatorTools)
2. **Динамические инструменты** - созданные через БД с конфигурацией
3. **Кастомные инструменты** - пользовательский Python код
4. **MCP серверы** - внешние инструменты через Model Context Protocol

### 💪 Типы инструментов

#### 🔧 Статические инструменты (прямая поддержка agno)
```json
{
  "tools": [                          // Список готовых agno инструментов
    {
      "type": "DuckDuckGoTools",      // ✅ Класс из agno.tools.*
      "search_engine": "duckduckgo",  // ✅ Параметры конфигурации
      "max_results": 10
    },
    {
      "type": "CalculatorTools"       // ✅ Простой инструмент без конфигурации
    },
    {
      "type": "YFinanceTools",        // ✅ Финансовые данные
      "enable_cache": true,
      "cache_ttl": 3600
    }
  ]
}
```

#### 🌟 Динамические инструменты (наша фишка!)
```json
{
  "dynamic_tools": [                 // ✅ ID инструментов из таблицы dynamic_tools
    "web_search_001",               // ✅ Ссылается на DynamicTool.tool_id
    "financial_data_002",           // ✅ Конфигурация хранится в БД
    "weather_api_003"               // ✅ Можно изменять без перезапуска!
  ]
}
```

#### 🎨 Кастомные инструменты (пользовательский код)
```json
{
  "custom_tools": [                  // ✅ ID кастомных Python инструментов
    "my_company_crm_tool",          // ✅ Ссылается на CustomTool.tool_id
    "internal_database_query",      // ✅ Исходный код хранится в БД
    "proprietary_algorithm"         // ✅ Полная безопасность выполнения
  ]
}
```

#### 🔌 MCP серверы (внешние инструменты)
```json
{
  "mcp_servers": [                   // ✅ ID MCP серверов из таблицы mcp_servers
    "filesystem_server",            // ✅ Локальная файловая система
    "database_server",              // ✅ Подключение к БД
    "external_api_server"           // ✅ Интеграция с внешними API
  ]
}
```

### 🎛️ Управление поведением инструментов

#### Основные параметры управления:
```json
{
  // 👁️ Видимость
  "show_tool_calls": true,            // Показывать ли вызовы инструментов пользователю
  
  // 🚦 Ограничения
  "tool_call_limit": 20,              // Максимум вызовов за запрос (1-100)
  
  // 🤖 Управление выбором инструментов
  "tool_choice": "auto",              // "auto" | "none" | "required" | объект
  
  // 🎣 Хуки и события
  "tool_hooks": [                     // Выполнить код до/после вызова
    {
      "type": "before_tool_call",
      "function": "log_tool_usage"
    },
    {
      "type": "after_tool_call", 
      "function": "validate_result"
    }
  ],
  
  // 📋 Дополнительные объявления (для Gemini)
  "function_declarations": []         // Альтернативный способ объявления функций
}
```

#### Детальные варианты tool_choice:
```json
{
  // Автоматический выбор (по умолчанию)
  "tool_choice": "auto",              // ✅ LLM сам решает когда использовать инструменты
  
  // Принудительное использование
  "tool_choice": "required",          // ✅ Обязательно использовать инструмент
  
  // Запрет инструментов
  "tool_choice": "none",              // ✅ Не использовать инструменты вообще
  
  // Принудительный выбор конкретного инструмента
  "tool_choice": {
    "type": "function",
    "function": {"name": "DuckDuckGoTools.search"}
  }
}
```
### ⚠️ Особенности валидации

1. **Лимиты безопасности**:
   - Максимум 50 статических инструментов на агента
   - Максимум 20 динамических инструментов  
   - Максимум 20 кастомных инструментов
   - Максимум 10 MCP серверов

2. **Проверка существования**:
   - Все `dynamic_tools` ID проверяются в БД
   - Все `custom_tools` ID проверяются в БД
   - Все `mcp_servers` ID проверяются в БД

3. **Автоматическая загрузка**:
   - Service слой автоматически создает объекты инструментов
   - Кэширование для производительности
   - Lazy loading для больших наборов инструментов

---

## 3. MemoryConfig - Конфигурация памяти ✅

### 🎯 Описание  
**MemoryConfig** дает агенту долговременную память - способность помнить предыдущие разговоры, изучать пользователя и накапливать знания. Поддерживается только PostgreSQL (включая Supabase).

### 🧠 Как работает память agno
1. **Обычная память** - сохраняет историю разговоров
2. **Agentic Memory** - агент сам решает что важно запомнить  
3. **User Memories** - факты о пользователе (предпочтения, контекст)
4. **Session Summaries** - краткое резюме длинных разговоров

### 📝 Структура конфигурации

#### 🔧 Основные типы памяти
```json
{
  // 🏪 Тип хранилища (только PostgreSQL)
  "memory_type": "postgres",          // ✅ "postgres" или "postgresql" 
  
  // 🤖 Автономная память (агент управляет сам)
  "enable_agentic_memory": true,      // ✅ Агент решает что запомнить
  "enable_user_memories": true,       // ✅ Сохранять факты о пользователе
  "add_memory_references": true,      // ✅ Добавлять ссылки на память в ответы
  
  // 📊 Метаданные для контекста
  "user_data": {                      // ✅ Данные о пользователе
    "name": "John Doe",
    "role": "developer", 
    "preferences": ["python", "ai"],
    "timezone": "UTC-5"
  },
  "agent_data": {                     // ✅ Данные об агенте
    "version": "1.0",
    "specialization": "coding_assistant",
    "memory_retention_policy": "important_only"
  }
}
```

#### 📚 Дополнительные функции памяти
```json
{
  // 📝 Резюме сессий (для длинных разговоров)
  "enable_session_summaries": true,   // ✅ Создавать сводки сессий
  "add_session_summary_references": true, // ✅ Ссылаться на резюме в ответах
  
  // 🔍 Фильтрация воспоминаний
  "memory_filters": {                 // ✅ Как фильтровать память
    "importance_level": "high",       // Только важные воспоминания
    "category": ["technical", "personal"], // Категории для запоминания
    "max_age_days": 30,               // Забывать воспоминания старше 30 дней
    "user_id": "user_123"             // Память только для конкретного пользователя
  }
}
```

#### 🗄️ PostgreSQL настройки
```json
{
  // 🔗 Подключение к БД
  "db_url": "postgresql://username:password@hostname:5432/database_name",
  
  // 📋 Схема и таблицы
  "table_name": "agent_memory",       // ✅ Название таблицы памяти (дефолт: agent_memory)
  "db_schema": "ai",                  // ✅ Схема БД (дефолт: ai)
  "auto_upgrade_schema": false,       // ✅ Автоматически создавать/обновлять таблицы
  
  // 🗄️ Deprecated параметр (но всё ещё работает)
  "num_history_responses": 10         // ✅ Количество последних ответов (устаревший параметр)
}
```

### 🔍 Детальное объяснение режимов памяти

#### 1. 🤖 Agentic Memory (enable_agentic_memory: true)
**Что это:** Агент сам анализирует разговор и решает что важно запомнить.

**Как работает:**
- Агент читает весь разговор
- Выделяет ключевые факты, предпочтения, важные моменты
- Сохраняет структурированные воспоминания  
- Использует их в будущих разговорах

**Пример воспоминания:**
```json
{
  "content": "Пользователь предпочитает писать код на Python и интересуется AI",
  "category": "preferences",
  "importance": "high",
  "timestamp": "2024-12-19T10:30:00Z"
}
```

#### 2. 👤 User Memories (enable_user_memories: true)  
**Что это:** Специальные воспоминания о пользователе - его профиль, предпочтения, контекст.

**Как работает:**
- Агент накапливает данные о пользователе
- Создает персональный профиль
- Адаптирует стиль общения под пользователя
- Помнит долгосрочный контекст работы

**Пример User Memory:**
```json
{
  "user_id": "john_doe",
  "facts": [
    "Работает Python разработчиком в стартапе",
    "Использует VS Code с расширениями для AI",
    "Предпочитает краткие ответы с примерами кода"
  ]
}
```

#### 3. 📝 Session Summaries (enable_session_summaries: true)
**Что это:** Краткие сводки длинных разговоров для экономии токенов.

**Как работает:**
- В конце сессии агент создает резюме
- Резюме содержит ключевые решения и выводы
- В следующих сессиях используется резюме вместо полной истории
- Экономит токены и ускоряет работу

### 🔧 Примеры конфигураций для разных случаев

#### Простой агент (только история)
```json
{
  "memory_type": "postgres",
  "db_url": "postgresql://localhost:5432/agno_db",
  "enable_agentic_memory": false,
  "enable_user_memories": false
}
```

#### Персональный ассистент (полная память)
```json
{
  "memory_type": "postgres", 
  "db_url": "postgresql://localhost:5432/agno_db",
  "enable_agentic_memory": true,
  "enable_user_memories": true,
  "enable_session_summaries": true,
  "add_memory_references": true,
  "user_data": {
    "name": "John",
    "timezone": "UTC-5",
    "communication_style": "concise"
  },
  "memory_filters": {
    "importance_level": "medium",
    "max_age_days": 90
  }
}
```

#### Корпоративный агент (с фильтрацией)
```json
{
  "memory_type": "postgres",
  "db_url": "postgresql://corporate.db:5432/agents",
  "table_name": "corporate_agent_memory",
  "db_schema": "company_ai",
  "enable_agentic_memory": true,
  "memory_filters": {
    "category": ["work", "projects", "technical"],
    "importance_level": "high",
    "exclude_personal": true
  }
}
```

### ⚠️ Важные ограничения и требования

1. **Только PostgreSQL**: Другие БД не поддерживаются agno
2. **Supabase совместимость**: Полностью работает с Supabase
3. **Требуются права**: БД пользователь должен иметь права CREATE TABLE
4. **Производительность**: Рекомендуется индексация для больших объемов
5. **Безопасность**: Никогда не храните API ключи в memory_filters или user_data

---

## 4. KnowledgeConfig - Конфигурация базы знаний ✅

### 🎯 Описание
**KnowledgeConfig** превращает агента в эксперта по вашим данным через RAG (Retrieval-Augmented Generation). Агент может искать релевантную информацию из документов, файлов и баз знаний.

### 📚 Как работает RAG в agno
1. **Документы** разбиваются на чанки (фрагменты)
2. **Эмбеддинги** создаются для каждого чанка
3. **Векторная БД** хранит эмбеддинги для быстрого поиска
4. **Агент** ищет релевантные чанки по запросу пользователя
5. **Контекст** добавляется в промпт для генерации ответа

### 📝 Структура конфигурации

#### 🔍 Основные RAG параметры
```json
{
  // 🎯 Включение RAG функциональности
  "add_references": true,             // ✅ Включить RAG (поиск по документам)
  "search_knowledge": true,           // ✅ Разрешить поиск по базе знаний
  "update_knowledge": false,          // ✅ Разрешить агенту обновлять знания
  
  // 📋 Формат возвращаемых ссылок
  "references_format": "json",        // ✅ "json" | "markdown" | "text" | "xml"
  
  // 📊 Контроль качества поиска
  "max_references": 10,               // ✅ Максимум ссылок на запрос (1-50)
  "similarity_threshold": 0.7,        // ✅ Минимальная схожесть (0.0-1.0)
  
  // 🏷️ ID конкретной базы знаний
  "knowledge_base": "technical_docs_v1" // ✅ Идентификатор коллекции
}
```

#### 🔧 Продвинутые функции
```json
{
  // 🤖 Умная фильтрация (агент выбирает сам)
  "enable_agentic_knowledge_filters": true, // ✅ Агент сам выбирает фильтры
  
  // 🏷️ Ручная фильтрация
  "knowledge_filters": {              // ✅ Фильтры для поиска
    "category": ["technical", "legal"], // Категории документов
    "document_type": "pdf",           // Тип файлов
    "author": "john.doe",             // Автор документа
    "date_range": "2024-01-01:2024-12-31", // Диапазон дат
    "tags": ["important", "verified"], // Теги документов
    "language": "en"                  // Язык документов
  },
  
  // 🔧 Кастомная функция поиска
  "retriever": {                      // ✅ Альтернативная функция поиска
    "type": "custom_retriever",
    "config": {"model": "custom_embedder"}
  }
}
```

#### 🗄️ Векторная база данных
```json
{
  // 🔗 Подключение к векторной БД
  "vector_db_url": "postgresql://localhost:5432/vector_db", // ✅ URL pgvector БД
  
  // 🧠 Модель эмбеддингов  
  "embedding_model": "text-embedding-3-small", // ✅ OpenAI/Azure/HuggingFace модель
  
  // 📄 Параметры разбивки документов
  "chunk_size": 1000,                 // ✅ Размер чанка в символах (100-8000)
  "chunk_overlap": 200,               // ✅ Перекрытие между чанками (0-500)
  
  // 🛠️ Дополнительные инструменты знаний (из Agent)
  "read_chat_history": false,         // ✅ Инструмент чтения истории чата
  "read_tool_call_history": false     // ✅ Инструмент истории вызовов инструментов
}
```

### 📋 Детальное объяснение форматов ссылок

#### 1. 📄 JSON формат (references_format: "json")
**Лучше для программной обработки**
```json
{
  "references": [
    {
      "id": "doc_123_chunk_5",
      "content": "Ключевая информация из документа...",
      "source": "technical_manual.pdf", 
      "page": 15,
      "similarity_score": 0.87,
      "metadata": {
        "author": "John Doe",
        "date": "2024-01-15",
        "category": "technical"
      }
    }
  ]
}
```

#### 2. 📝 Markdown формат (references_format: "markdown") 
**Лучше для читаемости**
```markdown
## 📚 Источники

### 1. Technical Manual (стр. 15) - 87% совпадения
> Ключевая информация из документа...
*Автор: John Doe | Дата: 2024-01-15*

### 2. User Guide (стр. 8) - 82% совпадения  
> Дополнительная релевантная информация...
*Категория: documentation*
```

#### 3. 📄 Text формат (references_format: "text")
**Простой текстовый формат**
```
ИСТОЧНИКИ:
[1] technical_manual.pdf (стр. 15): Ключевая информация из документа...
[2] user_guide.pdf (стр. 8): Дополнительная релевантная информация...
```

#### 4. 🏷️ XML формат (references_format: "xml")
**Структурированный XML**
```xml
<references>
  <reference id="doc_123_chunk_5" similarity="0.87">
    <source>technical_manual.pdf</source>
    <page>15</page>
    <content>Ключевая информация из документа...</content>
  </reference>
</references>
```

### 🎯 Примеры конфигураций для разных случаев

#### Простой документ-помощник
```json
{
  "add_references": true,
  "search_knowledge": true,
  "references_format": "markdown",
  "max_references": 5,
  "similarity_threshold": 0.6,
  "knowledge_base": "company_docs"
}
```

#### Продвинутый RAG с фильтрацией
```json
{
  "add_references": true,
  "search_knowledge": true,
  "update_knowledge": false,
  "references_format": "json",
  "max_references": 15,
  "similarity_threshold": 0.75,
  "enable_agentic_knowledge_filters": true,
  "knowledge_filters": {
    "category": ["technical", "legal", "compliance"],
    "verified": true,
    "language": "en"
  },
  "vector_db_url": "postgresql://prod.db:5432/vector_store",
  "embedding_model": "text-embedding-3-large",
  "chunk_size": 800,
  "chunk_overlap": 150
}
```

#### Эксперт с обновлением знаний
```json
{
  "add_references": true,
  "search_knowledge": true,
  "update_knowledge": true,           // ⚠️ Агент может изменять документы!
  "references_format": "markdown",
  "max_references": 20,
  "similarity_threshold": 0.5,
  "enable_agentic_knowledge_filters": true,
  "knowledge_base": "evolving_knowledge",
  "read_chat_history": true,          // Используется контекст истории
  "read_tool_call_history": true      // Учитывается история инструментов
}
```

### ⚙️ Поддерживаемые векторные БД и эмбеддинги

#### Векторные базы данных:
- **PostgreSQL + pgvector** (рекомендуется)
- **Supabase** (полная поддержка)  
- **Chroma** (через агно)
- **Pinecone** (через агно)
- **Weaviate** (через агно)

#### Модели эмбеддингов:
- **OpenAI**: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
- **Azure OpenAI**: Те же модели через Azure
- **HuggingFace**: `sentence-transformers/all-MiniLM-L6-v2`, etc.
- **Cohere**: `embed-english-v3.0`, `embed-multilingual-v3.0`

### ⚠️ Важные особенности и ограничения

1. **Производительность**: Больше чанков = медленнее поиск
2. **Токены**: References увеличивают расход токенов
3. **Качество**: similarity_threshold влияет на точность  
4. **Безопасность**: update_knowledge требует осторожности
5. **Память**: Эмбеддинги занимают много места в БД

---

## 5. StorageConfig - Конфигурация хранилища ✅

### 🎯 Описание
**StorageConfig** отвечает за постоянное хранение состояния агента - сессии, контекста, пользовательских данных. Позволяет агенту "помнить" где он остановился между перезапусками.

### 💾 Как работает хранилище
1. **Сессии** - каждый разговор имеет уникальный ID
2. **Состояние** - промежуточные данные работы агента  
3. **События** - лог всех действий агента (опционально)
4. **Персистентность** - данные сохраняются между перезапусками

### 📝 Структура конфигурации

#### 🏪 Основные параметры хранилища
```json
{
  // 🗄️ Тип хранилища (только PostgreSQL)
  "storage_type": "postgres",         // ✅ "postgres" или "postgresql"
  
  // 🔗 Подключение к БД
  "db_url": "postgresql://username:password@host:5432/db", // ✅ URL БД
  
  // ⚡ Включение/выключение
  "enabled": true,                    // ✅ Активировать хранилище
  
  // 📋 Сессия
  "session_name": "chat_session_001", // ✅ Человекочитаемое имя сессии
  "session_state": {                  // ✅ Произвольное состояние сессии
    "current_step": 3,
    "user_context": "technical_support",
    "last_action": "file_analysis",
    "workflow_stage": "investigation"
  },
  
  // 📦 Дополнительные данные
  "extra_data": {                     // ✅ Любая дополнительная информация
    "user_preferences": {"theme": "dark"},
    "session_metadata": {"start_time": "2024-12-19T10:00:00Z"},
    "custom_fields": {"department": "engineering"}
  }
}
```

#### 📊 Управление событиями
```json
{
  // 📝 Логирование событий
  "store_events": true,               // ✅ Сохранять события выполнения
  
  // 🚫 Фильтрация событий (какие НЕ сохранять)
  "events_to_skip": [                 // ✅ Пропускать указанные типы событий
    "tool_call_started",              // Не логировать начало вызова инструментов
    "debug_info",                     // Не сохранять отладочную информацию
    "intermediate_step"               // Пропускать промежуточные шаги
  ]
}
```

### 🔧 Примеры конфигураций для разных случаев

#### Простое хранилище (только сессии)
```json
{
  "storage_type": "postgres",
  "db_url": "postgresql://localhost:5432/agno_storage",
  "enabled": true,
  "session_name": "simple_chat"
}
```

#### Продвинутое хранилище с событиями
```json
{
  "storage_type": "postgres",
  "db_url": "postgresql://prod.db:5432/agent_storage",
  "enabled": true,
  "session_name": "advanced_session_001",
  "session_state": {
    "workflow_id": "customer_support_flow",
    "current_phase": "information_gathering",
    "collected_data": {
      "customer_id": "CUST_12345",
      "issue_category": "technical",
      "priority": "high"
    }
  },
  "store_events": true,
  "events_to_skip": ["debug_info", "heartbeat"],
  "extra_data": {
    "department": "customer_support",
    "agent_version": "2.1",
    "compliance_tracking": true
  }
}
```

#### Отключенное хранилище (для тестирования)
```json
{
  "enabled": false                    // ✅ Полностью отключить хранилище
}
```

### ⚠️ Важные особенности и ограничения

1. **Только PostgreSQL**: Другие БД не поддерживаются
2. **Требуются права**: CREATE TABLE для создания схемы
3. **Безопасность**: Не храните пароли в session_state или extra_data
4. **Производительность**: store_events может замедлить работу
5. **Размер данных**: session_state ограничен размером JSONB поля

---

## 6. ReasoningConfig - Конфигурация reasoning ✅

### 🎯 Описание
**ReasoningConfig** превращает агента в методичного аналитика, который решает сложные задачи пошагово. Особенно эффективен для логических задач, анализа и планирования.

### 🧠 Как работает reasoning в agno
1. **Анализ задачи** - агент разбивает проблему на шаги
2. **Пошаговое решение** - каждый шаг документируется и обосновывается
3. **Проверка результата** - сравнение с критериями успеха
4. **Итерация** - повторение шагов при необходимости

### 📝 Структура конфигурации

#### 🔧 Основные параметры reasoning
```json
{
  // ⚡ Включение reasoning режима
  "reasoning": true,                  // ✅ Активировать пошаговое рассуждение
  
  // 🤖 Модель для reasoning (может отличаться от основной)
  "reasoning_model": {                // ✅ Отдельная модель для рассуждений
    "id": "gpt-4o",                  // Лучше использовать самые умные модели
    "temperature": 0.1,              // Низкая температура для точности
    "max_tokens": 2000               // Достаточно токенов для рассуждений
  },
  
  // 📊 Контроль количества шагов
  "reasoning_min_steps": 2,           // ✅ Минимум шагов (1-20)
  "reasoning_max_steps": 15,          // ✅ Максимум шагов (1-50)
  
  // 🎯 Определение задачи
  "goal": "Проанализировать проблему и предложить решение", // ✅ Цель рассуждения
  "success_criteria": "Четкий план действий с обоснованием", // ✅ Критерии успеха
  "expected_output": "Структурированный анализ с выводами"   // ✅ Ожидаемый результат
}
```

#### 🎛️ Продвинутые параметры
```json
{
  // 🤖 Отдельный агент для reasoning (если нужен специализированный агент)
  "reasoning_agent": {                // ✅ Конфигурация агента-аналитика
    "model": {"id": "o1-preview"},    // Модель специально для сложного анализа
    "instructions": ["Будь максимально логичен", "Проверяй каждый вывод"]
  },
  
  // 💬 Кастомизация промптов
  "reasoning_prompt": "Пошагово проанализируй проблему:", // ✅ Стартовый промпт
  "reasoning_instructions": [          // ✅ Специальные инструкции
    "Каждый шаг должен быть обоснован",
    "Учитывай все возможные варианты", 
    "Проверяй логическую цепочку",
    "Делай промежуточные выводы"
  ],
  
  // 📡 Потоковая передача
  "stream_reasoning": true,           // ✅ Показывать шаги в реальном времени
  "save_reasoning_steps": true        // ✅ Сохранять шаги для анализа
}
```

### 🔍 Типы reasoning задач

#### 1. 🧮 Логические задачи
```json
{
  "reasoning": true,
  "goal": "Решить логическую задачу пошагово",
  "success_criteria": "Правильный ответ с полным обоснованием",
  "reasoning_instructions": [
    "Определи все условия задачи",
    "Выяви логические связи",
    "Проверь каждое умозаключение"
  ]
}
```

#### 2. 📊 Анализ данных
```json
{
  "reasoning": true,
  "goal": "Провести анализ данных и выявить закономерности",
  "success_criteria": "Обоснованные выводы с данными",
  "reasoning_model": {
    "id": "gpt-4o", 
    "temperature": 0.0              // Максимальная точность для анализа
  },
  "reasoning_instructions": [
    "Изучи структуру данных",
    "Найди статистические паттерны",
    "Сделай выводы на основе данных"
  ]
}
```

#### 3. 🎯 Планирование проектов
```json
{
  "reasoning": true,
  "goal": "Создать детальный план проекта",
  "success_criteria": "Реалистичный план с временными рамками",
  "reasoning_max_steps": 20,          // Больше шагов для сложного планирования
  "reasoning_instructions": [
    "Определи цели и требования",
    "Разбей на подзадачи",
    "Оцени ресурсы и время",
    "Учти возможные риски"
  ]
}
```

#### 4. 🐛 Отладка кода
```json
{
  "reasoning": true,
  "goal": "Найти и исправить ошибки в коде",
  "success_criteria": "Рабочий код с объяснением исправлений",
  "reasoning_instructions": [
    "Проследи выполнение кода пошагово",
    "Найди места потенциальных ошибок",
    "Проверь логику каждой функции",
    "Предложи исправления с обоснованием"
  ]
}
```

### 🎨 Форматы вывода reasoning

#### С stream_reasoning: true (реальное время)
```
🤖 ШАГ 1: Анализ проблемы
Изучаю условия задачи...
✅ Выявлено 3 ключевых условия

🤖 ШАГ 2: Поиск решения  
Рассматриваю возможные подходы...
⚠️ Подход А имеет ограничения
✅ Подход Б выглядит перспективно

🤖 ШАГ 3: Проверка решения
Тестирую предложенное решение...
✅ Решение соответствует всем критериям
```

#### С save_reasoning_steps: true (для анализа)
```json
{
  "reasoning_steps": [
    {
      "step": 1,
      "title": "Анализ проблемы",
      "content": "Изучение условий задачи показало...",
      "conclusion": "Выявлено 3 ключевых условия",
      "timestamp": "2024-12-19T10:15:30Z"
    },
    {
      "step": 2, 
      "title": "Поиск решения",
      "content": "Рассмотрены подходы А и Б...",
      "conclusion": "Подход Б наиболее эффективен",
      "timestamp": "2024-12-19T10:16:45Z"
    }
  ]
}
```

### ⚡ Оптимизация производительности

#### Быстрый reasoning (простые задачи)
```json
{
  "reasoning": true,
  "reasoning_min_steps": 1,
  "reasoning_max_steps": 5,
  "reasoning_model": {"id": "gpt-4o-mini", "temperature": 0.2},
  "stream_reasoning": false
}
```

#### Глубокий reasoning (сложные задачи)
```json
{
  "reasoning": true,
  "reasoning_min_steps": 5,
  "reasoning_max_steps": 25,
  "reasoning_model": {"id": "o1-preview", "temperature": 0.0},
  "stream_reasoning": true,
  "save_reasoning_steps": true
}
```

### ⚠️ Важные особенности и ограничения

1. **Расход токенов**: Reasoning увеличивает расход токенов в 2-5 раз
2. **Время выполнения**: Пошаговый анализ требует больше времени
3. **Качество модели**: Лучше использовать топовые модели (GPT-4o, o1)
4. **Количество шагов**: Много шагов не всегда означает лучший результат
5. **Streaming**: Может быть полезен для долгих рассуждений

---

## 7. TeamConfig - Конфигурация команды ✅

### 🎯 Описание
**TeamConfig** превращает одного агента в часть команды агентов. Позволяет создавать сложные мультиагентные системы с распределением ролей и задач.

### 👥 Режимы работы команды
1. **Route** - агенты передают задачи друг другу по очереди
2. **Coordinate** - один агент координирует работу остальных
3. **Collaborate** - агенты работают параллельно и обмениваются информацией

### 📝 Структура конфигурации

#### 🏢 Основные параметры команды
```json
{
  // 🎭 Режим работы команды
  "team_mode": "coordinate",          // ✅ "route" | "coordinate" | "collaborate"
  
  // 👤 Роль агента в команде
  "role": "lead_analyst",             // ✅ Специализация агента в команде
  
  // 💬 Поведение при ответах
  "respond_directly": false,          // ✅ Отвечать пользователю напрямую или через координатора
  "add_transfer_instructions": true,  // ✅ Добавлять инструкции по передаче задач
  "team_response_separator": "\\n---\\n", // ✅ Разделитель между ответами участников
  
  // 🔗 Связи с другими командами и процессами
  "workflow_id": "customer_support_flow", // ✅ ID рабочего процесса
  "parent_team_id": "support_department"  // ✅ ID родительской команды
}
```

#### 🆔 Идентификация команды
```json
{
  // 🏷️ Уникальные идентификаторы
  "team_id": "team_customer_support_001", // ✅ UUID команды
  "team_session_id": "session_456",       // ✅ ID текущей сессии команды
  
  // 📊 Состояние команды
  "team_session_state": {                 // ✅ Общее состояние команды
    "current_phase": "information_gathering",
    "active_members": ["agent_1", "agent_3"],
    "completed_tasks": ["initial_analysis"],
    "pending_decisions": ["escalation_required"]
  }
}
```

#### 👥 Участники команды
```json
{
  // 📋 Список участников команды
  "members": [                            // ✅ Конфигурация участников
    {
      "agent_id": "researcher_agent",
      "role": "information_researcher", 
      "capabilities": ["web_search", "data_analysis"],
      "priority": 1
    },
    {
      "agent_id": "writer_agent",
      "role": "content_writer",
      "capabilities": ["text_generation", "editing"],
      "priority": 2
    },
    {
      "agent_id": "reviewer_agent", 
      "role": "quality_reviewer",
      "capabilities": ["proofreading", "fact_checking"],
      "priority": 3
    }
  ]
}
```

#### ⚙️ Управление взаимодействием
```json
{
  // 🛠️ Инструменты и доступность
  "add_member_tools_to_system_message": true, // ✅ Показывать инструменты участников
  "show_members_responses": false,            // ✅ Показывать ответы других участников
  "stream_member_events": true,               // ✅ Стриминг событий команды
  "share_member_interactions": false,         // ✅ Делиться логами между участниками
  "get_member_information_tool": true         // ✅ Инструмент получения инфо об участниках
}
```

### 🔄 Примеры режимов работы

#### 1. 🎯 Route Mode (последовательная передача)
```json
{
  "team_mode": "route",
  "role": "step_1_analyzer",
  "respond_directly": false,
  "members": [
    {"agent_id": "analyzer", "role": "analyze_request"},
    {"agent_id": "processor", "role": "process_data"}, 
    {"agent_id": "responder", "role": "format_response"}
  ]
}
```

**Поток выполнения:**
```
Пользователь → Analyzer → Processor → Responder → Пользователь
```

#### 2. 🎭 Coordinate Mode (один координатор)
```json
{
  "team_mode": "coordinate",
  "role": "coordinator",
  "respond_directly": true,
  "members": [
    {"agent_id": "researcher", "role": "research_specialist"},
    {"agent_id": "analyst", "role": "data_analyst"},
    {"agent_id": "writer", "role": "content_creator"}
  ]
}
```

**Поток выполнения:**
```
Пользователь → Coordinator
                    ↓
              ┌─ Researcher ─┐
              ├─ Analyst   ─┤ → Coordinator → Пользователь
              └─ Writer    ─┘
```

#### 3. 🤝 Collaborate Mode (параллельная работа)
```json
{
  "team_mode": "collaborate",
  "role": "collaborative_member",
  "respond_directly": true,
  "share_member_interactions": true,
  "show_members_responses": true
}
```

**Поток выполнения:**
```
Пользователь → Все агенты работают параллельно ← → обмениваются данными → Объединенный ответ
```

### 🎯 Специализированные команды

#### Команда разработки
```json
{
  "team_mode": "coordinate",
  "role": "senior_developer",
  "workflow_id": "software_development",
  "members": [
    {"agent_id": "architect", "role": "system_architect"},
    {"agent_id": "backend_dev", "role": "backend_developer"},
    {"agent_id": "frontend_dev", "role": "frontend_developer"},
    {"agent_id": "tester", "role": "qa_engineer"}
  ],
  "team_session_state": {
    "project_phase": "implementation",
    "code_reviews_required": true
  }
}
```

#### Команда поддержки клиентов
```json
{
  "team_mode": "route",
  "role": "l1_support",
  "workflow_id": "customer_support_escalation",
  "members": [
    {"agent_id": "l1_agent", "role": "basic_support"},
    {"agent_id": "l2_agent", "role": "technical_support"},
    {"agent_id": "l3_agent", "role": "expert_support"}
  ],
  "add_transfer_instructions": true,
  "team_response_separator": "\\n--- Передача на следующий уровень ---\\n"
}
```

#### Исследовательская команда
```json
{
  "team_mode": "collaborate", 
  "role": "research_coordinator",
  "members": [
    {"agent_id": "literature_reviewer", "role": "academic_researcher"},
    {"agent_id": "data_scientist", "role": "quantitative_analyst"},
    {"agent_id": "market_researcher", "role": "market_analyst"}
  ],
  "share_member_interactions": true,
  "show_members_responses": true,
  "stream_member_events": true
}
```

### 🔧 Управление состоянием команды

#### Динамическое управление участниками
```json
{
  "team_session_state": {
    "active_members": ["agent_1", "agent_3"],    // Кто сейчас работает
    "paused_members": ["agent_2"],               // Кто временно приостановлен
    "escalation_chain": ["l1", "l2", "l3"],      // Цепочка эскалации
    "current_task": "customer_issue_analysis",   // Текущая задача
    "priority": "high",                          // Приоритет задачи
    "deadline": "2024-12-19T18:00:00Z"          // Дедлайн
  }
}
```

### ⚠️ Важные особенности и ограничения

1. **Сложность координации**: Много участников = сложнее управление
2. **Расход токенов**: Мультиагентные системы расходуют больше токенов
3. **Время выполнения**: Координация требует дополнительного времени
4. **Совместимость ролей**: Роли участников должны дополнять друг друга
5. **Обработка ошибок**: Нужны механизмы восстановления при сбоях участников

---

## 8. AgentSettings - Дополнительные настройки ✅

### 🎯 Описание
**AgentSettings** - это "центр управления" поведением агента. Здесь собраны все параметры, которые влияют на то, КАК агент общается, ЧТО помнит и КАК обрабатывает запросы.

### 🧩 Категории настроек
1. **Системные сообщения** - как агент представляется
2. **Пользовательские сообщения** - как обрабатываются запросы
3. **Контекст и состояние** - дополнительная информация
4. **История** - что помнить из прошлых разговоров  
5. **Форматирование** - как оформлять ответы
6. **Отладка и мониторинг** - логирование и диагностика

### 📝 Структура конфигурации

#### 🆔 Основная идентификация
```json
{
  // 👋 Представление агента
  "introduction": "Привет! Я ваш AI-ассистент по разработке", // ✅ Приветствие в начале чата
  
  // 🏷️ Идентификаторы
  "user_id": "user_john_doe_123",      // ✅ ID пользователя для персонализации
  "session_id": "session_456789",     // ✅ UUID текущей сессии
  "session_name": "Code Review Session", // ✅ Человекочитаемое имя сессии
  
  // 📊 Состояние и данные
  "session_state": {                  // ✅ Состояние сессии (любые данные)
    "current_project": "web_app_v2",
    "review_stage": "backend_apis",
    "files_reviewed": 5
  },
  "extra_data": {                     // ✅ Дополнительные данные агента
    "user_preferences": {"language": "ru", "code_style": "python_pep8"},
    "access_level": "senior_developer",
    "department": "engineering"
  }
}
```

#### 💬 Системные сообщения
```json
{
  // 🤖 Основное системное сообщение
  "system_message": "Ты опытный разработчик Python...", // ✅ Главные инструкции для агента
  "system_message_role": "system",    // ✅ Роль в чате ("system" | "user" | "assistant")
  "create_default_system_message": true, // ✅ Создавать автоматическое системное сообщение
  
  // 📜 Дополнительные инструкции
  "system_prompt": "Будь полезным и точным", // ✅ Краткий системный промпт
  "instructions": [                   // ✅ Список детальных инструкций
    "Всегда показывай примеры кода",
    "Объясняй сложные концепции простыми словами",
    "Предлагай лучшие практики",
    "Проверяй код на потенциальные ошибки"
  ]
}
```

#### 👤 Пользовательские сообщения
```json
{
  // 📝 Обработка входящих сообщений
  "user_message": null,               // ✅ Конкретное сообщение пользователя (обычно null)
  "user_message_role": "user",        // ✅ Роль пользователя в чате
  "create_default_user_message": true, // ✅ Создавать сообщение пользователя автоматически
  
  // 📋 Дополнительные сообщения
  "add_messages": [                   // ✅ Предварительные сообщения в контекст
    {
      "role": "assistant",
      "content": "Понял, начинаю анализ кода..."
    },
    {
      "role": "user", 
      "content": "Покажи мне структуру проекта"
    }
  ]
}
```

#### 🌍 Контекст и состояние
```json
{
  // 📦 Контекст для инструментов
  "context": {                        // ✅ Данные, доступные всем инструментам
    "environment": "production",
    "database_connection": "postgres://...",
    "api_endpoints": ["auth", "users", "payments"],
    "current_user_role": "admin"
  },
  
  // ⚙️ Управление контекстом
  "add_context": false,               // ✅ Добавлять контекст в системное сообщение
  "resolve_context": true,            // ✅ Выполнять функции в контексте
  "additional_context": "Проект находится в стадии бета-тестирования", // ✅ Доп. информация
  "add_state_in_messages": false      // ✅ Включать состояние в сообщения
}
```

#### 📚 История и память
```json
{
  // 📖 Управление историей
  "add_history_to_messages": true,    // ✅ Включать историю в контекст
  "num_history_runs": 5,              // ✅ Количество предыдущих запусков (1-20)
  "search_previous_sessions_history": true, // ✅ Искать в предыдущих сессиях
  "num_history_sessions": 3,          // ✅ Количество сессий для поиска (1-10)
  
  // 🛠️ Инструменты истории (добавляются автоматически)
  "read_chat_history": true,          // ✅ Инструмент чтения истории чата
  "read_tool_call_history": true      // ✅ Инструмент истории вызовов инструментов
}
```

#### 🎨 Форматирование ответов
```json
{
  // ✨ Стиль ответов
  "markdown": true,                   // ✅ Форматировать ответы в Markdown
  "add_name_to_instructions": true,   // ✅ Добавить имя агента к инструкциям
  "add_datetime_to_instructions": true, // ✅ Добавить текущие дату/время
  "add_location_to_instructions": false, // ✅ Добавить информацию о локации
  "timezone_identifier": "Europe/Moscow", // ✅ Временная зона (TZ Database)
  
  // 💾 Сохранение ответов
  "save_response_to_file": "/tmp/agent_responses.txt" // ✅ Путь для сохранения (опционально)
}
```

#### 📡 Потоковая передача
```json
{
  // 🌊 Стриминг
  "stream": true,                     // ✅ Потоковая передача ответа
  "stream_intermediate_steps": true   // ✅ Стримить промежуточные шаги выполнения
}
```

#### 🐛 Отладка и мониторинг
```json
{
  // 🔍 Отладка
  "debug_mode": false,                // ✅ Режим отладки (подробные логи)
  "monitoring": true,                 // ✅ Отправка метрик в agno.com
  "telemetry": true,                  // ✅ Минимальное логирование использования
  
  // 🔄 Обработка ошибок
  "retries": 3,                       // ✅ Количество повторов при ошибке (0-10)
  "delay_between_retries": 2,         // ✅ Задержка между повторами (секунды)
  "exponential_backoff": true,        // ✅ Увеличивать задержку экспоненциально
  
  // 📊 События
  "store_events": true,               // ✅ Сохранять события выполнения
  "events_to_skip": [                 // ✅ Какие события НЕ сохранять
    "debug_log",
    "heartbeat", 
    "intermediate_thinking"
  ]
}
```

#### 🎯 Парсинг и структурированные ответы
```json
{
  // 📋 Модели ответов
  "response_model": {                 // ✅ Pydantic модель для структурированного ответа
    "type": "CodeReviewResult",
    "schema": {
      "issues": "List[str]",
      "suggestions": "List[str]", 
      "rating": "int"
    }
  },
  "parse_response": true,             // ✅ Автоматически парсить ответ в модель
  "use_json_mode": false,             // ✅ Принудительный JSON формат ответа
  
  // 🔧 Парсинг с отдельной моделью
  "parser_model": {                   // ✅ Отдельная модель для парсинга
    "id": "gpt-4o-mini",
    "temperature": 0.0
  },
  "parser_model_prompt": "Извлеки структурированные данные из ответа" // ✅ Промпт для парсера
}
```

#### 👥 Командная работа
```json
{
  // 🏢 Команда
  "team_data": {                      // ✅ Общие данные команды
    "team_name": "Development Team Alpha",
    "shared_resources": ["database", "api_keys"],
    "current_sprint": "sprint_15"
  },
  "team_session_id": "team_session_789", // ✅ ID сессии команды
  
  // 🏷️ Метаинформация
  "config_version": "2.1",            // ✅ Версия конфигурации
  "tags": ["python", "backend", "code-review"], // ✅ Теги для поиска
  "app_id": "code_review_assistant"    // ✅ ID приложения
}
```

### 🔧 Примеры конфигураций для разных случаев

#### Простой чат-бот
```json
{
  "introduction": "Привет! Чем могу помочь?",
  "markdown": true,
  "stream": true,
  "debug_mode": false
}
```

#### Персональный ассистент
```json
{
  "introduction": "Добро пожаловать! Я ваш персональный ассистент.",
  "user_id": "john_doe",
  "add_history_to_messages": true,
  "num_history_runs": 10,
  "add_datetime_to_instructions": true,
  "timezone_identifier": "America/New_York",
  "extra_data": {
    "preferences": {"communication_style": "formal"},
    "access_level": "premium"
  }
}
```

#### Разработческий агент  
```json
{
  "system_message": "Ты опытный senior разработчик Python",
  "instructions": [
    "Всегда показывай примеры кода",
    "Следуй PEP 8",
    "Предлагай оптимизации",
    "Проверяй на безопасность"
  ],
  "context": {
    "environment": "development",
    "python_version": "3.11",
    "frameworks": ["fastapi", "sqlalchemy"]
  },
  "markdown": true,
  "read_chat_history": true,
  "stream_intermediate_steps": true,
  "tags": ["python", "development", "code-review"]
}
```

#### Корпоративный агент с мониторингом
```json
{
  "introduction": "Корпоративный AI-ассистент готов к работе",
  "monitoring": true,
  "telemetry": true,
  "store_events": true,
  "retries": 5,
  "exponential_backoff": true,
  "extra_data": {
    "company": "TechCorp Inc",
    "compliance_level": "enterprise",
    "audit_required": true
  },
  "save_response_to_file": "/var/log/corporate_agent.log"
}
```

### ⚠️ Важные особенности и ограничения

1. **Размер контекста**: Много истории = больше токенов
2. **Производительность**: store_events замедляет работу
3. **Безопасность**: Не храните пароли в context или extra_data
4. **Streaming**: Может не работать со всеми форматами ответов
5. **Парсинг**: response_model требует совместимой модели

---

## 9. DynamicTool - Динамические инструменты

### 9.1 Описание:
Динамические инструменты - это инструменты, которые могут быть добавлены или удалены в любое время. Они могут быть созданы пользователем или автоматически.

### 9.2 Пример конфигурации:
```json
{
  "tool_id": "search_web_001",
  "name": "Web Search Tool",
  "display_name": "🔍 Web Search",
  "agno_class": "DuckDuckGoTools",
  "module_path": "agno.tools.duckduckgo",
  "config": {
    "search_engine": "duckduckgo",
    "max_results": 10,
    "safe_search": "moderate",
    "region": "us-en",
    "time_range": "all"
  },
  "description": "Search the web using DuckDuckGo search engine",
  "category": "search",
  "icon": "🔍",
  "is_active": true
}
```

---

## 10. CustomTool - Кастомные инструменты

### 10.1 Описание:
Пользовательские Python инструменты с полным исходным кодом

### 10.2 Пример конфигурации:
```json
{
  "tool_id": "my_calculator",
  "name": "Advanced Calculator",
  "description": "Custom calculator with advanced mathematical functions",
  "source_code": "def calculate(expression: str) -> str:\n    \"\"\"Calculate mathematical expression\"\"\"\n    try:\n        result = eval(expression)\n        return f\"Result: {result}\"\n    except Exception as e:\n        return f\"Error: {str(e)}\"",
  "config": {
    "precision": 10,
    "allow_functions": ["sin", "cos", "tan", "log"]
  },
  "is_active": true
}
```

---

## 11. MCPServer - MCP серверы

### 11.1 Описание:
Model Context Protocol серверы для расширения функциональности

### 11.2 Пример конфигурации stdio transport:
```json
{
  "server_id": "filesystem_mcp",
  "name": "Filesystem MCP Server",
  "description": "File system operations via MCP protocol",
  "command": "npx -y @modelcontextprotocol/server-filesystem /tmp",
  "transport": "stdio",
  "env_config": {
    "NODE_ENV": "production",
    "DEBUG": "false"
  },
  "is_active": true
}
```

### 11.3 Пример конфигурации HTTP transport:
```json
{
  "server_id": "api_mcp_server",
  "name": "API MCP Server",
  "description": "HTTP-based MCP server",
  "url": "http://localhost:3000/mcp",
  "transport": "http",
  "env_config": {
    "API_KEY": "secret-key",
    "TIMEOUT": "30000"
  },
  "is_active": true
}
```

### 11.4 Поддерживаемые транспорты:
- **stdio** - Стандартный ввод/вывод
- **http** - HTTP соединение
- **sse** - Server-Sent Events

---

## 📊 Сводная таблица конфигураций

| Сущность | Статус | Количество параметров | Описание |
|----------|---------|----------------------|----------|
| **DynamicAgent** | ✅ Реализован | 150+ | Полная конфигурация агентов |
| **DynamicTool** | ✅ Реализован | 101 класс | Все Agno инструменты |
| **CustomTool** | ✅ Реализован | Unlimited | Python инструменты |
| **MCPServer** | ✅ Реализован | 3 транспорта | MCP протокол |
| **DynamicTeam** | ❌ Отсутствует | 50+ | Команды агентов |
| **DynamicWorkflow** | ❌ Отсутствует | 30+ | Рабочие процессы |
| **DynamicKnowledge** | ❌ Отсутствует | 40+ | Базы знаний |
| **DynamicMemory** | ❌ Отсутствует | 25+ | Системы памяти |
| **DynamicVectorDB** | ❌ Отсутствует | 8 провайдеров | Векторные БД |
| **DynamicModel** | ❌ Отсутствует | 15+ провайдеров | Конфигурации моделей |

---

## 🚀 Рекомендации по расширению

1. **Приоритет 1:** DynamicTeam - для создания команд агентов
2. **Приоритет 2:** DynamicWorkflow - для автоматизации процессов  
3. **Приоритет 3:** DynamicKnowledge - для управления знаниями
4. **Приоритет 4:** DynamicVectorDB - для гибкости векторного поиска
5. **Приоритет 5:** DynamicModel - для централизованного управления моделями

Каждая конфигурация следует принципам:
- ✅ Pydantic валидация
- ✅ JSONB хранение в PostgreSQL
- ✅ Кэширование для производительности
- ✅ Полная совместимость с Agno
- ✅ Динамическая загрузка без перезапуска 