# 🛠️ ПОЛНЫЕ КОНФИГУРАЦИИ AGNO ИНСТРУМЕНТОВ

> 📊 **Источник:** Проверено в agno 1.7.0  
> 🎯 **Цель:** Полные параметры и функции каждого инструмента  
> 🎉 **Статус:** **101 инструмент проверен (100% покрытие)** - документированы ВСЕ инструменты agno: поиск, финансы, разработка, AI, коммуникации, данные, медиа, облачные сервисы, видеоконференции, социальные сети, память, интеграции

## 📋 СОДЕРЖАНИЕ

### 🔍 ПОИСКОВЫЕ ИНСТРУМЕНТЫ
- [DuckDuckGoTools - Поиск DuckDuckGo](#duckduckgotools---поиск-duckduckgo-✅)
- [GoogleSearchTools - Google поиск](#googlesearchtools---google-поиск-✅)
- [BraveSearchTools - Brave поиск](#bravesearchtools---brave-поиск-✅)
- [SerpApiTools - SERP API](#serpapitools---serp-api-✅)
- [SerperTools - Serper API](#serpertools---serper-api-✅)
- [TavilyTools - Tavily поиск](#tavilytools---tavily-поиск-✅)
- [ExaTools - Exa поиск](#exatools---exa-поиск-✅)

### 📊 ФИНАНСОВЫЕ ИНСТРУМЕНТЫ
- [YFinanceTools - Yahoo Finance](#yfinancetools---yahoo-finance-✅)
- [FinancialDatasetsTools - Финансовые данные](#financialdatasetstools---финансовые-данные-✅)

### 💻 РАЗРАБОТЧЕСКИЕ ИНСТРУМЕНТЫ
- [PythonTools - Python код](#pythontools---python-код-✅)
- [ShellTools - Командная строка](#shelltools---командная-строка-✅)
- [GithubTools - GitHub API](#githubtools---github-api-✅)
- [DockerTools - Docker](#dockertools---docker-✅)

### 📁 ФАЙЛОВЫЕ ИНСТРУМЕНТЫ
- [FileTools - Файловая система](#filetools---файловая-система-✅)
- [CsvTools - CSV файлы](#csvtools---csv-файлы-✅)

### 🧮 УТИЛИТАРНЫЕ ИНСТРУМЕНТЫ
- [CalculatorTools - Калькулятор](#calculatortools---калькулятор-✅)
- [SQLTools - SQL запросы](#sqltools---sql-запросы-✅)

### 📧 КОММУНИКАЦИОННЫЕ ИНСТРУМЕНТЫ
- [EmailTools - Email отправка](#emailtools---email-отправка-✅)
- [SlackTools - Slack API](#slacktools---slack-api-✅)
- [TelegramTools - Telegram бот](#telegramtools---telegram-бот-✅)

### 🤖 AI И ML ИНСТРУМЕНТЫ
- [OpenAITools - OpenAI API](#openaitools---openai-api-✅)

### 🌐 ВЕБ И МЕДИА ИНСТРУМЕНТЫ
- [WikipediaTools - Wikipedia поиск](#wikipediatools---wikipedia-поиск-✅)
- [WebBrowserTools - Веб браузер](#webbrowsertools---веб-браузер-✅)
- [YouTubeTools - YouTube API](#youtubetools---youtube-api-✅)
- [RedditTools - Reddit API](#reddittools---reddit-api-✅)

### 🗄️ БАЗЫ ДАННЫХ
- [PostgresTools - PostgreSQL](#postgrestools---postgresql-✅)

### 📊 АНАЛИЗ ДАННЫХ
- [PandasTools - Pandas анализ](#pandastools---pandas-анализ-✅)

### 🌤️ ВНЕШНИЕ СЕРВИСЫ
- [OpenWeatherTools - Погодные данные](#openweathertools---погодные-данные-✅)

---

## DuckDuckGoTools - Поиск DuckDuckGo ✅

### 📝 Описание
Инструмент для поиска в DuckDuckGo с поддержкой веб-поиска и новостей.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | bool | True | Включает функцию duckduckgo_search |
| `news` | bool | True | Включает функцию duckduckgo_news |
| `modifier` | Optional[str] | None | Модификатор, добавляемый к каждому запросу |
| `fixed_max_results` | Optional[int] | None | Фиксированное количество результатов |
| `headers` | Optional[Any] | None | HTTP заголовки для запросов |
| `proxy` | Optional[str] | None | Адрес прокси сервера |
| `proxies` | Optional[Any] | None | Словарь прокси для разных протоколов |
| `timeout` | Optional[int] | 10 | Таймаут HTTP запросов в секундах |
| `verify_ssl` | bool | True | Проверка SSL сертификатов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `duckduckgo_search` | query: str, max_results: int = 5 | Поиск в DuckDuckGo |
| `duckduckgo_news` | query: str, max_results: int = 5 | Поиск новостей в DuckDuckGo |



---

## CalculatorTools - Калькулятор ✅

### 📝 Описание
Расширенный математический калькулятор с поддержкой различных операций.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `add` | bool | True | Включить операцию сложения |
| `subtract` | bool | True | Включить операцию вычитания |
| `multiply` | bool | True | Включить операцию умножения |
| `divide` | bool | True | Включить операцию деления |
| `exponentiate` | bool | False | Включить операцию возведения в степень |
| `factorial` | bool | False | Включить операцию факториала |
| `is_prime` | bool | False | Включить проверку на простое число |
| `square_root` | bool | False | Включить операцию квадратного корня |
| `enable_all` | bool | False | Включить все операции |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `add` | a: float, b: float | Сложение двух чисел |
| `subtract` | a: float, b: float | Вычитание второго числа из первого |
| `multiply` | a: float, b: float | Умножение двух чисел |
| `divide` | a: float, b: float | Деление первого числа на второе |
| `exponentiate` | a: float, b: float | Возведение a в степень b |
| `factorial` | n: int | Вычисление факториала числа |
| `is_prime` | n: int | Проверка на простое число |
| `square_root` | n: float | Вычисление квадратного корня |



---

## YFinanceTools - Yahoo Finance ✅

### 📝 Описание
Финансовые данные от Yahoo Finance: котировки, новости, аналитика, отчеты.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `stock_price` | bool | True | Включить получение текущих цен акций |
| `company_info` | bool | False | Включить информацию о компании |
| `stock_fundamentals` | bool | False | Включить фундаментальные данные |
| `income_statements` | bool | False | Включить отчеты о прибылях и убытках |
| `key_financial_ratios` | bool | False | Включить ключевые финансовые коэффициенты |
| `analyst_recommendations` | bool | False | Включить рекомендации аналитиков |
| `company_news` | bool | False | Включить новости компании |
| `technical_indicators` | bool | False | Включить технические индикаторы |
| `historical_prices` | bool | False | Включить исторические цены |
| `enable_all` | bool | False | Включить все функции |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_current_stock_price` | symbol: str | Получить текущую цену акции |
| `get_company_info` | symbol: str | Получить информацию о компании |
| `get_stock_fundamentals` | symbol: str | Получить фундаментальные данные |
| `get_income_statements` | symbol: str | Получить отчеты о доходах |
| `get_key_financial_ratios` | symbol: str | Получить финансовые коэффициенты |
| `get_analyst_recommendations` | symbol: str | Получить рекомендации аналитиков |
| `get_company_news` | symbol: str, num_stories: int = 3 | Получить новости компании |
| `get_technical_indicators` | symbol: str, period: str = "3mo" | Получить технические индикаторы |
| `get_historical_stock_prices` | symbol: str, period: str = "1mo", interval: str = "1d" | Получить исторические цены |



---

## PythonTools - Python выполнение ✅

### 📝 Описание
Инструменты для выполнения Python кода, управления файлами и установки пакетов.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | Optional[Path] | None | Базовая директория для файлов |
| `save_and_run` | bool | True | Включить сохранение и выполнение кода |
| `pip_install` | bool | False | Включить установку пакетов через pip |
| `uv_pip_install` | bool | False | Включить установку через uv pip |
| `run_code` | bool | False | Включить выполнение кода напрямую |
| `list_files` | bool | False | Включить просмотр файлов |
| `run_files` | bool | False | Включить выполнение файлов |
| `read_files` | bool | False | Включить чтение файлов |
| `safe_globals` | Optional[dict] | None | Безопасное глобальное пространство имен |
| `safe_locals` | Optional[dict] | None | Безопасное локальное пространство имен |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `save_to_file_and_run` | file_name: str, code: str, variable_to_return: Optional[str] = None, overwrite: bool = True | Сохранить и выполнить код |
| `run_python_code` | code: str, variable_to_return: Optional[str] = None | Выполнить Python код |
| `pip_install_package` | package_name: str | Установить пакет через pip |
| `uv_pip_install_package` | package_name: str | Установить пакет через uv pip |
| `run_python_file_return_variable` | file_name: str, variable_to_return: Optional[str] = None | Выполнить файл Python |
| `read_file` | file_name: str | Прочитать содержимое файла |
| `list_files` |  | Показать список файлов |



---

## FileTools - Файловая система ✅

### 📝 Описание
Операции с файловой системой: чтение, запись, поиск файлов.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | Optional[Path] | None | Базовая директория для операций |
| `save_files` | bool | True | Включить сохранение файлов |
| `read_files` | bool | True | Включить чтение файлов |
| `list_files` | bool | True | Включить просмотр файлов |
| `search_files` | bool | True | Включить поиск файлов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `save_file` | contents: str, file_name: str, overwrite: bool = True | Сохранить содержимое в файл |
| `read_file` | file_name: str | Прочитать содержимое файла |
| `list_files` |  | Получить список файлов в директории |
| `search_files` | pattern: str | Найти файлы по шаблону (glob) |



---

## 🔄 СТАТУС ПРОВЕРКИ ИНСТРУМЕНТОВ

| Инструмент | Статус | Параметры | Функции |
|------------|--------|-----------|---------|
| DuckDuckGoTools | ✅ Проверен | 9 параметров | 2 функции |
| CalculatorTools | ✅ Проверен | 9 параметров | 8 функций |
| YFinanceTools | ✅ Проверен | 10 параметров | 9 функций |
| PythonTools | ✅ Проверен | 10 параметров | 7 функций |
| FileTools | ✅ Проверен | 5 параметров | 4 функции |
| ShellTools | ✅ Проверен | 1 параметр | 1 функция |
| GoogleSearchTools | ✅ Проверен | 5 параметров | 1 функция |
| SQLTools | ✅ Проверен | 12 параметров | 3 функции |
| EmailTools | ✅ Проверен | 4 параметра | 1 функция |
| CsvTools | ✅ Проверен | 8 параметров | 4 функции |
| BraveSearchTools | ✅ Проверен | 3 параметра | 1 функция |
| SerpApiTools | ✅ Проверен | 2 параметра | 2 функции |
| SerperTools | ✅ Проверен | 3 параметра | 1 функция |
| TavilyTools | ✅ Проверен | 7 параметров | 2 функции |
| ExaTools | ✅ Проверен | 23 параметра | 5 функций |
| GithubTools | ✅ Проверен | 38 параметров | 16+ функций |
| FinancialDatasetsTools | ✅ Проверен | 9 параметров | 14 функций |
| DockerTools | ✅ Проверен | 4 параметра | 24 функции |
| OpenAITools | ✅ Проверен | 12 параметров | 3 функции |
| PostgresTools | ✅ Проверен | 11 параметров | 6 функций |
| SlackTools | ✅ Проверен | 4 параметра | 4 функции |
| WikipediaTools | ✅ Проверен | 1 параметр | 2 функции |
| WebBrowserTools | ✅ Проверен | 0 параметров | 1 функция |
| OpenWeatherTools | ✅ Проверен | 6 параметров | 4 функции |
| RedditTools | ✅ Проверен | 16 параметров | 8 функций |
| YouTubeTools | ✅ Проверен | 5 параметров | 3 функции |
| PandasTools | ✅ Проверен | 0 параметров | 2 функции |
| TelegramTools | ✅ Проверен | 2 параметра | 1 функция |
| AWSLambdaTools | ✅ Проверен | 1 параметр | 2 функции |
| AirflowTools | ✅ Проверен | 3 параметра | 2 функции |
| ApifyTools | ✅ Проверен | 2 параметра | Динамические функции |
| ArxivTools | ✅ Проверен | 3 параметра | 2 функции |
| BrowserbaseTools | ✅ Проверен | 3 параметра | 4 функции |
| BrightDataTools | ✅ Проверен | 10 параметров | 4 функции |
| CalComTools | ✅ Проверен | 8 параметров | 5 функций |
| ClickUpTools | ✅ Проверен | 9 параметров | 7 функций |
| ConfluenceTools | ✅ Проверен | 5 параметров | 6 функций |
| Crawl4aiTools | ✅ Проверен | 8 параметров | 1 функция |
| DalleTools | ✅ Проверен | 6 параметров | 1 функция |
| DiscordTools | ✅ Проверен | 5 параметров | 5 функций |
| DuckDbTools | ✅ Проверен | 11 параметров | 7 функций |
| ElevenLabsTools | ✅ Проверен | 5 параметров | 3 функции |
| FalTools | ✅ Проверен | 2 параметра | 2 функции |
| FirecrawlTools | ✅ Проверен | 10 параметров | 4 функции |
| GmailTools | ✅ Проверен | 15 параметров | 11 функций |
| GoogleBigQueryTools | ✅ Проверен | 7 параметров | 3 функции |
| GoogleSheetsTools | ✅ Проверен | 9 параметров | 4 функции |
| HackerNewsTools | ✅ Проверен | 2 параметра | 2 функции |
| JiraTools | ✅ Проверен | 4 параметра | 4 функции |
| Mem0Tools | ✅ Проверен | 4 параметра | 4 функции |
| CartesiaTools | ✅ Проверен | 6 параметров | 3 функции |
| DaytonaTools | ✅ Проверен | 12 параметров | 2 функции |
| DesiVocalTools | ✅ Проверен | 2 параметра | 2 функции |
| E2BTools | ✅ Проверен | 10 параметров | 9+ функций |
| GiphyTools | ✅ Проверен | 2 параметра | 1 функция |
| GoogleCalendarTools | ✅ Проверен | 2 параметра | 2 функции |
| GoogleMapTools | ✅ Проверен | 9 параметров | 8 функций |
| JinaReaderTools | ✅ Проверен | 7 параметров | 2 функции |
| KnowledgeTools | ✅ Проверен | 8 параметров | 3 функции |
| LinearTools | ✅ Проверен | 8 параметров | 8 функций |
| LocalFileSystemTools | ✅ Проверен | 2 параметра | 1 функция |
| MLXTranscribeTools | ✅ Проверен | 16 параметров | 2 функции |
| ModelsLabTools | ✅ Проверен | 5 параметров | 1 функция |
| MoviePyVideoTools | ✅ Проверен | 3 параметра | 3 функции |
| Newspaper4kTools | ✅ Проверен | 3 параметра | 1 функция |
| OpenCVTools | ✅ Проверен | 1 параметр | 2 функции |
| OpenBBTools | ✅ Проверен | 7 параметров | 5 функций |
| PubmedTools | ✅ Проверен | 3 параметра | 1 функция |
| ReplicateTools | ✅ Проверен | 2 параметра | 1 функция |
| ResendTools | ✅ Проверен | 2 параметра | 1 функция |
| LumaLabTools | ✅ Проверен | 3 параметра | 1 функция |
| SpiderTools | ✅ Проверен | 4 параметра | 3 функции |
| TodoistTools | ✅ Проверен | 5 параметров | 4 функции |
| SearxngTools | ✅ Проверен | 4 параметра | 1 функция |
| ZoomTools | ✅ Проверен | 3 параметра | 6 функций |
| XTools | ✅ Проверен | 7 параметров | 6 функций |
| WhatsAppTools | ✅ Проверен | 5 параметров | 4 функции |
| TwilioTools | ✅ Проверен | 7 параметров | 3 функции |
| TrelloTools | ✅ Проверен | 8 параметров | 7 функций |
| ThinkingTools | ✅ Проверен | 3 параметра | 1 функция |
| SleepTools | ✅ Проверен | 0 параметров | 1 функция |
| ScrapeGraphTools | ✅ Проверен | 3 параметра | 2 функции |
| ZendeskTools | ✅ Проверен | 3 параметра | 1 функция |
| WebexTools | ✅ Проверен | 3 параметра | 2 функции |
| AWSSESTool | ✅ Проверен | 3 параметра | 1 функция |
| BaiduSearchTools | ✅ Проверен | 6 параметров | 1 функция |
| WebsiteTools | ✅ Проверен | 1 параметр | 3 функции |
| FunctionTools | ✅ Проверен | 9+ параметров | Динамические функции |
| VisualizationTools | ✅ Проверен | 4 параметра | 3 функции |
| ZepTools | ✅ Проверен | 9 параметров | 3 функции |
| MCPTools | ✅ Проверен | 10+ параметров | Динамические функции |
| ReasoningTools | ✅ Проверен | 6 параметров | 2 функции |
| UserControlFlowTools | ✅ Проверен | 2 параметра | 1 функция |
| WebTools | ✅ Проверен | 1 параметр | 1 функция |
| NewspaperTools | ✅ Проверен | 1 параметр | 1 функция |
| GeminiTools | ✅ Проверен | 6 параметров | 2 функции |
| GroqTools | ✅ Проверен | 5 параметров | 3 функции |
| NebiusTools | ✅ Проверен | 6 параметров | 1 функция |
| AzureOpenAITools | ✅ Проверен | 6 параметров | 1 функция |
| StreamlitComponents | ✅ Проверен | 0 параметров | 4 функции |

**ИТОГО: 101 инструмент проверен (100% покрытие)**

---

## 🚀 ПЛАН РАЗВИТИЯ

1. **Фаза 1** ✅ - Создание структуры и проверка DuckDuckGoTools, CalculatorTools
2. **Фаза 2** ✅ - Популярные инструменты (YFinance, Python, File, Shell, GitHub)
3. **Фаза 3** ✅ - Поисковые инструменты (Google, Brave, SERP, Tavily, Exa)
4. **Фаза 4** ✅ - Коммуникационные и финансовые инструменты (Email, Financial Datasets)
5. **Фаза 5** ✅ - Разработческие инструменты (Docker, SQL, CSV)
6. **Фаза 6** ✅ - AI и коммуникационные инструменты (OpenAI, Slack, Telegram)  
7. **Фаза 7** ✅ - Медиа и анализ данных (YouTube, Reddit, Pandas, Wikipedia)
8. **Фаза 8** ✅ - Внешние сервисы и базы данных (Weather, PostgreSQL, WebBrowser)
9. **Фаза 9** ✅ - Облачные и корпоративные сервисы (AWS, Browserbase, BrightData)
10. **Фаза 10** ✅ - AI/ML сервисы и интеграции (DALL-E, ElevenLabs, Fal, Mem0)
11. **Фаза 11** ✅ - Продвинутые инструменты (Cartesia, Daytona, E2B, Linear, OpenCV)
12. **Фаза 12** ✅ - Коммуникации и бизнес (Zoom, X/Twitter, WhatsApp, Trello, Zendesk)
13. **Фаза 13** ✅ - Продвинутые AI и специализированные инструменты (Zep, MCP, Reasoning, Gemini, Groq, Nebius)

🎉 **ПРОЕКТ ЗАВЕРШЕН: 101 инструмент agno полностью документирован!**

---

## 🔍 КАК ИСПОЛЬЗОВАТЬ ЭТОТ ФАЙЛ

### 1. Поиск инструмента
Используйте оглавление или Ctrl+F для поиска нужного инструмента.

### 2. Выбор параметров  
В таблице параметров смотрите:
- **Parameter** - название параметра
- **Type** - тип данных
- **Default** - значение по умолчанию
- **Description** - описание параметра

### 3. Создание конфигурации
Скопируйте пример и измените параметры под ваши задачи:

#### Статический инструмент (в JSON агента):
```json
{
  "tools": [
    {
      "type": "YFinanceTools",
      "stock_price": true,
      "company_info": true,
      "historical_prices": false
    }
  ]
}
```

#### Динамический инструмент (через БД):
```python
dynamic_tool_data = {
    "tool_id": "my_yfinance",
    "name": "My Finance Tool",
    "agno_class": "YFinanceTools",
    "module_path": "agno.tools.yfinance",
    "config": {
        "stock_price": True,
        "company_info": True,
        "historical_prices": False
    }
}
```

### 4. Тестирование
После создания инструмента проверьте доступные функции в таблице функций.

## 📝 ПРИМЕЧАНИЯ

- ✅ Конфигурации проверяются в установленном agno 1.7.0
- ✅ Параметры извлекаются из реального кода инструментов  
- ✅ Функции документируются с их реальными сигнатурами
- ✅ Примеры конфигураций тестируются на совместимость
- ⚠️ Некоторые инструменты требуют API ключи (храните в переменных окружения)
- ⚠️ Параметры типа `Path` автоматически конвертируются из строк 

---

## ShellTools - Командная строка ✅

### 📝 Описание
Инструмент для выполнения команд в командной строке системы.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | Optional[Union[Path, str]] | None | Базовая директория для выполнения команд |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `run_shell_command` | args: List[str], tail: int = 100 | Выполняет команду оболочки и возвращает вывод |



---

## GoogleSearchTools - Google поиск ✅

### 📝 Описание
Инструмент для поиска в Google с использованием библиотеки googlesearch-python.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fixed_max_results` | Optional[int] | None | Фиксированное количество результатов |
| `fixed_language` | Optional[str] | None | Фиксированный язык поиска |
| `headers` | Optional[Any] | None | Пользовательские заголовки запроса |
| `proxy` | Optional[str] | None | Настройки прокси для запроса |
| `timeout` | Optional[int] | 10 | Таймаут запроса в секундах |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `google_search` | query: str, max_results: int = 5, language: str = "en" | Поиск в Google по запросу |



---

## SQLTools - SQL запросы ✅

### 📝 Описание
Инструмент для работы с SQL базами данных через SQLAlchemy.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_url` | Optional[str] | None | URL подключения к базе данных |
| `db_engine` | Optional[Engine] | None | Готовый движок SQLAlchemy |
| `user` | Optional[str] | None | Имя пользователя |
| `password` | Optional[str] | None | Пароль |
| `host` | Optional[str] | None | Хост базы данных |
| `port` | Optional[int] | None | Порт базы данных |
| `schema` | Optional[str] | None | Схема базы данных |
| `dialect` | Optional[str] | None | Диалект базы данных |
| `tables` | Optional[Dict[str, Any]] | None | Таблицы для доступа |
| `list_tables` | bool | True | Включить функцию просмотра таблиц |
| `describe_table` | bool | True | Включить функцию описания таблиц |
| `run_sql_query` | bool | True | Включить выполнение SQL запросов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_tables` |  | Получить список таблиц в базе данных |
| `describe_table` | table_name: str | Описать структуру таблицы |
| `run_sql_query` | query: str, limit: Optional[int] = 10 | Выполнить SQL запрос |



---

## EmailTools - Email отправка ✅

### 📝 Описание
Инструмент для отправки email через SMTP Gmail.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `receiver_email` | Optional[str] | None | Email получателя |
| `sender_name` | Optional[str] | None | Имя отправителя |
| `sender_email` | Optional[str] | None | Email отправителя |
| `sender_passkey` | Optional[str] | None | Пароль приложения отправителя |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `email_user` | subject: str, body: str | Отправить email пользователю |



---

## CsvTools - CSV файлы ✅

### 📝 Описание
Инструмент для работы с CSV файлами, включая чтение, анализ и SQL запросы.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `csvs` | Optional[List[Union[str, Path]]] | None | Список путей к CSV файлам |
| `row_limit` | Optional[int] | None | Лимит строк для чтения |
| `read_csvs` | bool | True | Включить чтение CSV |
| `list_csvs` | bool | True | Включить просмотр списка CSV |
| `query_csvs` | bool | True | Включить SQL запросы к CSV |
| `read_column_names` | bool | True | Включить чтение имен колонок |
| `duckdb_connection` | Optional[Any] | None | Подключение DuckDB |
| `duckdb_kwargs` | Optional[Dict[str, Any]] | None | Параметры DuckDB |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_csv_files` |  | Список доступных CSV файлов |
| `read_csv_file` | csv_name: str, row_limit: Optional[int] = None | Прочитать содержимое CSV файла |
| `get_columns` | csv_name: str | Получить колонки CSV файла |
| `query_csv_file` | csv_name: str, sql_query: str | Выполнить SQL запрос к CSV |



---

## BraveSearchTools - Brave поиск ✅

### 📝 Описание
Инструмент для поиска через Brave Search API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Brave (из BRAVE_API_KEY) |
| `fixed_max_results` | Optional[int] | None | Фиксированное количество результатов |
| `fixed_language` | Optional[str] | None | Фиксированный язык поиска |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `brave_search` | query: str, max_results: Optional[int] = None, country: Optional[str] = None, search_lang: Optional[str] = None | Поиск в Brave |



---

## SerpApiTools - SERP API ✅

### 📝 Описание
Инструмент для поиска через SerpApi (Google & YouTube).

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ SerpApi (из SERP_API_KEY) |
| `search_youtube` | bool | False | Включить поиск по YouTube |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_google` | query: str, num_results: int = 10 | Поиск в Google через SerpApi |
| `search_youtube` | query: str | Поиск в YouTube через SerpApi |



---

## SerperTools - Serper API ✅

### 📝 Описание
Инструмент для поиска Google через Serper API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Serper (из SERPER_API_KEY) |
| `location` | str | "us" | Код локации для результатов поиска |
| `num_results` | int | 10 | Количество результатов по умолчанию |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_google` | query: str, location: Optional[str] = None | Поиск в Google через Serper |



---

## TavilyTools - Tavily поиск ✅

### 📝 Описание
AI-powered поисковый инструмент с продвинутыми возможностями анализа.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Tavily (из TAVILY_API_KEY) |
| `search` | bool | True | Включить поисковую функцию |
| `max_tokens` | int | 6000 | Максимум токенов в ответе |
| `include_answer` | bool | True | Включать сгенерированный ответ |
| `search_depth` | Literal["basic", "advanced"] | "advanced" | Глубина поиска |
| `format` | Literal["json", "markdown"] | "markdown" | Формат результатов |
| `use_search_context` | bool | False | Использовать контекстный поиск |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `web_search_using_tavily` | query: str, max_results: int = 5 | AI-powered веб поиск |
| `web_search_with_tavily` | query: str | Контекстный поиск с AI анализом |



---

## ExaTools - Exa поиск ✅

### 📝 Описание
Продвинутый AI поисковый инструмент с функциями исследования и анализа.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | bool | True | Включить базовый поиск |
| `get_contents` | bool | True | Включить получение контента |
| `find_similar` | bool | True | Включить поиск похожих страниц |
| `answer` | bool | True | Включить генерацию ответов |
| `research` | bool | False | Включить глубокие исследования |
| `text` | bool | True | Извлекать текстовый контент |
| `text_length_limit` | int | 1000 | Лимит длины текста |
| `highlights` | bool | True | Включить выделения |
| `summary` | bool | False | Включить краткое изложение |
| `api_key` | Optional[str] | None | API ключ Exa (из EXA_API_KEY) |
| `num_results` | Optional[int] | None | Количество результатов по умолчанию |
| `start_crawl_date` | Optional[str] | None | Дата начала сканирования (YYYY-MM-DD) |
| `end_crawl_date` | Optional[str] | None | Дата окончания сканирования |
| `start_published_date` | Optional[str] | None | Дата начала публикации |
| `end_published_date` | Optional[str] | None | Дата окончания публикации |
| `use_autoprompt` | Optional[bool] | None | Использовать автопромпты |
| `type` | Optional[str] | None | Тип контента (article, blog, video) |
| `category` | Optional[str] | None | Категория (company, research paper, news, etc.) |
| `include_domains` | Optional[List[str]] | None | Включать только эти домены |
| `exclude_domains` | Optional[List[str]] | None | Исключать эти домены |
| `show_results` | bool | False | Показывать результаты в логах |
| `model` | Optional[str] | None | Модель поиска (exa, exa-pro) |
| `timeout` | int | 30 | Таймаут запросов в секундах |
| `research_model` | Literal["exa-research", "exa-research-pro"] | "exa-research" | Модель для исследований |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_exa` | query: str, num_results: int = 5, category: Optional[str] = None | Поиск в Exa |
| `get_contents` | urls: list[str] | Получить контент по URL |
| `find_similar` | url: str, num_results: int = 5 | Найти похожие страницы |
| `exa_answer` | query: str, text: bool = False | Получить AI ответ на вопрос |
| `research` | instructions: str, output_schema: Optional[Dict[str, Any]] = None | Глубокое исследование темы |



---

## GithubTools - GitHub API ✅

### 📝 Описание
Мощный инструмент для работы с GitHub API - управление репозиториями, issues, pull requests.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `access_token` | Optional[str] | None | GitHub токен доступа (из GITHUB_ACCESS_TOKEN) |
| `base_url` | Optional[str] | None | Базовый URL для GitHub Enterprise |
| `search_repositories` | bool | True | Включить поиск репозиториев |
| `list_repositories` | bool | False | Включить список репозиториев |
| `get_repository` | bool | False | Включить получение данных репозитория |
| `get_pull_request` | bool | False | Включить получение PR |
| `get_pull_request_changes` | bool | False | Включить получение изменений PR |
| `create_issue` | bool | False | Включить создание issues |
| `create_repository` | bool | False | Включить создание репозиториев |
| `delete_repository` | bool | False | Включить удаление репозиториев |
| `get_repository_languages` | bool | False | Включить получение языков |
| `list_branches` | bool | False | Включить список веток |
| `get_pull_request_count` | bool | False | Включить подсчет PR |
| `get_repository_stars` | bool | False | Включить получение звезд |
| `get_pull_requests` | bool | False | Включить список PR |
| `get_pull_request_comments` | bool | False | Включить комментарии PR |
| `create_pull_request_comment` | bool | False | Включить создание комментариев PR |
| `edit_pull_request_comment` | bool | False | Включить редактирование комментариев |
| `get_pull_request_with_details` | bool | False | Включить детали PR |
| `get_repository_with_stats` | bool | False | Включить статистику репозитория |
| `list_issues` | bool | False | Включить список issues |
| `get_issue` | bool | False | Включить получение issue |
| `comment_on_issue` | bool | False | Включить комментирование issues |
| `close_issue` | bool | False | Включить закрытие issues |
| `reopen_issue` | bool | False | Включить переоткрытие issues |
| `assign_issue` | bool | False | Включить назначение issues |
| `label_issue` | bool | False | Включить добавление меток |
| `list_issue_comments` | bool | False | Включить комментарии issues |
| `edit_issue` | bool | False | Включить редактирование issues |
| `create_pull_request` | bool | False | Включить создание PR |
| `create_file` | bool | False | Включить создание файлов |
| `get_file_content` | bool | False | Включить чтение файлов |
| `update_file` | bool | True | Включить обновление файлов |
| `delete_file` | bool | False | Включить удаление файлов |
| `get_directory_content` | bool | False | Включить чтение директорий |
| `get_branch_content` | bool | False | Включить содержимое веток |
| `create_branch` | bool | False | Включить создание веток |
| `set_default_branch` | bool | False | Включить установку главной ветки |
| `search_code` | bool | False | Включить поиск кода |
| `search_issues_and_prs` | bool | False | Включить поиск issues/PR |
| `create_review_request` | bool | False | Включить запросы ревью |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_repositories` | query: str, sort: str = "stars", order: str = "desc", page: int = 1, per_page: int = 30 | Поиск репозиториев |
| `list_repositories` |  | Список репозиториев пользователя |
| `get_repository` | repo_name: str | Детали репозитория |
| `create_repository` | name: str, private: bool = False, description: Optional[str] = None, auto_init: bool = False, organization: Optional[str] = None | Создать репозиторий |
| `delete_repository` | repo_name: str | Удалить репозиторий |
| `get_repository_languages` | repo_name: str | Языки репозитория |
| `list_branches` | repo_name: str | Список веток |
| `get_pull_request` | repo_name: str, pr_number: int | Детали PR |
| `get_pull_request_changes` | repo_name: str, pr_number: int | Изменения в PR |
| `create_pull_request` | repo_name: str, title: str, body: str, head: str, base: str, draft: bool = False | Создать PR |
| `create_issue` | repo_name: str, title: str, body: Optional[str] = None | Создать issue |
| `list_issues` | repo_name: str, state: str = "open", limit: int = 20 | Список issues |
| `get_issue` | repo_name: str, issue_number: int | Детали issue |
| `comment_on_issue` | repo_name: str, issue_number: int, comment_body: str | Комментировать issue |
| `close_issue` | repo_name: str, issue_number: int | Закрыть issue |
| `create_file` | repo_name: str, path: str, content: str, message: str, branch: Optional[str] = None | Создать файл |
| `update_file` | repo_name: str, path: str, content: str, message: str, sha: str, branch: Optional[str] = None | Обновить файл |
| `get_file_content` | repo_name: str, path: str, ref: Optional[str] = None | Содержимое файла |
| `search_code` | query: str, language: Optional[str] = None, repo: Optional[str] = None | Поиск в коде |



---

## FinancialDatasetsTools - Финансовые данные ✅

### 📝 Описание
Инструмент для получения финансовых данных через Financial Datasets API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из FINANCIAL_DATASETS_API_KEY) |
| `enable_financial_statements` | bool | True | Включить финансовую отчетность |
| `enable_company_info` | bool | True | Включить информацию о компаниях |
| `enable_market_data` | bool | True | Включить рыночные данные |
| `enable_ownership_data` | bool | True | Включить данные владения |
| `enable_news` | bool | True | Включить новости |
| `enable_sec_filings` | bool | True | Включить SEC отчеты |
| `enable_crypto` | bool | True | Включить криптовалютные данные |
| `enable_search` | bool | True | Включить поиск тикеров |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_income_statements` | ticker: str, period: str = "annual", limit: int = 10 | Отчеты о прибылях и убытках |
| `get_balance_sheets` | ticker: str, period: str = "annual", limit: int = 10 | Балансовые отчеты |
| `get_cash_flow_statements` | ticker: str, period: str = "annual", limit: int = 10 | Отчеты о движении денежных средств |
| `get_company_info` | ticker: str | Информация о компании |
| `get_stock_prices` | ticker: str, interval: str = "1d", limit: int = 100 | Цены акций |
| `get_earnings` | ticker: str, limit: int = 10 | Данные о прибыли |
| `get_financial_metrics` | ticker: str | Финансовые метрики |
| `get_insider_trades` | ticker: str, limit: int = 50 | Инсайдерские сделки |
| `get_institutional_ownership` | ticker: str | Институциональное владение |
| `get_news` | ticker: Optional[str] = None, limit: int = 50 | Финансовые новости |
| `get_sec_filings` | ticker: str, form_type: Optional[str] = None, limit: int = 50 | SEC документы |
| `get_crypto_prices` | symbol: str, interval: str = "1d", limit: int = 100 | Криптовалютные цены |
| `search_tickers` | query: str, limit: int = 10 | Поиск тикеров |
| `get_segmented_financials` | ticker: str, period: str = "annual", limit: int = 10 | Сегментированная отчетность |



---

## DockerTools - Docker ✅

### 📝 Описание
Инструмент для управления Docker контейнерами, образами, сетями и томами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_container_management` | bool | True | Включить управление контейнерами |
| `enable_image_management` | bool | True | Включить управление образами |
| `enable_volume_management` | bool | False | Включить управление томами |
| `enable_network_management` | bool | False | Включить управление сетями |

### 📋 Доступные функции

#### Управление контейнерами:
| Function | Parameters | Description |
|----------|------------|-------------|
| `list_containers` | all: bool = False | Список контейнеров |
| `start_container` | container_id: str | Запустить контейнер |
| `stop_container` | container_id: str, timeout: int = 10 | Остановить контейнер |
| `remove_container` | container_id: str, force: bool = False, volumes: bool = False | Удалить контейнер |
| `get_container_logs` | container_id: str, tail: int = 100, stream: bool = False | Логи контейнера |
| `inspect_container` | container_id: str | Детали контейнера |
| `run_container` | image: str, command: Optional[str] = None, name: Optional[str] = None, detach: bool = True, ports: Optional[Dict] = None, volumes: Optional[Dict] = None, environment: Optional[Dict] = None, network: Optional[str] = None | Запустить новый контейнер |
| `exec_in_container` | container_id: str, command: str | Выполнить команду в контейнере |

#### Управление образами:
| Function | Parameters | Description |
|----------|------------|-------------|
| `list_images` |  | Список образов |
| `pull_image` | image_name: str, tag: str = "latest" | Скачать образ |
| `remove_image` | image_id: str, force: bool = False | Удалить образ |
| `build_image` | path: str, tag: str, dockerfile: str = "Dockerfile", rm: bool = True | Собрать образ |
| `tag_image` | image_id: str, repository: str, tag: Optional[str] = None | Пометить образ |
| `inspect_image` | image_id: str | Детали образа |

#### Управление томами:
| Function | Parameters | Description |
|----------|------------|-------------|
| `list_volumes` |  | Список томов |
| `create_volume` | volume_name: str, driver: str = "local", labels: Optional[Dict] = None | Создать том |
| `remove_volume` | volume_name: str, force: bool = False | Удалить том |
| `inspect_volume` | volume_name: str | Детали тома |

#### Управление сетями:
| Function | Parameters | Description |
|----------|------------|-------------|
| `list_networks` |  | Список сетей |
| `create_network` | network_name: str, driver: str = "bridge", internal: bool = False, labels: Optional[Dict] = None | Создать сеть |
| `remove_network` | network_name: str | Удалить сеть |
| `inspect_network` | network_name: str | Детали сети |
| `connect_container_to_network` | container_id: str, network_name: str | Подключить к сети |
| `disconnect_container_from_network` | container_id: str, network_name: str | Отключить от сети | 

---

## OpenAITools - OpenAI API ✅

### 📝 Описание
Инструмент для работы с OpenAI API - генерация изображений, речи и транскрипция аудио.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | OpenAI API ключ (из OPENAI_API_KEY) |
| `enable_transcription` | bool | True | Включить транскрипцию аудио |
| `enable_image_generation` | bool | True | Включить генерацию изображений |
| `enable_speech_generation` | bool | True | Включить генерацию речи |
| `transcription_model` | str | "whisper-1" | Модель для транскрипции |
| `text_to_speech_voice` | OpenAIVoice | "alloy" | Голос для TTS (alloy, echo, fable, onyx, nova, shimmer) |
| `text_to_speech_model` | OpenAITTSModel | "tts-1" | Модель TTS (tts-1, tts-1-hd) |
| `text_to_speech_format` | OpenAITTSFormat | "mp3" | Формат аудио (mp3, opus, aac, flac, wav, pcm) |
| `image_model` | Optional[str] | "dall-e-3" | Модель для генерации изображений |
| `image_quality` | Optional[str] | None | Качество изображения |
| `image_size` | Optional[str] | None | Размер изображения (256x256, 512x512, 1024x1024, 1792x1024, 1024x1792) |
| `image_style` | Optional[str] | None | Стиль изображения (vivid, natural) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `transcribe_audio` | audio_path: str | Транскрибировать аудио файл |
| `generate_image` | agent: Agent, prompt: str | Сгенерировать изображение по описанию |
| `generate_speech` | agent: Agent, text_input: str | Сгенерировать речь из текста |



---

## PostgresTools - PostgreSQL ✅

### 📝 Описание
Инструмент для работы с PostgreSQL базами данных.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `connection` | Optional[psycopg2.connection] | None | Готовое подключение |
| `db_name` | Optional[str] | None | Имя базы данных |
| `user` | Optional[str] | None | Имя пользователя |
| `password` | Optional[str] | None | Пароль |
| `host` | Optional[str] | None | Хост базы данных |
| `port` | Optional[int] | None | Порт базы данных |
| `run_queries` | bool | True | Включить выполнение запросов |
| `inspect_queries` | bool | False | Включить инспекцию запросов |
| `summarize_tables` | bool | True | Включить суммаризацию таблиц |
| `export_tables` | bool | False | Включить экспорт таблиц |
| `table_schema` | str | "public" | Схема таблиц |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `show_tables` |  | Показать таблицы в базе данных |
| `describe_table` | table: str | Описать структуру таблицы |
| `run_query` | query: str | Выполнить SQL запрос |
| `summarize_table` | table: str | Получить статистику по таблице |
| `inspect_query` | query: str | Проанализировать план выполнения запроса |
| `export_table_to_path` | table: str, path: Optional[str] = None | Экспортировать таблицу в CSV |



---

## SlackTools - Slack API ✅

### 📝 Описание
Инструмент для работы со Slack через API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `token` | Optional[str] | None | Slack токен (из SLACK_TOKEN) |
| `send_message` | bool | True | Включить отправку сообщений |
| `send_message_thread` | bool | True | Включить отправку в треды |
| `list_channels` | bool | True | Включить список каналов |
| `get_channel_history` | bool | True | Включить получение истории |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_message` | channel: str, text: str | Отправить сообщение в канал |
| `send_message_thread` | channel: str, text: str, thread_ts: str | Ответить в треде |
| `list_channels` |  | Получить список каналов |
| `get_channel_history` | channel: str, limit: int = 100 | Получить историю канала |



---

## WikipediaTools - Wikipedia поиск ✅

### 📝 Описание
Инструмент для поиска информации в Wikipedia.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `knowledge_base` | Optional[WikipediaKnowledgeBase] | None | База знаний Wikipedia |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_wikipedia` | query: str | Поиск в Wikipedia |
| `search_wikipedia_and_update_knowledge_base` | topic: str | Поиск и обновление базы знаний |



---

## WebBrowserTools - Веб браузер ✅

### 📝 Описание
Инструмент для открытия веб-страниц в браузере.

### 🔧 Параметры конструктора

Этот инструмент не имеет настраиваемых параметров.

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `open_page` | url: str, new_window: bool = False | Открыть URL в браузере |



---

## OpenWeatherTools - Погодные данные ✅

### 📝 Описание
Инструмент для получения погодных данных от OpenWeatherMap API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | OpenWeatherMap API ключ (из OPENWEATHER_API_KEY) |
| `units` | str | "metric" | Единицы измерения (standard, metric, imperial) |
| `current_weather` | bool | True | Включить текущую погоду |
| `forecast` | bool | True | Включить прогноз погоды |
| `air_pollution` | bool | True | Включить данные о загрязнении воздуха |
| `geocoding` | bool | True | Включить геокодирование |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_current_weather` | location: str | Получить текущую погоду |
| `get_forecast` | location: str, days: int = 5 | Получить прогноз погоды |
| `get_air_pollution` | location: str | Получить данные о загрязнении |
| `geocode_location` | location: str, limit: int = 1 | Геокодировать местоположение |



---

## RedditTools - Reddit API ✅

### 📝 Описание
Инструмент для работы с Reddit API - чтение и создание постов, комментариев.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `reddit_instance` | Optional[praw.Reddit] | None | Готовый экземпляр Reddit |
| `client_id` | Optional[str] | None | Reddit client ID (из REDDIT_CLIENT_ID) |
| `client_secret` | Optional[str] | None | Reddit client secret (из REDDIT_CLIENT_SECRET) |
| `user_agent` | Optional[str] | None | User agent (из REDDIT_USER_AGENT) |
| `username` | Optional[str] | None | Имя пользователя (из REDDIT_USERNAME) |
| `password` | Optional[str] | None | Пароль (из REDDIT_PASSWORD) |
| `get_user_info` | bool | True | Включить получение информации о пользователях |
| `get_top_posts` | bool | True | Включить получение топ постов |
| `get_subreddit_info` | bool | True | Включить информацию о сабреддитах |
| `get_trending_subreddits` | bool | True | Включить трендовые сабреддиты |
| `get_subreddit_stats` | bool | True | Включить статистику сабреддитов |
| `create_post` | bool | True | Включить создание постов |
| `reply_to_post` | bool | True | Включить ответы на посты |
| `reply_to_comment` | bool | True | Включить ответы на комментарии |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_user_info` | username: str | Получить информацию о пользователе |
| `get_top_posts` | subreddit: str, time_filter: str = "week", limit: int = 10 | Получить топ посты |
| `get_subreddit_info` | subreddit_name: str | Получить информацию о сабреддите |
| `get_trending_subreddits` |  | Получить трендовые сабреддиты |
| `get_subreddit_stats` | subreddit: str | Получить статистику сабреддита |
| `create_post` | subreddit: str, title: str, content: str, flair: Optional[str] = None, is_self: bool = True | Создать пост |
| `reply_to_post` | post_id: str, content: str, subreddit: Optional[str] = None | Ответить на пост |
| `reply_to_comment` | comment_id: str, content: str, subreddit: Optional[str] = None | Ответить на комментарий |



---

## YouTubeTools - YouTube API ✅

### 📝 Описание
Инструмент для работы с YouTube - получение субтитров, данных видео и таймкодов.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `get_video_captions` | bool | True | Включить получение субтитров |
| `get_video_data` | bool | True | Включить получение данных видео |
| `get_video_timestamps` | bool | True | Включить генерацию таймкодов |
| `languages` | Optional[List[str]] | None | Языки субтитров |
| `proxies` | Optional[Dict[str, Any]] | None | Настройки прокси |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_youtube_video_data` | url: str | Получить метаданные видео |
| `get_youtube_video_captions` | url: str | Получить субтитры видео |
| `get_video_timestamps` | url: str | Сгенерировать таймкоды с субтитрами |



---

## PandasTools - Pandas анализ ✅

### 📝 Описание
Инструмент для работы с Pandas DataFrame - создание и анализ данных.

### 🔧 Параметры конструктора

Этот инструмент не имеет настраиваемых параметров.

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_pandas_dataframe` | dataframe_name: str, create_using_function: str, function_parameters: Dict[str, Any] | Создать DataFrame |
| `run_dataframe_operation` | dataframe_name: str, operation: str, operation_parameters: Dict[str, Any] | Выполнить операцию с DataFrame |



---

## TelegramTools - Telegram бот ✅

### 📝 Описание
Инструмент для отправки сообщений через Telegram Bot API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chat_id` | Union[str, int] | - | ID чата для отправки сообщений |
| `token` | Optional[str] | None | Telegram Bot токен (из TELEGRAM_TOKEN) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_message` | message: str | Отправить сообщение в чат |

---

## AWSLambdaTools - AWS Lambda ✅

### 📝 Описание
Инструмент для взаимодействия с AWS Lambda функциями.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `region_name` | str | "us-east-1" | Регион AWS для подключения |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_functions` |  | Список доступных Lambda функций |
| `invoke_function` | function_name: str, payload: str = "{}" | Вызов Lambda функции |



---

## AirflowTools - Apache Airflow ✅

### 📝 Описание
Инструмент для работы с Apache Airflow DAG файлами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dags_dir` | Optional[Union[Path, str]] | None | Директория для DAG файлов |
| `save_dag` | bool | True | Включить сохранение DAG файлов |
| `read_dag` | bool | True | Включить чтение DAG файлов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `save_dag_file` | contents: str, dag_file: str | Сохранить DAG в файл |
| `read_dag_file` | dag_file: str | Прочитать DAG файл |



---

## ApifyTools - Apify платформа ✅

### 📝 Описание
Инструмент для работы с Apify платформой веб-скрапинга и автоматизации.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `actors` | Optional[Union[str, List[str]]] | None | ID актеров для регистрации |
| `apify_api_token` | Optional[str] | None | API токен Apify (из APIFY_API_TOKEN) |

### 📋 Доступные функции

Функции динамически регистрируются на основе выбранных актеров. Каждый актер становится отдельной функцией.

| Function | Parameters | Description |
|----------|------------|-------------|
| `dynamic_actor_functions` | **kwargs | Функции создаются автоматически для каждого актера |



---

## ArxivTools - Академические статьи ✅

### 📝 Описание
Инструмент для поиска и чтения академических статей из ArXiv.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_arxiv` | bool | True | Включить поиск статей |
| `read_arxiv_papers` | bool | True | Включить чтение полных статей |
| `download_dir` | Optional[Path] | None | Директория для загрузки PDF |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_arxiv_and_return_articles` | query: str, num_articles: int = 10 | Поиск статей по запросу |
| `read_arxiv_papers` | id_list: List[str], pages_to_read: Optional[int] = None | Чтение полных статей |



---

## BrowserbaseTools - Браузерная автоматизация ✅

### 📝 Описание
Инструмент для автоматизации браузера через Browserbase API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Browserbase (из BROWSERBASE_API_KEY) |
| `project_id` | Optional[str] | None | ID проекта (из BROWSERBASE_PROJECT_ID) |
| `base_url` | Optional[str] | None | Базовый URL API (из BROWSERBASE_BASE_URL) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `navigate_to` | url: str, connect_url: Optional[str] = None | Навигация по URL |
| `screenshot` | path: str, full_page: bool = True, connect_url: Optional[str] = None | Создание скриншота |
| `get_page_content` | connect_url: Optional[str] = None | Получение HTML контента |
| `close_session` |  | Закрытие сессии браузера |



---

## BrightDataTools - Корпоративный веб-скрапинг ✅

### 📝 Описание
Инструмент для веб-скрапинга через Bright Data API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из BRIGHT_DATA_API_KEY) |
| `serp_zone` | str | "serp_api" | Зона для поисковых запросов |
| `web_unlocker_zone` | str | "web_unlocker1" | Зона для разблокировки веб-сайтов |
| `scrape_as_markdown` | bool | True | Включить скрапинг в Markdown |
| `get_screenshot` | bool | False | Включить создание скриншотов |
| `search_engine` | bool | True | Включить поиск в поисковых системах |
| `web_data_feed` | bool | True | Включить структурированные веб-данные |
| `verbose` | bool | False | Подробный вывод |
| `timeout` | int | 600 | Таймаут запросов в секундах |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `scrape_as_markdown` | url: str | Скрапинг страницы в формате Markdown |
| `get_screenshot` | agent: Agent, url: str, output_path: str = "screenshot.png" | Создание скриншота страницы |
| `search_engine` | query: str, engine: str = "google", num_results: int = 10, language: Optional[str] = None, country_code: Optional[str] = None | Поиск в поисковых системах |
| `web_data_feed` | source_type: str, url: str, num_of_reviews: Optional[int] = None | Получение структурированных данных |



---

## CalComTools - Календарное планирование ✅

### 📝 Описание
Инструмент для работы с Cal.com API для управления встречами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Cal.com (из CALCOM_API_KEY) |
| `event_type_id` | Optional[int] | None | ID типа события (из CALCOM_EVENT_TYPE_ID) |
| `user_timezone` | Optional[str] | None | Часовой пояс пользователя |
| `get_available_slots` | bool | True | Включить получение доступных слотов |
| `create_booking` | bool | True | Включить создание бронирований |
| `get_upcoming_bookings` | bool | True | Включить получение предстоящих встреч |
| `reschedule_booking` | bool | True | Включить перенос встреч |
| `cancel_booking` | bool | True | Включить отмену встреч |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_available_slots` | start_date: str, end_date: str | Получить доступные временные слоты |
| `create_booking` | start_time: str, name: str, email: str | Создать новое бронирование |
| `get_upcoming_bookings` | email: Optional[str] = None | Получить предстоящие встречи |
| `reschedule_booking` | booking_uid: str, new_start_time: str, reason: str | Перенести встречу |
| `cancel_booking` | booking_uid: str, reason: str | Отменить встречу |



---

## ClickUpTools - Управление проектами ✅

### 📝 Описание
Инструмент для работы с ClickUp API для управления задачами и проектами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ ClickUp (из CLICKUP_API_KEY) |
| `master_space_id` | Optional[str] | None | ID основного пространства (из MASTER_SPACE_ID) |
| `list_tasks` | bool | True | Включить просмотр задач |
| `create_task` | bool | True | Включить создание задач |
| `get_task` | bool | True | Включить получение задач |
| `update_task` | bool | True | Включить обновление задач |
| `delete_task` | bool | True | Включить удаление задач |
| `list_spaces` | bool | True | Включить просмотр пространств |
| `list_lists` | bool | True | Включить просмотр списков |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_tasks` | space_name: str | Список всех задач в пространстве |
| `create_task` | space_name: str, task_name: str, task_description: str | Создать новую задачу |
| `get_task` | task_id: str | Получить детали задачи |
| `update_task` | task_id: str, **kwargs | Обновить задачу |
| `delete_task` | task_id: str | Удалить задачу |
| `list_spaces` |  | Список всех пространств |
| `list_lists` | space_name: str | Список всех списков в пространстве |



---

## ConfluenceTools - Atlassian Confluence ✅

### 📝 Описание
Инструмент для работы с Atlassian Confluence API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | Optional[str] | None | Имя пользователя (из CONFLUENCE_USERNAME) |
| `password` | Optional[str] | None | Пароль |
| `url` | Optional[str] | None | URL экземпляра Confluence (из CONFLUENCE_URL) |
| `api_key` | Optional[str] | None | API ключ (из CONFLUENCE_API_KEY) |
| `verify_ssl` | bool | True | Проверять SSL сертификаты |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_page_content` | space_name: str, page_title: str, expand: Optional[str] = "body.storage" | Получить содержимое страницы |
| `get_space_key` | space_name: str | Получить ключ пространства |
| `create_page` | space_name: str, title: str, body: str, parent_id: Optional[str] = None | Создать новую страницу |
| `update_page` | page_id: str, title: str, body: str | Обновить существующую страницу |
| `get_all_space_detail` |  | Получить детали всех пространств |
| `get_all_page_from_space` | space_name: str | Получить все страницы из пространства |



---

## Crawl4aiTools - AI веб-краулинг ✅

### 📝 Описание
Инструмент для AI-powered веб-краулинга с использованием Crawl4AI.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_length` | Optional[int] | 5000 | Максимальная длина контента |
| `timeout` | int | 60 | Таймаут в секундах |
| `use_pruning` | bool | False | Использовать обрезку контента |
| `pruning_threshold` | float | 0.48 | Порог для обрезки |
| `bm25_threshold` | float | 1.0 | Порог BM25 для фильтрации |
| `headless` | bool | True | Запуск браузера в headless режиме |
| `wait_until` | str | "domcontentloaded" | Ожидание загрузки страницы |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `crawl` | url: Union[str, List[str]], search_query: Optional[str] = None | Краулинг URL и извлечение текстового контента |



---

## DalleTools - DALL-E генерация изображений ✅

### 📝 Описание
Инструмент для генерации изображений с помощью DALL-E OpenAI.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | "dall-e-3" | Модель DALL-E (dall-e-2, dall-e-3) |
| `n` | int | 1 | Количество изображений |
| `size` | Optional[Literal] | "1024x1024" | Размер изображения |
| `quality` | Literal["standard", "hd"] | "standard" | Качество изображения |
| `style` | Literal["vivid", "natural"] | "vivid" | Стиль изображения |
| `api_key` | Optional[str] | None | OpenAI API ключ (из OPENAI_API_KEY) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_image` | agent: Union[Agent, Team], prompt: str | Генерация изображения по описанию |



---

## DiscordTools - Discord интеграция ✅

### 📝 Описание
Инструмент для интеграции с Discord каналами и серверами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bot_token` | Optional[str] | None | Токен Discord бота (из DISCORD_BOT_TOKEN) |
| `enable_messaging` | bool | True | Включить отправку сообщений |
| `enable_history` | bool | True | Включить получение истории |
| `enable_channel_management` | bool | True | Включить управление каналами |
| `enable_message_management` | bool | True | Включить управление сообщениями |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_message` | channel_id: int, message: str | Отправить сообщение в канал |
| `get_channel_messages` | channel_id: int, limit: int = 100 | Получить историю сообщений канала |
| `get_channel_info` | channel_id: int | Получить информацию о канале |
| `list_channels` | guild_id: int | Список каналов сервера |
| `delete_message` | channel_id: int, message_id: int | Удалить сообщение |



---

## DuckDbTools - DuckDB аналитика ✅

### 📝 Описание
Инструмент для работы с DuckDB аналитической базой данных.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | Optional[str] | None | Путь к файлу базы данных |
| `connection` | Optional[duckdb.DuckDBPyConnection] | None | Готовое подключение |
| `init_commands` | Optional[List] | None | Команды инициализации |
| `read_only` | bool | False | Режим только для чтения |
| `config` | Optional[dict] | None | Конфигурация подключения |
| `run_queries` | bool | True | Включить выполнение запросов |
| `inspect_queries` | bool | False | Включить инспекцию запросов |
| `create_tables` | bool | True | Включить создание таблиц |
| `summarize_tables` | bool | True | Включить суммаризацию таблиц |
| `export_tables` | bool | False | Включить экспорт таблиц |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `show_tables` | show_tables: bool | Показать таблицы в базе данных |
| `describe_table` | table: str | Описать структуру таблицы |
| `run_query` | query: str | Выполнить SQL запрос |
| `inspect_query` | query: str | Инспектировать план запроса |
| `create_table_from_path` | path: str, table: Optional[str] = None, replace: bool = False | Создать таблицу из файла |
| `summarize_table` | table: str | Получить сводку по таблице |
| `export_table_to_path` | table: str, format: Optional[str] = "PARQUET", path: Optional[str] = None | Экспортировать таблицу |



---

## ElevenLabsTools - ElevenLabs голосовой AI ✅

### 📝 Описание
Инструмент для генерации речи и звуковых эффектов через ElevenLabs API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `voice_id` | str | "JBFqnCBsd6RMkjVDRZzb" | ID голоса |
| `api_key` | Optional[str] | None | API ключ (из ELEVEN_LABS_API_KEY) |
| `target_directory` | Optional[str] | None | Директория для сохранения файлов |
| `model_id` | str | "eleven_multilingual_v2" | ID модели |
| `output_format` | ElevenLabsAudioOutputFormat | "mp3_44100_64" | Формат аудио вывода |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_voices` |  | Получить список доступных голосов |
| `generate_sound_effect` | agent: Union[Agent, Team], prompt: str, duration_seconds: Optional[float] = None | Генерация звукового эффекта |
| `text_to_speech` | agent: Union[Agent, Team], prompt: str | Преобразование текста в речь |



---

## FalTools - Fal AI модели ✅

### 📝 Описание
Инструмент для работы с Fal AI платформой для запуска AI моделей.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Fal (из FAL_KEY) |
| `model` | str | "fal-ai/hunyuan-video" | Модель по умолчанию |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_media` | agent: Union[Agent, Team], prompt: str | Генерация медиа с помощью AI модели |
| `image_to_image` | agent: Union[Agent, Team], prompt: str, image_url: Optional[str] = None | Преобразование изображения в изображение |



---

## FirecrawlTools - Firecrawl сервис ✅

### 📝 Описание
Инструмент для веб-скрапинга и краулинга через Firecrawl API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из FIRECRAWL_API_KEY) |
| `formats` | Optional[List[str]] | None | Форматы для обработки |
| `limit` | int | 10 | Максимальное количество страниц |
| `poll_interval` | int | 30 | Интервал опроса в секундах |
| `scrape` | bool | True | Включить скрапинг |
| `crawl` | bool | False | Включить краулинг |
| `mapping` | bool | False | Включить маппинг сайта |
| `search` | bool | False | Включить поиск |
| `search_params` | Optional[Dict[str, Any]] | None | Параметры поиска |
| `api_url` | Optional[str] | "https://api.firecrawl.dev" | URL API |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `scrape_website` | url: str | Скрапинг веб-сайта |
| `crawl_website` | url: str, limit: Optional[int] = None | Краулинг веб-сайта |
| `map_website` | url: str | Маппинг структуры сайта |
| `search` | query: str, limit: Optional[int] = None | Поиск в интернете |



---

## GmailTools - Gmail интеграция ✅

### 📝 Описание
Мощный инструмент для работы с Gmail API - чтение, отправка, управление письмами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `get_latest_emails` | bool | True | Включить получение последних писем |
| `get_emails_from_user` | bool | True | Включить получение писем от пользователя |
| `get_unread_emails` | bool | True | Включить получение непрочитанных писем |
| `get_starred_emails` | bool | True | Включить получение помеченных писем |
| `get_emails_by_context` | bool | True | Включить поиск писем по контексту |
| `get_emails_by_date` | bool | True | Включить получение писем по дате |
| `get_emails_by_thread` | bool | True | Включить получение писем по треду |
| `create_draft_email` | bool | True | Включить создание черновиков |
| `send_email` | bool | True | Включить отправку писем |
| `send_email_reply` | bool | True | Включить отправку ответов |
| `search_emails` | bool | True | Включить поиск писем |
| `creds` | Optional[Credentials] | None | Готовые учетные данные |
| `credentials_path` | Optional[str] | None | Путь к файлу учетных данных |
| `token_path` | Optional[str] | None | Путь к файлу токена |
| `scopes` | Optional[List[str]] | None | OAuth области доступа |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_latest_emails` | count: int | Получить последние письма |
| `get_emails_from_user` | user: str, count: int | Получить письма от пользователя |
| `get_unread_emails` | count: int | Получить непрочитанные письма |
| `get_starred_emails` | count: int | Получить помеченные письма |
| `get_emails_by_context` | context: str, count: int | Найти письма по контексту |
| `get_emails_by_date` | start_date: int, range_in_days: Optional[int] = None, num_emails: Optional[int] = 10 | Получить письма по дате |
| `get_emails_by_thread` | thread_id: str | Получить письма из треда |
| `create_draft_email` | to: str, subject: str, body: str, cc: Optional[str] = None, attachments: Optional[Union[str, List[str]]] = None | Создать черновик |
| `send_email` | to: str, subject: str, body: str, cc: Optional[str] = None, attachments: Optional[Union[str, List[str]]] = None | Отправить письмо |
| `send_email_reply` | thread_id: str, message_id: str, to: str, subject: str, body: str, cc: Optional[str] = None, attachments: Optional[Union[str, List[str]]] = None | Ответить на письмо |
| `search_emails` | query: str, count: int | Поиск писем |



---

## GoogleBigQueryTools - Google BigQuery ✅

### 📝 Описание
Инструмент для работы с Google BigQuery аналитикой данных.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | str | - | Имя датасета |
| `project` | Optional[str] | None | ID проекта Google Cloud (из GOOGLE_CLOUD_PROJECT) |
| `location` | Optional[str] | None | Локация (из GOOGLE_CLOUD_LOCATION) |
| `list_tables` | Optional[bool] | True | Включить просмотр таблиц |
| `describe_table` | Optional[bool] | True | Включить описание таблиц |
| `run_sql_query` | Optional[bool] | True | Включить выполнение SQL запросов |
| `credentials` | Optional[Any] | None | Учетные данные Google Cloud |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_tables` |  | Список таблиц в датасете |
| `describe_table` | table_id: str | Описание схемы таблицы |
| `run_sql_query` | query: str | Выполнение BigQuery SQL запроса |



---

## GoogleSheetsTools - Google Таблицы ✅

### 📝 Описание
Инструмент для работы с Google Sheets API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scopes` | Optional[List[str]] | None | OAuth области доступа |
| `spreadsheet_id` | Optional[str] | None | ID таблицы |
| `spreadsheet_range` | Optional[str] | None | Диапазон в таблице |
| `creds` | Optional[Credentials] | None | Готовые учетные данные |
| `creds_path` | Optional[str] | None | Путь к файлу учетных данных |
| `token_path` | Optional[str] | None | Путь к файлу токена |
| `read` | bool | True | Включить операции чтения |
| `create` | bool | False | Включить создание таблиц |
| `update` | bool | False | Включить обновление данных |
| `duplicate` | bool | False | Включить дублирование таблиц |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `read_sheet` | spreadsheet_id: Optional[str] = None, spreadsheet_range: Optional[str] = None | Чтение данных из таблицы |
| `create_sheet` | title: str | Создание новой таблицы |
| `update_sheet` | data: List[List[Any]], spreadsheet_id: Optional[str] = None, range_name: Optional[str] = None | Обновление данных в таблице |
| `create_duplicate_sheet` | source_id: str, new_title: Optional[str] = None, copy_permissions: bool = True | Дублирование таблицы |



---

## HackerNewsTools - Hacker News API ✅

### 📝 Описание
Инструмент для получения новостей и информации о пользователях Hacker News.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `get_top_stories` | bool | True | Включить получение топ новостей |
| `get_user_details` | bool | True | Включить получение информации о пользователях |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_top_hackernews_stories` | num_stories: int = 10 | Получить топ новости |
| `get_user_details` | username: str | Получить информацию о пользователе |



---

## JiraTools - Atlassian Jira ✅

### 📝 Описание
Инструмент для работы с Atlassian Jira API для управления задачами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `server_url` | Optional[str] | None | URL сервера Jira (из JIRA_SERVER_URL) |
| `username` | Optional[str] | None | Имя пользователя (из JIRA_USERNAME) |
| `password` | Optional[str] | None | Пароль (из JIRA_PASSWORD) |
| `token` | Optional[str] | None | API токен (из JIRA_TOKEN) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_issue` | issue_key: str | Получить детали задачи |
| `create_issue` | project_key: str, summary: str, description: str, issuetype: str = "Task" | Создать новую задачу |
| `search_issues` | jql_str: str, max_results: int = 50 | Поиск задач по JQL |
| `add_comment` | issue_key: str, comment: str | Добавить комментарий к задаче |



---

## Mem0Tools - Управление памятью ✅

### 📝 Описание
Инструмент для управления памятью с помощью Mem0 платформы.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | Optional[Dict[str, Any]] | None | Конфигурация Mem0 |
| `api_key` | Optional[str] | None | API ключ (из MEM0_API_KEY) |
| `user_id` | Optional[str] | None | ID пользователя |
| `infer` | bool | True | Автоматическое извлечение фактов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `add_memory` | agent: Agent, content: Union[str, Dict[str, str]] | Добавить факты в память |
| `search_memory` | agent: Agent, query: str | Семантический поиск в памяти |
| `get_all_memories` | agent: Agent | Получить все воспоминания |
| `delete_all_memories` | agent: Agent | Удалить все воспоминания |



---

## CartesiaTools - Генерация речи ✅

### 📝 Описание
Инструмент для генерации высококачественной речи через Cartesia API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Cartesia (из CARTESIA_API_KEY) |
| `model_id` | str | "sonic-2" | ID модели для генерации речи |
| `default_voice_id` | str | "78ab82d5-25be-4f7d-82b3-7ad64e5b85b2" | ID голоса по умолчанию |
| `text_to_speech_enabled` | bool | True | Включить преобразование текста в речь |
| `list_voices_enabled` | bool | True | Включить список доступных голосов |
| `voice_localize_enabled` | bool | False | Включить локализацию голосов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `text_to_speech` | agent: Union[Agent, Team], transcript: str, voice_id: Optional[str] = None | Преобразование текста в речь |
| `list_voices` |  | Список доступных голосов |
| `localize_voice` | name: str, description: str, language: str, original_speaker_gender: str, voice_id: Optional[str] = None | Создание локализованного голоса |



---

## DaytonaTools - Удаленное выполнение кода ✅

### 📝 Описание
Инструмент для выполнения кода в удаленных песочницах Daytona.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Daytona (из DAYTONA_API_KEY) |
| `api_url` | Optional[str] | None | URL API Daytona (из DAYTONA_API_URL) |
| `sandbox_language` | Optional[CodeLanguage] | None | Язык программирования |
| `sandbox_target_region` | Optional[SandboxTargetRegion] | None | Регион песочницы |
| `sandbox_os` | Optional[str] | None | Операционная система (ubuntu) |
| `sandbox_os_user` | Optional[str] | None | Пользователь (root) |
| `sandbox_env_vars` | Optional[Dict[str, str]] | None | Переменные окружения |
| `sandbox_labels` | Optional[Dict[str, str]] | None | Метки песочницы |
| `sandbox_public` | Optional[bool] | None | Публичная песочница |
| `sandbox_auto_stop_interval` | Optional[int] | None | Интервал автоостановки (минуты) |
| `organization_id` | Optional[str] | None | ID организации |
| `timeout` | int | 300 | Таймаут в секундах (5 минут) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `run_python_code` | code: str | Выполнить Python код |
| `run_code` | code: str | Выполнить код (любой язык) |



---

## DesiVocalTools - Синтез голоса Desi ✅

### 📝 Описание
Инструмент для генерации речи на индийских языках через Desi Vocal API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из DESI_VOCAL_API_KEY) |
| `voice_id` | Optional[str] | "f27d74e5-ea71-4697-be3e-f04bbd80c1a8" | ID голоса по умолчанию |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_voices` |  | Список доступных голосов |
| `text_to_speech` | agent: Union[Agent, Team], prompt: str, voice_id: Optional[str] = None | Генерация аудио из текста |



---

## E2BTools - Интерпретатор кода ✅

### 📝 Описание
Мощный инструмент для выполнения кода, управления файлами и работы с песочницами E2B.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ E2B (из E2B_API_KEY) |
| `run_code` | bool | True | Включить выполнение кода |
| `upload_file` | bool | True | Включить загрузку файлов |
| `download_result` | bool | True | Включить скачивание результатов |
| `filesystem` | bool | False | Включить файловые операции |
| `internet_access` | bool | False | Включить интернет доступ |
| `sandbox_management` | bool | False | Включить управление песочницами |
| `timeout` | int | 300 | Таймаут песочницы (5 минут) |
| `sandbox_options` | Optional[Dict[str, Any]] | None | Дополнительные опции песочницы |
| `command_execution` | bool | False | Включить выполнение команд |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `run_python_code` | code: str | Выполнить Python код |
| `upload_file` | file_path: str, sandbox_path: Optional[str] = None | Загрузить файл в песочницу |
| `download_png_result` | agent: Union[Agent, Team], result_index: int = 0, output_path: Optional[str] = None | Скачать PNG результат |
| `download_chart_data` | agent: Agent, result_index: int = 0, output_path: Optional[str] = None, add_as_artifact: bool = True | Скачать данные графика |
| `download_file_from_sandbox` | sandbox_path: str, local_path: Optional[str] = None | Скачать файл из песочницы |
| `list_files` | directory_path: str = "/" | Список файлов в директории |
| `read_file_content` | file_path: str, encoding: str = "utf-8" | Прочитать содержимое файла |
| `write_file_content` | file_path: str, content: str | Записать содержимое в файл |
| `run_command` | command: str, on_stdout: Optional[Callable] = None, on_stderr: Optional[Callable] = None, background: bool = False | Выполнить команду оболочки |



---

## GiphyTools - Поиск GIF ✅

### 📝 Описание
Инструмент для поиска GIF анимаций через Giphy API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Giphy (из GIPHY_API_KEY) |
| `limit` | int | 1 | Количество GIF для возврата |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_gifs` | agent: Union[Agent, Team], query: str | Поиск GIF по запросу |



---

## GoogleCalendarTools - Google Календарь ✅

### 📝 Описание
Инструмент для работы с Google Calendar API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `credentials_path` | Optional[str] | None | Путь к файлу credentials.json |
| `token_path` | Optional[str] | None | Путь к файлу token.json |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `list_events` | limit: int = 10, date_from: str = today | Список событий календаря |
| `create_event` | start_datetime: str, end_datetime: str, title: Optional[str] = None, description: Optional[str] = None, location: Optional[str] = None, timezone: Optional[str] = None, attendees: List[str] = [], send_updates: Optional[str] = "all", add_google_meet_link: Optional[bool] = False | Создать событие |



---

## GoogleMapTools - Google Карты ✅

### 📝 Описание
Инструмент для работы с Google Maps API - поиск мест, маршруты, геокодирование.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | Optional[str] | None | API ключ Google Maps (из GOOGLE_MAPS_API_KEY) |
| `search_places` | bool | True | Включить поиск мест |
| `get_directions` | bool | True | Включить маршруты |
| `validate_address` | bool | True | Включить валидацию адресов |
| `geocode_address` | bool | True | Включить геокодирование |
| `reverse_geocode` | bool | True | Включить обратное геокодирование |
| `get_distance_matrix` | bool | True | Включить матрицу расстояний |
| `get_elevation` | bool | True | Включить данные высоты |
| `get_timezone` | bool | True | Включить данные часового пояса |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_places` | query: str | Поиск мест |
| `get_directions` | origin: str, destination: str, mode: str = "driving", departure_time: Optional[datetime] = None, avoid: Optional[List[str]] = None | Получить маршрут |
| `validate_address` | address: str, region_code: str = "US", locality: Optional[str] = None, enable_usps_cass: bool = False | Валидация адреса |
| `geocode_address` | address: str, region: Optional[str] = None | Геокодирование адреса |
| `reverse_geocode` | lat: float, lng: float, result_type: Optional[List[str]] = None, location_type: Optional[List[str]] = None | Обратное геокодирование |
| `get_distance_matrix` | origins: List[str], destinations: List[str], mode: str = "driving", departure_time: Optional[datetime] = None, avoid: Optional[List[str]] = None | Матрица расстояний |
| `get_elevation` | lat: float, lng: float | Данные высоты |
| `get_timezone` | lat: float, lng: float, timestamp: Optional[datetime] = None | Данные часового пояса |



---

## JinaReaderTools - Веб-чтение ✅

### 📝 Описание
Инструмент для чтения веб-страниц и поиска через Jina Reader API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Jina (из JINA_API_KEY) |
| `base_url` | str | "https://r.jina.ai/" | Базовый URL для чтения |
| `search_url` | str | "https://s.jina.ai/" | URL для поиска |
| `max_content_length` | int | 10000 | Максимальная длина контента |
| `timeout` | Optional[int] | None | Таймаут запросов |
| `read_url` | bool | True | Включить чтение URL |
| `search_query` | bool | False | Включить веб-поиск |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `read_url` | url: str | Чтение URL и возврат контента |
| `search_query` | query: str | Веб-поиск через Jina |



---

## KnowledgeTools - База знаний ✅

### 📝 Описание
Инструмент для работы с базой знаний агента - поиск, анализ, рассуждения.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `knowledge` | AgentKnowledge | - | База знаний агента |
| `think` | bool | True | Включить функцию рассуждений |
| `search` | bool | True | Включить поиск в базе знаний |
| `analyze` | bool | True | Включить анализ результатов |
| `instructions` | Optional[str] | None | Пользовательские инструкции |
| `add_instructions` | bool | True | Добавить инструкции по использованию |
| `add_few_shot` | bool | False | Добавить примеры использования |
| `few_shot_examples` | Optional[str] | None | Пользовательские примеры |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `think` | agent: Union[Agent, Team], thought: str | Записать размышления и планирование |
| `search` | agent: Union[Agent, Team], query: str | Поиск в базе знаний |
| `analyze` | agent: Union[Agent, Team], analysis: str | Анализ найденной информации |



---

## LinearTools - Linear управление задачами ✅

### 📝 Описание
Инструмент для работы с Linear API - управление задачами и проектами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `get_user_details` | bool | True | Включить получение данных пользователя |
| `get_teams_details` | bool | True | Включить получение данных команд |
| `get_issue_details` | bool | True | Включить получение данных задач |
| `create_issue` | bool | True | Включить создание задач |
| `update_issue` | bool | True | Включить обновление задач |
| `get_user_assigned_issues` | bool | True | Включить задачи пользователя |
| `get_workflow_issues` | bool | True | Включить задачи по workflow |
| `get_high_priority_issues` | bool | True | Включить высокоприоритетные задачи |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_user_details` |  | Получить данные аутентифицированного пользователя |
| `get_teams_details` |  | Получить данные команд |
| `get_issue_details` | issue_id: str | Получить детали задачи |
| `create_issue` | title: str, description: str, team_id: str, project_id: Optional[str] = None, assignee_id: Optional[str] = None | Создать задачу |
| `update_issue` | issue_id: str, title: Optional[str] | Обновить задачу |
| `get_user_assigned_issues` | user_id: str | Получить задачи пользователя |
| `get_workflow_issues` | workflow_id: str | Получить задачи workflow |
| `get_high_priority_issues` |  | Получить высокоприоритетные задачи |



---

## LocalFileSystemTools - Локальная файловая система ✅

### 📝 Описание
Инструмент для работы с локальной файловой системой.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target_directory` | Optional[str] | None | Целевая директория (по умолчанию текущая) |
| `default_extension` | str | "txt" | Расширение файлов по умолчанию |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `write_file` | content: str, filename: Optional[str] = None, directory: Optional[str] = None, extension: Optional[str] = None | Записать содержимое в файл |



---

## MLXTranscribeTools - Транскрипция аудио ✅

### 📝 Описание
Инструмент для транскрипции аудио с использованием MLX Whisper (оптимизирован для Apple Silicon).

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | Optional[Path] | None | Базовая директория для файлов |
| `read_files_in_base_dir` | bool | True | Включить чтение файлов из директории |
| `path_or_hf_repo` | str | "mlx-community/whisper-large-v3-turbo" | Модель или репозиторий |
| `verbose` | Optional[bool] | None | Подробный вывод |
| `temperature` | Optional[Union[float, Tuple[float, ...]]] | None | Температура для декодирования |
| `compression_ratio_threshold` | Optional[float] | None | Порог сжатия |
| `logprob_threshold` | Optional[float] | None | Порог логарифмической вероятности |
| `no_speech_threshold` | Optional[float] | None | Порог отсутствия речи |
| `condition_on_previous_text` | Optional[bool] | None | Использовать предыдущий текст |
| `initial_prompt` | Optional[str] | None | Начальный промпт |
| `word_timestamps` | Optional[bool] | None | Временные метки слов |
| `prepend_punctuations` | Optional[str] | None | Префиксная пунктуация |
| `append_punctuations` | Optional[str] | None | Суффиксная пунктуация |
| `clip_timestamps` | Optional[Union[str, List[float]]] | None | Обрезка временных меток |
| `hallucination_silence_threshold` | Optional[float] | None | Порог тишины для галлюцинаций |
| `decode_options` | Optional[dict] | None | Дополнительные опции декодирования |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `transcribe` | file_name: str | Транскрибировать аудио файл |
| `read_files` |  | Получить список файлов в базовой директории |



---

## ModelsLabTools - Генерация медиа ✅

### 📝 Описание
Инструмент для генерации видео, аудио и изображений через Models Lab API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из MODELS_LAB_API_KEY) |
| `wait_for_completion` | bool | False | Ожидать завершения генерации |
| `add_to_eta` | int | 15 | Дополнительное время ожидания |
| `max_wait_time` | int | 60 | Максимальное время ожидания |
| `file_type` | FileType | FileType.MP4 | Тип файла (MP4, MP3, GIF) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_media` | agent: Union[Agent, Team], prompt: str | Генерация медиа по описанию |



---

## MoviePyVideoTools - Обработка видео ✅

### 📝 Описание
Инструмент для обработки видео, добавления субтитров и работы с аудио.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `process_video` | bool | True | Включить обработку видео |
| `generate_captions` | bool | True | Включить генерацию субтитров |
| `embed_captions` | bool | True | Включить встраивание субтитров |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `extract_audio` | video_path: str, output_path: str | Извлечь аудио из видео |
| `create_srt` | transcription: str, output_path: str | Создать SRT файл субтитров |
| `embed_captions` | video_path: str, srt_path: str, output_path: Optional[str] = None, font_size: int = 24, font_color: str = "white", stroke_color: str = "black", stroke_width: int = 1 | Встроить субтитры в видео |



---

## Newspaper4kTools - Чтение статей ✅

### 📝 Описание
Инструмент для извлечения текста статей из веб-страниц.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `read_article` | bool | True | Включить чтение статей |
| `include_summary` | bool | False | Включить краткое изложение |
| `article_length` | Optional[int] | None | Ограничение длины статьи |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `read_article` | url: str | Прочитать статью по URL |



---

## OpenCVTools - Компьютерное зрение ✅

### 📝 Описание
Инструмент для захвата изображений и видео с веб-камеры.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `show_preview` | bool | False | Показывать предварительный просмотр |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `capture_image` | agent: Agent, prompt: str = "Webcam capture" | Захватить изображение с веб-камеры |
| `capture_video` | agent: Agent, duration: int = 10, prompt: str = "Webcam video capture" | Захватить видео с веб-камеры |



---

## OpenBBTools - Финансовые данные ✅

### 📝 Описание
Инструмент для получения финансовых данных через OpenBB платформу.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `obb` | Optional[Any] | None | Экземпляр OpenBB |
| `openbb_pat` | Optional[str] | None | Personal Access Token (из OPENBB_PAT) |
| `provider` | Literal | "yfinance" | Провайдер данных |
| `stock_price` | bool | True | Включить цены акций |
| `search_symbols` | bool | False | Включить поиск символов |
| `company_news` | bool | False | Включить новости компаний |
| `company_profile` | bool | False | Включить профили компаний |
| `price_targets` | bool | False | Включить целевые цены |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_stock_price` | symbol: str | Получить текущую цену акции |
| `search_company_symbol` | company_name: str | Поиск тикера компании |
| `get_company_news` | symbol: str, num_stories: int = 10 | Получить новости компании |
| `get_company_profile` | symbol: str | Получить профиль компании |
| `get_price_targets` | symbol: str | Получить целевые цены |



---

## PubmedTools - Медицинские исследования ✅

### 📝 Описание
Инструмент для поиска медицинских статей в базе данных PubMed.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `email` | str | "your_email@example.com" | Email для API запросов |
| `max_results` | Optional[int] | None | Максимальное количество результатов |
| `results_expanded` | bool | False | Расширенный формат результатов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_pubmed` | query: str, max_results: Optional[int] = 10 | Поиск статей в PubMed |



---

## ReplicateTools - AI модели ✅

### 📝 Описание
Инструмент для выполнения AI моделей через платформу Replicate.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API токен (из REPLICATE_API_TOKEN) |
| `model` | str | "minimax/video-01" | Модель по умолчанию |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_media` | agent: Union[Agent, Team], prompt: str | Генерация медиа через AI модель |



---

## ResendTools - Отправка email ✅

### 📝 Описание
Инструмент для отправки email через Resend API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из RESEND_API_KEY) |
| `from_email` | Optional[str] | None | Email отправителя |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_email` | to_email: str, subject: str, body: str | Отправить email |



---

## LumaLabTools - Генерация видео ✅

### 📝 Описание
Инструмент для генерации видео через Luma Labs API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из LUMA_API_KEY) |
| `wait_for_completion` | bool | True | Ожидать завершения генерации |
| `max_wait_time` | int | 300 | Максимальное время ожидания |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_video` | agent: Union[Agent, Team], prompt: str | Генерация видео по описанию |



---

## SpiderTools - Веб-краулинг ✅

### 📝 Описание
Инструмент для быстрого веб-краулинга через Spider API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ (из SPIDER_API_KEY) |
| `scrape` | bool | True | Включить скрапинг |
| `crawl` | bool | False | Включить краулинг |
| `search` | bool | False | Включить поиск |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `scrape_url` | url: str | Скрапинг одной страницы |
| `crawl_website` | url: str, limit: int = 10 | Краулинг веб-сайта |
| `search_web` | query: str, limit: int = 10 | Поиск в интернете |



---

## TodoistTools - Управление задачами ✅

### 📝 Описание
Инструмент для работы с Todoist - управление задачами и проектами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_token` | Optional[str] | None | API токен (из TODOIST_API_TOKEN) |
| `create_task` | bool | True | Включить создание задач |
| `get_tasks` | bool | True | Включить получение задач |
| `update_task` | bool | True | Включить обновление задач |
| `close_task` | bool | True | Включить закрытие задач |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_task` | content: str, project_id: Optional[str] = None, due_string: Optional[str] = None | Создать задачу |
| `get_tasks` | project_id: Optional[str] = None, filter_query: Optional[str] = None | Получить список задач |
| `update_task` | task_id: str, content: Optional[str] = None, due_string: Optional[str] = None | Обновить задачу |
| `close_task` | task_id: str | Закрыть задачу |



---

## SearxngTools - Мета-поиск ✅

### 📝 Описание
Инструмент для поиска через SearxNG - приватный мета-поисковик.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | str | "https://searx.org" | Базовый URL SearxNG |
| `categories` | Optional[List[str]] | None | Категории поиска |
| `engines` | Optional[List[str]] | None | Поисковые движки |
| `language` | str | "en" | Язык поиска |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search` | query: str, num_results: int = 10, categories: Optional[List[str]] = None | Поиск через SearxNG |



---

## ZoomTools - Видеоконференции Zoom ✅

### 📝 Описание
Инструмент для управления Zoom встречами через API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `account_id` | Optional[str] | None | ID аккаунта Zoom (из ZOOM_ACCOUNT_ID) |
| `client_id` | Optional[str] | None | Client ID для аутентификации (из ZOOM_CLIENT_ID) |
| `client_secret` | Optional[str] | None | Client Secret для аутентификации (из ZOOM_CLIENT_SECRET) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `schedule_meeting` | topic: str, start_time: str, duration: int, timezone: str = "UTC" | Запланировать встречу |
| `get_upcoming_meetings` | user_id: str = "me" | Получить предстоящие встречи |
| `list_meetings` | user_id: str = "me", type: str = "scheduled" | Список всех встреч |
| `get_meeting_recordings` | meeting_id: str, include_download_token: bool = False, token_ttl: Optional[int] = None | Получить записи встречи |
| `delete_meeting` | meeting_id: str, schedule_for_reminder: bool = True | Удалить встречу |
| `get_meeting` | meeting_id: str | Получить детали встречи |



---

## XTools - Twitter/X API ✅

### 📝 Описание
Инструмент для работы с Twitter/X API - посты, поиск, DM, таймлайн.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bearer_token` | Optional[str] | None | Bearer токен (из X_BEARER_TOKEN) |
| `consumer_key` | Optional[str] | None | Consumer Key (из X_CONSUMER_KEY) |
| `consumer_secret` | Optional[str] | None | Consumer Secret (из X_CONSUMER_SECRET) |
| `access_token` | Optional[str] | None | Access Token (из X_ACCESS_TOKEN) |
| `access_token_secret` | Optional[str] | None | Access Token Secret (из X_ACCESS_TOKEN_SECRET) |
| `include_post_metrics` | bool | False | Включать метрики постов |
| `wait_on_rate_limit` | bool | False | Ожидать при достижении лимита |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_post` | text: str | Создать новый пост |
| `reply_to_post` | post_id: str, text: str | Ответить на пост |
| `send_dm` | recipient: str, text: str | Отправить личное сообщение |
| `get_user_info` | username: str | Получить информацию о пользователе |
| `get_home_timeline` | max_results: int = 10 | Получить домашний таймлайн |
| `search_posts` | query: str, max_results: int = 10 | Поиск постов |



---

## WhatsAppTools - WhatsApp Business ✅

### 📝 Описание
Инструмент для отправки сообщений через WhatsApp Business API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `access_token` | Optional[str] | None | Access токен WhatsApp (из WHATSAPP_ACCESS_TOKEN) |
| `phone_number_id` | Optional[str] | None | ID номера телефона (из WHATSAPP_PHONE_NUMBER_ID) |
| `version` | str | "v22.0" | Версия API |
| `recipient_waid` | Optional[str] | None | ID получателя по умолчанию |
| `async_mode` | bool | False | Асинхронный режим |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_text_message_sync` | text: str, recipient: Optional[str] = None, preview_url: bool = False, recipient_type: str = "individual" | Отправить текстовое сообщение (синхронно) |
| `send_template_message_sync` | recipient: Optional[str] = None, template_name: str = "", language_code: str = "en_US", components: Optional[List[Dict]] = None | Отправить шаблонное сообщение (синхронно) |
| `send_text_message_async` | text: str, recipient: Optional[str] = None, preview_url: bool = False, recipient_type: str = "individual" | Отправить текстовое сообщение (асинхронно) |
| `send_template_message_async` | recipient: Optional[str] = None, template_name: str = "", language_code: str = "en_US", components: Optional[List[Dict]] = None | Отправить шаблонное сообщение (асинхронно) |



---

## TwilioTools - SMS и звонки ✅

### 📝 Описание
Инструмент для отправки SMS и управления звонками через Twilio API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `account_sid` | Optional[str] | None | Account SID Twilio (из TWILIO_ACCOUNT_SID) |
| `auth_token` | Optional[str] | None | Auth Token (из TWILIO_AUTH_TOKEN) |
| `api_key` | Optional[str] | None | API Key (из TWILIO_API_KEY) |
| `api_secret` | Optional[str] | None | API Secret (из TWILIO_API_SECRET) |
| `region` | Optional[str] | None | Регион Twilio |
| `edge` | Optional[str] | None | Edge локация |
| `debug` | bool | False | Включить отладку |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_sms` | to: str, from_: str, body: str | Отправить SMS сообщение |
| `get_call_details` | call_sid: str | Получить детали звонка |
| `list_messages` | limit: int = 20 | Список последних SMS |



---

## TrelloTools - Управление проектами ✅

### 📝 Описание
Инструмент для работы с Trello досками, списками и карточками.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Trello (из TRELLO_API_KEY) |
| `api_secret` | Optional[str] | None | API Secret (из TRELLO_API_SECRET) |
| `token` | Optional[str] | None | Токен авторизации (из TRELLO_TOKEN) |
| `create_card` | bool | True | Включить создание карточек |
| `get_board_lists` | bool | True | Включить получение списков доски |
| `move_card` | bool | True | Включить перемещение карточек |
| `get_cards` | bool | True | Включить получение карточек |
| `create_board` | bool | True | Включить создание досок |
| `create_list` | bool | True | Включить создание списков |
| `list_boards` | bool | True | Включить список досок |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_card` | board_id: str, list_name: str, card_title: str, description: str = "" | Создать карточку |
| `get_board_lists` | board_id: str | Получить списки доски |
| `move_card` | card_id: str, list_id: str | Переместить карточку |
| `get_cards` | list_id: str | Получить карточки списка |
| `create_board` | name: str, default_lists: bool = False | Создать доску |
| `create_list` | board_id: str, list_name: str, pos: str = "bottom" | Создать список |
| `list_boards` | board_filter: str = "all" | Список досок пользователя |



---

## ThinkingTools - Размышления агента ✅

### 📝 Описание
Инструмент для записи размышлений и планирования агента.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `think` | bool | True | Включить функцию размышлений |
| `instructions` | Optional[str] | None | Пользовательские инструкции |
| `add_instructions` | bool | False | Добавить инструкции в систему |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `think` | agent: Union[Agent, Team], thought: str | Записать размышление и вернуть полный лог |



---

## SleepTools - Задержки ✅

### 📝 Описание
Простой инструмент для создания задержек в выполнении.

### 🔧 Параметры конструктора

Этот инструмент не имеет настраиваемых параметров.

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `sleep` | seconds: int | Приостановить выполнение на указанное количество секунд |



---

## ScrapeGraphTools - Умный скрапинг ✅

### 📝 Описание
Инструмент для умного скрапинга веб-страниц с использованием ИИ.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ ScrapeGraph (из SGAI_API_KEY) |
| `smartscraper` | bool | True | Включить умный скрапинг |
| `markdownify` | bool | False | Включить конвертацию в Markdown |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `smartscraper` | url: str, prompt: str | Извлечь структурированные данные с помощью ИИ |
| `markdownify` | url: str | Конвертировать веб-страницу в Markdown |



---

## ZendeskTools - Поддержка клиентов ✅

### 📝 Описание
Инструмент для поиска статей в Zendesk Help Center.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | Optional[str] | None | Имя пользователя (из ZENDESK_USERNAME) |
| `password` | Optional[str] | None | Пароль (из ZENDESK_PW) |
| `company_name` | Optional[str] | None | Название компании (из ZENDESK_COMPANY_NAME) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `search_zendesk` | search_string: str | Поиск статей в Zendesk Help Center |



---

## WebexTools - Видеоконференции WebEx ✅

### 📝 Описание
Инструмент для отправки сообщений и управления комнатами в Cisco WebEx.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `access_token` | Optional[str] | None | Токен доступа WebEx (из WEBEX_ACCESS_TOKEN) |
| `send_message` | bool | True | Включить отправку сообщений |
| `list_rooms` | bool | True | Включить список комнат |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_message` | room_id: str, text: str | Отправить сообщение в комнату |
| `list_rooms` |  | Получить список всех комнат |



---

## AWSSESTool - AWS SES Email ✅

### 📝 Описание
Инструмент для отправки email через Amazon SES.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sender_email` | Optional[str] | None | Email отправителя |
| `sender_name` | Optional[str] | None | Имя отправителя |
| `region_name` | str | "us-east-1" | Регион AWS |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `send_email` | subject: str, body: str, receiver_email: str | Отправить email через AWS SES |



---

## BaiduSearchTools - Поиск Baidu ✅

### 📝 Описание
Инструмент для поиска в китайской поисковой системе Baidu.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fixed_max_results` | Optional[int] | None | Фиксированное количество результатов |
| `fixed_language` | Optional[str] | None | Фиксированный язык поиска |
| `headers` | Optional[Any] | None | HTTP заголовки |
| `proxy` | Optional[str] | None | Прокси сервер |
| `timeout` | Optional[int] | 10 | Таймаут запросов |
| `debug` | Optional[bool] | False | Режим отладки |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `baidu_search` | query: str, max_results: int = 5, language: str = "zh" | Поиск в Baidu |



---

## WebsiteTools - Работа с веб-сайтами ✅

### 📝 Описание
Инструмент для чтения веб-сайтов и добавления их в базу знаний.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `knowledge_base` | Optional[Union[WebsiteKnowledgeBase, CombinedKnowledgeBase]] | None | База знаний для веб-сайтов |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `add_website_to_knowledge_base` | url: str | Добавить веб-сайт в базу знаний |
| `add_website_to_combined_knowledge_base` | url: str | Добавить в комбинированную базу знаний |
| `read_url` | url: str | Прочитать содержимое URL |



---

## FunctionTools - Базовые функции ✅

### 📝 Описание
Основной инструмент для создания и выполнения пользовательских функций.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | - | Название функции |
| `description` | Optional[str] | None | Описание функции |
| `parameters` | Dict[str, Any] | {} | JSON Schema параметров |
| `strict` | Optional[bool] | None | Строгая схема |
| `entrypoint` | Optional[Callable] | None | Точка входа функции |
| `skip_entrypoint_processing` | bool | False | Пропустить обработку точки входа |
| `show_result` | bool | False | Показывать результат |
| `requires_confirmation` | Optional[bool] | None | Требует подтверждения |
| `cache_results` | bool | False | Кэшировать результаты |

### 📋 Доступные функции

Динамические функции на основе переданной точки входа и параметров.



---

## VisualizationTools - Визуализация данных ✅

### 📝 Описание
Инструмент для создания графиков и визуализаций данных.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `save_and_run` | bool | True | Сохранять и выполнять код |
| `base_dir` | Optional[Path] | None | Базовая директория |
| `read_files` | bool | False | Читать файлы |
| `list_files` | bool | False | Просматривать файлы |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `create_chart` | data: Any, chart_type: str, title: str, **kwargs | Создать график |
| `save_chart` | chart: Any, filename: str | Сохранить график |
| `create_visualization` | data: Dict, visualization_type: str | Создать визуализацию |



---

## ZepTools - Управление памятью ✅

### 📝 Описание
Инструмент для управления долгосрочной памятью и контекстом через Zep Cloud API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `session_id` | Optional[str] | None | ID сессии (автоматически генерируется если не указан) |
| `user_id` | Optional[str] | None | ID пользователя (автоматически генерируется если не указан) |
| `api_key` | Optional[str] | None | API ключ Zep (из ZEP_API_KEY) |
| `ignore_assistant_messages` | bool | False | Игнорировать сообщения ассистента |
| `add_zep_message` | bool | True | Включить добавление сообщений |
| `get_zep_memory` | bool | True | Включить получение памяти |
| `search_zep_memory` | bool | True | Включить поиск в памяти |
| `instructions` | Optional[str] | None | Пользовательские инструкции |
| `add_instructions` | bool | False | Добавить инструкции в систему |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `add_zep_message` | role: str, content: str | Добавить сообщение в память сессии |
| `get_zep_memory` | memory_type: str = "context" | Получить память сессии (context/messages/relevant_facts) |
| `search_zep_memory` | query: str, search_scope: str = "edges" | Поиск в знаниевом графе пользователя |



---

## MCPTools - Model Context Protocol ✅

### 📝 Описание
Универсальный инструмент для подключения MCP серверов и использования их инструментов.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `command` | Optional[str] | None | Команда для запуска MCP сервера |
| `url` | Optional[str] | None | URL для SSE/HTTP подключения |
| `env` | Optional[dict] | None | Переменные окружения для сервера |
| `transport` | Literal | "stdio" | Протокол транспорта (stdio/sse/streamable-http) |
| `server_params` | Optional[Union] | None | Параметры сервера |
| `session` | Optional[ClientSession] | None | Готовая сессия клиента |
| `timeout_seconds` | int | 5 | Таймаут чтения в секундах |
| `client` | Optional[Any] | None | Базовый MCP клиент |
| `include_tools` | Optional[List[str]] | None | Список включаемых инструментов |
| `exclude_tools` | Optional[List[str]] | None | Список исключаемых инструментов |

### 📋 Доступные функции

Динамические функции на основе подключенных MCP серверов.



---

## ReasoningTools - Структурированное мышление ✅

### 📝 Описание
Инструмент для пошагового рассуждения и анализа с записью логики принятия решений.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `think` | bool | True | Включить функцию размышлений |
| `analyze` | bool | True | Включить функцию анализа |
| `instructions` | Optional[str] | None | Пользовательские инструкции |
| `add_instructions` | bool | False | Добавить инструкции в систему |
| `add_few_shot` | bool | False | Добавить примеры использования |
| `few_shot_examples` | Optional[str] | None | Пользовательские примеры |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `think` | agent: Union[Agent, Team], title: str, thought: str, action: Optional[str] = None, confidence: float = 0.8 | Записать шаг размышления |
| `analyze` | agent: Union[Agent, Team], title: str, result: str, analysis: str, next_action: str = "continue", confidence: float = 0.8 | Проанализировать результаты |



---

## UserControlFlowTools - Интерактивный ввод ✅

### 📝 Описание
Инструмент для прерывания выполнения агента и запроса данных у пользователя.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instructions` | Optional[str] | None | Пользовательские инструкции |
| `add_instructions` | bool | True | Добавить инструкции в систему |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_user_input` | user_input_fields: List[dict] | Запросить ввод пользователя для указанных полей |



---

## WebTools - Веб-утилиты ✅

### 📝 Описание
Базовые инструменты для работы с веб-ресурсами.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `retries` | int | 3 | Количество попыток при ошибках |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `expand_url` | url: str | Расширить сокращенный URL до полного |



---

## NewspaperTools - Извлечение статей ✅

### 📝 Описание
Инструмент для извлечения текста статей из URL с использованием newspaper3k.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `get_article_text` | bool | True | Включить извлечение текста статей |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_article_text` | url: str | Извлечь текст статьи по URL |



---

## GeminiTools - Google Gemini API ✅

### 📝 Описание
Инструмент для генерации изображений и видео через Google Gemini API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Google (из GOOGLE_API_KEY) |
| `vertexai` | bool | False | Использовать Vertex AI |
| `project_id` | Optional[str] | None | ID проекта Google Cloud |
| `location` | Optional[str] | None | Локация Google Cloud |
| `image_generation_model` | str | "imagen-3.0-generate-002" | Модель для генерации изображений |
| `video_generation_model` | str | "veo-2.0-generate-001" | Модель для генерации видео |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_image` | agent: Agent, prompt: str | Генерация изображения через Imagen |
| `generate_video` | agent: Agent, prompt: str | Генерация видео через Veo (требует Vertex AI) |



---

## GroqTools - Groq API ✅

### 📝 Описание
Инструмент для высокоскоростной обработки аудио через Groq API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Groq (из GROQ_API_KEY) |
| `transcription_model` | str | "whisper-large-v3" | Модель для транскрипции |
| `translation_model` | str | "whisper-large-v3" | Модель для перевода |
| `tts_model` | str | "playai-tts" | Модель для синтеза речи |
| `tts_voice` | str | "Chip-PlayAI" | Голос для TTS |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `transcribe_audio` | audio_source: str | Транскрибировать аудио файл или URL |
| `translate_audio` | audio_source: str | Перевести аудио на английский |
| `generate_speech` | agent: Agent, text_input: str | Генерация речи из текста |



---

## NebiusTools - Nebius AI Studio ✅

### 📝 Описание
Инструмент для генерации изображений через Nebius AI Studio API.

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | API ключ Nebius (из NEBIUS_API_KEY) |
| `base_url` | str | "https://api.studio.nebius.com/v1" | Базовый URL API |
| `image_model` | str | "black-forest-labs/flux-schnell" | Модель генерации (flux-schnell/flux-dev/sdxl) |
| `image_quality` | Optional[str] | "standard" | Качество изображения |
| `image_size` | Optional[str] | "1024x1024" | Размер изображения |
| `image_style` | Optional[str] | None | Стиль изображения |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_image` | agent: Agent, prompt: str | Генерация изображения через FLUX модели |



---

## AzureOpenAITools - Azure OpenAI ✅

### 📝 Описание
Инструмент для работы с Azure OpenAI сервисами (DALL-E генерация).

### 🔧 Параметры конструктора

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | Optional[str] | None | Azure OpenAI API ключ (из AZURE_OPENAI_API_KEY) |
| `azure_endpoint` | Optional[str] | None | Azure endpoint (из AZURE_OPENAI_ENDPOINT) |
| `api_version` | Optional[str] | None | Версия API (из AZURE_OPENAI_API_VERSION) |
| `image_deployment` | Optional[str] | None | Deployment для изображений (из AZURE_OPENAI_IMAGE_DEPLOYMENT) |
| `image_model` | str | "dall-e-3" | Модель для генерации (dall-e-2/dall-e-3) |
| `image_quality` | Literal | "standard" | Качество изображения (standard/hd) |

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `generate_image` | agent: Agent, prompt: str, n: int = 1, size: Optional[str] = "1024x1024", style: str = "vivid" | Генерация изображений через DALL-E |



---

## StreamlitComponents - Streamlit UI ✅

### 📝 Описание
Набор готовых UI компонентов для Streamlit приложений.

### 🔧 Параметры конструктора

Компоненты используются как отдельные функции без общего конструктора.

### 📋 Доступные функции

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_username_sidebar` |  | Боковая панель для ввода имени пользователя |
| `reload_button_sidebar` | text: str = "Reload Session", **kwargs | Кнопка перезагрузки сессии |
| `check_password` | password_env_var: str = "APP_PASSWORD" | Проверка пароля приложения |
| `get_openai_key_sidebar` |  | Боковая панель для ввода OpenAI API ключа |

 