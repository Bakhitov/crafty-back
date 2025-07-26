# 📋 Руководство по API запросам для получения агентов и инструментов

## 🤖 **АГЕНТЫ**

### Базовые запросы

#### 1. **Получить список ID всех агентов**
```bash
GET /v1/agents
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents" \
  -H "Content-Type: application/json"
```

**Ответ:**
```json
[
  "demo-agent-123",
  "finance-agent-456", 
  "assistant-agent-789"
]
```

#### 2. **Получить подробную информацию о всех агентах**
```bash
GET /v1/agents/detailed
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents/detailed" \
  -H "Content-Type: application/json"
```

**Ответ:**
```json
[
  {
    "agent_id": "demo-agent-123",
    "name": "Демо Агент",
    "description": "Демонстрационный агент",
    "instructions": "Ты помощник...",
    "model_configuration": {
      "id": "gpt-4.1",
      "temperature": 0.7
    },
    "tools_config": {
      "tools": ["DuckDuckGoTools"],
      "show_tool_calls": true
    },
    "is_active": true,
    "is_active_api": true,
    "company_id": "company_123",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 3. **Получить конкретного агента**
```bash
GET /v1/agents/{agent_id}
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents/demo-agent-123" \
  -H "Content-Type: application/json"
```

#### 4. **🆕 Поиск агентов**
```bash
GET /v1/agents/search?query={query}&tags={tags}
```

**Параметры:**
- `query` - поисковый запрос (по имени, описанию, ID)
- `tags` - теги через запятую

**Примеры запросов:**
```bash
# Поиск по названию
curl -X GET "http://localhost:8000/v1/agents/search?query=финансовый" \
  -H "Content-Type: application/json"

# Поиск по тегам
curl -X GET "http://localhost:8000/v1/agents/search?tags=finance,assistant" \
  -H "Content-Type: application/json"

# Комбинированный поиск
curl -X GET "http://localhost:8000/v1/agents/search?query=помощник&tags=general" \
  -H "Content-Type: application/json"
```

#### 5. **🆕 Получить публичных агентов**
```bash
GET /v1/agents/public
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents/public" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает только агентов с `is_public=true`, доступных всем пользователям.

#### 6. **🆕 Получить агентов конкретной компании**
```bash
GET /v1/agents/company/{company_id}
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents/company/company_123" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает всех агентов (публичных и приватных) конкретной компании.

#### 7. **🆕 Получить доступных агентов для компании**
```bash
GET /v1/agents/company/{company_id}/accessible
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/agents/company/company_123/accessible" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает всех агентов, доступных для компании:
- Публичные агенты (`is_public=true`) - видны всем
- Приватные агенты своей компании (`is_public=false` AND `company_id=company_123`)

**💡 Примечание:** Доступность для запуска (`is_active_api`) проверяется автоматически при выполнении runs.

---

## 🔐 **ЛОГИКА ДОСТУПОВ К АГЕНТАМ**

### Поля управления доступом:

1. **`is_active`** - 🔧 **Техническое поле**
   - Включить/выключить агента в системе
   - Не показывается в API, используется только в БД
   - `false` = агент полностью скрыт

2. **`is_active_api`** - 🚀 **Доступ к запуску**
   - Разрешение на выполнение runs
   - Проверяется автоматически при запуске агента
   - `false` = агент виден, но не запускается

3. **`is_public`** - 👁️ **Видимость агента**
   - `true` = агент виден всем пользователям
   - `false` = агент виден только своей компании (`company_id`)

### Сценарии доступа:

```bash
# Сценарий 1: Получить всех агентов видимых компании
GET /v1/agents/company/my-company/accessible
# Результат: публичные + свои приватные агенты

# Сценарий 2: Получить только публичные агенты  
GET /v1/agents/public
# Результат: только is_public=true

# Сценарий 3: Запуск агента (автоматически проверяет is_active_api)
POST /v1/agents/agent-id/runs
# Система сама проверит доступность для запуска
```

### Матрица доступов:

| is_active | is_public | company_id | Видимость | Запуск |
|-----------|-----------|------------|-----------|---------|
| ❌ false  | any       | any        | Скрыт     | ❌      |
| ✅ true   | ✅ true   | any        | Всем      | Зависит от is_active_api |
| ✅ true   | ❌ false  | company_A  | Только company_A | Зависит от is_active_api |
| ✅ true   | ❌ false  | company_B  | Только company_B | Зависит от is_active_api |

---

## 🛠️ **ИНСТРУМЕНТЫ**

