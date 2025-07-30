"""
Простые эндпоинты для получения списка инструментов.
Аналогично эндпоинту получения списка агентов.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models.tool import Tool
from db.session import get_db

######################################################
## Routes for Tools List
######################################################

tools_router = APIRouter(prefix="/tools", tags=["Tools"])


@tools_router.get("", response_model=List[dict])
async def list_tools(
    type_filter: Optional[str] = Query(None, description="Фильтр по типу (builtin, mcp, custom)"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    is_active: bool = Query(True, description="Только активные инструменты"),
    db: Session = Depends(get_db)
):
    """
    Возвращает список всех доступных инструментов с возможностью фильтрации.
    Аналогично GET /agents для получения списка агентов.

    Args:
        type_filter: Фильтр по типу инструмента (builtin, mcp, custom)
        category: Фильтр по категории
        is_active: Только активные инструменты (по умолчанию True)
        db: Сессия БД

    Returns:
        List[dict]: Список инструментов с базовой информацией
    """
    query = db.query(Tool).filter(Tool.is_active == is_active)
    
    if type_filter:
        query = query.filter(Tool.type == type_filter)
    if category:
        query = query.filter(Tool.category == category)
    
    tools = query.all()
    
    # Возвращаем только основную информацию, как для агентов
    return [
        {
            "id": str(tool.id),
            "name": tool.name,
            "type": tool.type,
            "description": tool.description,
            "display_name": tool.display_name or tool.name,
            "category": tool.category,
            "is_public": tool.is_public,
            "is_active": tool.is_active
        }
        for tool in tools
    ] 