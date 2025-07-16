# Пример полной конфигурации агента

**Важное замечание:** Этот файл содержит полный список конфигурационных блоков, которые определены в моделях базы данных вашего проекта (`db/models.py`) и соответствуют возможностям `agno`.

Ниже приведено детальное описание статуса реализации каждого блока в `db/services/dynamic_agent_service.py`.

### Статус реализации:

---

#### ✅ **Полностью реализовано и работает:**

*   **`model_configuration`**: Практически полная поддержка всех параметров `agno` для моделей OpenAI, Claude и Gemini. Валидация через Pydantic обеспечивает надежность.
*   **`storage_config`**: **(Новое!)** Полностью динамическое управление хранилищем сессий. Все параметры, такие как `db_url`, `table_name`, `db_schema`, теперь задаются в JSON-конфигурации агента, что обеспечивает максимальную гибкость.
*   **`settings`**: Большинство общих настроек агента из `AgentSettings` (например, `debug_mode`, `stream`, `system_message`) корректно передаются в инстанс `agno.Agent`.

---

#### 🟡 **Частично реализовано или с особенностями:**

*   **`tools_config`**:
    *   ✅ **Полностью реализовано:** Ваша система **динамически расширяет** нативные возможности `agno`.
        *   **`dynamic_tools`**: Загрузка нативных инструментов `agno` (например, `DuckDuckGoTools`) по их ID из БД.
        *   **`custom_tools`**: Загрузка кастомных Python-инструментов, код которых хранится в БД.
        *   **`mcp_servers`**: Подключение к внешним серверам инструментов (MCP).
        *   **`tools`**: Полная поддержка нативного параметра `agno` для статического определения инструментов прямо в JSON (менее гибкий способ).
    *   ✅ **Полностью реализовано:** Прямая передача нативных параметров `agno`:
        *   `show_tool_calls`
        *   `tool_call_limit`
        *   `tool_choice`
        *   `function_declarations`
    *   ❌ **Не реализовано:**
        *   `tool_hooks`: Функциональность "хуков" (промежуточного ПО) для инструментов в `dynamic_agent_service.py` отсутствует.
*   **`memory_config`**:
    *   ✅ **Работает:** Основная функциональность памяти с `enable_agentic_memory`, `enable_user_memories`, `enable_session_summaries`, `add_memory_references`, `add_session_summary_references`, `memory_filters`.
*   **`knowledge_config`**: **(Новое!)**
    *   ✅ **Работает:** Конфигурация считывается и передается в `AgentKnowledge`.
    *   ❌ **Не реализовано:** Полноценная функциональность RAG. Требуется настройка векторной базы данных и логики получения данных.
*   **`reasoning_config`**: **(Новое!)**
    *   ✅ **Работает:** Конфигурация для ReAct считывается.
    *   ❌ **Не реализовано:** Полноценная логика выполнения шагов ReAct.

---

#### ❌ **Не реализовано (модели в БД есть, логика отсутствует):**

Эти блоки определены в `db/models.py`, но логика их подключения в `dynamic_agent_service.py` отсутствует. Это является "техническим долгом" и заделом на будущее развитие.

*   **`team_config`**: Функциональность **командной работы агентов**. Требует реализации логики для управления группой агентов (`team`).

---

Ниже представлен полный пример JSON, демонстрирующий все возможные поля, которые могут быть сохранены в БД.

```json
{
  "name": "my-complete-agent",
  "agent_id": "my-complete-agent-001",
  "description": "Агент для демонстрации ВСЕХ возможных конфигураций, поддерживаемых agno.",
  "instructions": "Внимательно следуй инструкциям и используй доступные инструменты.",
  
  "model_configuration": {
    "id": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "stop": ["\n"],
    "seed": 42
  },

  "tools_config": {
    "show_tool_calls": true,
    "tool_call_limit": 10,
    "tool_choice": "auto",
    "function_declarations": [],
    "tool_hooks": "реализовать",
    "dynamic_tools": ["duckduckgo_search"],
    "custom_tools": ["my_python_tool_id"],
    "mcp_servers": ["my_mcp_server_id"],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "static_calculator",
          "description": "Пример статически определенного инструмента."
        }
      }
    ]
  },

  "memory_config": {
    "memory_type": "postgres",
    "enable_agentic_memory": true,
    "enable_user_memories": true,
    "add_memory_references": true, 
    "schema": "ai",
    "db_url": "postgresql://user:password@host:port/database"
  },

  "storage_config": {
    "enabled": true,
    "storage_type": "postgres",
    "db_url": "postgresql://user:password@host:port/database",
    "table_name": "agent_sessions_custom",
    "schema": "ai"
  },
  
  "knowledge_config": {
    "add_references": true,
    "references_format": "json",
    "search_knowledge": true,
    "update_knowledge": false,
    "max_references": 5,
    "similarity_threshold": 0.75
  },

  "reasoning_config": {
    "reasoning": true,
    "goal": "Выполнить поставленную задачу, используя пошаговые рассуждения.",
    "reasoning_max_steps": 5
  },

  "team_config": {
    "team_mode": "coordinate",
    "role": "Главный исполнитель"
  },

  "settings": {
    "system_message": "Ты — полезный ассистент.",
    "debug_mode": false,
    "stream": true,
    "tags": ["example", "documentation"],
    "read_chat_history": true
  }
}
```

