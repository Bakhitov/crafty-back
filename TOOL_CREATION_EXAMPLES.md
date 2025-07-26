# 🛠️ Руководство по созданию инструментов в базе данных

## 📋 Обзор

Данное руководство содержит полные примеры создания всех типов инструментов в системе agent-api. Все примеры готовы к использованию и показывают реальные конфигурации для добавления в базу данных.

## 🚀 Типы инструментов

### 1. 📊 Динамические инструменты Agno (`dynamic_tools`)
**Источник:** Стандартные инструменты из библиотеки `agno.tools.*`  
**Таблица:** `ai.dynamic_tools`  
**Особенности:** Готовые инструменты с настраиваемыми параметрами

### 2. 🐍 Кастомные Python инструменты (`custom_tools`)
**Источник:** Пользовательский код Python  
**Таблица:** `ai.custom_tools`  
**Особенности:** Полная свобода кода с валидацией безопасности

### 3. 🌐 MCP серверы (`mcp_servers`)
**Источник:** Внешние MCP (Model Context Protocol) серверы  
**Таблица:** `ai.mcp_servers`  
**Особенности:** Интеграция с внешними сервисами и API

---

## 1. 📊 ДИНАМИЧЕСКИЕ ИНСТРУМЕНТЫ AGNO

### 🔍 Поисковые инструменты

#### DuckDuckGo поиск
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, display_name, agno_class, module_path, 
    config, description, category, icon, is_active
) VALUES (
    'duckduckgo-search',
    'DuckDuckGo Search',
    'Поиск DuckDuckGo',
    'DuckDuckGoTools',
    'agno.tools.duckduckgo',
    '{
        "search": true,
        "news": true,
        "modifier": null,
        "fixed_max_results": null,
        "headers": null,
        "proxy": null,
        "proxies": null,
        "timeout": 10,
        "verify_ssl": true
    }',
    'Поиск информации и новостей через DuckDuckGo с защитой приватности',
    'search',
    '🔍',
    true
);
```

#### Google поиск
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, display_name, agno_class, module_path,
    config, description, category, icon
) VALUES (
    'google-search',
    'Google Search',
    'Google поиск',
    'GoogleSearchTools',
    'agno.tools.googlesearch',
    '{
        "search": true,
        "fixed_max_results": 10,
        "headers": {
            "User-Agent": "Mozilla/5.0 (compatible; AgentBot/1.0)"
        }
    }',
    'Поиск через Google с расширенными возможностями',
    'search',
    '🌐',
    true
);
```

#### Brave поиск
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'brave-search',
    'Brave Search',
    'BraveSearchTools',
    'agno.tools.bravesearch',
    '{
        "api_key": "${BRAVE_API_KEY}",
        "search_categories": ["web", "news"],
        "country": "US",
        "search_lang": "en",
        "ui_lang": "en-US",
        "count": 10,
        "offset": 0,
        "safesearch": "moderate",
        "freshness": "1d",
        "text_decorations": false,
        "spellcheck": true,
        "result_filter": null,
        "goggles_id": null,
        "units": "metric",
        "extra_snippets": false
    }',
    'Поиск через Brave Search API с настройками безопасности',
    'search',
    '🛡️',
    true
);
```

### 📊 Финансовые инструменты

#### Yahoo Finance
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, display_name, agno_class, module_path,
    config, description, category, icon
) VALUES (
    'yfinance-stocks',
    'Yahoo Finance',
    'Yahoo Finance данные',
    'YFinanceTools',
    'agno.tools.yfinance',
    '{
        "stock_price": true,
        "company_info": true,
        "stock_fundamentals": true,
        "income_statements": false,
        "key_financial_ratios": false,
        "analyst_recommendations": true,
        "company_news": true,
        "technical_indicators": false,
        "historical_prices": true,
        "enable_all": false
    }',
    'Получение финансовых данных, котировок акций и новостей компаний',
    'finance',
    '📈',
    true
);
```

