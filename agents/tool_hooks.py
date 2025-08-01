"""
Реестр Tool Hooks для динамических агентов.
Предустановленные middleware функции для инструментов.
"""

from typing import Dict, List, Callable, Any, Optional
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)


# === ГОТОВЫЕ HOOK ФУНКЦИИ ===

def logging_hook(func: Callable) -> Callable:
    """Логирование вызовов инструментов"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"🔧 Tool called: {func.__name__}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"✅ Tool {func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ Tool {func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper


def rate_limiting_hook(max_calls_per_minute: int = 60):
    """Ограничение частоты вызовов инструментов"""
    call_times = []
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Очищаем старые вызовы (старше минуты)
            call_times[:] = [t for t in call_times if now - t < 60]
            
            if len(call_times) >= max_calls_per_minute:
                raise Exception(f"Rate limit exceeded: {max_calls_per_minute} calls/minute")
            
            call_times.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validation_hook(func: Callable) -> Callable:
    """Валидация входных параметров инструментов"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Проверяем на опасные паттерны
        dangerous_patterns = ['rm -rf', 'DELETE FROM', 'DROP TABLE', '__import__', 'eval(', 'exec(']
        
        all_args = ' '.join(str(arg) for arg in args) + ' '.join(str(v) for v in kwargs.values())
        
        for pattern in dangerous_patterns:
            if pattern.lower() in all_args.lower():
                logger.warning(f"🚨 Dangerous pattern detected in tool call: {pattern}")
                raise Exception(f"Dangerous operation blocked: {pattern}")
        
        return func(*args, **kwargs)
    return wrapper


def caching_hook(cache_ttl: int = 300):
    """Кэширование результатов инструментов"""
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша из аргументов
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            now = time.time()
            
            # Проверяем кэш
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if now - timestamp < cache_ttl:
                    logger.debug(f"🔄 Cache hit for {func.__name__}")
                    return result
                else:
                    del cache[cache_key]
            
            # Выполняем функцию и кэшируем результат
            result = func(*args, **kwargs)
            cache[cache_key] = (result, now)
            logger.debug(f"💾 Cached result for {func.__name__}")
            return result
        return wrapper
    return decorator


def metrics_hook(func: Callable) -> Callable:
    """Сбор метрик использования инструментов"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Здесь можно отправлять метрики в систему мониторинга
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Отправляем метрики (заглушка)
            logger.debug(f"📊 Metrics: {func.__name__} - success - {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.debug(f"📊 Metrics: {func.__name__} - error - {duration:.3f}s")
            raise
    return wrapper


def error_recovery_hook(func: Callable) -> Callable:
    """Автоматическое восстановление после ошибок"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"🔄 Tool {func.__name__} failed (attempt {attempt + 1}), retrying: {e}")
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    logger.error(f"❌ Tool {func.__name__} failed after {max_retries + 1} attempts: {e}")
                    raise
    return wrapper


# === РЕЕСТР HOOK'ОВ ===

TOOL_HOOKS_REGISTRY: Dict[str, Callable] = {
    "logging": logging_hook,
    "rate_limiting": lambda: rate_limiting_hook(max_calls_per_minute=30),
    "rate_limiting_strict": lambda: rate_limiting_hook(max_calls_per_minute=10),
    "rate_limiting_relaxed": lambda: rate_limiting_hook(max_calls_per_minute=60),
    "validation": validation_hook,
    "cache_5min": lambda: caching_hook(cache_ttl=300),
    "cache_1min": lambda: caching_hook(cache_ttl=60),
    "cache_15min": lambda: caching_hook(cache_ttl=900),
    "metrics": metrics_hook,
    "error_recovery": error_recovery_hook,
}


def get_tool_hooks(hook_names: List[str]) -> List[Callable]:
    """
    Получить hook функции по именам
    
    Args:
        hook_names: Список имен hook'ов
        
    Returns:
        Список hook функций
    """
    hooks = []
    for hook_name in hook_names:
        if hook_name in TOOL_HOOKS_REGISTRY:
            hook_func = TOOL_HOOKS_REGISTRY[hook_name]
            # Если это фабрика (lambda), вызываем её
            if callable(hook_func) and any(hook_name.startswith(prefix) for prefix in ['rate_limiting', 'cache']):
                hooks.append(hook_func())
            else:
                hooks.append(hook_func)
        else:
            logger.warning(f"Tool hook '{hook_name}' not found in registry")
    
    return hooks


def register_tool_hook(name: str, hook_func: Callable):
    """Зарегистрировать новый hook"""
    TOOL_HOOKS_REGISTRY[name] = hook_func


def list_available_hooks() -> List[str]:
    """Список доступных hook'ов"""
    return list(TOOL_HOOKS_REGISTRY.keys())


def get_hook_descriptions() -> Dict[str, str]:
    """Получить описания всех hook'ов"""
    return {
        "logging": "Логирование всех вызовов инструментов с временем выполнения",
        "rate_limiting": "Ограничение до 30 вызовов в минуту",
        "rate_limiting_strict": "Строгое ограничение до 10 вызовов в минуту",
        "rate_limiting_relaxed": "Мягкое ограничение до 60 вызовов в минуту",
        "validation": "Проверка на опасные команды и паттерны",
        "cache_1min": "Кэширование результатов на 1 минуту",
        "cache_5min": "Кэширование результатов на 5 минут",
        "cache_15min": "Кэширование результатов на 15 минут",
        "metrics": "Сбор метрик использования инструментов",
        "error_recovery": "Автоматические повторные попытки при ошибках"
    } 