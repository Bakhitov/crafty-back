"""Add custom tools and MCP servers

Revision ID: 003
Revises: 002
Create Date: 2025-01-28 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы кастомных инструментов
    op.create_table(
        'custom_tools',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tool_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_code', sa.Text(), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tool_id'),
        schema='ai'
    )
    
    # Создание таблицы MCP серверов
    op.create_table(
        'mcp_servers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('server_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('command', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('transport', sa.String(length=20), nullable=True, default='stdio'),
        sa.Column('env_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('server_id'),
        schema='ai'
    )
    
    # Создание индексов для производительности
    op.create_index('idx_custom_tools_active', 'custom_tools', ['is_active'], schema='ai')
    op.create_index('idx_custom_tools_tool_id', 'custom_tools', ['tool_id'], schema='ai')
    op.create_index('idx_mcp_servers_active', 'mcp_servers', ['is_active'], schema='ai')
    op.create_index('idx_mcp_servers_server_id', 'mcp_servers', ['server_id'], schema='ai')
    op.create_index('idx_mcp_servers_transport', 'mcp_servers', ['transport'], schema='ai')


def downgrade() -> None:
    # Удаление индексов
    op.drop_index('idx_mcp_servers_transport', table_name='mcp_servers', schema='ai')
    op.drop_index('idx_mcp_servers_server_id', table_name='mcp_servers', schema='ai')
    op.drop_index('idx_mcp_servers_active', table_name='mcp_servers', schema='ai')
    op.drop_index('idx_custom_tools_tool_id', table_name='custom_tools', schema='ai')
    op.drop_index('idx_custom_tools_active', table_name='custom_tools', schema='ai')
    
    # Удаление таблиц
    op.drop_table('mcp_servers', schema='ai')
    op.drop_table('custom_tools', schema='ai') 