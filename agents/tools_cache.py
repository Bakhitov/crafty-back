"""
Кэш для динамических инструментов с автоматической инвалидацией.
Любое изменение в БД = автоматическое обновление кэша через updated_at.

ВАЖНО: Webhook endpoints (/cache/invalidate) НЕ НУЖНЫ для обычных операций!
Кэш автоматически инвалидируется через хэширование updated_at триггеров.
Webhook нужен только для:
- Принудительной очистки (админ операции)
- Массовой инвалидации (несколько инструментов)
- Мониторинга и статистики
"""

from typing import Dict, List, Union, Tuple
from uuid import UUID
from threading import RLock
import time
import hashlib

from agno.tools import Toolkit, Function


class ToolsCache:
    """
    Кэш для динамических инструментов.
    Автоматически инвалидируется при ЛЮБЫХ изменениях в БД через updated_at триггеры.
    """
    
    def __init__(self, ttl_seconds: int = 7200):  # 2 часа TTL
        self._cache: Dict[str, Tuple] = {}  # cache_key -> (tool_object, created_at, config_hash)
        self._lock = RLock()
        self._ttl = ttl_seconds
    
    def _hash_tool_config(self, tool) -> str:
        """
        Создает хэш с updated_at - автоматически меняется при ЛЮБЫХ изменениях в БД.
        Триггеры уже настроены! Не нужно думать о том, какие поля важны.
        """
        # Простой подход: используем updated_at как индикатор ЛЮБЫХ изменений
        updated_at_str = tool.updated_at.isoformat() if tool.updated_at else "no_date"
        
        # Хэшируем tool_id + updated_at = уникальный хэш для каждой версии конфигурации
        hash_data = f"{tool.id}|{updated_at_str}"
        return hashlib.md5(hash_data.encode()).hexdigest()[:12]
    
    def _make_cache_key(self, tool_id: UUID, config_hash: str) -> str:
        """Генерация ключа кэша"""
        return f"{tool_id}|{config_hash}"
    
    def get(self, tool_id: UUID, tool_model=None) -> Union[Toolkit, Function, None]:
        """Получение инструмента из кэша"""
        if tool_model is None:
            # Fallback для обратной совместимости - ищем любую версию
            with self._lock:
                for key, cached_data in self._cache.items():
                    if key.startswith(f"{tool_id}|"):
                        tool_object, created_at, _ = cached_data
                        # Проверка TTL
                        if time.time() - created_at <= self._ttl:
                            return tool_object
                        else:
                            del self._cache[key]
            return None
        
        # Проверяем конкретную конфигурацию
        config_hash = self._hash_tool_config(tool_model)
        cache_key = self._make_cache_key(tool_id, config_hash)
        
        with self._lock:
            cached = self._cache.get(cache_key)
            if not cached:
                return None
            
            tool_object, created_at, cached_hash = cached
            
            # Проверка TTL
            if time.time() - created_at > self._ttl:
                del self._cache[cache_key]
                return None
            
            return tool_object
    
    def set(self, tool_id: UUID, tool_object: Union[Toolkit, Function], tool_model) -> None:
        """Сохранение инструмента в кэш"""
        config_hash = self._hash_tool_config(tool_model)
        cache_key = self._make_cache_key(tool_id, config_hash)
        
        with self._lock:
            self._cache[cache_key] = (tool_object, time.time(), config_hash)
    
    def get_batch(self, tool_requests: List[Tuple[UUID, any]]) -> Dict[UUID, Union[Toolkit, Function]]:
        """Получение нескольких инструментов с учетом их конфигураций"""
        result = {}
        with self._lock:
            for tool_id, tool_model in tool_requests:
                tool = self.get(tool_id, tool_model)
                if tool:
                    result[tool_id] = tool
        return result
    
    def invalidate_tool(self, tool_id: UUID) -> int:
        """Инвалидация всех версий инструмента"""
        count = 0
        with self._lock:
            keys_to_remove = [
                key for key in self._cache.keys() 
                if key.startswith(f"{tool_id}|")
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
                count += 1
                
        return count
    
    def invalidate_tools(self, tool_ids: List[UUID]) -> int:
        """Инвалидация нескольких инструментов"""
        count = 0
        for tool_id in tool_ids:
            count += self.invalidate_tool(tool_id)
        return count
    
    def clear(self) -> int:
        """Очистка всего кэша"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count
    
    def stats(self) -> Dict[str, int]:
        """Статистика кэша инструментов"""
        with self._lock:
            now = time.time()
            active = sum(1 for _, created_at, _ in self._cache.values() 
                        if now - created_at <= self._ttl)
            expired = len(self._cache) - active
            
            return {
                "total": len(self._cache),
                "active": active,
                "expired": expired
            }


# Глобальный кэш инструментов
tools_cache = ToolsCache(ttl_seconds=7200)  # 2 часа TTL 