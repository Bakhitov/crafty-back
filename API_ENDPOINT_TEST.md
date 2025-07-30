# 📚 **AGENT-API ДОКУМЕНТАЦИЯ ДЛЯ ФРОНТЕНДА**

Техническая документация REST API для интеграции с Agent-API проектом.

---

## 🌐 **БАЗОВАЯ ИНФОРМАЦИЯ**

**Base URL:** `http://localhost:8000/v1`  
**Content-Type:** `multipart/form-data` для запросов с файлами, `application/json` для остальных  
**Методы:** GET, POST, DELETE  

---

## 📋 **ПОЛНЫЙ СПИСОК ЭНДПОИНТОВ**

### **Health & System**
- `GET /health` - проверка состояния API

### **Agents**
- `GET /agents` - список всех агентов
- `POST /agents/{agent_id}/runs` - запуск агента
- `POST /agents/{agent_id}/runs/{run_id}/continue` - продолжение выполнения
- `GET /agents/{agent_id}/sessions` - список сессий агента
- `GET /agents/{agent_id}/sessions/{session_id}` - конкретная сессия
- `POST /agents/{agent_id}/sessions/{session_id}/rename` - переименование сессии
- `DELETE /agents/{agent_id}/sessions/{session_id}` - удаление сессии
- `GET /agents/{agent_id}/memories` - память агента
- `POST /agents/{agent_id}/knowledge/load` - загрузка базы знаний

### **Tools**
- `GET /tools` - список инструментов

### **Cache**
- `GET /cache/stats` - статистика кэша
- `POST /cache/invalidate` - инвалидация кэша
- `POST /cache/clear` - полная очистка кэша

---

## 🔍 **ДЕТАЛЬНОЕ ОПИСАНИЕ ЭНДПОИНТОВ**

### **1. Health Check**

```http
GET /v1/health
```

**Ответ:**
```json
{
  "status": "success"
}
```

**HTTP коды:** `200 OK`

---

### **2. Список агентов**

```http
GET /v1/agents
```

**Ответ:**
```json
[
  "web_agent",
  "agno_assist",
  "finance_agent",
  "custom_agent_1"
]
```

**HTTP коды:** `200 OK`

---

### **3. Запуск агента**

```http
POST /v1/agents/{agent_id}/runs
Content-Type: multipart/form-data
```

**Параметры формы:**
```
message: string (обязательно) - сообщение пользователя
stream: boolean (по умолчанию true) - потоковый ответ
model: string (по умолчанию "gpt-4.1-mini-2025-04-14") - модель
session_id: string (опционально) - ID сессии
user_id: string (опционально) - ID пользователя
files: File[] (опционально) - массив файлов
```

**Пример запроса:**
```javascript
const formData = new FormData();
formData.append('message', 'Привет! Как дела?');
formData.append('stream', 'true');
formData.append('model', 'gpt-4.1-mini-2025-04-14');
formData.append('session_id', 'session-123');
formData.append('user_id', 'user-456');
formData.append('files', fileInput.files[0]);

fetch('/v1/agents/web_agent/runs', {
  method: 'POST',
  body: formData
});
```

**Ответ (stream: false):**
```json
{
  "content": "Привет! У меня все отлично, спасибо!",
  "run_id": "run_abc123",
  "session_id": "session-123",
  "created_at": 1703123456,
  "images": [
    {
      "url": "/media/image123.jpg",
      "content_type": "image/jpeg",
      "name": "generated_image.jpg",
      "size": 245760
    }
  ],
  "metrics": {
    "input_tokens": 15,
    "output_tokens": 42,
    "total_cost": 0.0012
  }
}
```

