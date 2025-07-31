# Полный анализ конфигураций агентов Agno Framework

## Введение

Данный документ содержит исчерпывающий анализ всех конфигурационных параметров класса `Agent` в фреймворке Agno, их взаимосвязей и принципов работы. Анализ основан на изучении исходного кода Agno версии, установленной в проекте (.venv/lib/python3.12/site-packages/agno).

## Архитектура агентов в нашем проекте

В нашем проекте используется гибридная архитектура агентов:

### 1. Статические агенты (Hardcoded)
- **AgnoAssist** (`agno_assist`) - помощник по фреймворку Agno
- **WebAgent** (`web_agent`) - веб-поисковый агент
- **FinanceAgent** (`finance_agent`) - финансовый аналитик

### 2. Динамические агенты (Database-driven)
- Хранятся в таблице `agents` PostgreSQL
- Конфигурируются через JSON поля `model_config` и `agent_config`
- Поддерживают мультитенантность и организационную структуру

## 🚀 ПРАКТИЧЕСКОЕ РУКОВОДСТВО: Создание динамических агентов

### Структура таблицы agents

```sql
-- Основная структура таблицы agents
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Конфигурации (ОСНОВНЫЕ ПОЛЯ)
    model_config JSONB NOT NULL DEFAULT '{"provider": "openai", "id": "gpt-4.1-mini-2025-04-14"}',
    system_instructions TEXT[] DEFAULT '{}',
    tool_ids UUID[] DEFAULT '{}',
    agent_config JSONB NOT NULL DEFAULT '{}',
    
    -- Нативные поля Agno (опциональные, приоритет над agent_config)
    goal TEXT,                    -- Цель агента (приоритет над agent_config.goal)
    expected_output TEXT,         -- Ожидаемый результат (приоритет над agent_config.expected_output)
    role VARCHAR(255),            -- Роль в команде (приоритет над agent_config.role)
    
    -- Мультитенантность
    is_public BOOLEAN DEFAULT false,
    company_id UUID,
    user_id VARCHAR(255),
    photo TEXT,
    category TEXT,
    
    -- Метаданные
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 1. Базовый агент-ассистент

```sql
INSERT INTO agents (
    agent_id, 
    name, 
    description, 
    system_instructions,
    model_config,
    agent_config,
    is_public
) VALUES (
    'basic_assistant',
    'Базовый ассистент',
    'Простой помощник для общих задач',
    ARRAY['Ты полезный ассистент', 'Отвечай кратко и по делу', 'Используй русский язык'],
    '{
        "provider": "openai",
        "id": "gpt-4.1-mini-2025-04-14",
        "temperature": 0.7,
        "max_tokens": 2000
    }',
    '{
        "storage": {
            "table_name": "sessions"
        },
        "history": {
            "add_history_to_messages": true,
            "num_history_runs": 3,
            "read_chat_history": true
        },
        "markdown": true,
        "add_datetime_to_instructions": true,
        "debug_mode": false
    }',
    true
);
```

### 2. Агент с памятью и знаниями (RAG)

```sql
INSERT INTO agents (
    agent_id,
    name,
    description,
    system_instructions,
    model_config,
    agent_config,
    goal,                    -- DB поле имеет приоритет над agent_config.goal
    expected_output,         -- DB поле имеет приоритет над agent_config.expected_output
    is_public
) VALUES (
    'smart_assistant',
    'Умный ассистент с памятью',
    'Ассистент с долговременной памятью и базой знаний',
    ARRAY[
        'Ты умный ассистент с доступом к базе знаний',
        'Используй свою память для персонализации ответов',
        'При поиске информации всегда ссылайся на источники'
    ],
    '{
        "provider": "openai",
        "id": "gpt-4.1-2025-04-14",
        "temperature": 0.3,
        "max_tokens": 4000
    }',
    '{
        "storage": {
            "table_name": "sessions"
        },
        "memory": {
            "enabled": true,
            "table_name": "user_memories",
            "delete_memories": true,
            "clear_memories": true
        },
        "knowledge": {
            "enabled": true,
            "type": "url",
            "urls": ["https://docs.agno.com"],
            "table_name": "knowledge"
        },
        "history": {
            "add_history_to_messages": true,
            "num_history_runs": 5,
            "read_chat_history": true
        },
        "enable_agentic_memory": true,
        "search_knowledge": true,
        "add_references": true,
        "references_format": "json",
        "markdown": true,
        "add_datetime_to_instructions": true,
        "add_state_in_messages": true
    }',
    'Предоставлять персонализированную помощь с использованием памяти и знаний',
    'Подробные ответы с ссылками на источники и учетом предыдущих взаимодействий',
    true
);
```

### 3. Агент-аналитик с рассуждениями

```sql
INSERT INTO agents (
    agent_id,
    name,
    description,
    system_instructions,
    model_config,
    agent_config,
    role,                    -- DB поле имеет приоритет над agent_config.role
    is_public
) VALUES (
    'analyst_agent',
    'Агент-аналитик',
    'Специализированный агент для сложного анализа данных',
    ARRAY[
        'Ты эксперт-аналитик данных',
        'Используй пошаговое рассуждение для сложных задач',
        'Всегда показывай логику своих выводов'
    ],
    '{
        "provider": "openai",
        "id": "gpt-4.1-2025-04-14",
        "temperature": 0.1,
        "max_tokens": 8000
    }',
    '{
        "storage": {
            "table_name": "sessions"
        },
        "reasoning": {
            "enabled": true,
            "model_id": "gpt-4.1-2025-04-14",
            "min_steps": 2,
            "max_steps": 10
        },
        "parser": {
            "enabled": true,
            "model_id": "gpt-4.1-mini-2025-04-14"
        },
        "history": {
            "add_history_to_messages": true,
            "num_history_runs": 10,
            "read_chat_history": true
        },
        "structured_outputs": true,
        "show_tool_calls": true,
        "tool_call_limit": 20,
        "markdown": true,
        "add_datetime_to_instructions": true
    }',
    'analyst',
    true
);
```

### 4. Агент с инструментами и командной работой

```sql
-- Сначала создаем инструменты (если нужны кастомные)
INSERT INTO tools (
    id,
    name,
    description,
    function_definition,
    is_active
) VALUES (
    gen_random_uuid(),
    'calculator',
    'Калькулятор для математических вычислений',
    '{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Выполняет математические вычисления",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Математическое выражение для вычисления"
                    }
                },
                "required": ["expression"]
            }
        }
    }',
    true
);

