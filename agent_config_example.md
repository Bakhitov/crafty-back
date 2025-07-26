# Руководство по конфигурации агентов

## 📋 Обзор

Данное руководство содержит полное описание всех возможных конфигураций для создания динамических агентов в системе. Конфигурации основаны на моделях Pydantic из `db/models.py` и полностью совместимы с фреймворком Agno.

## 🚀 Минимальная конфигурация (быстрый старт)

### Простейший агент (только обязательные поля)

```json
{
  "name": "Мой первый агент",
  "agent_id": "simple-agent-001",
  "description": "Простой агент для тестирования",
  "instructions": "Ты дружелюбный помощник. Отвечай кратко и по делу."
}
```

### Минимальная практичная конфигурация

```json
{
  "name": "Базовый помощник",
  "agent_id": "basic-helper-001",
  "description": "Базовый агент с настроенной моделью",
  "instructions": "Ты умный помощник. Помогай пользователям решать задачи.",
  
  // ⚡ Настройка модели (рекомендуется)
  "model_configuration": {
    "id": "gpt-4.1",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  
  // 💾 Включение хранения сессий (рекомендуется)
  "storage_config": {
    "storage_type": "postgres",
    "enabled": true
  }
}
```

## 🔧 Полная конфигурация со всеми возможностями

### Расширенный агент с полным функционалом

