# Анализ поддержки конфигураций Agno в динамических агентах

## Введение

Данный документ анализирует, какие из 100+ конфигураций агентов Agno поддерживает текущая реализация динамических агентов в проекте, и что нужно добавить для полной поддержки.

## Текущая архитектура динамических агентов

### Модель базы данных (DynamicAgent)
```python
class DynamicAgent(Base):
    # Основная идентификация
    agent_id: str                    # ✅ Поддерживается
    name: str                        # ✅ Поддерживается  
    description: Text                # ✅ Поддерживается
    
    # Конфигурация модели
    model_config: JSONB              # ✅ Частично (только provider + id)
    
    # Инструкции и инструменты
    system_instructions: ARRAY[Text] # ✅ Поддерживается
    tool_ids: ARRAY[UUID]           # ✅ Поддерживается
    
    # Расширенная конфигурация
    agent_config: JSONB             # ✅ Гибкое поле для всех настроек
    
    # Мультитенантность
    user_id: str                    # ✅ Поддерживается
    company_id: UUID                # ✅ Поддерживается
    is_public: bool                 # ✅ Поддерживается
```

## Поддерживаемые конфигурации Agno

### ✅ ПОЛНОСТЬЮ ПОДДЕРЖИВАЕМЫЕ (15/100+)

#### 1. Основные настройки агента
- ✅ `name` - из `dynamic_agent.name`
- ✅ `agent_id` - из `dynamic_agent.agent_id`
- ✅ `description` - из `dynamic_agent.description`
- ✅ `user_id` - передается в конструктор
- ✅ `session_id` - передается в конструктор

#### 2. Модель
- ✅ `model` - создается `OpenAIChat(id=model_id)`

#### 3. Инструменты
- ✅ `tools` - загружаются из БД по `tool_ids`

#### 4. Инструкции
- ✅ `instructions` - из `system_instructions` (массив -> строка)

#### 5. Хранилище
- ✅ `storage` - `PostgresAgentStorage` с настройками из `agent_config.storage`

#### 6. Память
- ✅ `memory` - `Memory` с `PostgresMemoryDb` если `agent_config.memory.enabled=true`
- ✅ `enable_agentic_memory` - из `agent_config.enable_agentic_memory`

#### 7. История
- ✅ `add_history_to_messages` - из `agent_config.history.add_history_to_messages`
- ✅ `num_history_runs` - из `agent_config.history.num_history_runs`
- ✅ `read_chat_history` - из `agent_config.history.read_chat_history`

#### 8. Форматирование
- ✅ `markdown` - из `agent_config.markdown`
- ✅ `add_state_in_messages` - из `agent_config.add_state_in_messages`
- ✅ `add_datetime_to_instructions` - из `agent_config.add_datetime_to_instructions`
- ✅ `debug_mode` - из `agent_config.debug_mode`

### ⚠️ ЧАСТИЧНО ПОДДЕРЖИВАЕМЫЕ (10/100+)

#### 1. Модель
- ⚠️ `model_config` - поддерживается только `provider` и `id`, нет других параметров модели

#### 2. Память
- ⚠️ `memory` - поддерживается только `PostgresMemoryDb`, нет других типов
- ⚠️ Поддерживается только `delete_memories` и `clear_memories`
- ❌ НЕТ: `enable_user_memories`, `add_memory_references`, `enable_session_summaries`

#### 3. Хранилище
- ⚠️ `storage` - поддерживается только `PostgresAgentStorage`
- ❌ НЕТ: другие типы Storage

#### 4. Инструменты
- ⚠️ `tools` - поддерживаются только из БД
- ❌ НЕТ: `show_tool_calls`, `tool_call_limit`, `tool_choice`, `tool_hooks`

#### 5. Стандартные инструменты
- ❌ НЕТ: `read_chat_history`, `search_knowledge`, `update_knowledge`, `read_tool_call_history`

### ❌ НЕ ПОДДЕРЖИВАЕМЫЕ (75+/100+)

#### 1. Сессии
- ❌ `session_name`, `session_state`, `search_previous_sessions_history`
- ❌ `num_history_sessions`, `cache_session`

#### 2. Контекст
- ❌ `context`, `add_context`, `resolve_context`

#### 3. Знания (Knowledge)
- ❌ `knowledge`, `knowledge_filters`, `enable_agentic_knowledge_filters`
- ❌ `add_references`, `retriever`, `references_format`

#### 4. Рассуждения (Reasoning)
- ❌ `reasoning`, `reasoning_model`, `reasoning_agent`
- ❌ `reasoning_min_steps`, `reasoning_max_steps`