**Ответ (stream: true):**
```
data: {"event": "RunStarted", "run_id": "run_abc123", "created_at": 1703123456}

data: {"event": "RunResponseContent", "content": "Привет! У меня все", "created_at": 1703123456}

data: {"event": "RunResponseContent", "content": " отлично, спасибо!", "created_at": 1703123456}

data: {"event": "ToolCallStarted", "tool_name": "duckduckgo_search", "created_at": 1703123456}

data: {"event": "ToolCallCompleted", "tool_name": "duckduckgo_search", "tool_output": {...}, "created_at": 1703123456}

data: {"event": "RunCompleted", "run_id": "run_abc123", "created_at": 1703123456}
```

**HTTP коды:** `200 OK`, `404 Not Found` (агент не найден)

---

### **4. Продолжение выполнения**

```http
POST /v1/agents/{agent_id}/runs/{run_id}/continue
Content-Type: multipart/form-data
```

**Параметры формы:**
```
tools: string (обязательно) - JSON строка с инструментами
session_id: string (опционально) - ID сессии
user_id: string (опционально) - ID пользователя
stream: boolean (по умолчанию true) - потоковый ответ
```

**Пример запроса:**
```javascript
const formData = new FormData();
formData.append('tools', '[]'); // или JSON с инструментами
formData.append('session_id', 'session-123');
formData.append('user_id', 'user-456');
formData.append('stream', 'true');

fetch('/v1/agents/web_agent/runs/run_abc123/continue', {
  method: 'POST',
  body: formData
});
```

**Ответ:** Аналогично запуску агента (стрим или полный ответ)

**HTTP коды:** `200 OK`, `404 Not Found` (run не найден), `400 Bad Request` (неверный JSON)

---

### **5. Список сессий агента**

```http
GET /v1/agents/{agent_id}/sessions?user_id=user-123
```

**Query параметры:**
- `user_id` (опционально) - фильтр по пользователю

**Ответ:**
```json
[
  {
    "session_id": "session-123",
    "session_name": "Диалог о погоде",
    "created_at": "2024-12-01T10:30:00Z",
    "title": "Session abc12345"
  },
  {
    "session_id": "session-456",
    "session_name": null,
    "created_at": "2024-12-01T11:15:00Z", 
    "title": "Session def67890"
  }
]
```

**HTTP коды:** `200 OK`, `404 Not Found` (агент не найден)

---

### **6. Конкретная сессия**

```http
GET /v1/agents/{agent_id}/sessions/{session_id}?user_id=user-123
```

**Query параметры:**
- `user_id` (опционально) - ID пользователя

**Ответ:**
```json
{
  "session_id": "session-123",
  "agent_id": "web_agent",
  "user_id": "user-123",
  "created_at": "2024-12-01T10:30:00Z",
  "updated_at": "2024-12-01T10:35:00Z",
  "session_data": {
    "session_name": "Диалог о погоде",
    "messages_count": 5
  },
  "runs": [
    {
      "run_id": "run_abc123",
      "created_at": "2024-12-01T10:30:00Z",
      "message": "Какая погода сегодня?",
      "response": "Сегодня солнечно, +20°C"
    }
  ]
}
```

**HTTP коды:** `200 OK`, `404 Not Found` (сессия не найдена)

---

### **7. Переименование сессии**

```http
POST /v1/agents/{agent_id}/sessions/{session_id}/rename
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "name": "Новое название сессии",
  "user_id": "user-123"
}
```

**Ответ:**
```json
{
  "message": "Successfully renamed session session-123"
}
```

**HTTP коды:** `200 OK`, `404 Not Found`, `500 Internal Server Error`

---

### **8. Удаление сессии**

```http
DELETE /v1/agents/{agent_id}/sessions/{session_id}?user_id=user-123
```

**Query параметры:**
- `user_id` (опционально) - ID пользователя

**Ответ:**
```json
{
  "message": "Successfully deleted session session-123"
}
```

**HTTP коды:** `200 OK`, `404 Not Found`, `500 Internal Server Error`

---

### **9. Память агента**

```http
GET /v1/agents/{agent_id}/memories?user_id=user-123
```

**Query параметры:**
- `user_id` (обязательно) - ID пользователя

