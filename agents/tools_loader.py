"""
Загрузчик инструментов для agno с кэшированием конфигураций.
Автоматически учитывает изменения конфигураций через хэширование.
"""

from typing import List, Union, Dict, Tuple
from uuid import UUID
from sqlalchemy.orm import Session

# Нативные agno классы
from agno.tools import Toolkit, Function
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.mcp import MCPTools

# Модели проекта
from db.models.tool import Tool
from agents.tools_cache import tools_cache  # ← КЭШ С УЧЕТОМ КОНФИГУРАЦИЙ


def load_tools_for_agent(db: Session, tool_ids: List[UUID]) -> List[Union[Toolkit, Function]]:
    """
    Загружает инструменты с кэшированием конфигураций.
    Автоматически инвалидируется при изменении конфигураций в БД.
    """
    if not tool_ids:
        return []
    
    # 1. Загружаем все Tool модели из БД (нужны для проверки конфигураций)
    db_tools = db.query(Tool).filter(
        Tool.id.in_(tool_ids), 
        Tool.is_active == True
    ).all()
    
    # Создаем мапинг tool_id -> Tool модель
    tools_by_id = {tool.id: tool for tool in db_tools}
    
    # 2. Подготавливаем запросы для batch кэша с конфигурациями
    cache_requests = []
    for tool_id in tool_ids:
        if tool_id in tools_by_id:
            cache_requests.append((tool_id, tools_by_id[tool_id]))
    
    # 3. Проверяем кэш для всех инструментов с учетом конфигураций ⚡
    cached_tools = tools_cache.get_batch(cache_requests)
    
    # 4. Создаем недостающие инструменты
    result = []
    for tool_id in tool_ids:
        if tool_id in cached_tools:
            # Есть в кэше
            result.append(cached_tools[tool_id])
        elif tool_id in tools_by_id:
            # Создаем новый и кэшируем
            tool_model = tools_by_id[tool_id]
            try:
                agno_tool = _create_tool(tool_model)
                if agno_tool:
                    # Кэшируем с конфигурацией
                    tools_cache.set(tool_id, agno_tool, tool_model)
                    result.append(agno_tool)
            except Exception as e:
                print(f"Error loading tool {tool_model.name}: {e}")
                continue
    
    return result


def _create_tool(tool: Tool) -> Union[Toolkit, Function, None]:
    """Создание Agno инструмента из модели БД"""
    config = tool.configuration or {}
    
    if tool.type == 'builtin':
        return _create_builtin_tool(config)
    elif tool.type == 'mcp':
        return _create_mcp_tool(config)
    elif tool.type == 'custom':
        return _create_custom_tool(tool.name, tool.description, config)
    
    return None


def _create_builtin_tool(config: dict) -> Toolkit:
    """Создает builtin инструмент agno"""
    tool_class = config.get("class", "DuckDuckGoTools")
    params = config.get("params", {})
    
    # Простой маппинг встроенных классов
    if tool_class == "DuckDuckGoTools":
        return DuckDuckGoTools(**params)
    elif tool_class == "FileTools":
        return FileTools(**params)
    else:
        # Fallback
        return DuckDuckGoTools()


def _create_mcp_tool(config: dict) -> MCPTools:
    """Создает MCP инструмент через нативный agno MCPTools"""
    return MCPTools(
        command=config.get("command"),
        url=config.get("url"),
        env=config.get("env", {}),
        transport=config.get("transport", "stdio"),
        timeout_seconds=config.get("timeout_seconds", 5),
        include_tools=config.get("include_tools"),
        exclude_tools=config.get("exclude_tools")
    )


def _create_custom_tool(name: str, description: str, config: dict) -> Function:
    """
    Создает custom функцию из кода.
    ⚡ КЭШИРУЕТСЯ - exec() выполняется только при изменении configuration!
    """
    function_code = config.get("function_code", "")
    
    if not function_code:
        return None
    
    # Выполняем код (в продакшене нужна песочница)
    # ⚡ Это выполняется только при изменении configuration и кэшируется!
    exec_globals = {}
    exec(function_code, exec_globals)
    
    # Находим функцию
    functions = [v for v in exec_globals.values() if callable(v) and not v.__name__.startswith('_')]
    if not functions:
        return None
    
    # Создаем нативный agno Function
    return Function.from_callable(
        functions[0],
        name=name
    ) 