"""
Супер простые webhook endpoints для управления кэшем агентов и инструментов.
Вызываются при изменении агентов/инструментов в БД.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

from agents.agent_cache import agent_cache
from agents.tools_cache import tools_cache  # ← НОВЫЙ КЭШ ИНСТРУМЕНТОВ
from agents.selector import invalidate_available_agents_cache  # ← КЭШ СПИСКА АГЕНТОВ

cache_router = APIRouter(prefix="/cache", tags=["Cache Management"])


class CacheInvalidateRequest(BaseModel):
    """Запрос на инвалидацию кэша"""
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    tool_id: Optional[UUID] = None
    tool_ids: Optional[List[UUID]] = None


@cache_router.post("/invalidate")
async def invalidate_cache(request: CacheInvalidateRequest):
    """
    Webhook для инвалидации кэша агентов и инструментов.
    
    Вызывается при:
    - Изменении конфигурации агента/инструмента
    - Деактивации агента/инструмента
    - Изменении инструментов агента
    """
    invalidated_count = 0
    
    if request.agent_id:
        # Инвалидация конкретного агента (все его версии)
        invalidated_count = agent_cache.invalidate_agent(request.agent_id)
        # Также инвалидируем кэш списка агентов (для CREATE/DELETE случаев)
        invalidate_available_agents_cache()
        return {
            "message": f"Invalidated agent: {request.agent_id}",
            "invalidated_count": invalidated_count,
            "type": "agent"
        }
    
    elif request.user_id:
        # Инвалидация всех агентов пользователя
        invalidated_count = agent_cache.invalidate_user(request.user_id)
        return {
            "message": f"Invalidated user agents: {request.user_id}",
            "invalidated_count": invalidated_count,
            "type": "user_agents"
        }
    
    elif request.tool_id:
        # Инвалидация конкретного инструмента
        invalidated = tools_cache.invalidate_tool(request.tool_id)
        return {
            "message": f"Invalidated tool: {request.tool_id}",
            "invalidated_count": 1 if invalidated else 0,
            "type": "tool"
        }
    
    elif request.tool_ids:
        # Инвалидация нескольких инструментов
        invalidated_count = tools_cache.invalidate_tools(request.tool_ids)
        return {
            "message": f"Invalidated {len(request.tool_ids)} tools",
            "invalidated_count": invalidated_count,
            "type": "tools"
        }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either agent_id, user_id, tool_id, or tool_ids must be provided"
        )


@cache_router.post("/clear")
async def clear_cache():
    """Полная очистка кэша (для админов)"""
    agents_cleared = agent_cache.clear()
    tools_cleared = tools_cache.clear()
    # Также очищаем кэш списка агентов
    invalidate_available_agents_cache()
    
    return {
        "message": "All caches cleared completely",
        "agents_cleared": agents_cleared,
        "tools_cleared": tools_cleared,
        "available_agents_cache_cleared": True,
        "total_cleared": agents_cleared + tools_cleared
    }


@cache_router.get("/stats")
async def get_cache_stats():
    """Статистика всех кэшей"""
    agent_stats = agent_cache.stats()
    tools_stats = tools_cache.stats()
    
    return {
        "agents_cache": {
            **agent_stats,
            "ttl_seconds": 3600
        },
        "tools_cache": {
            **tools_stats,
            "ttl_seconds": 7200
        },
        "total_cached_objects": agent_stats["total"] + tools_stats["total"]
    } 