### Базовые запросы

#### 1. **Получить все динамические инструменты**
```bash
GET /v1/tools/
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/" \
  -H "Content-Type: application/json"
```

**Ответ:**
```json
{
  "tools": [
    {
      "id": 1,
      "tool_id": "duckduckgo_search",
      "name": "DuckDuckGo Search",
      "agno_class": "DuckDuckGoTools",
      "module_path": "agno.tools.duckduckgo",
      "description": "Поиск в интернете",
      "category": "search",
      "company_id": null,
      "is_public": true,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### 2. **🆕 Получить публичные инструменты**
```bash
GET /v1/tools/public
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/public" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает только инструменты с `is_public=true`, доступные всем пользователям.

#### 3. **🆕 Получить инструменты конкретной компании**
```bash
GET /v1/tools/company/{company_id}
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/company/company_123" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает все инструменты (публичные и приватные) конкретной компании.

#### 4. **🆕 Получить доступные инструменты для компании**
```bash
GET /v1/tools/company/{company_id}/accessible
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/company/company_123/accessible" \
  -H "Content-Type: application/json"
```

**Описание:** Возвращает все инструменты, доступные для компании:
- Публичные инструменты (`is_public=true`)
- Собственные приватные инструменты (`company_id=company_123`)

### Специализированные типы инструментов

#### 5. **Получить кастомные Python инструменты**
```bash
GET /v1/tools/custom
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/custom" \
  -H "Content-Type: application/json"
```

#### 6. **Получить MCP серверы**
```bash
GET /v1/tools/mcp
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/mcp" \
  -H "Content-Type: application/json"
```

#### 7. **Получить инструменты конкретного MCP сервера**
```bash
GET /v1/tools/mcp/{server_id}/tools
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/v1/tools/mcp/filesystem-server/tools" \
  -H "Content-Type: application/json"
```

---

## 🔍 **ЛОГИКА ДОСТУПА К ИНСТРУМЕНТАМ**

### Типы инструментов по доступности:

1. **🌍 Публичные** (`is_public=true`)
   - Доступны всем пользователям
   - Не привязаны к конкретной компании
   - Пример: общие поисковые инструменты

2. **🔒 Приватные** (`is_public=false`)
   - Доступны только своей компании
   - Привязаны к `company_id`
   - Пример: внутренние корпоративные инструменты

3. **🏢 Корпоративные**
   - Компания видит: свои приватные + все публичные
   - Используйте эндпоинт `/company/{company_id}/accessible`

### Примеры сценариев:

```bash
# Сценарий 1: Получить все доступные инструменты для компании
curl -X GET "http://localhost:8000/v1/tools/company/my-company/accessible"

# Сценарий 2: Получить только публичные инструменты (для неавторизованных)
curl -X GET "http://localhost:8000/v1/tools/public"

# Сценарий 3: Получить все инструменты администратором
curl -X GET "http://localhost:8000/v1/tools/"
```

---

## 📊 **МЕТА-ИНФОРМАЦИЯ**

### Получить поддерживаемые модели
```bash
GET /v1/agents/meta/models
```

### Получить поддерживаемые инструменты
```bash
GET /v1/agents/meta/tools
```

---

## 🔧 **ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ В КОДЕ**

### Python с requests:
```python
import requests

# Получить всех агентов
agents = requests.get("http://localhost:8000/v1/agents/detailed").json()

# Получить доступные инструменты для компании
tools = requests.get("http://localhost:8000/v1/tools/company/my-company/accessible").json()

# Поиск агентов
search_results = requests.get(
    "http://localhost:8000/v1/agents/search", 
    params={"query": "финансовый", "tags": "finance"}
).json()
```

### JavaScript/TypeScript:
```javascript
// Получить всех агентов
const agents = await fetch('/v1/agents/detailed').then(r => r.json());

// Получить публичные инструменты
const publicTools = await fetch('/v1/tools/public').then(r => r.json());

// Поиск агентов
const searchParams = new URLSearchParams({
  query: 'помощник',
  tags: 'general,assistant'
});
const searchResults = await fetch(`/v1/agents/search?${searchParams}`)
  .then(r => r.json());
```

---

## ✅ **Новые возможности**

🆕 **Добавлено в последнем обновлении:**
- Фильтрация инструментов по компаниям
- Поддержка публичных/приватных инструментов
- Поиск агентов по запросу и тегам
- Эндпоинты для получения доступных инструментов

🎯 **Все эндпоинты готовы к использованию и следуют принципам REST API!** 