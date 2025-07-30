"""
SQLAlchemy модель для динамических инструментов agno.
Соответствует нативной архитектуре и правилам проекта.
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List
from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from db.models import Base


class Tool(Base):
    """Модель для хранения конфигураций инструментов agno"""
    
    __tablename__ = "tools"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(255), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)  # builtin, mcp, custom
    description = Column(Text, nullable=False)
    configuration = Column(JSONB, nullable=False, default={})
    
    # Новые поля для мультитенантности и организации
    is_public = Column(Boolean, default=False, nullable=False, index=True)
    company_id = Column(UUID, nullable=True, index=True)
    user_id = Column(UUID, nullable=True, index=True)
    display_name = Column(Text, nullable=True)
    category = Column(Text, nullable=True, index=True)
    
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует модель в словарь"""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "configuration": self.configuration,
            "is_public": self.is_public,
            "company_id": str(self.company_id) if self.company_id else None,
            "user_id": str(self.user_id) if self.user_id else None,
            "display_name": self.display_name,
            "category": self.category,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
    def __repr__(self):
        return f"<Tool(name='{self.name}', type='{self.type}', active={self.is_active})>" 