-- Создаем агента с инструментами
INSERT INTO agents (
    agent_id,
    name,
    description,
    system_instructions,
    model_config,
    tool_ids,
    agent_config,
    role,                    -- DB поле имеет приоритет над agent_config.role
    is_public
) VALUES (
    'math_assistant',
    'Математический помощник',
    'Специализированный агент для решения математических задач',
    ARRAY[
        'Ты эксперт по математике',
        'Используй калькулятор для точных вычислений',
        'Объясняй каждый шаг решения'
    ],
    '{
        "provider": "openai",
        "id": "gpt-4.1-2025-04-14",
        "temperature": 0.0
    }',
    ARRAY[(SELECT id FROM tools WHERE name = 'calculator')],
    '{
        "storage": {
            "table_name": "sessions"
        },
        "history": {
            "add_history_to_messages": true,
            "num_history_runs": 5
        },
        "show_tool_calls": true,
        "tool_call_limit": 10,
        "team": {
            "enabled": true,
            "respond_directly": false,
            "add_transfer_instructions": true
        },
        "markdown": true,
        "add_datetime_to_instructions": true
    }',
    'specialist',
    true
);
```

### 5. Персональный агент пользователя

```sql
INSERT INTO agents (
    agent_id,
    name,
    description,
    system_instructions,
    model_config,
    agent_config,
    user_id,  -- ВАЖНО: привязка к пользователю
    is_public
) VALUES (
    'personal_assistant_user123',
    'Мой личный помощник',
    'Персональный ассистент для конкретного пользователя',
    ARRAY[
        'Ты мой личный помощник',
        'Знаешь мои предпочтения и историю',
        'Всегда обращайся ко мне по имени'
    ],
    '{
        "provider": "openai",
        "id": "gpt-4.1-mini-2025-04-14",
        "temperature": 0.5
    }',
    '{
        "storage": {
            "table_name": "sessions"
        },
        "memory": {
            "enabled": true,
            "table_name": "user_memories",
            "delete_memories": false,
            "clear_memories": false
        },
        "history": {
            "add_history_to_messages": true,
            "num_history_runs": 10,
            "read_chat_history": true
        },
        "enable_agentic_memory": true,
        "enable_user_memories": true,
        "search_previous_sessions_history": true,
        "num_history_sessions": 5,
        "add_state_in_messages": true,
        "markdown": true,
        "add_datetime_to_instructions": true,
        "add_name_to_instructions": true
    }',
    'user123',  -- ID пользователя
    false  -- Приватный агент
);
```

## 🎯 ОСОБЫЕ ПОЛЯ С ПРИОРИТЕТОМ

### Нативные поля Agno в таблице agents

Эти поля имеют **приоритет над agent_config** и обрабатываются особым образом в `selector.py`:

```sql
-- В таблице agents
goal TEXT,                    -- Цель агента для системного сообщения  
expected_output TEXT,         -- Ожидаемый результат работы агента
role VARCHAR(255),            -- Роль агента в команде
```

### Логика приоритета в коде

```python
# В agents/selector.py (строки 324-326, 367)
"goal": dynamic_agent.goal or agent_config.get("goal"),
"expected_output": dynamic_agent.expected_output or agent_config.get("expected_output"),
"role": dynamic_agent.role or agent_config.get("role"),
```

**Это означает:**
- ✅ Если поле заполнено в БД → используется значение из БД
- ✅ Если поле NULL в БД → используется значение из `agent_config`
- ✅ Если нет ни там, ни там → используется `None`

### Практический пример

```sql
-- Создаем агента с DB полями
INSERT INTO agents (
    agent_id, name, 
    goal, expected_output, role,  -- Заполняем в БД
    agent_config
) VALUES (
    'example_agent', 'Пример',
    'Помогать пользователям',                    -- DB: goal
    'Качественные ответы на русском языке',      -- DB: expected_output  
    'assistant',                                 -- DB: role
    '{
        "goal": "Это значение будет ИГНОРИРОВАНО",           -- agent_config игнорируется
        "expected_output": "И это тоже ИГНОРИРОВАНО",        -- agent_config игнорируется
        "role": "И это значение тоже ИГНОРИРОВАНО",          -- agent_config игнорируется
        "markdown": true
    }'
);
```

**Результат:** Агент получит `goal`, `expected_output`, `role` из DB полей, а `markdown` из `agent_config`.

## 📋 Полная структура конфигураций

### model_config (JSONB) - Настройки модели OpenAI

```json
{
    // Основные параметры
    "provider": "openai",
    "id": "gpt-4.1-2025-04-14",
    "temperature": 0.7,
    "max_tokens": 4000,
    "max_completion_tokens": 3000,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "seed": 42,
    "stop": ["END", "STOP"],
    
    // Продвинутые параметры
    "reasoning_effort": "high",
    "store": true,
    "metadata": {"version": "1.0"},
    "modalities": ["text", "audio"],
    "audio": {"voice": "alloy", "format": "mp3"},
    
    // Клиентские параметры
    "api_key": "sk-...",
    "organization": "org-...",
    "base_url": "https://api.openai.com/v1",
    "timeout": 60.0,
    "max_retries": 3
}
```

### agent_config (JSONB) - Полная конфигурация агента

```json
{
    // 1. Хранилище и сессии
    "storage": {
        "table_name": "sessions",
        "schema": "public"
    },
    "session_name": "Работа с документами",
    "session_state": {"current_task": "analysis"},
    "search_previous_sessions_history": true,
    "num_history_sessions": 5,
    "cache_session": true,
    
    // 2. Контекст
    "context": {"department": "IT", "role": "developer"},
    "add_context": true,
    "resolve_context": true,
    
    // 3. Память (v2)
    "memory": {
        "enabled": true,
        "table_name": "user_memories",
        "delete_memories": true,
        "clear_memories": true
    },
    "enable_agentic_memory": true,
    "enable_user_memories": true,
    "add_memory_references": true,
    "enable_session_summaries": true,
    "add_session_summary_references": true,
    
    // 4. История
    "history": {
        "add_history_to_messages": true,
        "num_history_runs": 5,
        "read_chat_history": true
    },
    
    // 5. Знания (RAG)
    "knowledge": {
        "enabled": true,
        "type": "url",  // или "pdf"
        "urls": ["https://docs.example.com"],
        "pdf_paths": ["/path/to/docs.pdf"],
        "table_name": "knowledge"
    },
    "knowledge_filters": {"category": "technical"},
    "enable_agentic_knowledge_filters": true,
    "add_references": true,
    "references_format": "json",  // или "yaml"
    "search_knowledge": true,
    "update_knowledge": false,
    
    // 6. Инструменты
    "show_tool_calls": true,
    "tool_call_limit": 10,
    "tool_choice": "auto",  // или {"type": "function", "function": {"name": "search"}}
    "read_tool_call_history": true,
    
    // 7. Рассуждения
    "reasoning": {
        "enabled": true,
        "model_id": "gpt-4.1-2025-04-14",
        "min_steps": 1,
        "max_steps": 10
    },
    
    // 8. Системное сообщение
    "introduction": "Привет! Я ваш ассистент.",
    "goal": "Помогать с техническими вопросами",
    "additional_context": "Учитывай специфику IT-сферы",
    "markdown": true,
    "add_name_to_instructions": true,
    "add_datetime_to_instructions": true,
    "add_location_to_instructions": false,
    "timezone_identifier": "Europe/Moscow",
    "add_state_in_messages": true,
    
    // 9. Дополнительные сообщения
    "add_messages": [
        {"role": "user", "content": "Пример вопроса"},
        {"role": "assistant", "content": "Пример ответа"}
    ],
    "success_criteria": "Пользователь получил полезный ответ",
    
    // 10. Пользовательские сообщения
    "user_message_role": "user",
    "create_default_user_message": true,
    
    // 11. Ответы и парсинг
    "retries": 2,
    "delay_between_retries": 1,
    "exponential_backoff": true,
    "parser": {
        "enabled": true,
        "model_id": "gpt-4.1-mini-2025-04-14",
        "prompt": "Извлеки ключевую информацию"
    },
    "parse_response": true,
    "structured_outputs": true,
    "use_json_mode": false,
    "save_response_to_file": "/tmp/responses.txt",
    
    // 12. Стриминг
    "stream": true,
    "stream_intermediate_steps": true,
    "store_events": true,
    "events_to_skip": ["run_response_content"],
    
    // 13. Команда
    "team": {
        "enabled": true,
        "data": {"team_name": "Support Team"}
    },
    "respond_directly": false,
    "add_transfer_instructions": true,
    "team_response_separator": "\n---\n",
    "team_session_id": "team_session_123",
    "team_id": "support_team",
    "team_session_state": {"active_agent": "analyst"},
    
    // 14. Workflow
    "app_id": "crm_system",
    "workflow_id": "customer_support",
    "workflow_session_id": "workflow_456",
    "workflow_session_state": {"step": "analysis"},
    
    // 15. Отладка
    "debug_mode": false,
    "debug_level": 1,
    "monitoring": true,
    "telemetry": true
}
```

## 🔧 Использование агентов в коде

### Получение агента через selector.py

```python
from agents.selector import get_agent

