"""
SQLAlchemy модель для динамических агентов agno.
Поддерживает связи с инструментами через tool_ids массив.
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List, Optional
from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID, Text, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from db.models import Base


class DynamicAgent(Base):
    """Модель для хранения конфигураций динамических агентов"""
    
    __tablename__ = "agents"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    agent_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    model_config = Column(JSONB, nullable=False, default={"provider": "openai", "id": "gpt-4.1-mini-2025-04-14"})
    system_instructions = Column(ARRAY(Text), default=[])
    tool_ids = Column(ARRAY(UUID), default=[], index=True)  # Связь с tools.id
    
    # Дополнительные настройки агента (memory, storage, knowledge и т.д.)
    agent_config = Column(JSONB, nullable=False, default={})
    
    # Нативные поля Agno для системного сообщения (опциональные)
    goal = Column(Text, nullable=True)  # Цель агента (agent.goal)
    expected_output = Column(Text, nullable=True)  # Ожидаемый результат (agent.expected_output)
    role = Column(String(255), nullable=True)  # Роль в команде (agent.role)
    
    # Новые поля для мультитенантности и организации
    is_public = Column(Boolean, default=False, nullable=False, index=True)
    company_id = Column(UUID, nullable=True, index=True)
    photo = Column(Text, nullable=True)
    category = Column(Text, nullable=True, index=True)
    
    user_id = Column(String(255), index=True)  # NULL для глобальных агентов
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует модель в словарь"""
        return {
            "id": str(self.id),
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "model_config": self.model_config,
            "system_instructions": self.system_instructions,
            "tool_ids": [str(tid) for tid in (self.tool_ids or [])],
            "agent_config": self.agent_config,
            "goal": self.goal,
            "expected_output": self.expected_output,
            "role": self.role,
            "is_public": self.is_public,
            "company_id": str(self.company_id) if self.company_id else None,
            "photo": self.photo,
            "category": self.category,
            "user_id": self.user_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
    def __repr__(self):
        return f"<DynamicAgent(agent_id='{self.agent_id}', name='{self.name}', active={self.is_active})>" 