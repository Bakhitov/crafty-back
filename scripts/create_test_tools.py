#!/usr/bin/env python3
"""
Скрипт для создания тестовых инструментов в БД.
Создает различные типы инструментов для тестирования GET /v1/tools.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Загружаем переменные окружения из .env файла
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.tool import Tool

def get_db_session() -> Session:
    """Создает сессию БД для скриптов"""
    return SessionLocal()

def create_test_tools():
    """Создает тестовые инструменты разных типов"""
    db = get_db_session()
    
    try:
        # Проверяем, что нет дубликатов
        existing_tools = db.query(Tool).filter(Tool.name.like('test_%')).all()
        if existing_tools:
            print(f"Удаляю {len(existing_tools)} существующих тестовых инструментов...")
            for tool in existing_tools:
                db.delete(tool)
            db.commit()
        
        # Создаем тестовые инструменты
        test_tools = [
            # Builtin инструменты
            Tool(
                name="test_duckduckgo_search",
                type="builtin",
                description="Тестовый инструмент поиска DuckDuckGo",
                configuration={
                    "class": "DuckDuckGoTools",
                    "params": {"max_results": 5}
                },
                is_public=True,
                category="search",
                display_name="Поиск DuckDuckGo"
            ),
            Tool(
                name="test_file_tools",
                type="builtin", 
                description="Тестовый инструмент работы с файлами",
                configuration={
                    "class": "FileTools",
                    "params": {"base_dir": "/tmp"}
                },
                is_public=True,
                category="files",
                display_name="Работа с файлами"
            ),
            
            # MCP инструменты
            Tool(
                name="test_mcp_weather",
                type="mcp",
                description="Тестовый MCP инструмент для погоды",
                configuration={
                    "command": ["node", "/path/to/weather/server.js"],
                    "env": {"API_KEY": "test_key"},
                    "transport": "stdio",
                    "timeout_seconds": 10
                },
                is_public=False,
                category="weather",
                display_name="Погода MCP"
            ),
            Tool(
                name="test_mcp_calendar",
                type="mcp",
                description="Тестовый MCP инструмент календаря",
                configuration={
                    "url": "http://localhost:3001/mcp",
                    "transport": "http",
                    "timeout_seconds": 5
                },
                is_public=True,
                category="productivity",
                display_name="Календарь MCP"
            ),
            
            # Custom инструменты
            Tool(
                name="test_custom_calculator",
                type="custom",
                description="Тестовая пользовательская функция калькулятора",
                configuration={
                    "function_code": """
def calculate(expression: str) -> str:
    '''Простой калькулятор для базовых операций'''
    try:
        result = eval(expression)
        return f"Результат: {result}"
    except Exception as e:
        return f"Ошибка: {str(e)}"
"""
                },
                is_public=False,
                category="math",
                display_name="Калькулятор"
            ),
            Tool(
                name="test_custom_text_processor",
                type="custom",
                description="Тестовая функция обработки текста",
                configuration={
                    "function_code": """
def process_text(text: str, operation: str = "uppercase") -> str:
    '''Обработка текста различными способами'''
    if operation == "uppercase":
        return text.upper()
    elif operation == "lowercase":
        return text.lower()
    elif operation == "reverse":
        return text[::-1]
    else:
        return text
"""
                },
                is_public=True,
                category="text",
                display_name="Обработка текста"
            ),
            
            # Деактивированный инструмент для тестирования фильтрации
            Tool(
                name="test_inactive_tool",
                type="builtin",
                description="Деактивированный тестовый инструмент",
                configuration={"class": "DuckDuckGoTools"},
                is_public=True,
                category="test",
                display_name="Неактивный инструмент",
                is_active=False
            )
        ]
        
        print(f"Создаю {len(test_tools)} тестовых инструментов...")
        for tool in test_tools:
            db.add(tool)
        
        db.commit()
        
        # Проверяем созданные инструменты
        created_tools = db.query(Tool).filter(Tool.name.like('test_%')).all()
        print(f"\n✅ Успешно создано {len(created_tools)} тестовых инструментов:")
        
        for tool in created_tools:
            status = "активный" if tool.is_active else "неактивный"
            visibility = "публичный" if tool.is_public else "приватный"
            print(f"  - {tool.name} ({tool.type}, {status}, {visibility}) [{tool.category}]")
            
        print(f"\n🧪 Теперь можно тестировать эндпоинт GET /v1/tools")
        print("Примеры тестов:")
        print("  curl http://localhost:8000/v1/tools")
        print("  curl 'http://localhost:8000/v1/tools?type_filter=builtin'")
        print("  curl 'http://localhost:8000/v1/tools?category=search'")
        print("  curl 'http://localhost:8000/v1/tools?is_active=false'")
        
    except Exception as e:
        print(f"❌ Ошибка создания тестовых инструментов: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("🔧 Создание тестовых инструментов для API тестирования...")
    success = create_test_tools()
    sys.exit(0 if success else 1) 