# Получение динамического агента
agent = get_agent(
    agent_id="smart_assistant",
    model_id="gpt-4.1-2025-04-14",
    user_id="user123",
    session_id="session_456",
    debug_mode=False
)

# Использование агента
response = agent.run("Проанализируй этот документ")
```

### Кэширование агентов

Система автоматически кэширует агентов на основе:
- `agent_id`
- `model_id` 
- `user_id`
- `debug_mode`
- Хеш конфигурации (`model_config` + `agent_config`)

Кэш инвалидируется при изменении конфигураций в БД.

## 🎯 Приоритеты и логика выбора

### 1. Приоритет агентов
```sql
-- Логика в selector.py
ORDER BY 
    user_id = 'current_user',  -- Пользовательские агенты приоритетнее
    user_id IS NULL            -- Потом глобальные
```

### 2. Приоритет полей (ВАЖНО!)
- **DB поля** > **agent_config**: `goal`, `expected_output`, `role`
  ```python
  # В selector.py логика приоритета:
  "goal": dynamic_agent.goal or agent_config.get("goal")
  "expected_output": dynamic_agent.expected_output or agent_config.get("expected_output") 
  "role": dynamic_agent.role or agent_config.get("role")
  ```
- **agent_config** > **defaults**: все остальные параметры

### 3. Мультитенантность
- `user_id` = конкретный пользователь → приватный агент
- `user_id` = NULL → глобальный агент
- `is_public` = true → доступен всем
- `company_id` → корпоративные агенты

## 📊 Примеры SQL запросов для управления

### Создание агента с инструментами

```sql
-- 1. Создаем инструмент
INSERT INTO tools (name, description, function_definition) 
VALUES (
    'web_search',
    'Поиск информации в интернете',
    '{"type": "function", "function": {"name": "search_web", "description": "Ищет информацию в интернете"}}'
);

