"""
API для управления динамическими инструментами.
Простые CRUD операции без избыточной сложности.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from db.services.dynamic_tool_service import dynamic_tool_service

tools_router = APIRouter(prefix="/tools", tags=["Dynamic Tools"])

# === Создание динамического инструмента ===
# module_path теперь опционален – вычисляется автоматически, если не передан

class ToolCreateRequest(BaseModel):
    tool_id: str
    name: str
    display_name: str | None = None
    agno_class: str
    module_path: str | None = None  # ← новое поле
    config: Dict[str, Any] = {}
    description: str | None = None
    category: str | None = None
    icon: str | None = None

class ToolUpdateRequest(BaseModel):
    name: str = None
    display_name: str = None
    config: Dict[str, Any] = None
    description: str = None
    category: str = None
    icon: str = None
    is_active: bool = None

@tools_router.get("/available-classes")
def get_available_agno_classes():
    """Получить список доступных классов Agno инструментов"""
    return {
        "classes": dynamic_tool_service.get_available_agno_classes(),
        "total": len(dynamic_tool_service.get_available_agno_classes())
    }

@tools_router.get("/")
def get_all_tools():
    """Получить все активные динамические инструменты"""
    tools = dynamic_tool_service.get_all_active_tools()
    return {
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }

@tools_router.get("/public")
def get_public_tools():
    """Получить все публичные инструменты (is_public=True)"""
    tools = dynamic_tool_service.get_public_tools()
    return {
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }

@tools_router.get("/company/{company_id}")
def get_tools_by_company(company_id: str):
    """Получить все инструменты конкретной компании"""
    tools = dynamic_tool_service.get_tools_by_company(company_id)
    return {
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }

@tools_router.get("/company/{company_id}/accessible")
def get_accessible_tools_for_company(company_id: str):
    """Получить все доступные инструменты для компании (публичные + свои приватные)"""
    tools = dynamic_tool_service.get_accessible_tools_for_company(company_id)
    return {
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }

@tools_router.get("/{tool_id}")
def get_tool(tool_id: str):
    """Получить инструмент по ID"""
    tool = dynamic_tool_service.get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инструмент {tool_id} не найден"
        )
    return tool.to_dict()

@tools_router.post("/")
def create_tool(request: ToolCreateRequest):
    """Создать новый динамический инструмент"""
    try:
        # Проверяем, что класс поддерживается
        available_classes = dynamic_tool_service.get_available_agno_classes()
        if request.agno_class not in available_classes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Класс {request.agno_class} не поддерживается. Доступные: {', '.join(available_classes)}"
            )
        
        # Проверяем уникальность ID
        existing_tool = dynamic_tool_service.get_tool_by_id(request.tool_id)
        if existing_tool:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Инструмент с ID {request.tool_id} уже существует"
            )
        
        # --- Автовычисляем module_path, если не передан
        tool_payload = request.dict()
        if not tool_payload.get("module_path"):
            try:
                import importlib
                # Пытаемся найти класс в agno.tools.*
                possible_module = f"agno.tools.{request.agno_class.lower().replace('tools', '')}"
                mod = importlib.import_module(possible_module)
                # module_path = полное имя модуля (например agno.tools.duckduckgo)
                tool_payload["module_path"] = mod.__name__
            except Exception:
                # Фоллбэк: agno.tools.<clsname lower>
                tool_payload["module_path"] = f"agno.tools.{request.agno_class.lower()}"

        tool = dynamic_tool_service.create_tool(tool_payload)
        return {
            "message": "Инструмент успешно создан",
            "tool": tool.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания инструмента: {str(e)}"
        )

@tools_router.put("/{tool_id}")
def update_tool(tool_id: str, request: ToolUpdateRequest):
    """Обновить динамический инструмент"""
    try:
        tool = dynamic_tool_service.update_tool(
            tool_id, 
            request.dict(exclude_none=True)
        )
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Инструмент {tool_id} не найден"
            )
        
        return {
            "message": "Инструмент успешно обновлен",
            "tool": tool.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления инструмента: {str(e)}"
        )

@tools_router.delete("/{tool_id}")
def delete_tool(tool_id: str):
    """Удалить динамический инструмент"""
    success = dynamic_tool_service.delete_tool(tool_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инструмент {tool_id} не найден"
        )
    
    return {"message": f"Инструмент {tool_id} успешно удален"}

@tools_router.get("/category/{category}")
def get_tools_by_category(category: str):
    """Получить инструменты по категории"""
    tools = dynamic_tool_service.get_tools_by_category(category)
    return {
        "category": category,
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }

@tools_router.get("/templates/{agno_class}")
def get_tool_template(agno_class: str):
    """Получить шаблон конфигурации для класса Agno инструмента"""
    available_classes = dynamic_tool_service.get_available_agno_classes()
    if agno_class not in available_classes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класс {agno_class} не поддерживается"
        )
    
    # Шаблоны конфигураций для популярных инструментов
    templates = {
        "DuckDuckGoTools": {
            "search": True,
            "news": True,
            "timeout": 10
        },
        "YFinanceTools": {
            "stock_price": True,
            "analyst_recommendations": True,
            "stock_fundamentals": True,
            "historical_prices": True,
            "company_info": True,
            "company_news": True
        },
        "GoogleSearchTools": {
            "api_key": "YOUR_API_KEY",
            "search_engine_id": "YOUR_SEARCH_ENGINE_ID"
        },
        "CalculatorTools": {},
        "PythonTools": {
            "base_dir": "/tmp",
            "pip_install": True,
            "run_code": True
        },
        "WebsiteTools": {
            "read_url": True,
            "search_url": True,
            "summarize_url": True
        },
        "FileTools": {
            "read_file": True,
            "write_file": True,
            "list_files": True
        },
        "GithubTools": {
            "search_repos": True,
            "get_repo_info": True,
            "search_issues": True
        },
        "EmailTools": {
            "send_email": True
        },
        "SlackTools": {
            "send_message": True,
            "read_messages": True
        },
        "PostgresTools": {
            "run_sql": True,
            "describe_table": True,
            "export_table_to_csv": True
        },
        "ShellTools": {
            "run_shell_command": True
        }
    }
    
    return {
        "agno_class": agno_class,
        "template": templates.get(agno_class, {}),
        "description": f"Шаблон конфигурации для {agno_class}"
    }

# === ENDPOINTS ДЛЯ КАСТОМНЫХ ИНСТРУМЕНТОВ ПЕРЕНЕСЕНЫ В custom_tools.py ===

# === ОБЩИЕ ENDPOINTS ДЛЯ ВСЕХ ТИПОВ ИНСТРУМЕНТОВ ===

@tools_router.get("/all-types")
def get_all_tool_types():
    """Получить статистику по всем типам инструментов"""
    from db.services.dynamic_tool_service import dynamic_tool_service
    from db.services.custom_tool_service import custom_tool_service
    from db.services.mcp_service import mcp_service
    
    # Получаем статистику
    agno_tools = dynamic_tool_service.get_all_active_tools()
    custom_tools = custom_tool_service.get_all_active_tools()
    mcp_servers = mcp_service.get_all_active_servers()
    
    return {
        "success": True,
        "statistics": {
            "agno_tools": len(agno_tools),
            "custom_tools": len(custom_tools),
            "mcp_servers": len(mcp_servers),
            "total": len(agno_tools) + len(custom_tools) + len(mcp_servers)
        },
        "summary": {
            "agno_tools": [tool.to_dict() for tool in agno_tools[:5]],  # Первые 5
            "custom_tools": [tool.to_dict() for tool in custom_tools[:5]],
            "mcp_servers": [server.to_dict() for server in mcp_servers[:5]]
        }
    }

@tools_router.post("/cache/cleanup")
def cleanup_tool_cache():
    """Очистить устаревшие элементы кэша инструментов"""
    from db.services.dynamic_tool_service import dynamic_tool_service
    
    expired_count = dynamic_tool_service.cleanup_expired_cache()
    
    return {
        "success": True,
        "message": f"Удалено {expired_count} устаревших элементов кэша"
    }

@tools_router.post("/cache/invalidate")
def invalidate_all_cache():
    """Принудительно очистить весь кэш инструментов"""
    from db.services.dynamic_tool_service import dynamic_tool_service
    
    dynamic_tool_service.invalidate_all_tool_cache()
    
    return {
        "success": True,
        "message": "Весь кэш инструментов очищен"
    } 