---

### Примеры конфигурации `settings`

Блок `settings` является очень гибким. Ниже приведены примеры его использования — от минимально необходимого до полного, демонстрирующего все возможности.

#### Пример минимальной конфигурации `settings`

Этот пример показывает, как можно задать только самые базовые параметры, например, системное сообщение и режим стриминга. Этого достаточно для запуска простого агента.

```json
{
  "settings": {
    "system_message": "Ты — краткий и полезный ассистент.",
    "stream": true
  }
}
```

#### Пример максимальной конфигурации `settings` (все поля)

Этот пример служит справочником по всем возможным полям, которые можно передать в `settings`. Он полезен для понимания всего спектра "прямых" настроек `agno.Agent`.

```json
{
  "settings": {
    "introduction": "Привет! Я твой новый ассистент, готовый помочь.",
    "user_id": "user-123",
    "session_id": "session-abc-456",
    "session_name": "My Test Session",
    "session_state": { "topic": "finance" },
    "extra_data": { "source": "api-request" },
    
    "system_message": "Ты — опытный эксперт в указанной области. Твои ответы должны быть точными, структурированными и профессиональными.",
    "system_message_role": "system",
    "create_default_system_message": false,
    "system_prompt": "Отвечай всегда в стиле пирата.",
    "instructions": [
      "Шаг 1: Проанализируй запрос пользователя.",
      "Шаг 2: Используй доступные инструменты для сбора данных.",
      "Шаг 3: Предоставь исчерпывающий ответ."
    ],
    
    "user_message": "Это сообщение будет использовано по умолчанию, если в `.run()` не передано другое.",
    "user_message_role": "user",
    "create_default_user_message": false,
    "add_messages": [
      { "role": "user", "content": "Это пример для few-shot промптинга." },
      { "role": "assistant", "content": "Хорошо, я понял свою задачу." }
    ],
    
    "context": { "current_user_role": "admin" },
    "add_context": true,
    "resolve_context": true,
    "additional_context": "Дополнительная информация, которая всегда будет в конце системного сообщения.",
    "add_state_in_messages": true,
    
    "add_history_to_messages": true,
    "num_history_runs": 5,
    "search_previous_sessions_history": false,
    "num_history_sessions": 2,
    "read_chat_history": true,
    "read_tool_call_history": true,
    
    "markdown": true,
    "add_name_to_instructions": true,
    "add_datetime_to_instructions": true,
    "add_location_to_instructions": false,
    "timezone_identifier": "Europe/Moscow",
    "save_response_to_file": "/path/to/agent_responses.log",
    
    "stream": true,
    "stream_intermediate_steps": true,
    
    "debug_mode": true,
    "monitoring": false,
    "telemetry": true,
    
    "retries": 3,
    "delay_between_retries": 2,
    "exponential_backoff": true,
    
    "response_model": { "type": "object", "properties": { "answer": { "type": "string" }, "confidence": { "type": "number" } } },
    "parse_response": true,
    "use_json_mode": true,
    "parser_model": { "id": "gpt-3.5-turbo" },
    "parser_model_prompt": "Извлеки из текста ответ и уровень уверенности.",
    
    "store_events": true,
    "events_to_skip": ["RunResponseContentEvent"],
    
    "team_data": { "project_id": "project_alpha" },
    "team_session_id": "team-session-xyz-789",
    
    "config_version": "2.0",
    "tags": ["documentation-example", "maximal-config"],
    "app_id": "my-super-app-id"
  }
}
``` 