-- 2. Создаем агента с этим инструментом
INSERT INTO agents (agent_id, name, tool_ids, agent_config)
VALUES (
    'research_agent',
    'Исследователь',
    ARRAY[(SELECT id FROM tools WHERE name = 'web_search')],
    '{"show_tool_calls": true, "tool_call_limit": 5}'
);
```

### Обновление конфигурации агента

```sql
-- Обновление agent_config (слияние JSON)
UPDATE agents 
SET agent_config = agent_config || '{"memory": {"enabled": true}}'
WHERE agent_id = 'smart_assistant';

-- Добавление инструмента
UPDATE agents 
SET tool_ids = array_append(tool_ids, (SELECT id FROM tools WHERE name = 'calculator'))
WHERE agent_id = 'math_assistant';
```

### Поиск агентов

```sql
-- Найти всех агентов пользователя
SELECT agent_id, name, description 
FROM agents 
WHERE user_id = 'user123' AND is_active = true;

-- Найти агентов с памятью
SELECT agent_id, name 
FROM agents 
WHERE agent_config->>'memory'->>'enabled' = 'true';

-- Найти агентов с конкретными инструментами
SELECT a.agent_id, a.name, t.name as tool_name
FROM agents a
JOIN tools t ON t.id = ANY(a.tool_ids)
WHERE t.name = 'web_search';
```

## ⚡ Система кэширования

### DynamicAgentCache

```python
# В agent_cache.py
class DynamicAgentCache:
    def get(self, agent_id, model_id, user_id, debug_mode, dynamic_agent):
        # Создает ключ кэша на основе конфигурации
        config_hash = self._hash_config(dynamic_agent)
        cache_key = f"{agent_id}:{model_id}:{user_id}:{debug_mode}:{config_hash}"
        return self._cache.get(cache_key)
```

### Инвалидация кэша

```python
# При изменении агента в БД
from agents.agent_cache import agent_cache
agent_cache.invalidate_agent(agent_id)

# При изменении инструментов
from agents.tools_cache import tools_cache
tools_cache.invalidate()
```

## 🔄 Миграции и обновления

### Добавление новых полей

```python
# В новой миграции Alembic
def upgrade():
    op.add_column('agents', sa.Column('new_field', sa.Text(), nullable=True))
    
    # Обновляем существующие agent_config
    op.execute("""
        UPDATE agents 
        SET agent_config = agent_config || '{"new_feature": {"enabled": false}}'
        WHERE agent_config IS NOT NULL
    """)