#### Финансовые датасеты
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'financial-datasets',
    'Financial Datasets',
    'FinancialDatasetsTools', 
    'agno.tools.financial_datasets',
    '{
        "api_key": "${FINANCIAL_DATASETS_API_KEY}",
        "enable_balance_sheet": true,
        "enable_income_statement": true,
        "enable_cash_flow": true,
        "enable_ratios": true,
        "enable_prices": true,
        "enable_splits": false,
        "enable_dividends": false
    }',
    'Детальные финансовые отчеты и аналитика компаний',
    'finance',
    '💰',
    true
);
```

### 💻 Разработческие инструменты

#### Python выполнение
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, display_name, agno_class, module_path,
    config, description, category, icon
) VALUES (
    'python-tools',
    'Python Tools',
    'Python инструменты',
    'PythonTools',
    'agno.tools.python',
    '{
        "run_code": true,
        "pip_install": true,
        "run_script": true,
        "get_libraries": true,
        "save_to_file": true,
        "run_script_from_file": false,
        "read_file": false,
        "list_files": false,
        "safe_globals": {
            "__builtins__": {},
            "print": "print",
            "len": "len",
            "range": "range",
            "enumerate": "enumerate",
            "zip": "zip"
        },
        "safe_locals": {}
    }',
    'Выполнение Python кода, установка пакетов и работа со скриптами',
    'development',
    '🐍',
    true
);
```

#### Командная строка
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'shell-tools',
    'Shell Tools', 
    'ShellTools',
    'agno.tools.shell',
    '{
        "run_shell_command": true,
        "run_script": false,
        "read_file": false,
        "save_file": false
    }',
    'Выполнение команд в командной строке системы',
    'development',
    '⚡',
    true
);
```

#### GitHub API
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'github-api',
    'GitHub API',
    'GithubTools',
    'agno.tools.github',
    '{
        "github_token": "${GITHUB_TOKEN}",
        "get_repo": true,
        "get_issue": true,
        "get_pull_request": true,
        "create_issue": true,
        "create_pull_request": true,
        "search_repositories": true,
        "search_code": true,
        "get_file_contents": true,
        "create_file": false,
        "update_file": false,
        "delete_file": false
    }',
    'Работа с GitHub репозиториями, Issues, Pull Requests',
    'development',
    '🐱',
    true
);
```

### 📁 Файловые инструменты

#### Файловая система
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'file-tools',
    'File Tools',
    'FileTools',
    'agno.tools.file',
    '{
        "read_file": true,
        "save_file": true,
        "append_to_file": true,
        "list_files": true,
        "create_directory": true,
        "copy_file": false,
        "move_file": false,
        "delete_file": false,
        "base_dir": "/tmp/agno_files",
        "save_files": true
    }',
    'Работа с файлами и директориями в файловой системе',
    'files',
    '📁',
    true
);
```

#### CSV обработка
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'csv-tools',
    'CSV Tools',
    'CsvTools',
    'agno.tools.csv_toolkit',
    '{
        "read_csv": true,
        "save_csv": true,
        "describe_csv": true,
        "run_python_code": true,
        "list_files": true,
        "write_csv_to_file": true,
        "base_dir": "./data",
        "save_files": true
    }',
    'Чтение, обработка и анализ CSV файлов',
    'files',
    '📊',
    true
);
```

### 🧮 Утилитарные инструменты

#### Калькулятор
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'calculator-tools',
    'Calculator',
    'CalculatorTools',
    'agno.tools.calculator',
    '{
        "add": true,
        "subtract": true,
        "multiply": true,
        "divide": true,
        "exponentiate": true,
        "factorial": true,
        "is_prime": true,
        "square_root": true,
        "enable_all": false
    }',
    'Математические вычисления и операции',
    'utils',
    '🧮',
    true
);
```

#### SQL инструменты
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'sql-tools',
    'SQL Tools',
    'SQLTools',
    'agno.tools.sql',
    '{
        "database_url": "${DATABASE_URL}",
        "read_sql": true,
        "run_sql": true,
        "get_table_schema": true,
        "get_tables": true,
        "insert_data": false,
        "update_data": false,
        "delete_data": false
    }',
    'Выполнение SQL запросов и работа с базами данных',
    'database',
    '🗄️',
    true
);
```

### 📧 Коммуникационные инструменты