**Ответ:**
```json
[
  {
    "memory": "Пользователь интересуется погодой и любит точные прогнозы",
    "topics": ["погода", "прогнозы", "температура"],
    "last_updated": "2024-12-01T10:35:00Z"
  },
  {
    "memory": "Предпочитает краткие ответы без лишних деталей",
    "topics": ["предпочтения", "стиль общения"],
    "last_updated": "2024-12-01T09:20:00Z"
  }
]
```

**HTTP коды:** `200 OK`, `404 Not Found` (агент без памяти), `422 Validation Error` (отсутствует user_id)

---

### **10. Загрузка базы знаний**

```http
POST /v1/agents/{agent_id}/knowledge/load
```

**Ответ:**
```json
{
  "message": "Knowledge base for agno_assist loaded successfully."
}
```

**HTTP коды:** `200 OK`, `400 Bad Request` (агент без базы знаний), `500 Internal Server Error`

---

### **11. Список инструментов**

```http
GET /v1/tools?type_filter=builtin&category=search&is_active=true
```

**Query параметры:**
- `type_filter` (опционально) - тип: `builtin`, `mcp`, `custom`
- `category` (опционально) - категория: `search`, `files`, `api`, etc.
- `is_active` (по умолчанию true) - только активные инструменты

**Ответ:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "duckduckgo_search",
    "type": "builtin",
    "description": "Поиск информации в интернете через DuckDuckGo",
    "display_name": "DuckDuckGo Search",
    "category": "search",
    "is_public": true,
    "is_active": true
  },
  {
    "id": "456e7890-e89b-12d3-a456-426614174001",
    "name": "file_processor",
    "type": "custom",
    "description": "Обработка и анализ загруженных файлов",
    "display_name": "File Processor",
    "category": "files",
    "is_public": false,
    "is_active": true
  }
]
```

**HTTP коды:** `200 OK`

---

### **12. Статистика кэша**

```http
GET /v1/cache/stats
```

**Ответ:**
```json
{
  "agents_cache": {
    "total": 5,
    "active": 3,
    "expired": 2,
    "ttl_seconds": 3600
  },
  "tools_cache": {
    "total": 12,
    "active": 10,
    "expired": 2,
    "ttl_seconds": 7200
  },
  "total_cached_objects": 17
}
```

**HTTP коды:** `200 OK`

---

### **13. Инвалидация кэша**

```http
POST /v1/cache/invalidate
Content-Type: application/json
```

**Тело запроса (один из вариантов):**
```json
{
  "agent_id": "custom_agent_1"
}
```
```json
{
  "user_id": "user-123"
}
```
```json
{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000"
}
```
```json
{
  "tool_ids": ["123e4567-e89b-12d3-a456-426614174000", "456e7890-e89b-12d3-a456-426614174001"]
}
```

**Ответ:**
```json
{
  "message": "Invalidated agent: custom_agent_1",
  "invalidated_count": 3,
  "type": "agent"
}
```

**HTTP коды:** `200 OK`, `400 Bad Request` (неверные параметры)

---

### **14. Полная очистка кэша**

```http
POST /v1/cache/clear
```

**Ответ:**
```json
{
  "message": "All caches cleared completely",
  "agents_cleared": 5,
  "tools_cleared": 12,
  "available_agents_cache_cleared": true,
  "total_cleared": 17
}
```

**HTTP коды:** `200 OK`

---

## 📊 **СТРУКТУРЫ ДАННЫХ**

### **StreamEvent (События стриминга)**

```typescript
interface StreamEvent {
  event: "RunStarted" | "RunResponseContent" | "RunCompleted" | 
         "ToolCallStarted" | "ToolCallCompleted" | "ReasoningStarted" | 
         "ReasoningStep" | "RunError";
  content?: string;
  agent_id?: string;
  run_id?: string;
  created_at: number;
  