```

## 🚨 Важные моменты

### 1. Обязательные поля
- `agent_id` - уникальный идентификатор
- `name` - имя агента
- `model_config` - конфигурация модели
- `agent_config` - конфигурация агента

### 2. Взаимосвязи компонентов
- **Memory** требует `user_id` для персонализации
- **Knowledge** требует настроенную `VectorDb`
- **Tools** загружаются через `tool_ids`
- **Storage** используется для сессий и истории

### 3. Производительность
- Кэширование агентов с учетом конфигураций
- Кэширование инструментов с TTL
- Индексы на `agent_id`, `user_id`, `is_active`

### 4. Безопасность
- Приватные агенты (`user_id` != NULL)
- Корпоративные агенты (`company_id`)
- Валидация `tool_ids` при создании

## Полная структура класса Agent в Agno

Класс `Agent` содержит **более 100 конфигурационных параметров**, разделенных на категории:

## 1. Основные настройки агента (Agent Settings)

### 1.1 Модель и идентификация
```python
model: Optional[Model] = None                    # Основная модель ИИ
name: Optional[str] = None                       # Имя агента
agent_id: Optional[str] = None                   # UUID агента (автогенерируется)
introduction: Optional[str] = None               # Введение агента
```

**Взаимосвязи**:
- `model` определяет доступные возможности (tool_calls, structured_outputs, streaming)
- `agent_id` используется для кэширования и идентификации в системе
- `name` добавляется в инструкции если `add_name_to_instructions=True`

## 2. Пользовательские настройки (User Settings)

### 2.1 Управление пользователями
```python
user_id: Optional[str] = None                    # ID пользователя по умолчанию
```

**Взаимосвязи**:
- Используется в системе памяти для персонализации
- Влияет на доступ к персональным агентам
- Связан с хранилищем сессий и мультитенантностью

## 3. Настройки сессии (Session Settings)

### 3.1 Управление сессиями
```python
session_id: Optional[str] = None                 # ID сессии (автогенерируется)
session_name: Optional[str] = None               # Имя сессии
session_state: Optional[Dict[str, Any]] = None   # Состояние сессии
search_previous_sessions_history: Optional[bool] = False  # Поиск в истории
num_history_sessions: Optional[int] = None       # Количество сессий истории
cache_session: bool = True                       # Кэширование сессии
```

**Взаимосвязи**:
- `session_state` доступно в промптах если `add_state_in_messages=True`
- Связано с `storage` для персистентности
- Влияет на `memory` и историю сообщений

## 4. Контекст агента (Agent Context)

### 4.1 Контекстуальные данные
```python
context: Optional[Dict[str, Any]] = None         # Контекст для инструментов
add_context: bool = False                        # Добавить контекст в промпт
resolve_context: bool = True                     # Разрешить функции в контексте
```

**Взаимосвязи**:
- Доступен в инструментах и функциях промптов
- Разрешается перед выполнением если `resolve_context=True`
- Может содержать динамические функции

## 5. Память агента (Agent Memory)

### 5.1 Система памяти (v2)
```python
memory: Optional[Union[AgentMemory, Memory]] = None      # Объект памяти
enable_agentic_memory: bool = False                      # Включить агентную память
enable_user_memories: bool = False                       # Включить пользовательские воспоминания
add_memory_references: Optional[bool] = None             # Добавить ссылки на память
enable_session_summaries: bool = False                   # Включить сводки сессий
add_session_summary_references: Optional[bool] = None    # Ссылки на сводки
```

**Взаимосвязи**:
- Работает с `user_id` и `session_id` для персонализации
- Требует настроенную `model` для управления памятью
- Связано с базой данных через `PostgresMemoryDb`
- Поддерживает два типа: `AgentMemory` (legacy) и `Memory` (v2)

## 6. История агента (Agent History)

### 6.1 Управление историей сообщений
```python
add_history_to_messages: bool = False            # Добавить историю в сообщения
num_history_responses: Optional[int] = None      # Количество исторических ответов (deprecated)
num_history_runs: int = 3                        # Количество исторических запусков
```

**Взаимосвязи**:
- Работает с `storage` для получения истории
- Влияет на размер контекста модели
- `num_history_responses` deprecated в пользу `num_history_runs`

## 7. Знания агента (Agent Knowledge)

### 7.1 База знаний и RAG
```python
knowledge: Optional[AgentKnowledge] = None               # База знаний
knowledge_filters: Optional[Dict[str, Any]] = None      # Фильтры знаний
enable_agentic_knowledge_filters: Optional[bool] = False # Агентные фильтры
add_references: bool = False                             # Добавить ссылки
retriever: Optional[Callable] = None                     # Функция поиска
references_format: Literal["json", "yaml"] = "json"     # Формат ссылок
```

**Взаимосвязи**:
- Требует `VectorDb` для хранения (например, `PgVector`)
- Использует `Embedder` для векторизации (например, `OpenAIEmbedder`)
- Связано с `search_knowledge` инструментом
- Работает с `ChunkingStrategy` для разбиения документов

## 8. Хранилище агента (Agent Storage)

### 8.1 Персистентное хранилище
```python
storage: Optional[Storage] = None                # Объект хранилища
extra_data: Optional[Dict[str, Any]] = None      # Дополнительные данные
```

**Взаимосвязи**:
- Поддерживает режимы: "agent", "team", "workflow", "workflow_v2"
- Связано с сессиями и историей
- В нашем проекте используется `PostgresAgentStorage`

## 9. Инструменты агента (Agent Tools)

### 9.1 Система инструментов
```python
tools: Optional[List[Union[Toolkit, Callable, Function, Dict]]] = None  # Список инструментов
show_tool_calls: bool = True                     # Показать вызовы инструментов
tool_call_limit: Optional[int] = None            # Лимит вызовов инструментов
tool_choice: Optional[Union[str, Dict[str, Any]]] = None  # Выбор инструмента
tool_hooks: Optional[List[Callable]] = None      # Хуки для инструментов
```

**Взаимосвязи**:
- Преобразуются в JSON Schema для модели
- Влияют на возможности агента
- Связаны с `Function` объектами
- В нашем проекте поддерживаются встроенные, MCP и кастомные инструменты

### 9.2 Стандартные инструменты
```python
read_chat_history: bool = False                  # Чтение истории чата
search_knowledge: bool = True                    # Поиск в базе знаний
update_knowledge: bool = False                   # Обновление базы знаний
read_tool_call_history: bool = False             # История вызовов инструментов
```

**Взаимосвязи**:
- Автоматически добавляются если соответствующие компоненты настроены
- `search_knowledge` требует настроенную `knowledge`

## 10. Рассуждения агента (Agent Reasoning)

### 10.1 Система пошагового рассуждения
```python
reasoning: bool = False                          # Включить рассуждения
reasoning_model: Optional[Model] = None          # Модель для рассуждений
reasoning_agent: Optional[Agent] = None          # Агент для рассуждений
reasoning_min_steps: int = 1                     # Минимум шагов рассуждений
reasoning_max_steps: int = 10                    # Максимум шагов рассуждений
```

**Взаимосвязи**:
- Использует отдельную модель или агента для рассуждений
- Работает пошагово через `ReasoningSteps`
- Может использоваться для сложных аналитических задач

## 11. Системные сообщения (System Message Settings)

### 11.1 Конфигурация системного сообщения
```python
system_message: Optional[Union[str, Callable, Message]] = None  # Системное сообщение
system_message_role: str = "system"              # Роль системного сообщения
create_default_system_message: bool = True       # Создать системное сообщение по умолчанию
```

### 11.2 Построение системного сообщения
```python
description: Optional[str] = None                # Описание агента
goal: Optional[str] = None                       # Цель агента
instructions: Optional[Union[str, List[str], Callable]] = None  # Инструкции
expected_output: Optional[str] = None            # Ожидаемый вывод
additional_context: Optional[str] = None         # Дополнительный контекст
markdown: bool = False                           # Форматирование Markdown
add_name_to_instructions: bool = False           # Добавить имя в инструкции
add_datetime_to_instructions: bool = False       # Добавить дату/время
add_location_to_instructions: bool = False       # Добавить локацию
timezone_identifier: Optional[str] = None        # Идентификатор часового пояса
add_state_in_messages: bool = False              # Добавить состояние в сообщения
```

**Взаимосвязи**:
- Все параметры влияют на финальное системное сообщение
- `instructions` может быть функцией с доступом к агенту
- Связано с `session_state` и `context`

## 12. Дополнительные сообщения (Extra Messages)

### 12.1 Дополнительные сообщения для few-shot learning
```python
add_messages: Optional[List[Union[Dict, Message]]] = None  # Дополнительные сообщения
success_criteria: Optional[str] = None           # Критерии успеха
```

**Взаимосвязи**:
- Добавляются после системного сообщения
- Используются для few-shot learning и примеров

## 13. Пользовательские сообщения (User Message Settings)

### 13.1 Настройки пользовательских сообщений
```python
user_message: Optional[Union[List, Dict, str, Callable, Message]] = None  # Пользовательское сообщение
user_message_role: str = "user"                  # Роль пользователя
create_default_user_message: bool = True         # Создать сообщение по умолчанию
```

**Взаимосвязи**:
- Может переопределить входящее сообщение
- Связано с `add_references` и `add_history_to_messages`

## 14. Настройки ответа агента (Agent Response Settings)

### 14.1 Повторные попытки и надежность
```python
retries: int = 0                                 # Количество повторных попыток
delay_between_retries: int = 1                   # Задержка между попытками
exponential_backoff: bool = False                # Экспоненциальная задержка
```

### 14.2 Модель ответа и парсинг
```python
response_model: Optional[Type[BaseModel]] = None # Модель ответа Pydantic
parser_model: Optional[Model] = None             # Модель для парсинга
parser_model_prompt: Optional[str] = None        # Промпт для парсера
parse_response: bool = True                      # Парсить ответ
structured_outputs: Optional[bool] = None        # Структурированные выводы
use_json_mode: bool = False                      # Режим JSON
save_response_to_file: Optional[str] = None      # Сохранить ответ в файл
```

**Взаимосвязи**:
- `response_model` требует совместимую модель
- `parser_model` используется для парсинга если основная модель не поддерживает structured outputs
- `structured_outputs` зависит от возможностей модели (например, OpenAI поддерживает нативно)

## 15. Потоковая передача (Agent Streaming)

### 15.1 Настройки стриминга
```python
stream: Optional[bool] = None                    # Потоковая передача ответа
stream_intermediate_steps: bool = False          # Стриминг промежуточных шагов
store_events: bool = False                       # Сохранять события
events_to_skip: Optional[List[RunEvent]] = None  # События для пропуска
```

**Взаимосвязи**:
- Зависит от поддержки стриминга моделью
- Связано с `RunResponseEvent` системой
- По умолчанию пропускает `run_response_content` события

## 16. Команда агентов (Agent Team)

### 16.1 Командная работа и координация
```python
team: Optional[List[Agent]] = None               # Команда агентов
team_data: Optional[Dict[str, Any]] = None       # Данные команды
role: Optional[str] = None                       # Роль в команде
respond_directly: bool = False                   # Отвечать напрямую
add_transfer_instructions: bool = True           # Добавить инструкции передачи
team_response_separator: str = "\n"              # Разделитель ответов команды
team_session_id: Optional[str] = None            # ID сессии команды
team_id: Optional[str] = None                    # ID команды
team_session_state: Optional[Dict[str, Any]] = None  # Состояние сессии команды
```

**Взаимосвязи**:
- Агенты в команде могут передавать задачи друг другу
- Связано с `TeamRunResponse` и `team_session_state`
- Поддерживает иерархическую структуру агентов

## 17. Приложение и Workflow

### 17.1 Интеграция с внешними системами
```python
app_id: Optional[str] = None                     # ID приложения
workflow_id: Optional[str] = None                # ID workflow
workflow_session_id: Optional[str] = None        # ID сессии workflow
workflow_session_state: Optional[Dict[str, Any]] = None  # Состояние workflow
```

**Взаимосвязи**:
- Используется для интеграции с приложениями и workflow системами
- Поддерживает сложные бизнес-процессы

## 18. Отладка и мониторинг (Debug & Monitoring)

### 18.1 Настройки отладки
```python
debug_mode: bool = False                         # Режим отладки
debug_level: Literal[1, 2] = 1                   # Уровень отладки
monitoring: bool = False                         # Мониторинг в agno.com
telemetry: bool = True                           # Телеметрия
```

**Взаимосвязи**:
- Влияет на уровень логирования
- `monitoring` отправляет данные на agno.com
- Переопределяется переменными окружения `AGNO_DEBUG`, `AGNO_MONITOR`, `AGNO_TELEMETRY`

## Конфигурации моделей

### OpenAI Chat Model (Основная модель в проекте)

```python
# Основные параметры
id: str = "gpt-4o"                               # ID модели
temperature: Optional[float] = None              # Температура (креативность)
max_tokens: Optional[int] = None                 # Максимум токенов
max_completion_tokens: Optional[int] = None      # Максимум токенов завершения
top_p: Optional[float] = None                    # Top-p сэмплинг
frequency_penalty: Optional[float] = None        # Штраф за частоту
presence_penalty: Optional[float] = None         # Штраф за присутствие
seed: Optional[int] = None                       # Семя для воспроизводимости
stop: Optional[Union[str, List[str]]] = None     # Стоп-последовательности

