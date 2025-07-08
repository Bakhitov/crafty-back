# Simple Agent API

Welcome to the Simple Agent API: a robust, production-ready application for serving Agents as an API. It includes:
  * A **FastAPI server** for handling API requests.
  * **PostgreSQL database support** for storing Agent sessions, knowledge, and memories.
  * A set of **pre-built Agents** to use as a starting point.

For more information, checkout [Agno](https://agno.link/gh) and give it a ⭐️

## Quickstart

Follow these steps to get your Agent API up and running:

> Prerequisites: 
> - [docker desktop](https://www.docker.com/products/docker-desktop) should be installed and running.
> - A PostgreSQL database (you can use the included example.env for Supabase configuration).

### Clone the repo

```sh
git clone https://github.com/agno-agi/agent-api.git
cd agent-api
```

### Configure environment variables

First, copy the example environment file and update it with your configuration:

```sh
cp example.env .env
```

Edit the `.env` file to set your API keys and database configuration:

```sh
# Required: OpenAI API key for GPT 4.1 model
export OPENAI_API_KEY="YOUR_API_KEY_HERE"

# Database configuration (example for Supabase is provided in example.env)
export DB_URL="postgresql://username:password@host:port/database"
export DB_SCHEME="ai"
```

> **Note**: 
> - You can use any model provider, just update the agents in the `/agents` folder.
> - The `example.env` file contains a sample Supabase database configuration.

### Start the application

Run the application using docker compose:

```sh
docker compose up -d
```

This command starts:
* The **FastAPI server**, running on [http://localhost:8000](http://localhost:8000).

Once started, you can:
* Test the API at [http://localhost:8000/docs](http://localhost:8000/docs).

### Connect to Agno Playground or Agent UI

* Open the [Agno Playground](https://app.agno.com/playground).
* Add `http://localhost:8000` as a new endpoint. You can name it `Agent API` (or any name you prefer).
* Select your newly added endpoint and start chatting with your Agents.

https://github.com/user-attachments/assets/a0078ade-9fb7-4a03-a124-d5abcca6b562

### Stop the application

When you're done, stop the application using:

```sh
docker compose down
```

## Prebuilt Agents

The `/agents` folder contains pre-built agents that you can use as a starting point.
- Web Search Agent: A simple agent that can search the web.
- Agno Assist: An Agent that can help answer questions about Agno.
  - Important: Make sure to load the `agno_assist` [knowledge base](http://localhost:8000/docs#/Agents/load_agent_knowledge_v1_agents__agent_id__knowledge_load_post) before using this agent.
- Finance Agent: An agent that uses the YFinance API to get stock prices and financial data.

## Development Setup

To setup your local virtual environment:

### Install `uv`

We use `uv` for python environment and package management. Install it by following the the [`uv` documentation](https://docs.astral.sh/uv/#getting-started) or use the command below for unix-like systems:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create Virtual Environment & Install Dependencies

Run the `dev_setup.sh` script. This will create a virtual environment and install project dependencies:

```sh
./scripts/dev_setup.sh
```

### Activate Virtual Environment

Activate the created virtual environment:

```sh
source .venv/bin/activate
```

(On Windows, the command might differ, e.g., `.venv\Scripts\activate`)

## Managing Python Dependencies

If you need to add or update python dependencies:

### Modify pyproject.toml

Add or update your desired Python package dependencies in the `[dependencies]` section of the `pyproject.toml` file.

### Generate requirements.txt

The `requirements.txt` file is used to build the application image. After modifying `pyproject.toml`, regenerate `requirements.txt` using:

```sh
./scripts/generate_requirements.sh
```

To upgrade all existing dependencies to their latest compatible versions, run:

```sh
./scripts/generate_requirements.sh upgrade
```

### Rebuild Docker Images

Rebuild your Docker images to include the updated dependencies:

```sh
docker compose up -d --build
```

## Community & Support

Need help, have a question, or want to connect with the community?

* 📚 **[Read the Agno Docs](https://docs.agno.com)** for more in-depth information.
* 💬 **Chat with us on [Discord](https://agno.link/discord)** for live discussions.
* ❓ **Ask a question on [Discourse](https://agno.link/community)** for community support.
* 🐛 **[Report an Issue](https://github.com/agno-agi/agent-api/issues)** on GitHub if you find a bug or have a feature request.

## Running in Production

This repository includes a `Dockerfile` for building a production-ready container image of the application.

The general process to run in production is:

1. Update the `scripts/build_image.sh` file and set your IMAGE_NAME and IMAGE_TAG variables.
2. Build and push the image to your container registry:

```sh
./scripts/build_image.sh
```
3. Run in your cloud provider of choice.

### Detailed Steps

1. **Configure for Production**
  * Ensure your production environment variables (e.g., `OPENAI_API_KEY`, database connection strings) are securely managed. Most cloud providers offer a way to set these as environment variables for your deployed service.
  * Review the agent configurations in the `/agents` directory and ensure they are set up for your production needs (e.g., correct model versions, any production-specific settings).

2. **Build Your Production Docker Image**
  * Update the `scripts/build_image.sh` script to set your desired `IMAGE_NAME` and `IMAGE_TAG` (e.g., `your-repo/agent-api:v1.0.0`).
  * Run the script to build and push the image:

    ```sh
    ./scripts/build_image.sh
    ```

3. **Deploy to a Cloud Service**
  With your image in a registry, you can deploy it to various cloud services that support containerized applications. Some common options include:

  * **Serverless Container Platforms**:
    * **Google Cloud Run**: A fully managed platform that automatically scales your stateless containers. Ideal for HTTP-driven applications.
    * **AWS App Runner**: Similar to Cloud Run, AWS App Runner makes it easy to deploy containerized web applications and APIs at scale.
    * **Azure Container Apps**: Build and deploy modern apps and microservices using serverless containers.

  * **Container Orchestration Services**:
    * **Amazon Elastic Container Service (ECS)**: A highly scalable, high-performance container orchestration service that supports Docker containers. Often used with AWS Fargate for serverless compute or EC2 instances for more control.
    * **Google Kubernetes Engine (GKE)**: A managed Kubernetes service for deploying, managing, and scaling containerized applications using Google infrastructure.
    * **Azure Kubernetes Service (AKS)**: A managed Kubernetes service for deploying and managing containerized applications in Azure.

  * **Platform as a Service (PaaS) with Docker Support**
    * **Railway.app**: Offers a simple way to deploy applications from a Dockerfile. It handles infrastructure, scaling, and networking.
    * **Render**: Another platform that simplifies deploying Docker containers, databases, and static sites.
    * **Heroku**: While traditionally known for buildpacks, Heroku also supports deploying Docker containers.

  * **Specialized Platforms**:
    * **Modal**: A platform designed for running Python code (including web servers like FastAPI) in the cloud, often with a focus on batch jobs, scheduled functions, and model inference, but can also serve web endpoints.

  The specific deployment steps will vary depending on the chosen provider. Generally, you'll point the service to your container image in the registry and configure aspects like port mapping (the application runs on port 8000 by default inside the container), environment variables, scaling parameters, and any necessary database connections.

4. **Database Configuration**
  * This application requires an external PostgreSQL database. For production, use a managed database service provided by your cloud provider (e.g., AWS RDS, Google Cloud SQL, Azure Database for PostgreSQL, or Supabase) for better reliability, scalability, and manageability.
  * Ensure your deployed application is configured with the correct database connection URL via the `DB_URL` environment variable. You can also set individual database parameters (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, etc.) if preferred.
  * The database schema should be set to `ai` via the `DB_SCHEME` environment variable.

# Agent API

Агентский API для работы с различными типами агентов ИИ, построенный на основе фреймворка Agno.

## Возможности

- 🤖 Множественные специализированные агенты (Demo, Agno Assist, Finance)
- 💬 Поддержка потокового и обычного режимов ответов
- 📁 **Поддержка загрузки файлов** (изображения, аудио, видео, документы)
- 🧠 Персистентная память и история сессий
- 🔍 Интеграция с базами знаний
- 🎮 Веб-интерфейс для тестирования (Playground)
- 🐳 Контейнеризация с Docker

## Быстрый старт

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd agent-api
```

2. Создайте файл `.env` на основе `example.env`
3. Запустите с помощью Docker:
```bash
docker compose up -d --build
```

API будет доступен по адресу `http://localhost:8000`

## Использование API

### Базовые запросы (только текст)

```bash
# Простой текстовый запрос
curl -X POST "http://localhost:8000/v1/agents/demo_agent/runs/json" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Привет! Как дела?",
    "stream": false,
    "user_id": "user123",
    "session_id": "session456"
  }'
```

### Запросы с файлами

#### Загрузка изображения
```bash
curl -X POST "http://localhost:8000/v1/agents/demo_agent/runs" \
  -F "message=Опиши что изображено на картинке" \
  -F "stream=false" \
  -F "user_id=user123" \
  -F "files=@path/to/image.jpg"
```

#### Загрузка документа
```bash
curl -X POST "http://localhost:8000/v1/agents/agno_assist/runs" \
  -F "message=Проанализируй этот документ" \
  -F "stream=false" \
  -F "files=@document.pdf"
```

#### Множественные файлы
```bash
curl -X POST "http://localhost:8000/v1/agents/demo_agent/runs" \
  -F "message=Обработай эти файлы" \
  -F "stream=true" \
  -F "files=@image1.jpg" \
  -F "files=@document.pdf" \
  -F "files=@audio.mp3"
```

### Поддерживаемые типы файлов

#### Изображения
- PNG, JPEG, JPG, WebP
- Автоматическое кодирование в base64
- Передача агенту для анализа

#### Аудио
- WAV, MP3, MPEG
- Поддержка транскрипции (зависит от агента)

#### Видео  
- MP4, WebM, MOV, AVI, FLV, WMV, 3GPP
- Обработка видеоконтента

#### Документы
- **PDF** - извлечение текста и изображений
- **CSV** - обработка табличных данных  
- **DOCX** - извлечение текста из Word документов
- **TXT** - обработка простого текста
- **JSON** - парсинг структурированных данных

### Поведение с базами знаний

Если у агента есть база знаний (например, `agno_assist`):
- Документы автоматически загружаются в базу знаний
- Агент может искать информацию из загруженных документов
- Контент становится доступен для последующих запросов

Если базы знаний нет:
- Файлы передаются агенту как прямой ввод
- Обработка зависит от возможностей конкретного агента

### Примеры на Python

```python
import requests

# Простой текстовый запрос
response = requests.post(
    "http://localhost:8000/v1/agents/demo_agent/runs/json",
    json={
        "message": "Привет!",
        "stream": False,
        "user_id": "user123"
    }
)

# Запрос с изображением
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/v1/agents/demo_agent/runs",
        data={
            "message": "Что на картинке?",
            "stream": "false",
            "user_id": "user123"
        },
        files={"files": f}
    )

# Потоковый запрос с документом
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/v1/agents/agno_assist/runs",
        data={
            "message": "Summarize this document",
            "stream": "true"
        },
        files={"files": f},
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
```

### Примеры на JavaScript

```javascript
// Запрос с файлом
const formData = new FormData();
formData.append('message', 'Analyze this image');
formData.append('stream', 'false');
formData.append('files', fileInput.files[0]);

const response = await fetch('/v1/agents/demo_agent/runs', {
    method: 'POST',
    body: formData
});

const result = await response.text();
console.log(result);

// Потоковый запрос
const streamResponse = await fetch('/v1/agents/demo_agent/runs', {
    method: 'POST',
    body: formData
});

const reader = streamResponse.body.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = new TextDecoder().decode(value);
    console.log(chunk);
}
```

## Доступные агенты

### Demo Agent (`demo_agent`)
- Универсальный демонстрационный агент
- Поддержка русского языка
- Инструменты: DuckDuckGo поиск
- Персистентная память

### Agno Assist (`agno_assist`)  
- Специалист по фреймворку Agno
- База знаний из документации Agno
- Помощь с кодом и примерами
- Поддержка загрузки документов в базу знаний

### Finance Agent (`finance_agent`)
- Финансовый аналитик "FinMaster"
- Инструменты: YFinance, DuckDuckGo
- Анализ акций и рекомендации
- Профессиональные отчеты

## API Endpoints

- `GET /v1/agents` - Список доступных агентов
- `POST /v1/agents/{agent_id}/runs` - Запуск агента с поддержкой файлов
- `POST /v1/agents/{agent_id}/runs/json` - Запуск агента только с текстом
- `POST /v1/agents/{agent_id}/knowledge/load` - Загрузка базы знаний
- `GET /v1/health` - Проверка состояния API
- `/v1/playground/*` - Веб-интерфейс для тестирования

## Разработка

### Структура проекта
```
agent-api/
├── agents/          # Определения агентов
├── api/            # FastAPI приложение
├── db/             # Настройки базы данных
└── scripts/        # Утилиты разработки
```

### Добавление нового агента

1. Создайте файл в `agents/your_agent.py`
2. Добавьте тип в `agents/selector.py`
3. Обновите селектор в `get_agent()`

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.
