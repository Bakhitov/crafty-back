"""
API endpoints для кастомных Python инструментов.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, Optional
from db.services.custom_tool_service import custom_tool_service

custom_tools_router = APIRouter(prefix="/tools/custom", tags=["custom-tools"])


@custom_tools_router.get("")
def get_custom_tools():
    """Получить все кастомные инструменты"""
    tools = custom_tool_service.get_all_active_tools()
    return {
        "success": True,
        "tools": [tool.to_dict() for tool in tools],
        "total": len(tools)
    }


@custom_tools_router.post("")
def create_custom_tool(tool_data: dict):
    """Создать кастомный Python инструмент"""
    # Валидация обязательных полей
    required_fields = ['tool_id', 'name', 'source_code']
    for field in required_fields:
        if field not in tool_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Поле '{field}' обязательно"
            )
    
    try:
        # Сначала тестируем код
        test_result = custom_tool_service.test_tool_code(
            tool_data['source_code'], 
            tool_data.get('config', {})
        )
        
        if not test_result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка в коде: {test_result['error']}"
            )
        
        # Создаем инструмент
        tool = custom_tool_service.create_tool(tool_data)
        
        return {
            "success": True,
            "tool": tool.to_dict(),
            "functions": test_result['functions']
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания инструмента: {str(e)}"
        )


@custom_tools_router.get("/{tool_id}")
def get_custom_tool(tool_id: str):
    """Получить кастомный инструмент по ID"""
    tool = custom_tool_service.get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кастомный инструмент не найден"
        )
    
    return {
        "success": True,
        "tool": tool.to_dict()
    }


@custom_tools_router.put("/{tool_id}")
def update_custom_tool(tool_id: str, tool_data: dict):
    """Обновить кастомный инструмент"""
    try:
        # Если обновляется код, тестируем его
        if 'source_code' in tool_data:
            test_result = custom_tool_service.test_tool_code(
                tool_data['source_code'],
                tool_data.get('config', {})
            )
            
            if not test_result['success']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ошибка в коде: {test_result['error']}"
                )
        
        # Обновляем инструмент
        updated_tool = custom_tool_service.update_tool(tool_id, tool_data)
        
        if not updated_tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Кастомный инструмент не найден"
            )
        
        return {
            "success": True,
            "tool": updated_tool.to_dict()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления инструмента: {str(e)}"
        )


@custom_tools_router.delete("/{tool_id}")
def delete_custom_tool(tool_id: str):
    """Удалить кастомный инструмент"""
    success = custom_tool_service.delete_tool(tool_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кастомный инструмент не найден"
        )
    
    return {
        "success": True,
        "message": f"Кастомный инструмент '{tool_id}' удален"
    }


@custom_tools_router.post("/test")
def test_custom_tool_code(request: dict):
    """Протестировать код кастомного инструмента"""
    if 'source_code' not in request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поле 'source_code' обязательно"
        )
    
    result = custom_tool_service.test_tool_code(
        request['source_code'],
        request.get('config', {})
    )
    
    return result


@custom_tools_router.get("/{tool_id}/functions")
def get_custom_tool_functions(tool_id: str):
    """Получить список функций кастомного инструмента"""
    result = custom_tool_service.get_tool_functions(tool_id)
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result['error']
        )
    
    return result


@custom_tools_router.post("/{tool_id}/execute/{function_name}")
def execute_custom_tool_function(tool_id: str, function_name: str, parameters: dict = None):
    """Выполнить функцию кастомного инструмента"""
    if parameters is None:
        parameters = {}
    
    result = custom_tool_service.execute_tool_function(tool_id, function_name, parameters)
    
    if not result['success']:
        if 'available_functions' in result:
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