# Продвинутые параметры
reasoning_effort: Optional[str] = None           # Усилие рассуждения
store: Optional[bool] = None                     # Хранение разговора
metadata: Optional[Dict[str, Any]] = None        # Метаданные
modalities: Optional[List[str]] = None           # Модальности (text, audio)
audio: Optional[Dict[str, Any]] = None           # Настройки аудио

# Клиентские параметры
api_key: Optional[str] = None                    # API ключ
organization: Optional[str] = None               # Организация
base_url: Optional[Union[str, httpx.URL]] = None # Базовый URL
timeout: Optional[float] = None                  # Таймаут
max_retries: Optional[int] = None                # Максимум повторов
```

## Архитектура динамических агентов в нашем проекте

### Модель DynamicAgent (PostgreSQL)

```python
class DynamicAgent(Base):
    id = Column(UUID, primary_key=True)
    agent_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Конфигурации
    model_config = Column(JSONB, default={"provider": "openai", "id": "gpt-4.1-mini-2025-04-14"})
    system_instructions = Column(ARRAY(Text), default=[])
    tool_ids = Column(ARRAY(UUID), default=[])
    agent_config = Column(JSONB, default={})
    
    # Мультитенантность
    is_public = Column(Boolean, default=False)
    company_id = Column(UUID, nullable=True)
    user_id = Column(String(255), nullable=True)
    
    # Метаданные
    photo = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
