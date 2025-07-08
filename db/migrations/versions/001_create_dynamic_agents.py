"""Create dynamic_agents table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create dynamic_agents table
    op.create_table(
        'dynamic_agents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('agent_id', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('model_configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('tools_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('knowledge_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('memory_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('storage_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True, 
                  default=sa.text("'{\"type\": \"postgres\", \"db_url\": null, \"enabled\": true, \"db_schema\": \"ai\", \"table_name\": \"sessions\"}'::jsonb")),
        sa.Column('reasoning_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('team_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('agent_id'),
        schema='ai'
    )
    
    # Create indexes
    op.create_index(
        'idx_dynamic_agents_active_agent_id',
        'dynamic_agents',
        ['agent_id', 'is_active'],
        unique=False,
        postgresql_where=sa.text('is_active = true'),
        schema='ai'
    )
    
    op.create_index(
        'idx_dynamic_agents_active_created',
        'dynamic_agents',
        ['is_active', sa.text('created_at DESC')],
        unique=False,
        postgresql_where=sa.text('is_active = true'),
        schema='ai'
    )
    
    op.create_index(
        'idx_dynamic_agents_active',
        'dynamic_agents',
        ['is_active'],
        unique=False,
        schema='ai'
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_dynamic_agents_active', table_name='dynamic_agents', schema='ai')
    op.drop_index('idx_dynamic_agents_active_created', table_name='dynamic_agents', schema='ai')
    op.drop_index('idx_dynamic_agents_active_agent_id', table_name='dynamic_agents', schema='ai')
    
    # Drop table
    op.drop_table('dynamic_agents', schema='ai') 