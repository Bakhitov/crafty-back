"""
API endpoints для MCP серверов.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, Optional
from db.services.mcp_service import mcp_service

mcp_tools_router = APIRouter(prefix="/tools/mcp", tags=["mcp-tools"])


@mcp_tools_router.get("")
def get_mcp_servers():
    """Получить все MCP серверы"""
    servers = mcp_service.get_all_active_servers()
    return {
        "success": True,
        "servers": [server.to_dict() for server in servers],
        "total": len(servers)
    }


@mcp_tools_router.post("")
def create_mcp_server(server_data: dict):
    """Подключить новый MCP сервер"""
    # Валидация конфигурации
    validation = mcp_service.validate_server_config(server_data)
    if not validation['valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибки валидации: {', '.join(validation['errors'])}"
        )
    
    try:
        # Создаем сервер
        server = mcp_service.create_server(server_data)
        
        return {
            "success": True,
            "server": server.to_dict()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания MCP сервера: {str(e)}"
        )


@mcp_tools_router.get("/{server_id}")
def get_mcp_server(server_id: str):
    """Получить MCP сервер по ID"""
    server = mcp_service.get_server_by_id(server_id)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP сервер не найден"
        )
    
    return {
        "success": True,
        "server": server.to_dict()
    }


@mcp_tools_router.put("/{server_id}")
def update_mcp_server(server_id: str, server_data: dict):
    """Обновить MCP сервер"""
    # Валидация обновленных данных
    current_server = mcp_service.get_server_by_id(server_id)
    if not current_server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP сервер не найден"
        )
    
    # Объединяем текущие данные с обновлениями для валидации
    updated_data = current_server.to_dict()
    updated_data.update(server_data)
    
    validation = mcp_service.validate_server_config(updated_data)
    if not validation['valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибки валидации: {', '.join(validation['errors'])}"
        )
    
    try:
        updated_server = mcp_service.update_server(server_id, server_data)
        
        return {
            "success": True,
            "server": updated_server.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления MCP сервера: {str(e)}"
        )


@mcp_tools_router.delete("/{server_id}")
def delete_mcp_server(server_id: str):
    """Удалить MCP сервер"""
    success = mcp_service.delete_server(server_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP сервер не найден"
        )
    
    return {
        "success": True,
        "message": f"MCP сервер '{server_id}' удален"
    }


@mcp_tools_router.post("/{server_id}/test")
async def test_mcp_server(server_id: str):
    """Протестировать подключение к MCP серверу"""
    result = await mcp_service.test_server_connection(server_id)
    
    if not result['success']:
        return result  # Возвращаем как есть, с информацией об ошибке
    
    return result


@mcp_tools_router.get("/{server_id}/tools")
async def get_mcp_server_tools(server_id: str):
    """Получить список инструментов MCP сервера"""
    result = await mcp_service.get_server_tools(server_id)
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result['error']
        )
    
    return result


@mcp_tools_router.post("/{server_id}/execute/{tool_name}")
async def execute_mcp_tool(server_id: str, tool_name: str, parameters: dict = None):
    """Выполнить инструмент MCP сервера"""
    if parameters is None:
        parameters = {}
    
    result = await mcp_service.execute_server_tool(server_id, tool_name, parameters)
    
    if not result['success']:
        if 'available_tools' in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result['error']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result['error']
            )
    
    return result


@mcp_tools_router.get("/transport/{transport}")
def get_mcp_servers_by_transport(transport: str):
    """Получить MCP серверы по типу транспорта"""
    valid_transports = ['stdio', 'sse', 'streamable-http']
    if transport not in valid_transports:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый транспорт. Доступные: {', '.join(valid_transports)}"
        )
    
    servers = mcp_service.get_servers_by_transport(transport)
    return {
        "success": True,
        "transport": transport,
        "servers": [server.to_dict() for server in servers],
        "total": len(servers)
    }


@mcp_tools_router.post("/validate")
def validate_mcp_config(server_data: dict):
    """Валидировать конфигурацию MCP сервера"""
    validation = mcp_service.validate_server_config(server_data)
    return {
        "success": True,
        "validation": validation
    } 