  // Медиа контент
  images?: MediaItem[];
  videos?: MediaItem[];
  audio?: MediaItem[];
  response_audio?: string;
  
  // Инструменты
  tool_name?: string;
  tool_input?: any;
  tool_output?: any;
  
  // Ошибки
  error_type?: "NotFound" | "RuntimeError" | "General";
}
```

### **MediaItem**

```typescript
interface MediaItem {
  url?: string;          // URL для скачивания
  content?: string;      // Base64 контент
  content_type: string;  // MIME тип
  name?: string;         // Имя файла
  size?: number;         // Размер в байтах
}
```

### **Tool**

```typescript
interface Tool {
  id: string;
  name: string;
  type: "builtin" | "mcp" | "custom";
  description: string;
  display_name: string;
  category: string;
  is_public: boolean;
  is_active: boolean;
}
```

### **Session**

```typescript
interface Session {
  session_id: string;
  session_name?: string;
  created_at: string;
  title: string;
}
```

### **Memory**

```typescript
interface Memory {
  memory: string;
  topics: string[];
  last_updated?: string;
}
```

---

## 🔄 **ПОДДЕРЖИВАЕМЫЕ ФАЙЛЫ**

### **Изображения**
- JPEG, PNG, GIF, WebP
- Автоматическое распознавание содержимого

### **Документы**
- PDF - нативная обработка
- CSV - конвертация в текст
- TXT, JSON - прямая обработка

### **Аудио/Видео**
- MP3, WAV, MP4, MOV
- Транскрипция и анализ

---

## ❌ **КОДЫ ОШИБОК**

| Код | Описание | Примеры |
|-----|----------|---------|
| 200 | OK | Успешный запрос |
| 400 | Bad Request | Неверные параметры, невалидный JSON |
| 404 | Not Found | Агент/сессия/run не найдены |
| 422 | Validation Error | Отсутствует обязательный параметр |
| 500 | Internal Server Error | Внутренние ошибки сервера |
| 501 | Not Implemented | Функция не поддерживается агентом |

### **Формат ошибки**

```json
{
  "detail": "Agent not found",
  "status_code": 404
}
```

### **Ошибки в стриминге**

```json
{
  "event": "RunError",
  "content": "Continue run failed: Run not found",
  "error_type": "NotFound",
  "created_at": 1703123456
}
```

---

## 🧪 **ПРИМЕРЫ ЗАПРОСОВ**

### **JavaScript/Fetch**

```javascript
// Простой запрос к агенту
const response = await fetch('/v1/agents/web_agent/runs', {
  method: 'POST',
  body: new FormData([
    ['message', 'Привет!'],
    ['stream', 'false']
  ])
});
const data = await response.json();

// Стриминг
const response = await fetch('/v1/agents/web_agent/runs', {
  method: 'POST',
  body: formData
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = new TextDecoder().decode(value);
  const events = chunk.split('\n').filter(Boolean);
  
  for (const event of events) {
    try {
      const data = JSON.parse(event);
      console.log('Event:', data.event, 'Content:', data.content);
    } catch (e) {
      // Игнорируем невалидный JSON
    }
  }
}
```

### **cURL**

```bash
# Простой запрос
curl -X POST "http://localhost:8000/v1/agents/web_agent/runs" \
  -F "message=Привет!" \
  -F "stream=false"

# С файлами
curl -X POST "http://localhost:8000/v1/agents/web_agent/runs" \
  -F "message=Проанализируй этот файл" \
  -F "files=@image.jpg" \
  -F "user_id=user-123" \
  -F "session_id=session-456"

# Получение сессий
curl "http://localhost:8000/v1/agents/web_agent/sessions?user_id=user-123"

# Инвалидация кэша
curl -X POST "http://localhost:8000/v1/cache/invalidate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "web_agent"}'
```

---

**📋 Данная документация содержит полное описание всех доступных эндпоинтов, форматов запросов и ответов для интеграции с Agent-API.** 