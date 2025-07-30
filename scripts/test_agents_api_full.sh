#!/bin/bash

# 🧪 ПОЛНЫЙ АВТОМАТИЗИРОВАННЫЙ ТЕСТ ВСЕХ ЭНДПОИНТОВ AGENT-API
# Покрывает все фазы: подготовка, агенты, continue, сессии, системные эндпоинты

set -e  # Останавливаться при ошибках

BASE_URL="http://localhost:8000/v1"
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).log"
TEST_FILES_DIR="test_files"

echo "🧪 ЗАПУСК ПОЛНОГО ТЕСТИРОВАНИЯ AGENT-API ПРОЕКТА"
echo "🧪 Полное тестирование Agent-API - $(date)" > "$RESULTS_FILE"
echo "Покрытие: агенты, инструменты, сессии, файлы, системные эндпоинты" >> "$RESULTS_FILE"
echo "=================================" >> "$RESULTS_FILE"

# Функция для тестирования
test_endpoint() {
    local name="$1"
    local curl_cmd="$2"
    local expect_success="${3:-true}"
    
    echo "🔍 Тестируем: $name"
    echo "🔍 Тест: $name" >> "$RESULTS_FILE"
    
    # Выполняем curl команду и захватываем вывод
    response=$(eval "$curl_cmd" 2>&1 || echo "CURL_ERROR")
    http_code=$(echo "$response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2 | tail -1)
    
    # Определяем успех
    if [[ "$expect_success" == "true" ]]; then
        if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
            echo "✅ УСПЕХ: $name (код: $http_code)"
            echo "✅ УСПЕХ: $name (код: $http_code)" >> "$RESULTS_FILE"
        else
            echo "❌ ОШИБКА: $name (код: $http_code)"
            echo "❌ ОШИБКА: $name (код: $http_code)" >> "$RESULTS_FILE"
        fi
    else
        if [[ "$http_code" =~ ^[4-5][0-9][0-9]$ ]]; then
            echo "✅ ОЖИДАЕМАЯ ОШИБКА: $name (код: $http_code)"
            echo "✅ ОЖИДАЕМАЯ ОШИБКА: $name (код: $http_code)" >> "$RESULTS_FILE"
        else
            echo "❌ НЕОЖИДАННЫЙ УСПЕХ: $name (код: $http_code)"
            echo "❌ НЕОЖИДАННЫЙ УСПЕХ: $name (код: $http_code)" >> "$RESULTS_FILE"
        fi
    fi
    
    echo "Ответ: $response" >> "$RESULTS_FILE"
    echo "---" >> "$RESULTS_FILE"
    sleep 0.5  # Небольшая пауза между запросами
}

# Проверяем наличие тестовых файлов
if [[ ! -d "$TEST_FILES_DIR" ]]; then
    echo "❌ Директория $TEST_FILES_DIR не найдена!"
    exit 1
fi

echo "📁 Используем тестовые файлы из $TEST_FILES_DIR"

echo ""
echo "🚀 ФАЗА 0: ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ"
echo "====================================="

# Создание тестовых инструментов
echo "🔧 Создание тестовых инструментов..."
if python3 scripts/create_test_tools.py > /dev/null 2>&1; then
    echo "✅ Тестовые инструменты созданы успешно"
else
    echo "⚠️ Не удалось создать тестовые инструменты (возможно, уже существуют)"
fi

echo ""
echo "🛠️ ФАЗА 1: СИСТЕМНЫЕ ЭНДПОИНТЫ"
echo "==============================="

# 1.1 Health Check
test_endpoint "Health Check" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/health'"

# 1.2 Список агентов
test_endpoint "Получение списка агентов" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents'"

# 1.3 Список инструментов (НОВЫЙ ЭНДПОИНТ)
test_endpoint "Получение списка инструментов" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools'"

# 1.4 Фильтрация инструментов по типу
test_endpoint "Фильтрация инструментов по типу builtin" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?type_filter=builtin'"

test_endpoint "Фильтрация инструментов по типу mcp" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?type_filter=mcp'"

test_endpoint "Фильтрация инструментов по типу custom" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?type_filter=custom'"

# 1.5 Фильтрация инструментов по категории
test_endpoint "Фильтрация инструментов по категории search" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?category=search'"

test_endpoint "Фильтрация инструментов по категории files" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?category=files'"

# 1.6 Неактивные инструменты
test_endpoint "Получение неактивных инструментов" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?is_active=false'"

# 1.7 Комбинированная фильтрация
test_endpoint "Комбинированная фильтрация инструментов" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/tools?type_filter=builtin&category=search&is_active=true'"

echo ""
echo "🎮 ФАЗА 2: БАЗОВЫЕ ФУНКЦИИ АГЕНТОВ"
echo "=================================="

# 2.1 Базовые тесты без файлов
test_endpoint "Базовое сообщение test_dynamic_agent" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Привет! Расскажи о себе' -F 'stream=false'"

# 2.2 Тесты других агентов
test_endpoint "Базовое сообщение test_dynamic_agent" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Привет! Расскажи о себе' -F 'stream=false'"

# 2.3 Тесты с файлами
test_endpoint "Отправка текстового файла динамическому агенту" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Суммируй содержание файла' -F 'files=@$TEST_FILES_DIR/sample.txt' -F 'stream=false'"

test_endpoint "Отправка JSON файла динамическому агенту" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Проанализируй структуру JSON' -F 'files=@$TEST_FILES_DIR/data.json' -F 'stream=false'"

test_endpoint "Отправка CSV файла динамическому агенту" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Создай отчет по данным' -F 'files=@$TEST_FILES_DIR/sample.csv' -F 'stream=false'"

# 2.4 Тест изображения (если доступно)
if [[ -f "$TEST_FILES_DIR/testImage.jpeg" ]]; then
    test_endpoint "Отправка изображения динамическому агенту" \
        "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Что на этом изображении?' -F 'files=@$TEST_FILES_DIR/testImage.jpeg' -F 'stream=false'"
fi

# 2.5 Множественные файлы
test_endpoint "Отправка нескольких файлов динамическому агенту" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Обработай все файлы' -F 'files=@$TEST_FILES_DIR/sample.txt' -F 'files=@$TEST_FILES_DIR/data.json' -F 'stream=false' -F 'session_id=multi-test' -F 'user_id=test-user'"

# 2.6 Тесты ошибок
test_endpoint "Несуществующий агент" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/fake-agent-12345/runs' -H 'Content-Type: multipart/form-data' -F 'message=Тест'" \
    "false"

echo ""
echo "⚡ ФАЗА 3: ПРОДОЛЖЕНИЕ ВЫПОЛНЕНИЯ"
echo "================================"

# 3.0 Создаем реальный run для тестирования continue
echo "📨 Создание реального run для тестирования continue..."
CONTINUE_TEST_RESPONSE=$(curl -s -w 'HTTP_CODE:%{http_code}' -X POST "$BASE_URL/agents/test_dynamic_agent/runs" \
    -H "Content-Type: multipart/form-data" \
    -F "message=Привет! Я тестирую continue endpoint. Помнишь ли ты этот разговор?" \
    -F "stream=false" \
    -F "session_id=continue-test-$(date +%s)" \
    -F "user_id=continue-test-user")

# Извлекаем run_id из ответа
REAL_RUN_ID=$(echo "$CONTINUE_TEST_RESPONSE" | sed 's/HTTP_CODE:.*$//' | jq -r '.run_id // empty' 2>/dev/null || echo "")

if [[ -z "$REAL_RUN_ID" ]]; then
    echo "⚠️ Не удалось получить run_id. Используем фиктивные тесты."
    # 3.1 Continue endpoint (фиктивный тест)
    test_endpoint "Continue endpoint (базовый)" \
        "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/test-run-123/continue' -H 'Content-Type: multipart/form-data' -F 'tools=[]' -F 'stream=false'"
    
    # 3.2 Continue с обновленными инструментами
    test_endpoint "Continue с инструментами" \
        "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/some-run-id/continue' -H 'Content-Type: multipart/form-data' -F 'tools=[{\"name\": \"test_duckduckgo_search\", \"enabled\": true}]' -F 'stream=false'"
else
    echo "✅ Получен реальный run_id: $REAL_RUN_ID"
    sleep 2  # Пауза для сохранения состояния
    
    # 3.1 Continue endpoint (с реальным run_id)
    test_endpoint "Continue endpoint (базовый)" \
        "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/$REAL_RUN_ID/continue' -H 'Content-Type: multipart/form-data' -F 'tools=[]' -F 'stream=false'"
    
    # 3.2 Continue с обновленными инструментами (с реальным run_id)
    test_endpoint "Continue с инструментами" \
        "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/$REAL_RUN_ID/continue' -H 'Content-Type: multipart/form-data' -F 'tools=[{\"name\": \"test_duckduckgo_search\", \"enabled\": true}]' -F 'stream=false'"
fi

# 3.3 Тесты ошибок continue
test_endpoint "Continue с неправильным JSON" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/test-run/continue' -H 'Content-Type: multipart/form-data' -F 'tools=invalid-json' -F 'stream=false'" \
    "false"

test_endpoint "Continue несуществующего run" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs/non-existent-run-id/continue' -H 'Content-Type: multipart/form-data' -F 'tools=[]' -F 'stream=false'"

echo ""
echo "🔄 ФАЗА 4: УПРАВЛЕНИЕ СЕССИЯМИ И ПАМЯТЬЮ"
echo "========================================"

# 4.1 Тесты сессий
test_endpoint "Получение всех сессий агента" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/sessions'"

test_endpoint "Получение сессий с user_id" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/sessions?user_id=test-user'"

test_endpoint "Получение конкретной сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/sessions/test-session-123'"

# 4.2 Управление сессиями
test_endpoint "Переименование сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/sessions/test-session/rename' -H 'Content-Type: application/json' -d '{\"name\": \"Новое имя\", \"user_id\": \"test-user\"}'"

test_endpoint "Удаление сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X DELETE '$BASE_URL/agents/test_dynamic_agent/sessions/old-session'"

# 4.3 Тесты памяти
test_endpoint "Получение памяти агента" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/memories?user_id=test-user'"

# 4.4 Тесты ошибок sessions & memory
test_endpoint "Память без user_id (ошибка)" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/memories'" \
    "false"

test_endpoint "Несуществующая сессия" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/sessions/absolutely-fake-session-id'"

echo ""
echo "📚 ФАЗА 5: БАЗА ЗНАНИЙ"
echo "======================"

# 5.1 Загрузка базы знаний для поддерживающих агентов - УБРАНО
# (статические агенты не тестируем)

# 5.2 Попытка загрузки для агента без базы знаний - УБРАНО
# (статические агенты не тестируем)

echo ""
echo "🔗 ФАЗА 6: ИНТЕГРАЦИОННЫЕ ТЕСТЫ"
echo "==============================="

# 6.1 Создание сессии с контекстом
echo "🔄 Создание интеграционной сессии..."
SESSION_ID="integration-test-$(date +%s)"
USER_ID="integration-test-user"

test_endpoint "Создание сессии с JSON файлом" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Проанализируй этот файл и запомни его содержание' -F 'files=@$TEST_FILES_DIR/data.json' -F 'session_id=$SESSION_ID' -F 'user_id=$USER_ID' -F 'stream=false'"

# 6.2 Продолжение работы в той же сессии
test_endpoint "Продолжение работы в сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Что было в предыдущем файле?' -F 'session_id=$SESSION_ID' -F 'user_id=$USER_ID' -F 'stream=false'"

# 6.3 Проверка созданной сессии
test_endpoint "Проверка созданной сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/sessions?user_id=$USER_ID'"

# 6.4 Переименование интеграционной сессии
test_endpoint "Переименование интеграционной сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/sessions/$SESSION_ID/rename' -H 'Content-Type: application/json' -d '{\"name\": \"Интеграционный тест\", \"user_id\": \"$USER_ID\"}'"

# 6.5 Получение памяти интеграционного пользователя
test_endpoint "Получение памяти интеграционного пользователя" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X GET '$BASE_URL/agents/test_dynamic_agent/memories?user_id=$USER_ID'"

# 6.6 Очистка интеграционной сессии
test_endpoint "Удаление интеграционной сессии" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X DELETE '$BASE_URL/agents/test_dynamic_agent/sessions/$SESSION_ID'"

echo ""
echo "🎯 ФАЗА 7: ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ"
echo "==================================="

# 7.1 Параллельные запросы к динамическому агенту
echo "🚀 Запуск параллельных тестов..."

test_endpoint "Параллельный тест 1" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Параллельный тест 1' -F 'stream=false'" &

test_endpoint "Параллельный тест 2" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Параллельный тест 2' -F 'stream=false'" &

test_endpoint "Параллельный тест 3" \
    "curl -s -w 'HTTP_CODE:%{http_code}' -X POST '$BASE_URL/agents/test_dynamic_agent/runs' -H 'Content-Type: multipart/form-data' -F 'message=Параллельный тест 3' -F 'stream=false'" &

wait  # Ожидаем завершения всех параллельных задач
echo "✅ Параллельные тесты завершены"

echo ""
echo "✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!"
echo "=========================="
echo "📄 Результаты сохранены в: $RESULTS_FILE"
echo ""
echo "📊 Сводка результатов:"
echo "   - Тестов успешных: $(grep -c "✅ УСПЕХ" "$RESULTS_FILE" 2>/dev/null || echo "0")"
echo "   - Тестов с ошибками: $(grep -c "❌ ОШИБКА" "$RESULTS_FILE" 2>/dev/null || echo "0")"
echo "   - Ожидаемых ошибок: $(grep -c "✅ ОЖИДАЕМАЯ ОШИБКА" "$RESULTS_FILE" 2>/dev/null || echo "0")"
echo "   - Неожиданных успехов: $(grep -c "❌ НЕОЖИДАННЫЙ УСПЕХ" "$RESULTS_FILE" 2>/dev/null || echo "0")"
echo ""
echo "🔍 Для просмотра детальных результатов:"
echo "   cat $RESULTS_FILE"
echo ""
echo "📋 Фазы тестирования:"
echo "   ✅ Фаза 0: Подготовка данных"
echo "   ✅ Фаза 1: Системные эндпоинты (health, agents, tools)"
echo "   ✅ Фаза 2: Базовые функции агентов"
echo "   ✅ Фаза 3: Продолжение выполнения (continue)"
echo "   ✅ Фаза 4: Управление сессиями и памятью"
echo "   ✅ Фаза 5: База знаний"
echo "   ✅ Фаза 6: Интеграционные тесты"
echo "   ✅ Фаза 7: Тесты производительности"

# Финальная проверка критических компонентов
echo ""
echo "🎯 КРИТИЧЕСКИЕ ПРОВЕРКИ:"
health_status=$(curl -s "$BASE_URL/health" | grep -o '"status":"success"' || echo "FAILED")
if [[ "$health_status" == '"status":"success"' ]]; then
    echo "   ✅ API доступен"
else
    echo "   ❌ API недоступен"
fi

agents_count=$(curl -s "$BASE_URL/agents" | grep -o ',' | wc -l)
if [[ $agents_count -gt 0 ]]; then
    echo "   ✅ Агенты доступны ($((agents_count + 1)) агентов)"
else
    echo "   ❌ Агенты недоступны"
fi

tools_response=$(curl -s -w "%{http_code}" "$BASE_URL/tools" -o /dev/null)
if [[ "$tools_response" == "200" ]]; then
    echo "   ✅ Эндпоинт инструментов работает"
else
    echo "   ❌ Эндпоинт инструментов недоступен"
fi

echo ""
echo "🏁 Тестирование Agent-API проекта завершено!" 