```json
{
  "name": "Продвинутый AI-ассистент",
  "agent_id": "advanced-assistant-v2",
  "description": "Многофункциональный агент с расширенными возможностями",
  "instructions": [
    "Ты экспертный AI-ассистент с доступом к множеству инструментов.",
    "Всегда думай пошагово при решении сложных задач.",
    "Используй доступные инструменты для получения актуальной информации.",
    "Будь точным, полезным и дружелюбным в общении."
  ],
  
  // ===== 🤖 КОНФИГУРАЦИЯ МОДЕЛИ =====
  "model_configuration": {
    // Основные параметры
    "id": "gpt-4.1",                    // Модель AI
    "provider": "openai",               // Провайдер (openai, anthropic, google)
    "temperature": 0.7,                 // Креативность (0.0-2.0)
    "max_tokens": 4000,                 // Максимум токенов в ответе
    
    // Продвинутые параметры OpenAI
    "top_p": 0.9,                      // Nucleus sampling (0.0-1.0)
    "frequency_penalty": 0.1,          // Штраф за повторения (-2.0 до 2.0)
    "presence_penalty": 0.1,           // Штраф за присутствие токенов (-2.0 до 2.0)
    "stop": ["КОНЕЦ", "СТОП"],          // Стоп-последовательности
    
    // API параметры
    "timeout": 60.0,                   // Таймаут запроса в секундах
    "max_retries": 3,                  // Максимум повторных попыток
    
    // Дополнительные параметры
    "seed": 12345,                     // Сид для воспроизводимости
    "user": "production-user",         // ID пользователя для логирования
    "metadata": {                      // Метаданные запроса
      "environment": "production",
      "version": "1.0"
    }
  },
  
  // ===== 🛠️ КОНФИГУРАЦИЯ ИНСТРУМЕНТОВ =====
  "tools_config": {
    // Управление инструментами
    "show_tool_calls": true,           // Показывать вызовы инструментов
    "tool_call_limit": 10,             // Максимум вызовов за раз
    "tool_choice": "auto",             // Стратегия выбора: "auto", "none", "required"
    
    // 🔧 Статические инструменты (встроенные в конфигурацию)
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "calculate",
          "description": "Выполнить математическое вычисление",
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
      }
    ],
    
    // 🚀 Динамические инструменты Agno (из БД)
    "dynamic_tools": [
      "duckduckgo-search",             // Поиск в интернете
      "yfinance-stocks",               // Финансовые данные
      "weather-api",                   // Информация о погоде
      "email-sender"                   // Отправка email
    ],
    
    // 🐍 Кастомные Python инструменты (код в БД)
    "custom_tools": [
      "custom-db-query",               // Запросы к БД
      "custom-report-generator",       // Генератор отчетов
      "custom-data-processor"          // Обработка данных
    ],
    
    // 🌐 MCP серверы (внешние инструменты)
    "mcp_servers": [
      "github-mcp-server",             // Работа с GitHub
      "jira-mcp-server",               // Интеграция с Jira
      "slack-mcp-server"               // Интеграция со Slack
    ],
    
    // 🪝 Хуки инструментов (промежуточное ПО)
    "tool_hooks": [
      {
        "hook_type": "before_tool_call",
        "registry_id": "auth-validation-hook"
      },
      {
        "hook_type": "after_tool_call", 
        "registry_id": "logging-hook"
      }
    ]
  },
  
  // ===== 🧠 КОНФИГУРАЦИЯ ПАМЯТИ =====
  "memory_config": {
    "memory_type": "postgres",         // Тип памяти (только postgres)
    
    // Включение функций памяти
    "enable_agentic_memory": true,     // Агент управляет своей памятью
    "enable_user_memories": true,      // Запоминание фактов о пользователе
    "enable_session_summaries": true,  // Создание резюме сессий
    
    // Настройки отображения
    "add_memory_references": true,     // Показывать ссылки на память
    "add_session_summary_references": true, // Показывать ссылки на резюме
    
    // Фильтрация памяти
    "memory_filters": {
      "topics": ["работа", "проекты"],
      "min_importance": 0.7
    },
    
    // Подключение к БД
    "db_url": "postgresql://user:pass@localhost/db",
    "table_name": "agent_memory",
    "db_schema": "ai"
  },
  
  // ===== 📚 КОНФИГУРАЦИЯ БАЗЫ ЗНАНИЙ =====
  "knowledge_config": {
    // RAG (поиск по документам)
    "add_references": true,            // Включить RAG
    "search_knowledge": true,          // Разрешить поиск в знаниях
    "update_knowledge": false,         // Запретить обновление знаний
    
    // Параметры поиска
    "max_references": 5,               // Максимум документов в контексте
    "similarity_threshold": 0.75,      // Порог релевантности (0.0-1.0)
    "references_format": "json",       // Формат ссылок: json, markdown, text
    
    // Фильтрация знаний
    "knowledge_filters": {
      "document_type": ["manual", "faq"],
      "department": "engineering"
    },
    "enable_agentic_knowledge_filters": true, // Агент выбирает фильтры
    
    // Векторная БД
    "vector_db_url": "postgresql://user:pass@localhost/vector_db",
    "embedding_model": "text-embedding-3-small",
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  
  // ===== 💾 КОНФИГУРАЦИЯ ХРАНИЛИЩА =====
  "storage_config": {
    "storage_type": "postgres",        // Тип хранилища (только postgres)
    "enabled": true,                   // Включить хранилище
    
    // Подключение к БД
    "db_url": "postgresql://user:pass@localhost/db",
    "table_name": "agent_sessions",
    "db_schema": "ai",
    
    // Дополнительные опции
    "store_events": true,              // Сохранять события выполнения
    "extra_data": {
      "retention_days": 90,
      "backup_enabled": true
    }
  },
  
  // ===== 🤔 КОНФИГУРАЦИЯ РАССУЖДЕНИЙ =====
  "reasoning_config": {
    "reasoning": true,                 // Включить пошаговое рассуждение
    
    // Параметры рассуждения
    "reasoning_min_steps": 2,          // Минимум шагов рассуждения
    "reasoning_max_steps": 8,          // Максимум шагов рассуждения
    
    // Цели и критерии
    "goal": "Решить задачу пользователя максимально эффективно",
    "success_criteria": "Пользователь получил полный и точный ответ",
    "expected_output": "Структурированный ответ с объяснением",
    
    // Отдельная модель для рассуждений (опционально)
    "reasoning_model": "reasoning-model-v1", // ID из ModelRegistry
    
    // Отдельный агент для рассуждений (опционально)
    "reasoning_agent": "expert-reasoner", // ID из AgentRegistry
    
    // Дополнительные параметры
    "reasoning_prompt": "Думай пошагово и объясняй свои действия",
    "reasoning_instructions": [
      "Разбей задачу на подзадачи",
      "Проанализируй каждый шаг",
      "Сделай обоснованный вывод"
    ],
    "stream_reasoning": true,          // Показывать рассуждения в реальном времени
    "save_reasoning_steps": true,      // Сохранять шаги рассуждения
    "show_full_reasoning": false       // Показывать полное рассуждение в ответе
  },
  

  
  // ===== ⚙️ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ =====
  "settings": {
    // === Системные сообщения ===
    "introduction": "Привет! Я ваш AI-ассистент. Готов помочь с любыми задачами!",
    "system_message": "Ты эксперт в области данных и аналитики",
    "system_message_role": "system",
    "create_default_system_message": true,
    
    // === Пользовательские сообщения ===
    "user_message_role": "user",
    "create_default_user_message": true,
    "add_messages": [
      {
        "role": "assistant",
        "content": "Какую задачу будем решать сегодня?"
      }
    ],
    
    // === Контекст и состояние ===
    "context": {
      "company": "TechCorp",
      "department": "Analytics",
      "access_level": "senior"
    },
    "add_context": true,               // Добавлять контекст к сообщениям
    "resolve_context": true,           // Выполнять функции в контексте
    "additional_context": "Пользователь работает в аналитическом отделе",
    "add_state_in_messages": true,     // Включать состояние в сообщения
    
    // === История диалогов ===
    "add_history_to_messages": true,   // Включать историю в контекст
    "num_history_runs": 5,             // Количество предыдущих запусков
    "search_previous_sessions_history": true, // Поиск по предыдущим сессиям
    "num_history_sessions": 3,         // Количество предыдущих сессий
    "read_chat_history": true,         // Инструмент чтения истории
    "read_tool_call_history": true,    // Инструмент истории вызовов
    
    // === Форматирование и вывод ===
    "markdown": true,                  // Форматировать ответы как Markdown
    "add_name_to_instructions": true,  // Добавлять имя агента в инструкции
    "add_datetime_to_instructions": true, // Добавлять дату/время
    "add_location_to_instructions": false, // Добавлять геолокацию
    "timezone_identifier": "Europe/Moscow", // Временная зона
    
    // === Потоковая передача ===
    "stream": true,                    // Потоковая передача ответов
    "stream_intermediate_steps": true, // Стримить промежуточные шаги
    
    // === Структурированные ответы ===
    "response_model": {                // Pydantic модель для ответа
      "type": "object",
      "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number"},
        "sources": {"type": "array"}
      }
    },
    "parse_response": true,            // Парсить ответ в модель
    "use_json_mode": false,            // Принуждать JSON ответы
    "parser_model": "parser-model-v1", // Отдельная модель для парсинга
    "parser_model_prompt": "Извлеки структурированные данные из ответа",
    
    // === Обработка ошибок ===
    "retries": 3,                      // Количество повторных попыток
    "delay_between_retries": 2,        // Задержка между попытками (сек)
    "exponential_backoff": true,       // Экспоненциальное увеличение задержки
    
    // === Отладка и мониторинг ===
    "debug_mode": false,               // Режим отладки
    "monitoring": true,                // Отправка метрик в agno.com
    "telemetry": true,                 // Анонимная телеметрия
    "store_events": true,              // Сохранять события выполнения
    "events_to_skip": ["ToolCallStarted"], // Пропускать определенные события
    

    
    // === Метаданные ===
    "config_version": "2.0",          // Версия конфигурации
    "tags": ["analytics", "production", "expert"], // Теги для поиска
    "app_id": "analytics-platform",   // ID приложения
    "extra_data": {                    // Дополнительные данные
      "created_by": "admin",
      "environment": "production",
      "feature_flags": {
        "experimental_reasoning": true,
        "enhanced_memory": true
      }
    }
  }
}
```