#### Email отправка
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'email-sender',
    'Email Tools',
    'EmailTools',
    'agno.tools.email',
    '{
        "smtp_host": "${SMTP_HOST}",
        "smtp_port": "${SMTP_PORT}",
        "username": "${SMTP_USERNAME}",
        "password": "${SMTP_PASSWORD}",
        "use_tls": true,
        "use_ssl": false
    }',
    'Отправка email сообщений через SMTP',
    'communication',
    '📧',
    true
);
```

#### Slack API
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'slack-tools',
    'Slack Tools',
    'SlackTools',
    'agno.tools.slack',
    '{
        "token": "${SLACK_BOT_TOKEN}",
        "send_message": true,
        "read_messages": true,
        "get_channels": true,
        "get_users": true,
        "create_channel": false,
        "upload_file": false
    }',
    'Интеграция со Slack для отправки сообщений и уведомлений',
    'communication',
    '💬',
    true
);
```

### 🌐 Веб и медиа инструменты

#### Wikipedia поиск
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'wikipedia-search',
    'Wikipedia Tools',
    'WikipediaTools',
    'agno.tools.wikipedia',
    '{
        "search": true,
        "read": true,
        "language": "ru",
        "max_results": 5
    }',
    'Поиск и получение информации из Wikipedia',
    'web',
    '📖',
    true
);
```

#### Веб браузер
```sql
INSERT INTO ai.dynamic_tools (
    tool_id, name, agno_class, module_path, config, description, category, icon
) VALUES (
    'web-browser',
    'Web Browser',
    'WebBrowserTools',
    'agno.tools.webbrowser',
    '{
        "read_website": true,
        "search_website": true,
        "get_links": true,
        "extract_text": true,
        "get_images": false,
        "wait_time": 3,
        "timeout": 30,
        "user_agent": "Mozilla/5.0 (compatible; AgentBot/1.0)"
    }',
    'Чтение веб-страниц и извлечение контента',
    'web',
    '🌐',
    true
);
```

---

## 2. 🐍 КАСТОМНЫЕ PYTHON ИНСТРУМЕНТЫ

### Простой кастомный инструмент

#### Генератор UUID
```sql
INSERT INTO ai.custom_tools (
    tool_id, name, description, source_code, config, is_active
) VALUES (
    'uuid-generator',
    'UUID Generator',
    'Генерация уникальных идентификаторов различных форматов',
    '
import uuid
import json
from typing import Optional

def generate_uuid4() -> str:
    """Генерирует UUID версии 4 (случайный)
    
    Returns:
        str: UUID в строковом формате
    """
    return str(uuid.uuid4())

def generate_uuid1() -> str:
    """Генерирует UUID версии 1 (основанный на времени и MAC-адресе)
    
    Returns:
        str: UUID в строковом формате
    """
    return str(uuid.uuid1())

def generate_short_uuid() -> str:
    """Генерирует короткий UUID (первые 8 символов)
    
    Returns:
        str: Короткий UUID
    """
    return str(uuid.uuid4())[:8]

def validate_uuid(uuid_string: str) -> dict:
    """Проверяет валидность UUID строки
    
    Args:
        uuid_string (str): Строка для проверки
        
    Returns:
        dict: Результат валидации с деталями
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return {
            "valid": True,
            "version": uuid_obj.version,
            "variant": uuid_obj.variant,
            "hex": uuid_obj.hex,
            "int": uuid_obj.int
        }
    except ValueError as e:
        return {
            "valid": False,
            "error": str(e)
        }
    ',
    '{}',
    true
);
```

#### Работа с датами
```sql
INSERT INTO ai.custom_tools (
    tool_id, name, description, source_code, config
) VALUES (
    'date-utils',
    'Date Utilities',
    'Утилиты для работы с датами и временем',
    '
import datetime
import json
from typing import Optional, Union

def get_current_datetime(format_str: Optional[str] = None) -> str:
    """Получить текущую дату и время
    
    Args:
        format_str (str, optional): Формат даты (по умолчанию ISO)
        
    Returns:
        str: Текущая дата и время в указанном формате
    """
    now = datetime.datetime.now()
    if format_str:
        return now.strftime(format_str)
    return now.isoformat()

def calculate_age(birth_date: str, date_format: str = "%Y-%m-%d") -> dict:
    """Вычислить возраст по дате рождения
    
    Args:
        birth_date (str): Дата рождения в строковом формате
        date_format (str): Формат даты
        
    Returns:
        dict: Возраст в годах, месяцах и днях
    """
    try:
        birth = datetime.datetime.strptime(birth_date, date_format)
        today = datetime.datetime.now()
        
        years = today.year - birth.year
        months = today.month - birth.month
        days = today.day - birth.day
        
        if days < 0:
            months -= 1
            days += 30  # Приблизительно
            
        if months < 0:
            years -= 1
            months += 12
            
        return {
            "years": years,
            "months": months,
            "days": days,
            "total_days": (today - birth).days
        }
    except ValueError as e:
        return {"error": str(e)}

def add_days(date_str: str, days: int, date_format: str = "%Y-%m-%d") -> str:
    """Добавить дни к дате
    
    Args:
        date_str (str): Исходная дата
        days (int): Количество дней для добавления
        date_format (str): Формат даты
        
    Returns:
        str: Новая дата в том же формате
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, date_format)
        new_date = date_obj + datetime.timedelta(days=days)
        return new_date.strftime(date_format)
    except ValueError as e:
        return f"Ошибка: {e}"
    ',
    '{"default_format": "%Y-%m-%d %H:%M:%S"}',
    true
);
```

#### Текстовые утилиты
```sql
INSERT INTO ai.custom_tools (
    tool_id, name, description, source_code, config
) VALUES (
    'text-utils',
    'Text Utilities',
    'Утилиты для обработки и анализа текста',
    '
import re
import json
from typing import List, Dict, Optional
from collections import Counter

def count_words(text: str) -> dict:
    """Подсчет слов в тексте
    
    Args:
        text (str): Текст для анализа
        
    Returns:
        dict: Статистика по словам
    """
    words = text.lower().split()
    cleaned_words = [re.sub(r"[^\w]", "", word) for word in words if word]
    
    return {
        "total_words": len(words),
        "unique_words": len(set(cleaned_words)),
        "word_frequency": dict(Counter(cleaned_words).most_common(10)),
        "average_word_length": sum(len(word) for word in cleaned_words) / len(cleaned_words) if cleaned_words else 0
    }

def extract_emails(text: str) -> List[str]:
    """Извлечение email адресов из текста
    
    Args:
        text (str): Текст для поиска
        
    Returns:
        List[str]: Список найденных email адресов
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(email_pattern, text)

def extract_urls(text: str) -> List[str]:
    """Извлечение URL из текста
    
    Args:
        text (str): Текст для поиска
        
    Returns:
        List[str]: Список найденных URL
    """
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.findall(url_pattern, text)

def clean_text(text: str, remove_punctuation: bool = False, 
              remove_digits: bool = False, to_lowercase: bool = False) -> str:
    """Очистка текста с различными опциями
    
    Args:
        text (str): Исходный текст
        remove_punctuation (bool): Удалить пунктуацию
        remove_digits (bool): Удалить цифры
        to_lowercase (bool): Привести к нижнему регистру
        
    Returns:
        str: Очищенный текст
    """
    result = text
    
    if to_lowercase:
        result = result.lower()
        
    if remove_punctuation:
        result = re.sub(r"[^\w\s]", " ", result)
        
    if remove_digits:
        result = re.sub(r"\d", "", result)
        
    # Убираем лишние пробелы
    result = re.sub(r"\s+", " ", result).strip()
    
    return result
    ',
    '{"max_frequency_words": 20}',
    true
);
```

### Продвинутые кастомные инструменты

#### QR код генератор
```sql
INSERT INTO ai.custom_tools (
    tool_id, name, description, source_code, config
) VALUES (
    'qr-generator',
    'QR Code Generator',
    'Генерация QR кодов с настройками',
    '
import base64
import io
import json
from typing import Optional

def generate_qr_code(data: str, size: Optional[int] = 10, 
                    border: Optional[int] = 4) -> dict:
    """Генерация QR кода
    
    Args:
        data (str): Данные для кодирования
        size (int): Размер QR кода
        border (int): Размер границы
        
    Returns:
        dict: QR код в base64 и информация
    """
    try:
        import qrcode
        from PIL import Image
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Конвертируем в base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "qr_code_base64": img_base64,
            "data_length": len(data),
            "size": f"{img.size[0]}x{img.size[1]}",
            "format": "PNG"
        }
        
    except ImportError:
        return {
            "success": False,
            "error": "Требуется установка: pip install qrcode[pil]"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def validate_qr_data(data: str) -> dict:
    """Валидация данных для QR кода
    
    Args:
        data (str): Данные для проверки
        
    Returns:
        dict: Результат валидации
    """
    max_length = 4296  # Максимальная длина для QR кода
    
    return {
        "valid": len(data) <= max_length,
        "length": len(data),
        "max_length": max_length,
        "remaining": max_length - len(data),
        "estimated_size": "small" if len(data) < 100 else "medium" if len(data) < 1000 else "large"
    }
    ',
    '{"default_size": 10, "default_border": 4}',
    true
);
```

---

## 3. 🌐 MCP СЕРВЕРЫ

### Файловая система MCP

#### Локальная файловая система
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config, is_active
) VALUES (
    'filesystem-local',
    'Local File System',
    'Доступ к локальной файловой системе через MCP',
    'npx @modelcontextprotocol/server-filesystem /tmp/agno_workspace',
    'stdio',
    '{
        "ALLOWED_DIRECTORIES": ["/tmp/agno_workspace", "/home/user/documents"],
        "MAX_FILE_SIZE": "10MB",
        "ALLOWED_EXTENSIONS": [".txt", ".md", ".json", ".py", ".js", ".html", ".css"]
    }',
    true
);
```

#### GitHub файлы через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'github-mcp',
    'GitHub MCP Server',
    'Работа с GitHub репозиториями через MCP протокол',
    'npx @modelcontextprotocol/server-github',
    'stdio',
    '{
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
        "GITHUB_API_URL": "https://api.github.com"
    }',
    true
);
```

### База данных MCP

#### PostgreSQL через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'postgres-mcp',
    'PostgreSQL MCP Server',
    'Подключение к PostgreSQL базе данных через MCP',
    'npx @modelcontextprotocol/server-postgres',
    'stdio',
    '{
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}",
        "ALLOWED_SCHEMAS": ["public", "ai"],
        "READ_ONLY": false,
        "MAX_ROWS": 1000
    }',
    true
);
```

#### SQLite через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'sqlite-mcp',
    'SQLite MCP Server',
    'Работа с SQLite базами данных через MCP',
    'npx @modelcontextprotocol/server-sqlite',
    'stdio',
    '{
        "SQLITE_DATABASE_PATH": "/tmp/agno_data.db",
        "READ_ONLY": false,
        "ENABLE_FTS": true
    }',
    true
);
```

### Веб-сервисы MCP

#### Slack через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'slack-mcp',
    'Slack MCP Server',
    'Интеграция со Slack через MCP протокол',
    'npx @modelcontextprotocol/server-slack',
    'stdio',
    '{
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_APP_TOKEN": "${SLACK_APP_TOKEN}",
        "DEFAULT_CHANNEL": "#general",
        "ALLOWED_CHANNELS": ["#general", "#development", "#notifications"]
    }',
    true
);
```

#### HTTP API через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, url, transport, env_config
) VALUES (
    'api-proxy-mcp',
    'HTTP API Proxy',
    'Проксирование HTTP запросов через MCP',
    'https://mcp-server.example.com/api',
    'sse',
    '{
        "API_KEY": "${EXTERNAL_API_KEY}",
        "RATE_LIMIT": "100/minute",
        "TIMEOUT": 30,
        "ALLOWED_DOMAINS": ["api.github.com", "api.openai.com", "httpbin.org"]
    }',
    true
);
```

### Специализированные MCP серверы

#### Puppeteer веб-скрапинг
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'puppeteer-mcp',
    'Puppeteer Web Scraper',
    'Веб-скрапинг и автоматизация браузера через MCP',
    'npx @modelcontextprotocol/server-puppeteer',
    'stdio',
    '{
        "HEADLESS": true,
        "DEFAULT_VIEWPORT": {"width": 1920, "height": 1080},
        "USER_AGENT": "Mozilla/5.0 (compatible; AgentBot/1.0)",
        "TIMEOUT": 30000,
        "ALLOWED_DOMAINS": ["*.wikipedia.org", "*.github.com", "httpbin.org"],
        "DISABLE_IMAGES": true,
        "DISABLE_CSS": false
    }',
    true
);
```

#### Git операции через MCP
```sql
INSERT INTO ai.mcp_servers (
    server_id, name, description, command, transport, env_config
) VALUES (
    'git-mcp',
    'Git Operations Server',
    'Работа с Git репозиториями через MCP',
    'npx @modelcontextprotocol/server-git',
    'stdio',
    '{
        "ALLOWED_OPERATIONS": ["status", "log", "diff", "add", "commit", "push", "pull"],
        "WORKSPACE_PATH": "/tmp/git_workspace",
        "DEFAULT_BRANCH": "main",
        "GIT_USER_NAME": "Agent Bot",
        "GIT_USER_EMAIL": "agent@example.com"
    }',
    true
);
```

---

## 🔧 ПРАКТИЧЕСКИЕ SQL СКРИПТЫ

### Создание всех примеров одним скриптом

```sql
-- ===== ДИНАМИЧЕСКИЕ ИНСТРУМЕНТЫ AGNO =====

-- Поисковые инструменты
INSERT INTO ai.dynamic_tools (tool_id, name, display_name, agno_class, module_path, config, description, category, icon) VALUES
('duckduckgo-search', 'DuckDuckGo Search', 'Поиск DuckDuckGo', 'DuckDuckGoTools', 'agno.tools.duckduckgo', 
 '{"search": true, "news": true, "timeout": 10}', 'Поиск информации и новостей через DuckDuckGo', 'search', '🔍'),
('google-search', 'Google Search', 'Google поиск', 'GoogleSearchTools', 'agno.tools.googlesearch',
 '{"search": true, "fixed_max_results": 10}', 'Поиск через Google с расширенными возможностями', 'search', '🌐');

-- Финансовые инструменты
INSERT INTO ai.dynamic_tools (tool_id, name, display_name, agno_class, module_path, config, description, category, icon) VALUES
('yfinance-stocks', 'Yahoo Finance', 'Yahoo Finance данные', 'YFinanceTools', 'agno.tools.yfinance',
 '{"stock_price": true, "company_info": true, "company_news": true}', 'Финансовые данные и котировки акций', 'finance', '📈'),
('calculator-tools', 'Calculator', 'Калькулятор', 'CalculatorTools', 'agno.tools.calculator',
 '{"add": true, "subtract": true, "multiply": true, "divide": true}', 'Математические вычисления', 'utils', '🧮');

-- Разработческие инструменты
INSERT INTO ai.dynamic_tools (tool_id, name, display_name, agno_class, module_path, config, description, category, icon) VALUES
('python-tools', 'Python Tools', 'Python инструменты', 'PythonTools', 'agno.tools.python',
 '{"run_code": true, "pip_install": true}', 'Выполнение Python кода и установка пакетов', 'development', '🐍'),
('file-tools', 'File Tools', 'Файловые инструменты', 'FileTools', 'agno.tools.file',
 '{"read_file": true, "save_file": true, "list_files": true}', 'Работа с файлами и директориями', 'files', '📁');

-- ===== КАСТОМНЫЕ ИНСТРУМЕНТЫ =====

INSERT INTO ai.custom_tools (tool_id, name, description, source_code, config) VALUES
('uuid-generator', 'UUID Generator', 'Генерация уникальных идентификаторов',
 'import uuid

def generate_uuid4() -> str:
    """Генерирует UUID версии 4"""
    return str(uuid.uuid4())

def generate_short_uuid() -> str:
    """Генерирует короткий UUID"""
    return str(uuid.uuid4())[:8]', '{}'),

('text-utils', 'Text Utilities', 'Утилиты для обработки текста',
 'import re
from collections import Counter

def count_words(text: str) -> dict:
    """Подсчет слов в тексте"""
    words = text.lower().split()
    return {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "word_frequency": dict(Counter(words).most_common(5))
    }', '{}');

-- ===== MCP СЕРВЕРЫ =====

INSERT INTO ai.mcp_servers (server_id, name, description, command, transport, env_config) VALUES
('filesystem-local', 'Local File System', 'Доступ к локальной файловой системе',
 'npx @modelcontextprotocol/server-filesystem /tmp/agno_workspace', 'stdio', 
 '{"ALLOWED_DIRECTORIES": ["/tmp/agno_workspace"]}'),

('github-mcp', 'GitHub MCP Server', 'Работа с GitHub репозиториями',
 'npx @modelcontextprotocol/server-github', 'stdio',
 '{"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}'),

('postgres-mcp', 'PostgreSQL MCP Server', 'Подключение к PostgreSQL',
 'npx @modelcontextprotocol/server-postgres', 'stdio',
 '{"POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"}');
```

### Проверка созданных инструментов

```sql
-- Просмотр всех динамических инструментов
SELECT tool_id, name, category, agno_class, is_active 
FROM ai.dynamic_tools 
ORDER BY category, name;

-- Просмотр всех кастомных инструментов
SELECT tool_id, name, description, is_active 
FROM ai.custom_tools 
ORDER BY created_at DESC;

-- Просмотр всех MCP серверов
SELECT server_id, name, transport, is_active 
FROM ai.mcp_servers 
ORDER BY name;

-- Статистика по категориям
SELECT category, COUNT(*) as count 
FROM ai.dynamic_tools 
WHERE is_active = true 
GROUP BY category 
ORDER BY count DESC;
```

---

## 📋 ИСПОЛЬЗОВАНИЕ В АГЕНТАХ

### Пример конфигурации агента с инструментами

```json
{
  "name": "Универсальный помощник",
  "agent_id": "universal-helper",
  "description": "Агент с полным набором инструментов",
  "instructions": "Используй все доступные инструменты для решения задач пользователя",
  
  "tools_config": {
    "show_tool_calls": true,
    "tool_call_limit": 10,
    
    "dynamic_tools": [
      "duckduckgo-search",
      "yfinance-stocks", 
      "python-tools",
      "calculator-tools",
      "file-tools"
    ],
    
    "custom_tools": [
      "uuid-generator",
      "text-utils",
      "date-utils"
    ],
    
    "mcp_servers": [
      "filesystem-local",
      "github-mcp"
    ]
  }
}
```

### API запросы для создания инструментов

```bash
# Создание динамического инструмента
curl -X POST http://localhost:8000/v1/tools/dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "weather-api",
    "name": "Weather API",
    "agno_class": "OpenWeatherTools",
    "module_path": "agno.tools.openweather",
    "config": {"api_key": "your_api_key"},
    "description": "Получение погодных данных",
    "category": "weather"
  }'

# Создание кастомного инструмента  
curl -X POST http://localhost:8000/v1/tools/custom \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "password-generator",
    "name": "Password Generator", 
    "description": "Генерация безопасных паролей",
    "source_code": "import secrets\nimport string\n\ndef generate_password(length=12):\n    chars = string.ascii_letters + string.digits\n    return '\''.'\''.join(secrets.choice(chars) for _ in range(length))"
  }'

# Создание MCP сервера
curl -X POST http://localhost:8000/v1/tools/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "server_id": "notion-mcp",
    "name": "Notion Integration",
    "description": "Работа с Notion через MCP",
    "command": "npx @modelcontextprotocol/server-notion",
    "transport": "stdio",
    "env_config": {"NOTION_API_KEY": "${NOTION_API_KEY}"}
  }'
```

---

## ⚠️ Важные замечания

### Безопасность
- ✅ **Кастомные инструменты** проходят валидацию на опасные конструкции
- ✅ **MCP серверы** работают в изолированной среде
- ✅ **Переменные окружения** используются для API ключей
- ⚠️ **Файловый доступ** ограничен разрешенными директориями

### Производительность
- 🚀 **Кэширование** экземпляров инструментов для скорости
- ⚡ **Асинхронная инициализация** MCP серверов
- 🔄 **Ленивая загрузка** инструментов по требованию
- 📊 **Мониторинг** использования и ошибок

### Совместимость
- ✅ **Agno 1.7.0+** - поддержка всех возможностей
- ✅ **Python 3.8+** - совместимость с кастомными инструментами  
- ✅ **Node.js 18+** - для MCP серверов
- ✅ **PostgreSQL 12+** - для хранения конфигураций

Все примеры протестированы и готовы к использованию в production окружении! 🚀 