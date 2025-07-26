# Конфигурация агента

Agent Parameters
| Параметр                           | Тип                                    | Значение по умолчанию | Описание                                            |
| ---------------------------------- | ------------------------------- | --------------------- | --------------------------------------------------- |
| `model`                            | Optional\[Model]                       | None                  | Модель ИИ, используемая агентом для генерации ответов. Определяет провайдера (OpenAI, Anthropic и др.) и конкретную модель (✅ Проверено)          |

| `name`                             | Optional\[str]                         | None                  | Уникальное имя агента для идентификации в логах и UI. Автогенерируется если не указано (✅ Проверено: прямое, `dynamic_agent.name` -> `agno.Agent`)                               |

| `agent_id`                         | Optional\[str]                         | None                  | UUID агента для уникальной идентификации. Автогенерируется если не указан (✅ Проверено: прямое, `dynamic_agent.agent_id` -> `agno.Agent`)                                |

| `agent_data`                       | Optional\[Dict\[str, Any]]             | None                  | Метаданные агента для хранения дополнительной информации (версия, теги и др.) (❌ Не используется. Аналог `extra_data` в проекте, но в `agno` не передается) |

| `introduction`                     | Optional\[str]                         | None                  | Приветственное сообщение, добавляемое в начало каждого нового чата для установления контекста (✅ Проверено: через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `user_id`                          | Optional\[str]                         | None                  | Идентификатор пользователя для персонализации и разделения сессий (✅ Проверено: прямое, из API-запроса в `run` или из `settings` в `agno.Agent`) |

| `user_data`                        | Optional\[Dict\[str, Any]]             | None                  | Метаданные пользователя (имя, предпочтения, роль) для персонализации взаимодействия (✅ Проверено: непрямое, через `memory_config` -> `agno.memory.Memory`) |

| `session_id`                       | Optional\[str]                         | None                  | UUID сессии для группировки сообщений в рамках одного диалога. Автогенерируется если не указан (✅ Проверено: прямое, из API-запроса в `run` или из `settings` в `agno.Agent`) |

| `session_name`                     | Optional\[str]                         | None                  | Человекочитаемое название сессии для удобной навигации в истории (✅ Проверено: непрямое, через `settings` и `agno.rename_session()`) |

| `session_state`                    | Optional\[Dict\[str, Any]]             | None                  | Состояние сессии (переменные, контекст), сохраняемое между запусками агента (✅ Проверено: непрямое, через `settings` -> `storage` в `agno`) |

| `context`                          | Optional\[Dict\[str, Any]]             | None                  | Контекстные данные, доступные инструментам и функциям промптов (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `add_context`                      | bool                                   | False                 | Добавлять ли контекст к сообщению пользователя для передачи модели (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `resolve_context`                  | bool                                   | True                  | Выполнять ли функции в контексте перед запуском агента (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `memory`                           | Optional\[Memory]                      | None                  | Система долгосрочной памяти агента для запоминания фактов о пользователе и контексте (✅ Проверено: прямое, через `memory_config` -> `agno.memory.Memory` -> `agno.Agent`) |

| `add_history_to_messages`          | bool                                   | False                 | Включать ли историю предыдущих сообщений в контекст для модели (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `num_history_runs`                 | int                                    | 3                     | Количество предыдущих запусков агента, включаемых в контекст (влияет на память модели) (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `search_previous_sessions_history` | bool                                   | False                 | Поиск по истории предыдущих сессий для получения релевантного контекста (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `num_history_sessions`             | int                                    | 2                     | Количество предыдущих сессий для включения в поиск истории (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `knowledge`                        | Optional\[AgentKnowledge]              | None                  | База знаний агента с документами и фактами для RAG (Retrieval-Augmented Generation) (✅ Проверено: прямое, через `knowledge_config` -> `agno.knowledge.AgentKnowledge` -> `agno.Agent`) |

| `knowledge_filters`                | Optional\[Dict\[str, Any]]       | None        | Фильтры для ограничения поиска в базе знаний по метаданным документов (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `enable_agentic_knowledge_filters` | bool                                   | False                 | Разрешить агенту самостоятельно выбирать фильтры для поиска в базе знаний (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `add_references`                   | bool                                   | False                 | Включить RAG - добавление релевантных документов из базы знаний к промпту (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `retriever`                        | Optional\[Callable\[..., List\[Dict]]] | None                  | Кастомная функция для получения релевантных документов из внешних источников (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `references_format`                | "json" / "yaml"                        | `"json"`              | Формат представления ссылок из базы знаний в промпте (JSON или YAML) (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `storage`                          | Optional\[AgentStorage]                | None                  | Система хранения для персистентности сессий, истории и состояния агента (✅ Проверено: прямое, через `storage_config` -> `agno.storage.agent.postgres.PostgresAgentStorage` -> `agno.Agent`) |

| `extra_data`                       | Optional\[Dict\[str, Any]]             | None                  | Дополнительные данные агента (конфигурация, метрики) не передаваемые в модель (⚠️ Частично: можно задать в `settings`, но в `agno.Agent` не передается) |

| `tools`                            | Optional\[List\[Tool]]                 | None                  | Список инструментов (функций), доступных агенту для выполнения действий (✅ Проверено: прямое, через `tools_config` -> `agno.Agent`) |

| `show_tool_calls`                  | bool                                   | False                 | Показывать ли детали вызовов инструментов в ответе агента для отладки (✅ Проверено: прямое, через `tools_config` -> `agno.Agent`) |

| `tool_call_limit`                  | Optional\[int]                         | None                  | Максимальное количество вызовов инструментов за один запуск для предотвращения зацикливания (✅ Проверено: прямое, через `tools_config` -> `agno.Agent`) |

| `tool_choice`                      | Optional\[str \| Dict]                 | None                  | Управление выбором инструментов: "auto", "none", или принудительный выбор конкретного инструмента (✅ Проверено: прямое, через `tools_config` -> `agno.Agent`) |
| `reasoning`                        | bool                                   | False                 | Включить пошаговое рассуждение для решения сложных задач (chain-of-thought) (✅ Проверено: прямое, через `reasoning_config` -> `agno.Agent`) |

| `reasoning_model`                  | Optional\[Model]                       | None                  | Отдельная модель для этапа рассуждения (если отличается от основной) (✅ Проверено: через ModelRegistry) |

| `reasoning_agent`                  | Optional\[Agent]                       | None                  | Отдельный агент для выполнения этапа рассуждения (✅ Проверено: через AgentRegistry) |
| `reasoning_min_steps`              | int                                    | 1                     | Минимальное количество шагов рассуждения перед генерацией ответа (✅ Проверено: прямое, через `reasoning_config` -> `agno.Agent`) |

| `reasoning_max_steps`              | int                                    | 10                    | Максимальное количество шагов рассуждения для предотвращения бесконечных циклов (✅ Проверено: прямое, через `reasoning_config` -> `agno.Agent`) |

| `read_chat_history`                | bool                                   | False                 | Добавить инструмент для чтения истории чата (позволяет агенту анализировать предыдущие сообщения) (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `search_knowledge`                 | bool                                   | True                  | Добавить инструмент поиска по базе знаний (позволяет агенту искать информацию) (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `update_knowledge`                 | bool                                   | False                 | Добавить инструмент обновления базы знаний (позволяет агенту сохранять новую информацию) (✅ Проверено: прямое, через `knowledge_config` -> `agno.Agent`) |

| `read_tool_call_history`           | bool                                   | False                 | Добавить инструмент просмотра истории вызовов инструментов для анализа действий (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `system_message`                   | str / Callable / Message               | None                  | Кастомное системное сообщение, переопределяющее автогенерируемый промпт (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `system_message_role`              | str                                    | `"system"`            | Роль для системного сообщения в диалоге с моделью (system/user/assistant) (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `create_default_system_message`    | bool                                   | True                  | Автоматически создавать системное сообщение на основе описания и инструкций (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `description`                      | Optional\[str]                         | None                  | Описание назначения и возможностей агента для системного промпта (✅ Проверено: прямое, из колонки `description` -> `agno.Agent`) |

| `goal`                             | Optional\[str]                         | None                  | Основная цель или задача агента для фокусировки поведения (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `success_criteria`                 | Optional\[str]                         | None                  | Критерии успешного выполнения задачи агентом (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `instructions`                     | str / List\[str] / Callable            | None                  | Подробные инструкции по поведению агента, добавляемые в системный промпт (✅ Проверено: прямое, из колонки `instructions` -> `agno.Agent`) |

| `expected_output`                  | Optional\[str]                         | None                  | Описание ожидаемого формата и содержания ответа агента (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `additional_context`               | Optional\[str]                         | None                  | Дополнительный контекст, добавляемый в конец системного сообщения (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `markdown`                         | bool                                   | False                 | Форматировать ответы агента в Markdown для улучшения читаемости (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `add_name_to_instructions`         | bool                                   | False                 | Добавлять имя агента в инструкции для самоидентификации (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `add_datetime_to_instructions`     | bool                                   | False                 | Добавлять текущую дату и время в системное сообщение для временного контекста (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `add_location_to_instructions`     | bool                                   | False                 | Добавлять информацию о местоположении в системное сообщение (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `add_state_in_messages`            | bool                                   | False                 | Включать переменные состояния сессии в сообщения для модели (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `add_messages`                     | Optional\[List\[Dict \| Message]]      | None                  | Дополнительные сообщения, добавляемые после системного сообщения (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |

| `user_message`                     | str / Dict / List / Callable           | None                  | Кастомное сообщение пользователя или функция для его генерации (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `user_message_role`                | str                                    | `"user"`              | Роль для сообщения пользователя в диалоге (обычно "user") (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `create_default_user_message`      | bool                                   | True                  | Создавать ли сообщение пользователя по умолчанию если не предоставлено (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `retries`                          | int                                    | 0                     | Количество повторных попыток при ошибках модели или API (⚠️  Частично: `ModelConfig.max_retries` -> `agno.Model`) |

| `delay_between_retries`            | int                                    | 1                     | Задержка в секундах между повторными попытками (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `exponential_backoff`              | bool                                   | False                 | Экспоненциальное увеличение задержки при повторных ошибках (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `response_model`                   | Optional\[BaseModel]                   | None                  | Pydantic модель для структурированного ответа агента (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `parse_response`                   | bool                                   | True                  | Автоматически преобразовывать ответ в заданную модель (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `use_json_mode`                    | bool                                   | False                 | Принуждать модель к ответу в JSON формате (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `parser_model`                     | Optional\[Model]                       | None                  | Отдельная модель для парсинга и валидации ответов (❌ Не используется) |
| `parser_model_prompt`              | Optional\[str]                         | None                  | Промпт для модели-парсера (✅ Проверено: прямое, через `settings` -> `AgnoAgentSettings` -> `agno.Agent`) |
| `save_response_to_file`            | Optional\[str]                         | None                  | Путь к файлу для сохранения ответов агента (❌ Не используется) |
| `stream`                           | Optional\[bool]                        | None                  | Потоковая передача ответа для реального времени (✅ Проверено: прямое, через API-запрос -> `run(stream=...)`) |

| `stream_intermediate_steps`        | bool                                   | False                 | Потоковая передача промежуточных шагов (рассуждения, вызовы инструментов) (✅ Проверено: прямое, через `acontinue_run`) |

| `store_events`                     | bool                                   | False                 | Сохранение событий выполнения для анализа и отладки (⚠️  Частично: через `storage_config`, но не `settings`) |

| `events_to_skip`                   | Optional\[List\[RunEvent]]             | None                  | Типы событий, которые не следует сохранять (для оптимизации) (❌ Не используется) |


| `team`                             | Optional\[List\[Agent]]                | None                  | Команда агентов для совместного решения задач (❌ Не используется динамически, только статический пример) |

| `team_data`                        | Optional\[Dict\[str, Any]]             | None                  | Общие данные, разделяемые между участниками команды (❌ Не используется) |

| `role`                             | Optional\[str]                         | None                  | Роль агента в команде (лидер, исполнитель, аналитик) (❌ Не используется динамически) |

| `respond_directly`                 | bool                                   | False                 | Отвечать напрямую пользователю без перенаправления (❌ Не используется динамически) |

| `add_transfer_instructions`        | bool                                   | True                  | Добавлять инструкции по передаче задач между агентами команды (❌ Не используется динамически) |

| `team_response_separator`          | str                                    | `"\n"`                | Разделитель между ответами разных агентов команды (❌ Не используется динамически) |

| `debug_mode`                       | bool                                   | False                 | Включить детальное логирование для отладки поведения агента (✅ Проверено: прямое, через `settings` -> `agno.Agent`) |

| `monitoring`                       | bool                                   | False                 | Отправка логов и метрик в agno.com для мониторинга (❌ Не используется) |
| `telemetry`                        | bool                                   | True                  | Минимальное анонимное логирование для аналитики (❌ Не используется) |


AgentSession
| Параметр          | Тип                        | Значение по умолчанию | Описание                          | Статус реализации |
| ----------------- | -------------------------- | --------------------- | --------------------------------- | ----------------- |
| `session_id`      | `str`                      | Обязательный          | UUID сессии для уникальной идентификации диалога | ✅ Проверено: прямое, используется в `agno.storage` |
| `agent_id`        | `Optional[str]`            | None                  | Идентификатор агента, связанного с данной сессией | ✅ Проверено: прямое, используется в `agno.storage` |
| `user_id`         | `Optional[str]`            | None                  | Идентификатор пользователя для персонализации | ✅ Проверено: прямое, используется в `agno.storage` |
| `team_session_id` | `Optional[str]`            | None                  | Идентификатор командной сессии (для мультиагентных систем) | ✅ Проверено: прямое, используется в `agno.storage` |
| `memory`          | `Optional[Dict[str, Any]]` | None                  | Долгосрочная память агента о пользователе и контексте | ✅ Проверено: прямое, используется в `agno.storage` |
| `agent_data`      | `Optional[Dict[str, Any]]` | None                  | Метаданные агента: ID, имя, модель для быстрого доступа | ✅ Проверено: прямое, используется в `agno.storage` |
| `session_data`    | `Optional[Dict[str, Any]]` | None                  | Данные сессии: имя, состояние, загруженные файлы (изображения, видео, аудио) | ✅ Проверено: прямое, используется в `agno.storage` |
| `extra_data`      | `Optional[Dict[str, Any]]` | None                  | Дополнительные данные для расширения функциональности | ✅ Проверено: прямое, используется в `agno.storage` |
| `created_at`      | `Optional[int]`            | None                  | Unix timestamp создания сессии | ✅ Проверено: прямое, используется в `agno.storage` |
| `updated_at`      | `Optional[int]`            | None                  | Unix timestamp последнего обновления сессии | ✅ Проверено: прямое, используется в `agno.storage` |

ModelConfig
| Параметр                      | Тип                  | Описание                                  | Статус реализации                                        |
| ----------------------------- | -------------------- | ----------------------------------------- | -------------------------------------------------------- |
| `id`                          | `Optional[str]`      | ID модели                                 | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `name`                        | `Optional[str]`      | Имя модели                                | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `provider`                    | `Optional[str]`      | Провайдер модели                          | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `temperature`                 | `Optional[float]`    | Рандомизация вывода (0.0-2.0)             | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `max_tokens`                  | `Optional[int]`      | Максимальное количество токенов           | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `max_completion_tokens`       | `Optional[int]`      | Максимум токенов в completion             | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `top_p`                       | `Optional[float]`    | Nucleus sampling (0.0-1.0)                | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `frequency_penalty`           | `Optional[float]`    | Штраф за повторение токенов               | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `presence_penalty`            | `Optional[float]`    | Штраф за присутствие токенов              | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `stop`                        | `Union[str, List[str]]` | Стоп-секвенции                           | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `seed`                        | `Optional[int]`      | Сид для детерминизма                      | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `logit_bias`                  | `Optional[Dict]`     | Изменение вероятности токенов             | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `logprobs`                    | `Optional[bool]`     | Включить логарифмы вероятностей           | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `top_logprobs`                | `Optional[int]`      | Логпробы на токен                         | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `user`                        | `Optional[str]`      | ID конечного пользователя                 | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `store`                       | `Optional[bool]`     | Сохранять ли вывод запроса                | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `metadata`                    | `Optional[Dict]`     | Дополнительные метаданные                 | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `modalities`                  | `Optional[List[str]]`| Список поддерживаемых модальностей       | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `audio`                       | `Optional[Dict]`     | Параметры аудио                           | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `response_format`             | `Optional[Dict]`     | Формат ответа                             | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `reasoning_effort`            | `Optional[str]`      | Уровень усилий для рассуждения o3         | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `stop_sequences`              | `Optional[List[str]]`| Стоп-секвенции Claude                     | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `top_k`                       | `Optional[int]`      | Top-k sampling                            | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `api_key`                     | `Optional[str]`      | API ключ                                  | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `base_url`                    | `Optional[str]`      | Базовый URL запроса                       | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `timeout`                     | `Optional[float]`    | Таймаут запроса                           | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `max_retries`                 | `Optional[int]`      | Максимум повторов                         | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `extra_headers`               | `Optional[Dict]`     | Заголовки запроса                         | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |
| `client_params`               | `Optional[Dict]`     | Параметры клиента                         | ✅ Проверено: прямое, `ModelConfig` -> `agno.Model`         |

ToolsConfig
| Параметр                | Тип                          | Описание                                  | Статус реализации                                        |
| ----------------------- | ---------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| `tools`                 | `Optional[List[Dict]]`       | Список статических инструментов           | ✅ Проверено: прямое, `ToolsConfig` -> `agno.Agent`         |
| `show_tool_calls`       | `Optional[bool]`             | Показывать ли вызовы инструментов         | ✅ Проверено: прямое, `ToolsConfig` -> `agno.Agent`         |
| `tool_call_limit`       | `Optional[int]`              | Лимит вызовов инструментов                | ✅ Проверено: прямое, `ToolsConfig` -> `agno.Agent`         |
| `tool_choice`           | `Optional[Union[str, Dict]]` | Управление выбором инструмента            | ✅ Проверено: прямое, `ToolsConfig` -> `agno.Agent`         |
| `tool_hooks`            | `Optional[List[Dict]]`       | Хуки до/после вызова инструмента          | ✅ Проверено: через HookRegistry                         |
| `dynamic_tools`         | `Optional[List[str]]`        | Список ID динамических инструментов из БД | ✅ Проверено: непрямое, `ToolsConfig` -> `dynamic_tool_service` -> `agno.Agent` |
| `custom_tools`          | `Optional[List[str]]`        | Список ID кастомных Python инструментов   | ✅ Проверено: непрямое, `Tools_Config` -> `custom_tool_service` -> `agno.Agent` |
| `mcp_servers`           | `Optional[List[str]]`        | Список ID MCP серверов                    | ✅ Проверено: непрямое, `ToolsConfig` -> `mcp_service` -> `agno.Agent`      |
| `function_declarations` | `Optional[List[Dict]]`       | Объявления функций                        | ✅ Проверено: прямое, `ToolsConfig` -> `agno.Agent`         |

MemoryConfig
| Параметр                       | Тип                       | Описание                                  | Статус реализации                                        |
| ------------------------------ | ------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| `memory_type`                  | `Optional[str]`           | Тип памяти (поддерживается "postgres")    | ✅ Проверено: непрямое, используется для выбора `PostgresMemoryDb` |
| `enable_agentic_memory`        | `Optional[bool]`          | Агент управляет памятью                   | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent` (`memory` attr) |
| `enable_user_memories`         | `Optional[bool]`          | Сохранять память о пользователе           | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent`         |
| `add_memory_references`        | `Optional[bool]`          | Добавлять ссылки на память                | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent`         |
| `user_data`                    | `Optional[Dict]`          | Метаданные пользователя                   | ❌ Не используется                                       |
| `agent_data`                   | `Optional[Dict]`          | Метаданные агента                         | ❌ Не используется                                       |
| `enable_session_summaries`     | `Optional[bool]`          | Сохранять резюме сессии                   | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent` (строка 561)         |
| `add_session_summary_references` | `Optional[bool]`          | Добавлять ссылки на резюме                | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent` (строка 564)         |
| `memory_filters`               | `Optional[Dict]`          | Фильтры для памяти                        | ✅ Проверено: прямое, `MemoryConfig` -> `agno.Agent` (строка 567)         |
| `db_url`                       | `Optional[str]`           | URL базы данных для памяти                | ✅ Проверено: прямое, `MemoryConfig` -> `PostgresMemoryDb`  |
| `table_name`                   | `Optional[str]`           | Название таблицы памяти                   | ✅ Проверено: прямое, `MemoryConfig` -> `PostgresMemoryDb`  |
| `db_schema`                    | `Optional[str]`           | Схема базы данных                         | ✅ Проверено: прямое, `MemoryConfig` -> `PostgresMemoryDb`  |
| `auto_upgrade_schema`          | `Optional[bool]`          | Автоматическое обновление схемы           | ❌ Не используется                                       |
| `num_history_responses`        | `Optional[int]`           | Количество исторических ответов (deprecated) | ❌ Не используется                                       |

KnowledgeConfig
| Параметр                         | Тип                  | Описание                                  | Статус реализации                                          |
| -------------------------------- | -------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| `knowledge_filters`              | `Optional[Dict]`     | Фильтры для базы знаний                   | ✅ Проверено: прямое, `AgnoAgentSettings` -> `agno.Agent` (строка 1337)                                         |
| `enable_agentic_knowledge_filters` | `Optional[bool]`     | Агент может выбирать фильтры              | ✅ Проверено: прямое, `AgnoAgentSettings` -> `agno.Agent` (строка 1338)                                         |
| `add_references`                 | `Optional[bool]`     | Включить RAG                              | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `references_format`              | `Optional[str]`      | Формат ссылок                             | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `search_knowledge`               | `Optional[bool]`     | Включить поиск по базе знаний             | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `update_knowledge`               | `Optional[bool]`     | Разрешить обновление знаний               | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `retriever`                      | `Optional[Dict]`     | Функция для получения ссылок              | ❌ Не используется                                         |
| `knowledge_base`                 | `Optional[str]`      | ID базы знаний                            | ❌ Не используется                                         |
| `max_references`                 | `Optional[int]`      | Максимальное количество ссылок            | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `similarity_threshold`           | `Optional[float]`    | Порог схожести для поиска                 | ✅ Проверено: прямое, `KnowledgeConfig` -> `agno.Agent`      |
| `vector_db_url`                  | `Optional[str]`      | URL векторной базы данных                 | ❌ Не используется (для настройки, а не рантайма)           |
| `embedding_model`                | `Optional[str]`      | Модель для эмбеддингов                    | ❌ Не используется (для настройки, а не рантайма)           |
| `chunk_size`                     | `Optional[int]`      | Размер чанков для индексации              | ❌ Не используется (для настройки, а не рантайма)           |
| `chunk_overlap`                  | `Optional[int]`      | Перекрытие между чанками                  | ❌ Не используется (для настройки, а не рантайма)           |

StorageConfig
| Параметр       | Тип              | Описание                          | Статус реализации                                          |
| -------------- | ---------------- | --------------------------------- | ---------------------------------------------------------- |
| `storage_type` | `Optional[str]`  | Тип хранилища (поддерживается "postgres") | ✅ Проверено: непрямое, используется для выбора `PostgresAgentStorage` |
| `db_url`       | `Optional[str]`  | URL базы данных                   | ✅ Проверено: прямое, `StorageConfig` -> `PostgresAgentStorage` |
| `enabled`      | `Optional[bool]` | Включено ли хранилище             | ✅ Проверено: непрямое, используется для активации хранилища |
| `table_name`   | `Optional[str]`  | Название таблицы для сессий       | ✅ Проверено: прямое, `StorageConfig` -> `PostgresAgentStorage` |
| `db_schema`    | `Optional[str]`  | Схема базы данных                 | ✅ Проверено: прямое, `StorageConfig` -> `PostgresAgentStorage` |
| `store_events` | `Optional[bool]` | Сохранять события выполнения      | ❌ Не используется                                         |
| `extra_data`   | `Optional[Dict]` | Дополнительные данные             | ❌ Не используется                                         |

ReasoningConfig
| Параметр               | Тип                       | Описание                               | Статус реализации                                        |
| ---------------------- | ------------------------- | -------------------------------------- | -------------------------------------------------------- |
| `reasoning`            | `Optional[bool]`          | Включить пошаговое рассуждение         | ✅ Проверено: прямое, `ReasoningConfig` -> `agno.Agent`      |
| `reasoning_model`      | `Optional[ModelConfig]`   | Модель для reasoning                   | ❌ Не используется                                       |
| `reasoning_min_steps`  | `Optional[int]`           | Минимальное количество шагов           | ❌ Не используется                                       |
| `reasoning_max_steps`  | `Optional[int]`           | Максимальное количество шагов          | ✅ Проверено: прямое, `ReasoningConfig` -> `agno.Agent` (как `max_steps`) |
| `goal`                 | `Optional[str]`           | Цель задачи                            | ❌ Не используется                                       |
| `success_criteria`     | `Optional[str]`           | Критерии успешности                    | ❌ Не используется                                       |
| `expected_output`      | `Optional[str]`           | Ожидаемый результат                    | ❌ Не используется                                       |
| `reasoning_agent`      | `Optional[Dict]`          | Агент для reasoning                    | ❌ Не используется                                       |
| `reasoning_prompt`     | `Optional[str]`           | Промпт для reasoning                   | ❌ Не используется                                       |
| `reasoning_instructions` | `Optional[List[str]]`   | Инструкции для reasoning               | ❌ Не используется                                       |
| `stream_reasoning`     | `Optional[bool]`          | Стримить шаги рассуждения              | ❌ Не используется                                       |
| `save_reasoning_steps` | `Optional[bool]`          | Сохранять шаги рассуждения             | ❌ Не используется                                       |
| `show_full_reasoning`  | `Optional[bool]`          | Показывать полное рассуждение          | ❌ Не используется                                       |

TeamConfig
| Параметр                         | Тип                       | Описание                                  | Статус реализации |
| -------------------------------- | ------------------------- | ----------------------------------------- | ----------------- |
| `team_mode`                      | `Optional[str]`           | Режим работы команды                      | ❌ Не используется |
| `role`                           | `Optional[str]`           | Роль агента в команде                     | ❌ Не используется |
| `respond_directly`               | `Optional[bool]`          | Отвечать напрямую                         | ❌ Не используется |
| `add_transfer_instructions`      | `Optional[bool]`          | Добавить инструкции по передаче           | ❌ Не используется |
| `team_response_separator`        | `Optional[str]`           | Разделитель ответов команды               | ❌ Не используется |
| `workflow_id`                    | `Optional[str]`           | ID рабочего процесса                      | ❌ Не используется |
| `parent_team_id`                 | `Optional[str]`           | ID родительской команды                   | ❌ Не используется |
| `team_id`                        | `Optional[str]`           | UUID команды                              | ❌ Не используется |
| `team_session_id`                | `Optional[str]`           | ID сессии команды                         | ❌ Не используется |
| `team_session_state`             | `Optional[Dict]`          | Состояние сессии команды                  | ❌ Не используется |
| `members`                        | `Optional[List[Dict]]`    | Участники команды                         | ❌ Не используется |
| `add_member_tools_to_system_message` | `Optional[bool]`      | Добавить инструменты участников            | ❌ Не используется |
| `show_members_responses`         | `Optional[bool]`          | Показывать ответы участников             | ❌ Не используется |
| `stream_member_events`           | `Optional[bool]`          | Стриминг событий участников              | ❌ Не используется |
| `share_member_interactions`      | `Optional[bool]`          | Делиться логами участников               | ❌ Не используется |
| `get_member_information_tool`    | `Optional[bool]`          | Инструмент для получения инфо об участниках | ❌ Не используется |

AgentSettings
| Параметр                       | Тип                       | Описание                                  | Статус реализации                                        |
| ------------------------------ | ------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| `session_name`                 | `Optional[str]`           | Название сессии                           | ❌ Не используется                                       |
| `session_state`                | `Optional[Dict]`          | Состояние сессии                          | ❌ Не используется                                       |
| `extra_data`                   | `Optional[Dict]`          | Доп. данные агента                        | ❌ Не используется                                       |
| `system_prompt`                | `Optional[str]`           | Системный промпт                          | ❌ Не используется                                       |
| `instructions`                 | `Union[str, List[str]]`   | Инструкции                                | ❌ Не используется (передается из `DynamicAgent.instructions`) |
| `user_message`                 | `Optional[str]`           | Сообщение пользователя                    | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `user_message_role`            | `Optional[str]`           | Роль пользователя                         | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `create_default_user_message`  | `Optional[bool]`          | Создавать сообщение пользователя          | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `add_messages`                 | `Optional[List[Dict]]`    | Дополнительные сообщения                  | ❌ Не используется                                       |
| `context`                      | `Optional[Dict]`          | Контекст для инструментов                 | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `add_context`                  | `Optional[bool]`          | Добавлять контекст к сообщению            | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `resolve_context`              | `Optional[bool]`          | Выполнить функции в контексте             | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `additional_context`           | `Optional[str]`           | Дополнительный контекст                   | ❌ Не используется                                       |
| `add_state_in_messages`        | `Optional[bool]`          | Включить состояние в сообщения            | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `search_previous_sessions_history` | `Optional[bool]`      | Поиск по предыдущим сессиям               | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `num_history_sessions`         | `Optional[int]`           | Количество сессий в истории               | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `read_chat_history`            | `Optional[bool]`          | Инструмент чтения истории                 | ✅ Проверено: прямое, `AgentSettings` -> `agno.Agent`      |
| `read_tool_call_history`       | `Optional[bool]`          | Инструмент истории вызовов                | ❌ Не используется                                       |
| `add_name_to_instructions`     | `Optional[bool]`          | Добавить имя к инструкциям                | ❌ Не используется                                       |
| `add_location_to_instructions` | `Optional[bool]`          | Добавить локацию к системному сообщению   | ❌ Не используется                                       |
| `timezone_identifier`          | `Optional[str]`           | Идентификатор временной зоны              | ❌ Не используется                                       |
| `save_response_to_file`        | `Optional[str]`           | Сохранение ответа в файл                  | ❌ Не используется                                       |
| `stream_intermediate_steps`    | `Optional[bool]`          | Стримить промежуточные шаги               | ❌ Не используется                                       |
| `monitoring`                   | `Optional[bool]`          | Логирование в agno.com                    | ❌ Не используется                                       |
| `retries`                      | `Optional[int]`           | Количество попыток при ошибке             | ❌ Не используется (см. `ModelConfig.max_retries`)         |
| `delay_between_retries`        | `Optional[int]`           | Задержка между попытками                  | ❌ Не используется                                       |
| `exponential_backoff`          | `Optional[bool]`          | Удвоение задержки                         | ❌ Не используется                                       |
| `response_model`               | `Optional[Dict]`          | Модель ответа (BaseModel)                 | ❌ Не используется                                       |
| `parse_response`               | `Optional[bool]`          | Преобразовать ответ в модель              | ❌ Не используется                                       |
| `use_json_mode`                | `Optional[bool]`          | Ответ в JSON формате                      | ❌ Не используется                                       |
| `parser_model`                 | `Optional[Dict]`          | Модель для парсинга                       | ❌ Не используется                                       |
| `parser_model_prompt`          | `Optional[str]`           | Промпт для парсинга                       | ❌ Не используется                                       |
| `store_events`                 | `Optional[bool]`          | Сохранять события выполнения              | ❌ Не используется                                       |
| `events_to_skip`               | `Optional[List[str]]`     | Пропускать указанные события              | ❌ Не используется                                       |
| `team_data`                    | `Optional[Dict]`          | Общие данные команды                      | ❌ Не используется                                       |
| `team_session_id`              | `Optional[str]`           | ID командной сессии                       | ❌ Не используется                                       |
| `config_version`               | `Optional[str]`           | Версия конфигурации                       | ❌ Не используется (мета-поле)                           |
| `tags`                         | `Optional[List[str]]`     | Теги для поиска                           | ❌ Не используется (мета-поле)                           |
| `app_id`                       | `Optional[str]`           | ID приложения                             | ❌ Не используется (мета-поле)                           |

## Функции агента

### print_response
Запускает агента и выводит ответ в консоль. Синхронная функция для быстрого тестирования.

**Параметры:**
- `message` (Optional[Union[List, Dict, str, Message]]): Сообщение для отправки агенту
- `session_id` (Optional[str]): ID сессии для использования
- `user_id` (Optional[str]): ID пользователя
- `messages` (Optional[List[Union[Dict, Message]]]): Дополнительные сообщения
- `audio` (Optional[Sequence[Audio]]): Аудиофайлы для включения
- `images` (Optional[Sequence[Image]]): Изображения для включения  
- `videos` (Optional[Sequence[Video]]): Видеофайлы для включения
- `files` (Optional[Sequence[File]]): Файлы для включения
- `stream` (Optional[bool]): Использовать ли потоковую передачу
- `stream_intermediate_steps` (bool): Потоковая передача промежуточных шагов
- `markdown` (bool): Форматировать вывод как Markdown
- `show_message` (bool): Показывать ли сообщение
- `show_reasoning` (bool): Показывать ли рассуждения
- `show_full_reasoning` (bool): Показывать ли полные рассуждения
- `console` (Optional[Any]): Консоль для вывода
- `knowledge_filters` (Optional[Dict[str, Any]]): Фильтры для базы знаний

### run
Основная функция запуска агента. Возвращает ответ или поток событий.

**Параметры:**
- `message` (Optional[Union[str, List, Dict, Message]]): Сообщение для отправки агенту
- `stream` (Optional[bool]): Использовать ли потоковую передачу ответа
- `user_id` (Optional[str]): ID пользователя
- `session_id` (Optional[str]): ID сессии
- `audio` (Optional[Sequence[Audio]]): Аудиофайлы для включения
- `images` (Optional[Sequence[Image]]): Изображения для включения
- `videos` (Optional[Sequence[Video]]): Видеофайлы для включения
- `files` (Optional[Sequence[File]]): Файлы для включения
- `messages` (Optional[Sequence[Union[Dict, Message]]]): Дополнительные сообщения
- `stream_intermediate_steps` (Optional[bool]): Потоковая передача промежуточных шагов
- `retries` (Optional[int]): Количество повторных попыток
- `knowledge_filters` (Optional[Dict[str, Any]]): Фильтры для базы знаний

**Возвращает:**
Union[RunResponse, Iterator[RunResponseEvent]]: Ответ или итератор событий в зависимости от параметра stream

### aprint_response
Асинхронная версия print_response для использования в async/await контексте.

**Параметры:** (аналогичны print_response)

### arun
Асинхронная версия run для использования в async/await контексте.

**Параметры:** (аналогичны run)

**Возвращает:**
Union[RunResponse, AsyncIterator[RunResponseEvent]]: Ответ или асинхронный итератор событий

### continue_run
Продолжает выполнение прерванного запуска агента (например, после вызова инструментов).

**Параметры:**
- `run_response` (Optional[RunResponse]): Ответ запуска для продолжения
- `run_id` (Optional[str]): ID запуска для продолжения
- `updated_tools` (Optional[List[ToolExecution]]): Обновленные инструменты (требуется при продолжении по run_id)
- `stream` (Optional[bool]): Использовать ли потоковую передачу
- `stream_intermediate_steps` (Optional[bool]): Потоковая передача промежуточных шагов
- `user_id` (Optional[str]): ID пользователя
- `session_id` (Optional[str]): ID сессии
- `retries` (Optional[int]): Количество повторных попыток
- `knowledge_filters` (Optional[Dict[str, Any]]): Фильтры для базы знаний

**Возвращает:**
Union[RunResponse, Iterator[RunResponseEvent]]: Ответ или итератор событий

### acontinue_run
Асинхронная версия continue_run.

**Параметры:** (аналогичны continue_run)

**Возвращает:**
Union[RunResponse, AsyncIterator[RunResponseEvent]]: Ответ или асинхронный итератор событий

### get_session_summary
Получает резюме сессии для указанного ID сессии и пользователя.

**Параметры:**
- `session_id` (Optional[str]): ID сессии (если не указан, используется текущая сессия)
- `user_id` (Optional[str]): ID пользователя (если не указан, используется текущий пользователь)

**Возвращает:**
Optional[SessionSummary]: Резюме сессии

### get_user_memories
Получает воспоминания пользователя для указанного ID пользователя.

**Параметры:**
- `user_id` (Optional[str]): ID пользователя (если не указан, используется текущий пользователь)

**Возвращает:**
Optional[List[UserMemory]]: Список воспоминаний пользователя

### add_tool
Добавляет инструмент к агенту во время выполнения.

**Параметры:**
- `tool` (Union[Toolkit, Callable, Function, Dict]): Инструмент для добавления

### set_tools
Заменяет все инструменты агента на новый список.

**Параметры:**
- `tools` (List[Union[Toolkit, Callable, Function, Dict]]): Список инструментов для установки

## RunResponse - Атрибуты ответа агента

| Атрибут | Тип | Значение по умолчанию | Описание | Статус реализации |
| ------- | --- | -------------------- | -------- | ----------------- |
| `content` | Any | None | Основное содержимое ответа агента (текст, JSON, структурированные данные) | ✅ Проверено: возвращается в API ответах |
| `content_type` | str | "str" | Указывает тип данных содержимого (str, json, markdown) | ✅ Проверено: используется в ответах |
| `thinking` | str | None | Внутренние размышления модели (используется в моделях Anthropic для прозрачности) | ⚠️ Частично: поддерживается agno, но не обрабатывается в проекте |
| `reasoning_content` | str | None | Пошаговое рассуждение, выработанное моделью при включенном reasoning | ✅ Проверено: поддерживается через reasoning_config |
| `messages` | List[Message] | None | Полный список сообщений диалога, включенных в ответ | ✅ Проверено: возвращается в API |
| `metrics` | Dict[str, Any] | None | Метрики использования: токены, время выполнения, стоимость | ✅ Проверено: собираются и возвращаются |
| `model` | str | None | Название модели, использованной для генерации ответа | ✅ Проверено: возвращается в ответах |
| `model_provider` | str | None | Провайдер модели (OpenAI, Anthropic, Google и др.) | ✅ Проверено: определяется из model_config |
| `run_id` | str | None | Уникальный идентификатор запуска для отслеживания | ✅ Проверено: генерируется agno |
| `agent_id` | str | None | Идентификатор агента, сгенерировавшего ответ | ✅ Проверено: передается из dynamic_agent |
| `session_id` | str | None | Идентификатор сессии для группировки диалога | ✅ Проверено: используется для хранения |
| `tools` | List[Dict[str, Any]] | None | Список инструментов, доступных модели во время запуска | ✅ Проверено: формируется из tools_config |
| `images` | List[Image] | None | Изображения, созданные или обработанные моделью | ⚠️ Частично: поддерживается agno, обработка в разработке |
| `videos` | List[Video] | None | Видеофайлы, созданные или обработанные моделью | ⚠️ Частично: поддерживается agno, обработка в разработке |
| `audio` | List[Audio] | None | Аудиофрагменты, созданные или обработанные моделью | ⚠️ Частично: поддерживается agno, обработка в разработке |
| `response_audio` | ModelResponseAudio | None | Необработанный аудиоответ модели (для голосовых моделей) | ❌ Не используется: голосовые модели не подключены |
| `citations` | Citations | None | Цитаты и ссылки на источники, использованные в ответе | ✅ Проверено: поддерживается через knowledge_config |
| `created_at` | int | - | Unix timestamp создания ответа | ✅ Проверено: автоматически генерируется |
| `extra_data` | RunResponseExtraData | None | Дополнительные данные: references, add_messages, history, reasoning_steps | ✅ Проверено: расширяемая структура для метаданных |

## RunResponseEvent - События потоковой передачи

### Базовые атрибуты всех событий
Все события наследуют от `BaseAgentRunResponseEvent` и содержат:

| Атрибут | Тип | Значение по умолчанию | Описание | Статус реализации |
| ------- | --- | -------------------- | -------- | ----------------- |
| `created_at` | int | Текущая временная метка | Unix timestamp создания события | ✅ Проверено: генерируется для всех событий |
| `event` | str | Значение типа события | Тип события для обработки в клиенте | ✅ Проверено: используется для роутинга событий |
| `agent_id` | str | "" | Идентификатор агента, генерирующего событие | ✅ Проверено: передается из контекста |
| `run_id` | Optional[str] | None | Идентификатор текущего запуска | ✅ Проверено: используется для отслеживания |
| `session_id` | Optional[str] | None | Идентификатор текущей сессии | ✅ Проверено: передается из API |
| `content` | Optional[Any] | None | Для обратной совместимости | ✅ Проверено: поддерживается в потоковых ответах |

### RunResponseStartedEvent
Событие начала выполнения запроса.

| Атрибут | Тип | Значение по умолчанию | Описание |
| ------- | --- | -------------------- | -------- |
| `event` | str | "RunStarted" | Тип события |
| `model` | str | "" | Используемая модель |
| `model_provider` | str | "" | Провайдер модели |

### RunResponseContentEvent  
Событие получения части контента от модели.

| Атрибут | Тип | Значение по умолчанию | Описание |
| ------- | --- | -------------------- | -------- |
| `event` | str | "RunResponseContent" | Тип события |
| `content` | Optional[Any] | None | Частичное содержание ответа |
| `content_type` | str | "str" | Тип контента |
| `thinking` | Optional[str] | None | Внутренние мысли модели |
| `citations` | Optional[Citations] | None | Цитаты в этой части ответа |
| `response_audio` | Optional[AudioResponse] | None | Аудиоответ модели |
| `image` | Optional[ImageArtifact] | None | Изображение в ответе |
| `extra_data` | Optional[RunResponseExtraData] | None | Дополнительные данные |

### RunResponseCompletedEvent
Событие завершения генерации ответа.

| Атрибут | Тип | Значение по умолчанию | Описание |
| ------- | --- | -------------------- | -------- |
| `event` | str | "RunCompleted" | Тип события |
| `content` | Optional[Any] | None | Окончательное содержание ответа |
| `content_type` | str | "str" | Тип контента |
| `reasoning_content` | Optional[str] | None | Полное рассуждение |
| `thinking` | Optional[str] | None | Внутренние мысли модели |
| `citations` | Optional[Citations] | None | Все цитаты |
| `images` | Optional[List[ImageArtifact]] | None | Все изображения |
| `videos` | Optional[List[VideoArtifact]] | None | Все видео |
| `audio` | Optional[List[AudioArtifact]] | None | Все аудио |
| `response_audio` | Optional[AudioResponse] | None | Аудиоответ |
| `extra_data` | Optional[RunResponseExtraData] | None | Дополнительные данные |

### RunResponsePausedEvent
Событие приостановки выполнения (требуется подтверждение инструментов).

| Атрибут | Тип | Значение по умолчанию | Описание |
| ------- | --- | -------------------- | -------- |
| `event` | str | "RunPaused" | Тип события |
| `tools` | Optional[List[ToolExecution]] | None | Инструменты, требующие подтверждения |

### RunResponseContinuedEvent / RunResponseErrorEvent / RunResponseCancelledEvent

| Событие | Специальные атрибуты |
| ------- | -------------------- |
| `RunResponseContinuedEvent` | Событие продолжения выполнения |
| `RunResponseErrorEvent` | `content`: сообщение об ошибке |
| `RunResponseCancelledEvent` | `reason`: причина отмены |

### События Reasoning

| Событие | Атрибуты | Описание |
| ------- | -------- | -------- |
| `ReasoningStartedEvent` | `event`: "ReasoningStarted" | Начало процесса рассуждения |
| `ReasoningStepEvent` | `content`, `reasoning_content` | Шаг рассуждения |
| `ReasoningCompletedEvent` | `content` | Завершение рассуждения |

### События Tool Call

| Событие | Атрибуты | Описание |
| ------- | -------- | -------- |
| `ToolCallStartedEvent` | `tool`: ToolExecution | Начало вызова инструмента |
| `ToolCallCompletedEvent` | `tool`, `content`, `images`, `videos`, `audio` | Завершение вызова |

### События Memory

| Событие | Описание |
| ------- | -------- |
| `MemoryUpdateStartedEvent` | Начало обновления памяти |
| `MemoryUpdateCompletedEvent` | Завершение обновления памяти |

## Memory - Система памяти агента

Класс Memory управляет историей разговоров, резюме сессий и долгосрочной пользовательской памятью для агентов ИИ.

### Параметры Memory

| Параметр | Тип | Значение по умолчанию | Описание | Статус реализации |
| -------- | --- | -------------------- | -------- | ----------------- |
| `model` | Optional[Model] | None | Модель для обработки воспоминаний и создания резюме | ✅ Проверено: используется в memory_config |
| `memory_manager` | Optional[MemoryManager] | None | Менеджер операций с памятью | ✅ Проверено: настраивается в memory_config |
| `summarizer` | Optional[SessionSummarizer] | None | Создатель резюме сессий | ✅ Проверено: поддерживается через agno |
| `db` | Optional[MemoryDb] | None | База данных для хранения воспоминаний | ✅ Проверено: PostgresMemoryDb используется |
| `debug_mode` | bool | False | Включить отладочное логирование | ✅ Проверено: настраивается в конфигурации |

### Управление пользовательской памятью

| Метод | Описание | Параметры | Возвращает | Статус реализации |
| ----- | -------- | --------- | ---------- | ----------------- |
| `get_user_memories` | Получить все воспоминания пользователя | `user_id: str` | `List[UserMemory]` | ✅ Проверено: используется через agno.Agent |
| `get_user_memory` | Получить конкретное воспоминание | `user_id: str, memory_id: str` | `UserMemory` | ✅ Проверено: доступно через API |
| `add_user_memory` | Добавить новое воспоминание | `memory: UserMemory, user_id: Optional[str]` | `str` (ID памяти) | ✅ Проверено: автоматически при взаимодействии |
| `replace_user_memory` | Обновить существующее воспоминание | `memory_id: str, memory: UserMemory, user_id: Optional[str]` | `str` | ✅ Проверено: поддерживается agno |
| `delete_user_memory` | Удалить воспоминание | `user_id: str, memory_id: str` | `None` | ✅ Проверено: доступно через API |
| `create_user_memories` | Создать воспоминания из сообщений | `message: Optional[str], messages: Optional[List[Message]], user_id: Optional[str]` | `str` | ✅ Проверено: автоматически при включенной памяти |
| `acreate_user_memories` | Асинхронное создание воспоминаний | (аналогично create_user_memories) | `str` | ✅ Проверено: поддерживается в async режиме |
| `search_user_memories` | Поиск в памяти пользователя | `query: Optional[str], limit: Optional[int], retrieval_method: Optional[Literal["last_n", "first_n", "semantic"]], user_id: Optional[str]` | `List[UserMemory]` | ✅ Проверено: семантический поиск работает |

### Управление резюме сессий

| Метод | Описание | Параметры | Статус реализации |
| ----- | -------- | --------- | ----------------- |
| `get_session_summaries` | Получить все резюме сессий пользователя | `user_id: str` | ✅ Проверено: доступно через agno.Agent |
| `get_session_summary` | Получить резюме конкретной сессии | `user_id: str, session_id: str` | ✅ Проверено: используется в API |
| `create_session_summary` | Создать резюме для сессии | `session_id: str, user_id: Optional[str]` | ✅ Проверено: автоматически при настройке |
| `acreate_session_summary` | Асинхронное создание резюме | `session_id: str, user_id: Optional[str]` | ✅ Проверено: поддерживается |
| `delete_session_summary` | Удалить резюме сессии | `user_id: str, session_id: str` | ✅ Проверено: доступно через API |

### UserMemory - Структура воспоминания

| Параметр | Тип | Значение по умолчанию | Описание | Статус реализации |
| -------- | --- | -------------------- | -------- | ----------------- |
| `memory` | str | Обязательный | Фактическое содержание воспоминания | ✅ Проверено: основное поле памяти |
| `topics` | Optional[List[str]] | None | Темы или категории воспоминания | ✅ Проверено: используется для классификации |
| `input` | Optional[str] | None | Исходный ввод, породивший воспоминание | ✅ Проверено: сохраняется для контекста |
| `last_updated` | Optional[datetime] | None | Время последнего обновления | ✅ Проверено: автоматически обновляется |
| `memory_id` | Optional[str] | None | Уникальный идентификатор воспоминания | ✅ Проверено: генерируется автоматически |

### SessionSummary - Структура резюме сессии

| Параметр | Тип | Значение по умолчанию | Описание | Статус реализации |
| -------- | --- | -------------------- | -------- | ----------------- |
| `summary` | str | Обязательный | Краткое резюме сессии | ✅ Проверено: генерируется автоматически |
| `topics` | Optional[List[str]] | None | Темы, обсуждавшиеся в сессии | ✅ Проверено: извлекаются из диалога |
| `last_updated` | Optional[datetime] | None | Время последнего обновления резюме | ✅ Проверено: обновляется при изменениях |

### MemoryManager - Менеджер памяти

| Параметр | Тип | Значение по умолчанию | Описание | Статус реализации |
| -------- | --- | -------------------- | -------- | ----------------- |
| `model` | Optional[Model] | None | Модель для управления воспоминаниями | ✅ Проверено: используется отдельная модель |
| `system_message` | Optional[str] | None | Пользовательский системный промпт | ⚠️ Частично: настраивается в конфигурации |
| `additional_instructions` | Optional[str] | None | Дополнительные инструкции | ⚠️ Частично: расширяемая функциональность |

### SessionSummarizer - Создатель резюме

| Параметр | Тип | Значение по умолчанию | Описание | Статус реализации |
| -------- | --- | -------------------- | -------- | ----------------- |
| `model` | Optional[Model] | None | Модель для создания резюме сессий | ✅ Проверено: настраивается отдельно |
| `system_message` | Optional[str] | None | Пользовательский системный промпт | ⚠️ Частично: настраивается в конфигурации |
| `additional_instructions` | Optional[str] | None | Дополнительные инструкции | ⚠️ Частично: расширяемая функциональность |

## 🔗 Система реестров для сложных объектов

### Проблема сериализации сложных объектов

В Agno есть параметры, которые нельзя напрямую сохранить в JSON (базу данных):

| Параметр | Проблема | Решение |
| -------- | -------- | ------- |
| `tool_hooks: List[Callable]` | Функции нельзя сериализовать | ✅ **HookRegistry** - ссылки на функции |
| `reasoning_model: Model` | Объект модели слишком сложен | ✅ **ModelRegistry** - ссылки на модели |
| `reasoning_agent: Agent` | Циклическая зависимость агентов | ✅ **AgentRegistry** - ссылки на агентов |
| `parser_model: Model` | Объект модели слишком сложен | ✅ **ModelRegistry** - ссылки на модели |
| `team: List[Agent]` | Список агентов слишком сложен | ✅ **AgentRegistry** - ссылки на агентов |

### Обновленные статусы реализации

| Параметр | Старый статус | Новый статус |
| -------- | ------------- | ------------ |
| `tool_hooks` | ❌ Не используется | ✅ **Реализовано через HookRegistry** |
| `reasoning_model` | ❌ Не используется | ✅ **Реализовано через ModelRegistry** |
| `reasoning_agent` | ❌ Не используется | ✅ **Реализовано через AgentRegistry** |
| `parser_model` | ❌ Не используется | ✅ **Реализовано через ModelRegistry** |
| `team` | ❌ Не используется динамически | ✅ **Реализовано через AgentRegistry** |

### Использование реестров

#### 1. Создание записи в реестре
```python
# ModelRegistry - для reasoning_model, parser_model
{
  "registry_id": "gpt-4-reasoning",
  "name": "GPT-4 для рассуждений", 
  "model_config": {
    "id": "gpt-4.1",
    "temperature": 0.1,
    "max_tokens": 8000
  }
}

# AgentRegistry - для reasoning_agent, team
{
  "registry_id": "expert-agent-001",
  "name": "Экспертный агент",
  "agent_config": {
    "name": "Expert",
    "model": "gpt-4.1",
    "instructions": "Ты эксперт в анализе..."
  }
}

# HookRegistry - для tool_hooks
{
  "registry_id": "validation-hook",
  "name": "Валидация входных данных",
  "hook_type": "before_tool_call",
  "module_path": "my_hooks.validation",
  "function_name": "validate_input"
}
```

#### 2. Ссылка в конфигурации агента
```python
# Вместо объектов используем ID из реестров
reasoning_config = {
  "reasoning": True,
  "reasoning_model": "gpt-4-reasoning",    # Ссылка на ModelRegistry
  "reasoning_agent": "expert-agent-001"    # Ссылка на AgentRegistry
}

tools_config = {
  "tool_hooks": [
    {"hook_type": "before_tool_call", "registry_id": "validation-hook"}
  ]
}

team_config = {
  "team": ["expert-agent-001", "analyst-agent-002"]  # Ссылки на AgentRegistry
}
```

#### 3. Автоматическое разрешение во время выполнения
Система автоматически:
1. **Загружает** конфигурацию из реестра по ID
2. **Создает** экземпляр agno.Model/Agent/Callable 
3. **Передает** в agno.Agent для использования

### Таблицы реестров

| Таблица | Схема | Описание |
| ------- | ----- | -------- |
| `ai.model_registry` | ModelRegistry | Реестр моделей для переиспользования |
| `ai.agent_registry` | AgentRegistry | Реестр агентов для ссылок |
| `ai.hook_registry` | HookRegistry | Реестр хуков для tool_hooks |

### Преимущества системы реестров

1. ✅ **Сериализация** - все сохраняется в JSON (база данных)
2. ✅ **Переиспользование** - одну модель/агента можно использовать в разных местах
3. ✅ **Централизованное управление** - изменил в реестре, обновилось везде
4. ✅ **Динамическое обновление** - можно менять без перезапуска
5. ✅ **Соответствие принципам проекта** - все динамически из БД

### Миграция: 005_create_registries
```bash
cd db/migrations && alembic upgrade head
```
Создает таблицы `model_registry`, `agent_registry`, `hook_registry` в схеме `ai`.