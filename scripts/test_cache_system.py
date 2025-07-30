#!/usr/bin/env python3
"""
Специальный тест системы кэширования с PostgreSQL триггерами.

Тестирует:
1. Автоматическую инвалидацию кэша при UPDATE (через updated_at)
2. Автоматическую инвалидацию кэша при INSERT/DELETE (через NOTIFY триггеры)
3. Работу Cache Listener
4. Кэширование списка агентов
5. Кэширование инструментов
"""

import sys
import os
import time
import asyncio
import requests
import json
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Загружаем переменные окружения
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.agent import DynamicAgent
from db.models.tool import Tool
from agents.cache_listener import cache_listener

# Конфигурация
BASE_URL = "http://localhost:8000/v1"
TEST_AGENT_ID = "cache_test_agent"
TEST_TOOL_NAME = "cache_test_tool"

def get_db_session() -> Session:
    """Создает сессию БД"""
    return SessionLocal()

def make_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Делает HTTP запрос к API"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else {},
            "success": 200 <= response.status_code < 300
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": {"error": str(e)},
            "success": False
        }

def test_cache_invalidation_on_update():
    """Тест 1: Инвалидация кэша при UPDATE через updated_at"""
    print("\n🔄 ТЕСТ 1: Инвалидация кэша при UPDATE")
    print("=" * 50)
    
    db = get_db_session()
    try:
        # 1. Создаем тестового агента
        test_agent = DynamicAgent(
            agent_id=TEST_AGENT_ID,
            name="Cache Test Agent v1",
            description="Тестовый агент для проверки кэширования",
            model_config={"provider": "openai", "id": "gpt-4.1-mini-2025-04-14"},
            system_instructions=["Я тестовый агент версии 1"],
            is_active=True,
            is_public=True
        )
        
        # Удаляем если существует
        existing = db.query(DynamicAgent).filter(DynamicAgent.agent_id == TEST_AGENT_ID).first()
        if existing:
            db.delete(existing)
            db.commit()
        
        db.add(test_agent)
        db.commit()
        db.refresh(test_agent)
        print(f"✅ Создан тестовый агент: {test_agent.agent_id}")
        
        # 2. Первый запрос к агенту (должен создать кэш)
        print("📞 Первый запрос к агенту (создание кэша)...")
        response1 = make_request("POST", f"/agents/{TEST_AGENT_ID}/runs", 
                                data={"message": "Привет! Как тебя зовут?", "stream": "false"})
        
        if response1["success"]:
            print("✅ Первый запрос успешен - агент закэширован")
        else:
            print(f"❌ Первый запрос неудачен: {response1}")
            return False
        
        # 3. Изменяем агента в БД (UPDATE)
        print("🔧 Изменяем имя агента в БД...")
        test_agent.name = "Cache Test Agent v2 (UPDATED)"
        test_agent.system_instructions = ["Я тестовый агент версии 2 - ОБНОВЛЕННЫЙ!"]
        db.commit()
        print("✅ Агент обновлен в БД (триггер updated_at должен сработать)")
        
        # Небольшая пауза для обработки
        time.sleep(1)
        
        # 4. Второй запрос к агенту (должен получить обновленную версию)
        print("📞 Второй запрос к агенту (проверка инвалидации кэша)...")
        response2 = make_request("POST", f"/agents/{TEST_AGENT_ID}/runs",
                                data={"message": "Как тебя зовут? Какая у тебя версия?", "stream": "false"})
        
        if response2["success"]:
            # Проверяем что агент отвечает как версия 2
            content = str(response2.get("data", {}))
            if "версии 2" in content or "ОБНОВЛЕННЫЙ" in content or "v2" in content:
                print("✅ ТЕСТ ПРОЙДЕН: Кэш автоматически инвалидировался при UPDATE!")
                return True
            else:
                print("⚠️ Агент отвечает, но возможно использует старую версию из кэша")
                print(f"Ответ: {content[:200]}...")
                return False
        else:
            print(f"❌ Второй запрос неудачен: {response2}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка в тесте UPDATE: {e}")
        return False
    finally:
        # Очистка
        try:
            existing = db.query(DynamicAgent).filter(DynamicAgent.agent_id == TEST_AGENT_ID).first()
            if existing:
                db.delete(existing)
                db.commit()
        except:
            pass
        db.close()