#### 5. Системные сообщения
- ❌ `system_message`, `system_message_role`, `create_default_system_message`
- ❌ `goal`, `expected_output`, `additional_context`
- ❌ `add_name_to_instructions`, `add_location_to_instructions`, `timezone_identifier`

#### 6. Дополнительные сообщения
- ❌ `add_messages`, `success_criteria`

#### 7. Пользовательские сообщения
- ❌ `user_message`, `user_message_role`, `create_default_user_message`

#### 8. Настройки ответа
- ❌ `retries`, `delay_between_retries`, `exponential_backoff`
- ❌ `response_model`, `parser_model`, `parser_model_prompt`
- ❌ `parse_response`, `structured_outputs`, `use_json_mode`
- ❌ `save_response_to_file`

#### 9. Стриминг
- ❌ `stream`, `stream_intermediate_steps`
- ❌ `store_events`, `events_to_skip`

#### 10. Команды
- ❌ `team`, `team_data`, `role`, `respond_directly`
- ❌ `add_transfer_instructions`, `team_response_separator`
- ❌ `team_session_id`, `team_id`, `team_session_state`

#### 11. Workflow и приложения
- ❌ `app_id`, `workflow_id`, `workflow_session_id`, `workflow_session_state`

#### 12. Мониторинг
- ❌ `debug_level`, `monitoring`, `telemetry`

## Пример текущей конфигурации

### В базе данных:
```json
{
  "agent_id": "my_agent",
  "name": "My Dynamic Agent",
  "description": "Test agent",
  "model_config": {
    "provider": "openai",
    "id": "gpt-4"
  },
  "system_instructions": [
    "You are a helpful assistant",
    "Always be polite"
  ],
  "tool_ids": ["uuid1", "uuid2"],
  "agent_config": {
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
    "markdown": true,
    "add_state_in_messages": true,
    "add_datetime_to_instructions": true,
    "enable_agentic_memory": true,
    "debug_mode": false
  }
}
```

### Создается Agent:
```python
Agent(
    name="My Dynamic Agent",
    agent_id="my_agent", 
    user_id=user_id,
    session_id=session_id,
    model=OpenAIChat(id="gpt-4"),
    tools=[tool1, tool2],  # Из БД
    description="Test agent",
    instructions="You are a helpful assistant\nAlways be polite",
    storage=PostgresAgentStorage(...),
    memory=Memory(...),
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=3,
    read_chat_history=True,
    add_state_in_messages=True,
    markdown=True,
    add_datetime_to_instructions=True,
    debug_mode=False
)
```

## Рекомендации по расширению

### 1. Высокий приоритет (критичные функции)

#### Knowledge (Знания)
```python
# В agent_config добавить:
"knowledge": {
    "enabled": true,
    "type": "url",  # url, file, text
    "config": {
        "urls": ["https://example.com"],
        "vector_db": {
            "type": "pgvector",
            "table_name": "knowledge_vectors"
        }
    },
    "num_documents": 5,
    "add_references": true,
    "search_knowledge": true
}
```

#### Response Model
```python
# В agent_config добавить:
"response": {
    "model": "MyPydanticModel",
    "parse_response": true,
    "structured_outputs": true,
    "retries": 3
}
```

#### Reasoning
```python
# В agent_config добавить:
"reasoning": {
    "enabled": true,
    "model_id": "gpt-4",
    "min_steps": 1,
    "max_steps": 10
}
```

### 2. Средний приоритет

#### Tool Settings
```python
# В agent_config добавить:
"tools": {
    "show_tool_calls": true,
    "tool_call_limit": 10,
    "tool_choice": "auto"
}
```

#### Streaming
```python
# В agent_config добавить:
"streaming": {
    "enabled": true,
    "intermediate_steps": false
}
```

### 3. Низкий приоритет
- Team/Workflow функции
- Расширенные настройки сообщений
- Мониторинг и телеметрия

## Заключение

**Текущая поддержка: ~25/100+ конфигураций Agno (25%)**

**Поддерживается хорошо:**
- Базовые настройки агента
- Память и история
- Простые инструменты
- Хранилище сессий

**Критически не хватает:**
- Система знаний (Knowledge/RAG)
- Structured outputs
- Система рассуждений
- Расширенные настройки инструментов
- Стриминг

**Архитектура готова к расширению** благодаря гибкому полю `agent_config: JSONB`, которое может хранить любые дополнительные конфигурации без изменения схемы БД. 