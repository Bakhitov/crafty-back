"""
Супер простой кэш для динамических агентов с автоматической инвалидацией.
Любое изменение в БД = автоматическое обновление кэша через updated_at.

ВАЖНО: Webhook endpoints (/cache/invalidate) НЕ НУЖНЫ для обычных операций!
Кэш автоматически инвалидируется через хэширование updated_at триггеров.
Webhook нужен только для:
- Принудительной очистки (админ операции)  
- Массовой инвалидации (все агенты пользователя)
- Мониторинга и статистики
"""

from typing import Dict, Optional
from dataclasses import dataclass
from threading import RLock
import time
import hashlib
import json

from agno.agent import Agent


@dataclass
class CachedAgent:
    """Обертка для кэшированного агента"""
    agent: Agent
    created_at: float
    agent_id: str
    user_id: Optional[str]
    config_hash: str


class DynamicAgentCache:
    """
    Thread-safe кэш для динамических агентов.
    Автоматически инвалидируется при ЛЮБЫХ изменениях в БД через updated_at триггеры.
    """
    
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, CachedAgent] = {}
        self._lock = RLock()
        self._ttl = ttl_seconds
    
    def _hash_config(self, dynamic_agent) -> str:
        """
        Создает хэш с updated_at - автоматически меняется при ЛЮБЫХ изменениях в БД.
        Триггеры уже настроены! Не нужно думать о том, какие поля важны.
        """
        # Простой подход: используем updated_at как индикатор ЛЮБЫХ изменений
        updated_at_str = dynamic_agent.updated_at.isoformat() if dynamic_agent.updated_at else "no_date"
        
        # Хэшируем agent_id + updated_at = уникальный хэш для каждой версии конфигурации
        hash_data = f"{dynamic_agent.agent_id}|{updated_at_str}"
        return hashlib.md5(hash_data.encode()).hexdigest()[:12]
    
    def _make_key(self, agent_id: str, model_id: str, user_id: Optional[str], 
                  debug_mode: bool, config_hash: str) -> str:
        """Генерация ключа кэша"""
        return f"{agent_id}|{model_id}|{user_id or 'global'}|{debug_mode}|{config_hash}"
    
    def get(self, agent_id: str, model_id: str, user_id: Optional[str], 
            debug_mode: bool, dynamic_agent) -> Optional[Agent]:
        """Получение агента из кэша"""
        config_hash = self._hash_config(dynamic_agent)
        key = self._make_key(agent_id, model_id, user_id, debug_mode, config_hash)
        
        with self._lock:
            cached = self._cache.get(key)
            if not cached:
                return None
            
            # Проверка TTL
            if time.time() - cached.created_at > self._ttl:
                del self._cache[key]
                return None
            
            return cached.agent
    
    def set(self, agent: Agent, model_id: str, user_id: Optional[str], 
            debug_mode: bool, dynamic_agent) -> None:
        """Сохранение агента в кэш"""
        config_hash = self._hash_config(dynamic_agent)
        key = self._make_key(agent.agent_id, model_id, user_id, debug_mode, config_hash)
        
        with self._lock:
            self._cache[key] = CachedAgent(
                agent=agent,
                created_at=time.time(),
                agent_id=agent.agent_id,
                user_id=user_id,
                config_hash=config_hash
            )
    
    def invalidate_agent(self, agent_id: str) -> int:
        """Инвалидация всех версий агента"""
        with self._lock:
            keys_to_remove = [
                key for key, cached in self._cache.items() 
                if cached.agent_id == agent_id
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
            
            return len(keys_to_remove)
    
    def invalidate_user(self, user_id: str) -> int:
        """Инвалидация всех агентов пользователя"""
        with self._lock:
            keys_to_remove = [
                key for key, cached in self._cache.items() 
                if cached.user_id == user_id
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
                
            return len(keys_to_remove)
    
    def clear(self) -> int:
        """Очистка всего кэша"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count
    
    def stats(self) -> Dict[str, int]:
        """Статистика кэша"""
        with self._lock:
            now = time.time()
            active = sum(1 for cached in self._cache.values() 
                        if now - cached.created_at <= self._ttl)
            expired = len(self._cache) - active
            
            return {
                "total": len(self._cache),
                "active": active,
                "expired": expired
            }


# Глобальный экземпляр кэша (синглтон)
agent_cache = DynamicAgentCache(ttl_seconds=3600)  # 1 час TTL 