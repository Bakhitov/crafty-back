"""add_dynamic_agents_and_tools_tables

Revision ID: debe81ec8e6f
Revises: 
Create Date: 2025-07-30 01:01:51.390810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'debe81ec8e6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Создает таблицы для динамических агентов и инструментов"""
    
    # Таблица инструментов
    op.create_table(
        'tools',
        sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Таблица агентов
    op.create_table(
        'agents',
        sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('agent_id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('model_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False, 
                 server_default='{"provider": "openai", "id": "gpt-4o"}'),
        sa.Column('system_instructions', postgresql.ARRAY(sa.Text()), server_default='{}'),
        sa.Column('tool_ids', postgresql.ARRAY(sa.UUID()), server_default='{}'),
        sa.Column('user_id', sa.String(255)),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('agent_id')
    )
    
    # Индексы для производительности
    op.create_index('idx_tools_type_active', 'tools', ['type', 'is_active'])
    op.create_index('idx_agents_agent_id_active', 'agents', ['agent_id'], 
                   postgresql_where=sa.text('is_active = true'))
    op.create_index('idx_agents_user_id', 'agents', ['user_id'])
    op.create_index('idx_agents_tool_ids', 'agents', ['tool_ids'], postgresql_using='gin')
    
    # Триггер для автообновления updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER update_tools_updated_at 
        BEFORE UPDATE ON tools 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_agents_updated_at 
        BEFORE UPDATE ON agents 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Удаляет таблицы динамических агентов и инструментов"""
    op.execute("DROP TRIGGER IF EXISTS update_agents_updated_at ON agents;")
    op.execute("DROP TRIGGER IF EXISTS update_tools_updated_at ON tools;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    op.drop_index('idx_agents_tool_ids')
    op.drop_index('idx_agents_user_id')
    op.drop_index('idx_agents_agent_id_active')
    op.drop_index('idx_tools_type_active')
    
    op.drop_table('agents')
    op.drop_table('tools')
