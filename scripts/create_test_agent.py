#!/usr/bin/env python3
"""
Скрипт для создания полноценного тестового динамического агента в БД.
Создает агента со всеми необходимыми конфигурациями для поддержки continue endpoint.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Загружаем переменные окружения из .env файла
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.agent import DynamicAgent
from db.models.tool import Tool

def get_db_session() -> Session:
    """Создает сессию БД для скриптов"""
    return SessionLocal()

def create_test_agent():
    """Создает полноценного тестового агента с поддержкой continue endpoint"""
    db = get_db_session()
    
    try:
        # Проверяем, что есть тестовые инструменты
        tools = db.query(Tool).filter(Tool.name.like('test_%'), Tool.is_active == True).all()
        if not tools:
            print("❌ Тестовые инструменты не найдены. Запустите сначала: python scripts/create_test_tools.py")
            return False
        
        tool_ids = [tool.id for tool in tools[:3]]  # Берем первые 3 инструмента
        print(f"🔧 Будет использовано {len(tool_ids)} инструментов: {[tool.name for tool in tools[:3]]}")
        
        # Удаляем существующий тестовый агент
        existing_agent = db.query(DynamicAgent).filter(DynamicAgent.agent_id == 'test_dynamic_agent').first()
        if existing_agent:
            print(f"🗑️ Удаляю существующий агент: {existing_agent.name}")
            db.delete(existing_agent)
            db.commit()
        
        # Создаем полноценного тестового агента
        test_agent = DynamicAgent(
            agent_id="test_dynamic_agent",
            name="Тестовый Динамический Агент",
            description="Полноценный тестовый агент с поддержкой continue endpoint, памяти и всех необходимых конфигураций.",
            
            # Модель (как в статических агентах)
            model_config={
                "provider": "openai",
                "id": "gpt-4.1-mini-2025-04-14"
            },
            
            # Системные инструкции (детальные, как в статических агентах)
            system_instructions=[
                "Вы - Тестовый Динамический Агент, созданный для проверки функциональности continue endpoint.",
                "",
                "Ваши возможности:",
                "1. Поиск информации в интернете с помощью DuckDuckGo",
                "2. Работа с файлами и документами", 
                "3. Математические вычисления",
                "4. Обработка текста",
                "",
                "Инструкции:",
                "1. Всегда отвечайте на русском языке, если не указано иное.",
                "2. Используйте доступные инструменты для получения актуальной информации.",
                "3. Сохраняйте контекст разговора и ссылайтесь на предыдущие сообщения.",
                "4. При запросе продолжения диалога - корректно обрабатывайте updated_tools.",
                "5. Будьте дружелюбны и полезны.",
                "",
                "Дополнительная информация:",
                "- ID пользователя: {current_user_id}",
                "- Имя пользователя может отличаться от ID - спросите при необходимости."
            ],
            
            # Связанные инструменты
            tool_ids=tool_ids,
            
            # Конфигурация агента (ключевые настройки для continue endpoint)
            agent_config={
                # Storage настройки
                "storage": {
                    "enabled": True,
                    "table_name": "sessions",
                    "type": "postgres"
                },
                
                # Memory настройки (КРИТИЧНО для continue endpoint)
                "memory": {
                    "enabled": True,
                    "table_name": "test_dynamic_agent_memories",
                    "type": "postgres",
                    "delete_memories": True,
                    "clear_memories": True
                },
                
                # History настройки
                "history": {
                    "add_history_to_messages": True,
                    "num_history_runs": 3,
                    "read_chat_history": True
                },
                
                # Agentic memory (КРИТИЧНО для continue endpoint)
                "enable_agentic_memory": True,
                
                # Состояние для continue endpoint
                "continue_support": {
                    "enabled": True,
                    "save_run_state": True,
                    "max_saved_runs": 10
                },
                
                # Другие настройки
                "add_state_in_messages": True,
                "markdown": True,
                "add_datetime_to_instructions": True,
                "debug_mode": True
            },
            
            # Мультитенантность
            is_public=True,  # Доступен всем для тестирования
            category="testing",
            user_id=None,  # Глобальный агент
            is_active=True
        )
        
        db.add(test_agent)
        db.commit()
        db.refresh(test_agent)
        
        print(f"\n✅ Успешно создан тестовый агент:")
        print(f"   - ID: {test_agent.agent_id}")
        print(f"   - Имя: {test_agent.name}")
        print(f"   - Инструментов: {len(test_agent.tool_ids)}")
        print(f"   - UUID: {test_agent.id}")
        
        # Выводим детали конфигурации
        print(f"\n🔧 Конфигурация агента:")
        print(f"   - Storage: включен")
        print(f"   - Memory: включена (критично для continue)")
        print(f"   - History: 3 последних сообщения")
        print(f"   - Continue support: включен")
        print(f"   - Agentic memory: включена")
        
        print(f"\n🧪 Теперь можно тестировать:")
        print(f"1. Базовый запрос:")
        print(f"   curl -X POST 'http://localhost:8000/v1/agents/test_dynamic_agent/runs' \\")
        print(f"     -H 'Content-Type: multipart/form-data' \\")
        print(f"     -F 'message=Привет! Расскажи о себе' \\")
        print(f"     -F 'stream=false' \\")
        print(f"     -F 'session_id=test-session' \\")
        print(f"     -F 'user_id=test-user'")
        
        print(f"\n2. Continue endpoint (после получения run_id из первого запроса):")
        print(f"   curl -X POST 'http://localhost:8000/v1/agents/test_dynamic_agent/runs/RUN_ID/continue' \\")
        print(f"     -H 'Content-Type: multipart/form-data' \\")
        print(f"     -F 'tools=[]' \\")
        print(f"     -F 'stream=false' \\")
        print(f"     -F 'session_id=test-session' \\")
        print(f"     -F 'user_id=test-user'")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания тестового агента: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def create_continue_test_script():
    """Создает скрипт для автоматического тестирования continue endpoint"""
    
    script_content = '''#!/bin/bash

# 🧪 АВТОМАТИЧЕСКИЙ ТЕСТ CONTINUE ENDPOINT
# Тестирует полный цикл: создание диалога -> получение run_id -> continue

set -e

BASE_URL="http://localhost:8000/v1"
AGENT_ID="test_dynamic_agent"
SESSION_ID="continue-test-$(date +%s)"
USER_ID="continue-test-user"

echo "🧪 ТЕСТИРОВАНИЕ CONTINUE ENDPOINT С ДИНАМИЧЕСКИМ АГЕНТОМ"
echo "======================================================="
echo "Агент: $AGENT_ID"
echo "Сессия: $SESSION_ID"
echo "Пользователь: $USER_ID"
echo ""

# 1. Первоначальный запрос для создания run
echo "📨 Шаг 1: Создание первичного run..."
RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs" \\
  -H "Content-Type: multipart/form-data" \\
  -F "message=Привет! Я тестирую continue endpoint. Помнишь ли ты этот разговор?" \\
  -F "stream=false" \\
  -F "session_id=$SESSION_ID" \\
  -F "user_id=$USER_ID")

echo "Ответ первого запроса:"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
echo ""

# Извлекаем run_id из ответа (если есть)
RUN_ID=$(echo "$RESPONSE" | jq -r '.run_id // empty' 2>/dev/null || echo "")

if [[ -z "$RUN_ID" ]]; then
    echo "⚠️ run_id не найден в ответе первого запроса."
    echo "Попытка извлечь из других полей..."
    RUN_ID=$(echo "$RESPONSE" | jq -r '.id // .session_id // empty' 2>/dev/null || echo "")
fi

if [[ -z "$RUN_ID" ]]; then
    echo "❌ Не удалось получить run_id. Continue тест невозможен."
    echo "Это может означать, что агент не сохраняет состояние выполнения."
    exit 1
fi

echo "✅ Получен run_id: $RUN_ID"
echo ""

# 2. Небольшая пауза для сохранения состояния
echo "⏳ Пауза 2 секунды для сохранения состояния..."
sleep 2

# 3. Continue запрос
echo "🔄 Шаг 2: Тестирование continue endpoint..."
CONTINUE_RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs/$RUN_ID/continue" \\
  -H "Content-Type: multipart/form-data" \\
  -F "tools=[]" \\
  -F "stream=false" \\
  -F "session_id=$SESSION_ID" \\
  -F "user_id=$USER_ID")

echo "Ответ continue запроса:"
echo "$CONTINUE_RESPONSE" | jq . 2>/dev/null || echo "$CONTINUE_RESPONSE"
echo ""

# 4. Проверка результата
if echo "$CONTINUE_RESPONSE" | grep -q "error\\|Error\\|404\\|500"; then
    echo "❌ Continue endpoint вернул ошибку"
    echo "Возможные причины:"
    echo "  - run_id не сохранился в агенте"
    echo "  - Агент не поддерживает continue_run"
    echo "  - Неправильная конфигурация storage/memory"
else
    echo "✅ Continue endpoint работает успешно!"
fi

# 5. Тест с обновленными инструментами
echo ""
echo "🔧 Шаг 3: Тестирование continue с обновленными инструментами..."
TOOLS_RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs/$RUN_ID/continue" \\
  -H "Content-Type: multipart/form-data" \\
  -F 'tools=[{"name": "test_duckduckgo_search", "enabled": true}]' \\
  -F "stream=false" \\
  -F "session_id=$SESSION_ID" \\
  -F "user_id=$USER_ID")

echo "Ответ continue с инструментами:"
echo "$TOOLS_RESPONSE" | jq . 2>/dev/null || echo "$TOOLS_RESPONSE"

echo ""
echo "🏁 Тестирование continue endpoint завершено!"
'''

    with open('scripts/test_continue_endpoint.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('scripts/test_continue_endpoint.sh', 0o755)
    print(f"\n📝 Создан скрипт тестирования: scripts/test_continue_endpoint.sh")


if __name__ == "__main__":
    print("🚀 Создание полноценного тестового агента...")
    
    # Создаем агента
    success = create_test_agent()
    
    if success:
        # Создаем скрипт тестирования
        create_continue_test_script()
        
        print(f"\n🎯 Следующие шаги:")
        print(f"1. Запустите сервер: docker compose up -d")
        print(f"2. Протестируйте агента: ./scripts/test_continue_endpoint.sh")
        print(f"3. Или используйте автотест: ./scripts/test_agents_api_full.sh")
        
    sys.exit(0 if success else 1) 