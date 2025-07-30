#!/bin/bash

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
RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs" \
  -H "Content-Type: multipart/form-data" \
  -F "message=Привет! Я тестирую continue endpoint. Помнишь ли ты этот разговор?" \
  -F "stream=false" \
  -F "session_id=$SESSION_ID" \
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
CONTINUE_RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs/$RUN_ID/continue" \
  -H "Content-Type: multipart/form-data" \
  -F "tools=[]" \
  -F "stream=false" \
  -F "session_id=$SESSION_ID" \
  -F "user_id=$USER_ID")

echo "Ответ continue запроса:"
echo "$CONTINUE_RESPONSE" | jq . 2>/dev/null || echo "$CONTINUE_RESPONSE"
echo ""

# 4. Проверка результата
if echo "$CONTINUE_RESPONSE" | grep -q "error\|Error\|404\|500"; then
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
TOOLS_RESPONSE=$(curl -s -X POST "$BASE_URL/agents/$AGENT_ID/runs/$RUN_ID/continue" \
  -H "Content-Type: multipart/form-data" \
  -F 'tools=[{"name": "test_duckduckgo_search", "enabled": true}]' \
  -F "stream=false" \
  -F "session_id=$SESSION_ID" \
  -F "user_id=$USER_ID")

echo "Ответ continue с инструментами:"
echo "$TOOLS_RESPONSE" | jq . 2>/dev/null || echo "$TOOLS_RESPONSE"

echo ""
echo "🏁 Тестирование continue endpoint завершено!"
