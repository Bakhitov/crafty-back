"""add_multitenancy_and_organization_fields

Revision ID: c7dd7b0ce41c
Revises: debe81ec8e6f
Create Date: 2025-07-30 13:07:47.179513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c7dd7b0ce41c'
down_revision: Union[str, None] = 'debe81ec8e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавляет поля для мультитенантности и организации в таблицы tools и agents"""
    
    # Добавляем новые поля в таблицу tools
    op.add_column('tools', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('tools', sa.Column('company_id', sa.UUID(), nullable=True))
    op.add_column('tools', sa.Column('user_id', sa.UUID(), nullable=True))
    op.add_column('tools', sa.Column('display_name', sa.Text(), nullable=True))
    op.add_column('tools', sa.Column('category', sa.Text(), nullable=True))
    
    # Добавляем новые поля в таблицу agents
    op.add_column('agents', sa.Column('agent_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('agents', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('agents', sa.Column('company_id', sa.UUID(), nullable=True))
    op.add_column('agents', sa.Column('photo', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('category', sa.Text(), nullable=True))
    
    # Создаем индексы для производительности
    op.create_index('idx_tools_is_public', 'tools', ['is_public'])
    op.create_index('idx_tools_company_id', 'tools', ['company_id'])
    op.create_index('idx_tools_user_id', 'tools', ['user_id'])
    op.create_index('idx_tools_category', 'tools', ['category'])
    
    op.create_index('idx_agents_is_public', 'agents', ['is_public'])
    op.create_index('idx_agents_company_id', 'agents', ['company_id'])
    op.create_index('idx_agents_category', 'agents', ['category'])


def downgrade() -> None:
    """Удаляет поля мультитенантности и организации из таблиц tools и agents"""
    
    # Удаляем индексы
    op.drop_index('idx_agents_category')
    op.drop_index('idx_agents_company_id')
    op.drop_index('idx_agents_is_public')
    
    op.drop_index('idx_tools_category')
    op.drop_index('idx_tools_user_id')
    op.drop_index('idx_tools_company_id')
    op.drop_index('idx_tools_is_public')
    
    # Удаляем поля из таблицы agents
    op.drop_column('agents', 'category')
    op.drop_column('agents', 'photo')
    op.drop_column('agents', 'company_id')
    op.drop_column('agents', 'is_public')
    op.drop_column('agents', 'agent_config')
    
    # Удаляем поля из таблицы tools
    op.drop_column('tools', 'category')
    op.drop_column('tools', 'display_name')
    op.drop_column('tools', 'user_id')
    op.drop_column('tools', 'company_id')
    op.drop_column('tools', 'is_public')