## 📝 Практические примеры по категориям

### 🔍 Агент для поиска и анализа

```json
{
  "name": "Аналитик-исследователь",
  "agent_id": "research-analyst-v1",
  "description": "Специализируется на поиске и анализе информации",
  "instructions": "Ищи информацию из надежных источников и делай обоснованные выводы",
  
  "model_configuration": {
    "id": "gpt-4.1",
    "temperature": 0.3,
    "max_tokens": 3000
  },
  
  "tools_config": {
    "dynamic_tools": ["duckduckgo-search", "yfinance-stocks"],
    "show_tool_calls": true
  },
  
  "memory_config": {
    "enable_user_memories": true,
    "memory_filters": {"topics": ["исследования", "анализ"]}
  },
  
  "reasoning_config": {
    "reasoning": true,
    "reasoning_max_steps": 5
  }
}
```

### 🛠️ Агент-разработчик

```json
{
  "name": "Помощник разработчика",
  "agent_id": "dev-assistant-v1", 
  "description": "Помогает с программированием и техническими задачами",
  "instructions": "Помогай с кодом, объясняй технические концепции, предлагай решения",
  
  "model_configuration": {
    "id": "claude-3-5-sonnet-20241022",
    "temperature": 0.1,
    "max_tokens": 4000
  },
  
  "tools_config": {
    "dynamic_tools": ["python-tools", "shell-tools", "file-tools"],
    "custom_tools": ["git-helper", "code-reviewer"]
  },
  
  "settings": {
    "markdown": true,
    "context": {"language": "python", "framework": "fastapi"}
  }
}
```

### 📊 Агент для работы с данными

```json
{
  "name": "Специалист по данным",
  "agent_id": "data-specialist-v1",
  "description": "Анализирует данные и создает отчеты",
  "instructions": "Анализируй данные, создавай визуализации, делай выводы",
  
  "model_configuration": {
    "id": "gpt-4.1",
    "temperature": 0.2
  },
  
  "tools_config": {
    "dynamic_tools": ["python-tools", "sql-tools"],
    "custom_tools": ["chart-generator", "report-builder"]
  },
  
  "knowledge_config": {
    "add_references": true,
    "knowledge_filters": {"document_type": ["data_guide", "analysis_template"]}
  }
}
```

## ⚠️ Важные замечания

### Статус реализации функций

- ✅ **Полностью работает**: `model_configuration`, `tools_config` (кроме `tool_hooks`), `storage_config`, `memory_config`, базовые `settings`
- 🟡 **Частично работает**: `knowledge_config` (RAG требует настройки), `reasoning_config` (базовый функционал)
- ❌ **В разработке**: `tool_hooks` (хуки инструментов)

### Рекомендации по использованию

1. **Начните с минимальной конфигурации** и постепенно добавляйте функции
2. **Всегда указывайте `model_configuration`** для контроля поведения модели
3. **Включайте `storage_config`** для сохранения истории диалогов
4. **Используйте `memory_config`** для персонализации взаимодействия
5. **Тестируйте конфигурации** на небольших задачах перед production

### Валидация конфигураций

Все конфигурации проходят валидацию через Pydantic модели:
- Проверка типов данных
- Валидация обязательных полей  
- Кросс-валидация зависимых параметров
- Проверка совместимости провайдеров моделей

Используйте эндпоинт `POST /agents/{agent_id}/validate` для проверки конфигурации перед созданием агента. 