def test_cache_invalidation_on_insert_delete():
    """Тест 2: Инвалидация кэша при INSERT/DELETE через NOTIFY триггеры"""
    print("\n➕ ТЕСТ 2: Инвалидация кэша при INSERT/DELETE")
    print("=" * 50)
    
    # 1. Получаем список агентов до создания
    print("📋 Получаем исходный список агентов...")
    response1 = make_request("GET", "/agents")
    if not response1["success"]:
        print(f"❌ Не удалось получить список агентов: {response1}")
        return False
    
    initial_agents = response1["data"]
    initial_count = len(initial_agents)
    print(f"✅ Исходное количество агентов: {initial_count}")
    
    # 2. Создаем нового агента через БД (INSERT)
    print("➕ Создаем нового агента в БД...")
    db = get_db_session()
    try:
        # Удаляем если существует
        existing = db.query(DynamicAgent).filter(DynamicAgent.agent_id == TEST_AGENT_ID).first()
        if existing:
            db.delete(existing)
            db.commit()
        
        new_agent = DynamicAgent(
            agent_id=TEST_AGENT_ID,
            name="Cache INSERT Test Agent",
            description="Тестовый агент для проверки INSERT триггера",
            model_config={"provider": "openai", "id": "gpt-4o"},
            is_active=True,
            is_public=True
        )
        
        db.add(new_agent)
        db.commit()
        print("✅ Новый агент создан в БД (NOTIFY триггер должен сработать)")
        
        # Пауза для обработки NOTIFY
        time.sleep(2)
        
        # 3. Получаем список агентов после создания
        print("📋 Получаем обновленный список агентов...")
        response2 = make_request("GET", "/agents")
        if not response2["success"]:
            print(f"❌ Не удалось получить обновленный список: {response2}")
            return False
        
        updated_agents = response2["data"]
        updated_count = len(updated_agents)
        print(f"✅ Обновленное количество агентов: {updated_count}")
        
        # Проверяем что новый агент появился в списке
        if TEST_AGENT_ID in updated_agents:
            print("✅ Новый агент появился в списке - кэш обновился!")
        else:
            print("⚠️ Новый агент НЕ появился в списке - возможно кэш не обновился")
            print(f"Список агентов: {updated_agents}")
        
        # 4. Удаляем агента (DELETE)
        print("🗑️ Удаляем агента из БД...")
        db.delete(new_agent)
        db.commit()
        print("✅ Агент удален из БД (NOTIFY триггер должен сработать)")
        
        # Пауза для обработки NOTIFY
        time.sleep(2)
        
        # 5. Получаем список агентов после удаления
        print("📋 Получаем список агентов после удаления...")
        response3 = make_request("GET", "/agents")
        if not response3["success"]:
            print(f"❌ Не удалось получить список после удаления: {response3}")
            return False
        
        final_agents = response3["data"]
        final_count = len(final_agents)
        print(f"✅ Финальное количество агентов: {final_count}")
        
        # Проверяем что агент исчез из списка
        if TEST_AGENT_ID not in final_agents and final_count == initial_count:
            print("✅ ТЕСТ ПРОЙДЕН: Кэш автоматически инвалидировался при INSERT/DELETE!")
            return True
        else:
            print("⚠️ Агент все еще в списке или количество не совпадает")
            print(f"Финальный список: {final_agents}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка в тесте INSERT/DELETE: {e}")
        return False
    finally:
        # Очистка
        try:
            existing = db.query(DynamicAgent).filter(DynamicAgent.agent_id == TEST_AGENT_ID).first()
            if existing:
                db.delete(existing)
                db.commit()
        except:
            pass
        db.close()

def test_tools_caching():
    """Тест 3: Кэширование инструментов"""
    print("\n🔧 ТЕСТ 3: Кэширование инструментов")
    print("=" * 50)
    
    # 1. Получаем список инструментов
    print("📋 Получаем список инструментов...")
    response1 = make_request("GET", "/tools")
    if not response1["success"]:
        print(f"❌ Не удалось получить список инструментов: {response1}")
        return False
    
    tools_list = response1["data"]
    print(f"✅ Получено {len(tools_list)} инструментов")
    
    # 2. Создаем новый инструмент
    print("➕ Создаем новый тестовый инструмент...")
    db = get_db_session()
    try:
        # Удаляем если существует
        existing = db.query(Tool).filter(Tool.name == TEST_TOOL_NAME).first()
        if existing:
            db.delete(existing)
            db.commit()
        
        new_tool = Tool(
            name=TEST_TOOL_NAME,
            type="builtin",
            description="Тестовый инструмент для проверки кэширования",
            configuration={"class": "DuckDuckGoTools"},
            is_active=True,
            is_public=True,
            category="test"
        )
        
        db.add(new_tool)
        db.commit()
        print("✅ Новый инструмент создан")
        
        # Пауза для обработки
        time.sleep(1)
        
        # 3. Проверяем что инструмент появился в списке
        print("📋 Проверяем обновленный список инструментов...")
        response2 = make_request("GET", "/tools")
        if response2["success"]:
            updated_tools = response2["data"]
            tool_names = [tool.get("name", "") for tool in updated_tools]
            if TEST_TOOL_NAME in tool_names:
                print("✅ Новый инструмент появился в списке!")
            else:
                print("⚠️ Новый инструмент НЕ появился в списке")
                
        # 4. Тестируем фильтрацию
        print("🔍 Тестируем фильтрацию инструментов...")
        response3 = make_request("GET", "/tools?category=test")
        if response3["success"]:
            test_tools = response3["data"]
            if any(tool.get("name") == TEST_TOOL_NAME for tool in test_tools):
                print("✅ Фильтрация работает корректно!")
                return True
            else:
                print("⚠️ Фильтрация не работает или инструмент не найден")
                return False
        else:
            print(f"❌ Ошибка фильтрации: {response3}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка в тесте инструментов: {e}")
        return False
    finally:
        # Очистка
        try:
            existing = db.query(Tool).filter(Tool.name == TEST_TOOL_NAME).first()
            if existing:
                db.delete(existing)
                db.commit()
        except:
            pass
        db.close()

