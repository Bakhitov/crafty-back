"""
Pydantic модели для реестров.
Отдельный файл для избежания конфликтов с SQLAlchemy моделями.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, validator


class ModelRegistry(BaseModel):
    """Реестр моделей для переиспользования и ссылок"""
    registry_id: str = Field(description="Уникальный ID модели в реестре")
    name: str = Field(description="Имя модели")
    description: Optional[str] = Field(default=None, description="Описание модели")
    config_data: Dict[str, Any] = Field(description="Конфигурация модели")
    is_active: bool = Field(default=True, description="Активна ли модель")
    tags: Optional[List[str]] = Field(default=None, description="Теги для поиска")
    created_at: Optional[datetime] = Field(default=None, description="Время создания")
    updated_at: Optional[datetime] = Field(default=None, description="Время обновления")


class AgentRegistry(BaseModel):
    """Реестр агентов для ссылок в reasoning_agent и team"""
    registry_id: str = Field(description="Уникальный ID агента в реестре")
    name: str = Field(description="Имя агента")
    description: Optional[str] = Field(default=None, description="Описание агента")
    agent_config: Dict[str, Any] = Field(description="Упрощенная конфигурация агента")
    is_active: bool = Field(default=True, description="Активен ли агент")
    tags: Optional[List[str]] = Field(default=None, description="Теги для поиска")
    created_at: Optional[datetime] = Field(default=None, description="Время создания")
    updated_at: Optional[datetime] = Field(default=None, description="Время обновления")


class HookRegistry(BaseModel):
    """Реестр хуков для tool_hooks"""
    registry_id: str = Field(description="Уникальный ID хука в реестре")
    name: str = Field(description="Имя хука")
    description: Optional[str] = Field(default=None, description="Описание хука")
    hook_type: str = Field(description="Тип хука: before_tool_call, after_tool_call, on_tool_error")
    module_path: str = Field(description="Путь к модулю с функцией хука")
    function_name: str = Field(description="Имя функции хука")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Конфигурация хука")
    is_active: bool = Field(default=True, description="Активен ли хук")
    tags: Optional[List[str]] = Field(default=None, description="Теги для поиска")
    created_at: Optional[datetime] = Field(default=None, description="Время создания")
    updated_at: Optional[datetime] = Field(default=None, description="Время обновления")
    
    @validator('hook_type')
    def validate_hook_type(cls, v):
        """Валидация типа хука"""
        allowed_types = {'before_tool_call', 'after_tool_call', 'on_tool_error'}
        if v not in allowed_types:
            raise ValueError(f"hook_type должен быть одним из: {', '.join(allowed_types)}")
        return v 