```

### Структура agent_config

```json
{
  "storage": {
    "table_name": "sessions"
  },
  "memory": {
    "enabled": true,
    "table_name": "user_memories",
    "delete_memories": true,
    "clear_memories": true
  },
  "history": {
    "add_history_to_messages": true,
    "num_history_runs": 3,
    "read_chat_history": true
  },
  "enable_agentic_memory": true,
  "add_state_in_messages": true,
  "markdown": true,
  "add_datetime_to_instructions": true,
  "debug_mode": false
}
```

## Ключевые взаимосвязи конфигураций

### 1. Модель и возможности
- `model` определяет доступные возможности (tool_calls, structured_outputs, streaming)
- `reasoning_model` и `parser_model` могут быть разными для специализированных задач
- OpenAI модели поддерживают нативные structured outputs

### 2. Память и персистентность
- `memory` + `user_id` + `session_id` обеспечивают персональную память
- `storage` сохраняет историю и состояние сессий
- `enable_agentic_memory` позволяет агенту управлять памятью автономно

### 3. Знания и поиск (RAG)
- `knowledge` + `VectorDb` + `Embedder` обеспечивают RAG
- `search_knowledge=True` автоматически добавляет инструмент поиска
- `retriever` может переопределить стандартный поиск

### 4. Инструменты и функции
- `tools` преобразуются в JSON Schema для модели
- `tool_choice` управляет выбором инструментов
- `tool_hooks` позволяют middleware обработку
- Поддерживаются встроенные, MCP и кастомные инструменты

### 5. Сообщения и промпты
- `system_message` строится из множества параметров
- `add_history_to_messages` + `num_history_runs` контролируют историю
- `add_references` добавляет результаты поиска знаний

### 6. Команды и workflow
- `team` позволяет агентам сотрудничать
- `workflow_*` параметры интегрируют с workflow системами
- `respond_directly` изменяет поток ответов в команде

### 7. Кэширование и производительность
- В нашем проекте используется `DynamicAgentCache` с учетом конфигураций
- Кэш учитывает `agent_id`, `model_id`, `user_id`, `debug_mode` и хеш конфигурации
- Статические агенты не кэшируются

## Примеры конфигураций

### Базовая конфигурация
```python
agent = Agent(
    name="BasicAgent",
    model=OpenAIChat(id="gpt-4.1-mini-2025-04-14"),
    description="Базовый агент",
    instructions="Ты полезный ассистент",
    debug_mode=True
)
```

### Конфигурация с памятью и знаниями
```python
agent = Agent(
    name="SmartAgent",
    model=OpenAIChat(id="gpt-4.1-mini-2025-04-14"),
    # Память
    memory=Memory(
        model=OpenAIChat(id="gpt-4.1-mini-2025-04-14"),
        db=PostgresMemoryDb(db_url="postgresql://...", table_name="user_memories")
    ),
    enable_agentic_memory=True,
    # Знания
    knowledge=UrlKnowledge(
        urls=["https://example.com"],
        vector_db=PgVector(db_url="postgresql://...", table_name="knowledge")
    ),
    search_knowledge=True,
    # История
    add_history_to_messages=True,
    num_history_runs=3,
    # Хранилище
    storage=PostgresAgentStorage(
        db_url="postgresql://...",
        table_name="sessions"
    )
)
```

### Конфигурация с инструментами и командой
```python
agent = Agent(
    name="TeamLeader",
    model=OpenAIChat(id="gpt-4.1-2025-04-14"),
    tools=[DuckDuckGoTools(), PythonTools()],
    team=[web_agent, finance_agent],
    show_tool_calls=True,
    tool_call_limit=10,
    add_transfer_instructions=True
)
```

## Особенности нашего проекта

### 1. Гибридная архитектура
- **Статические агенты**: Hardcoded конфигурации для специализированных задач
- **Динамические агенты**: Конфигурируемые через базу данных

### 2. Мультитенантность
- Поддержка `company_id` и `user_id`
- Публичные и приватные агенты
- Приоритет пользовательских агентов над глобальными

### 3. Система кэширования
- Кэш учитывает конфигурации агентов
- Инвалидация при изменении конфигураций
- Оптимизация производительности

### 4. Инструменты
- **Встроенные**: DuckDuckGo, Python, File operations
- **MCP**: Model Context Protocol инструменты
- **Кастомные**: Пользовательские функции

### 5. Единая база данных
- Общие таблицы для sessions, user_memories
- Централизованное управление
- Поддержка миграций Alembic

## Заключение

Система конфигурации агентов Agno предоставляет исключительно гибкие возможности для создания специализированных ИИ-агентов. Ключевые принципы:

1. **Модульность**: Каждый компонент (память, знания, инструменты) независим
2. **Гибкость**: Более 100 параметров для тонкой настройки поведения
3. **Интеграция**: Компоненты работают вместе для создания мощных агентов
4. **Расширяемость**: Возможность добавления собственных компонентов
5. **Производительность**: Система кэширования и оптимизации
6. **Мультитенантность**: Поддержка организационной структуры

Правильная конфигурация требует глубокого понимания взаимосвязей между параметрами и целей использования агента. Наш проект демонстрирует эффективное использование всех возможностей фреймворка Agno. 