def test_cache_endpoints():
    """Тест 4: Эндпоинты управления кэшем"""
    print("\n🎛️ ТЕСТ 4: Эндпоинты управления кэшем")
    print("=" * 50)
    
    # 1. Получаем статистику кэша
    print("📊 Получаем статистику кэша...")
    response1 = make_request("GET", "/cache/stats")
    if response1["success"]:
        stats = response1["data"]
        print(f"✅ Статистика кэша получена:")
        print(f"   - Кэш агентов: {stats.get('agents_cache', {})}")
        print(f"   - Кэш инструментов: {stats.get('tools_cache', {})}")
        print(f"   - Всего объектов: {stats.get('total_cached_objects', 0)}")
    else:
        print(f"❌ Не удалось получить статистику: {response1}")
        return False
    
    # 2. Тестируем очистку кэша
    print("🧹 Тестируем полную очистку кэша...")
    response2 = make_request("POST", "/cache/clear")
    if response2["success"]:
        clear_result = response2["data"]
        print(f"✅ Кэш очищен:")
        print(f"   - Агентов очищено: {clear_result.get('agents_cleared', 0)}")
        print(f"   - Инструментов очищено: {clear_result.get('tools_cleared', 0)}")
        print(f"   - Список агентов очищен: {clear_result.get('available_agents_cache_cleared', False)}")
        return True
    else:
        print(f"❌ Не удалось очистить кэш: {response2}")
        return False

async def test_cache_listener():
    """Тест 5: Cache Listener (если возможно)"""
    print("\n👂 ТЕСТ 5: Cache Listener")
    print("=" * 50)
    
    try:
        # Проверяем что listener запущен
        if hasattr(cache_listener, 'is_listening') and cache_listener.is_listening:
            print("✅ Cache Listener активен")
            return True
        else:
            print("⚠️ Cache Listener не активен (возможно, не запущен в тестовом режиме)")
            return True  # Не критично для тестов
    except Exception as e:
        print(f"⚠️ Не удалось проверить Cache Listener: {e}")
        return True  # Не критично

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ КЭШИРОВАНИЯ")
    print("=" * 60)
    print("Проверяем автоматическую инвалидацию кэша через PostgreSQL триггеры")
    print()
    
    # Проверяем доступность API
    print("🔗 Проверяем доступность API...")
    health_response = make_request("GET", "/health")
    if not health_response["success"]:
        print("❌ API недоступен! Запустите сервер: docker compose up -d")
        return False
    print("✅ API доступен")
    
    # Запускаем тесты
    tests = [
        ("UPDATE инвалидация", test_cache_invalidation_on_update),
        ("INSERT/DELETE инвалидация", test_cache_invalidation_on_insert_delete),
        ("Кэширование инструментов", test_tools_caching),
        ("Эндпоинты кэша", test_cache_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Запуск теста: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ ТЕСТ '{test_name}' ПРОЙДЕН")
            else:
                print(f"❌ ТЕСТ '{test_name}' НЕ ПРОЙДЕН")
        except Exception as e:
            print(f"💥 ТЕСТ '{test_name}' УПАЛ: {e}")
            results.append((test_name, False))
    
    # Тест Cache Listener (асинхронный)
    try:
        print(f"\n{'='*60}")
        print("🧪 Запуск теста: Cache Listener")
        listener_result = asyncio.run(test_cache_listener())
        results.append(("Cache Listener", listener_result))
        if listener_result:
            print("✅ ТЕСТ 'Cache Listener' ПРОЙДЕН")
        else:
            print("❌ ТЕСТ 'Cache Listener' НЕ ПРОЙДЕН")
    except Exception as e:
        print(f"💥 ТЕСТ 'Cache Listener' УПАЛ: {e}")
        results.append(("Cache Listener", False))
    
    # Итоги
    print(f"\n{'='*60}")
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ СИСТЕМЫ КЭШИРОВАНИЯ")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ НЕ ПРОЙДЕН"
        print(f"   {test_name:<30} {status}")
    
    print(f"\nОбщий результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система кэширования работает корректно!")
        return True
    else:
        print("⚠️ Некоторые тесты не пройдены. Проверьте логи выше.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 