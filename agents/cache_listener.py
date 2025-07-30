"""
PostgreSQL LISTEN/NOTIFY система для автоматической инвалидации кэша.

Слушает уведомления от триггеров БД и автоматически инвалидирует соответствующие кэши.
Это устраняет необходимость в webhook'ах для большинства случаев.
"""

import json
import asyncio
import logging
from typing import Optional
import asyncpg
from contextlib import asynccontextmanager

from agents.agent_cache import agent_cache
from agents.tools_cache import tools_cache  
from agents.selector import invalidate_available_agents_cache
from db.session import db_url

logger = logging.getLogger(__name__)


def convert_sqlalchemy_url_to_asyncpg(sqlalchemy_url: str) -> str:
    """
    Преобразует SQLAlchemy URL в asyncpg URL.
    
    SQLAlchemy: postgresql+psycopg://user:pass@host:port/db?connect_timeout=30&...
    asyncpg:    postgresql://user:pass@host:port/db
    
    Удаляет SQLAlchemy-специфичные параметры, которые не поддерживаются asyncpg.
    """
    # Убираем SQLAlchemy драйвер
    if sqlalchemy_url.startswith("postgresql+psycopg://"):
        url = sqlalchemy_url.replace("postgresql+psycopg://", "postgresql://", 1)
    elif sqlalchemy_url.startswith("postgresql://"):
        url = sqlalchemy_url
    else:
        # Fallback - возвращаем как есть
        return sqlalchemy_url
    
    # Убираем SQLAlchemy параметры, которые не поддерживаются asyncpg
    if "?" in url:
        base_url, params = url.split("?", 1)
        # Список параметров, которые нужно удалить для asyncpg
        sqlalchemy_params = {
            "connect_timeout", "keepalives_idle", "keepalives_interval", 
            "keepalives_count", "pool_pre_ping", "pool_recycle"
        }
        
        # Парсим параметры
        param_pairs = []
        for param in params.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                # Оставляем только asyncpg-совместимые параметры
                if key not in sqlalchemy_params:
                    param_pairs.append(param)
        
        # Собираем URL обратно
        if param_pairs:
            return f"{base_url}?{'&'.join(param_pairs)}"
        else:
            return base_url
    
    return url


class CacheInvalidationListener:
    """
    Слушает PostgreSQL NOTIFY события и автоматически инвалидирует кэши.
    
    Работает через механизм LISTEN/NOTIFY PostgreSQL:
    1. Триггеры в БД отправляют NOTIFY при INSERT/DELETE
    2. Этот listener получает уведомления
    3. Автоматически инвалидирует соответствующие кэши
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection: Optional[asyncpg.Connection] = None
        self.is_listening = False
        
    async def start_listening(self):
        """Запускает прослушивание уведомлений от PostgreSQL"""
        try:
            self.connection = await asyncpg.connect(self.database_url)
            await self.connection.add_listener('cache_invalidation', self._handle_cache_notification)
            self.is_listening = True
            logger.info("Cache invalidation listener started successfully")
            
            # Держим соединение активным
            while self.is_listening:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in cache listener: {e}")
            await self.stop_listening()
    
    async def stop_listening(self):
        """Останавливает прослушивание"""
        self.is_listening = False
        if self.connection:
            try:
                await self.connection.remove_listener('cache_invalidation', self._handle_cache_notification)
                await self.connection.close()
            except Exception as e:
                logger.error(f"Error stopping cache listener: {e}")
            finally:
                self.connection = None
        logger.info("Cache invalidation listener stopped")
    
    async def _handle_cache_notification(self, connection, pid, channel, payload):
        """
        Обрабатывает уведомления от PostgreSQL триггеров.
        
        Payload format:
        {
            "operation": "INSERT|DELETE",
            "table": "agents|tools", 
            "id": "uuid",
            "agent_id": "string" (только для agents)
        }
        """
        try:
            data = json.loads(payload)
            operation = data.get('operation')
            table = data.get('table')
            record_id = data.get('id')
            agent_id = data.get('agent_id')
            
            logger.debug(f"Cache invalidation: {operation} on {table}, id={record_id}")
            
            if table == 'agents':
                if operation == 'INSERT':
                    # Новый агент создан - инвалидируем кэш списка агентов
                    invalidate_available_agents_cache()
                    logger.info(f"Invalidated available agents cache due to INSERT: {agent_id}")
                    
                elif operation == 'DELETE':
                    # Агент удален - инвалидируем конкретного агента + список
                    if agent_id:
                        invalidated_count = agent_cache.invalidate_agent(agent_id)
                        logger.info(f"Invalidated agent cache: {agent_id} ({invalidated_count} entries)")
                    invalidate_available_agents_cache()
                    logger.info(f"Invalidated available agents cache due to DELETE: {agent_id}")
            
            elif table == 'tools':
                if operation == 'INSERT':
                    # Новый инструмент создан - можно добавить кэш списка инструментов если нужно
                    logger.info(f"New tool created: {record_id}")
                    
                elif operation == 'DELETE':
                    # Инструмент удален - инвалидируем из кэша инструментов
                    try:
                        from uuid import UUID
                        tool_uuid = UUID(record_id)
                        invalidated_count = tools_cache.invalidate_tool(tool_uuid)
                        logger.info(f"Invalidated tool cache: {record_id} ({invalidated_count} entries)")
                    except ValueError:
                        logger.warning(f"Invalid UUID for tool: {record_id}")
                        
        except Exception as e:
            logger.error(f"Error handling cache notification: {e}, payload: {payload}")


# Глобальный экземпляр listener'а
cache_listener = CacheInvalidationListener(convert_sqlalchemy_url_to_asyncpg(db_url))


@asynccontextmanager
async def cache_listener_context():
    """Context manager для запуска/остановки cache listener'а"""
    try:
        # Запускаем listener в фоновой задаче
        listener_task = asyncio.create_task(cache_listener.start_listening())
        yield cache_listener
    finally:
        # Останавливаем listener
        await cache_listener.stop_listening()
        if not listener_task.done():
            listener_task.cancel()
            try:
                await listener_task
            except asyncio.CancelledError:
                pass


async def start_cache_listener_background():
    """Запускает cache listener в фоновом режиме (для использования в FastAPI)"""
    asyncio.create_task(cache_listener.start_listening())


async def stop_cache_listener_background():
    """Останавливает фоновый cache listener"""
    await cache_listener.stop_listening() 