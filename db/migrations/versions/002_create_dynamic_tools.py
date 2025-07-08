"""Create dynamic_tools table

Revision ID: 002
Revises: 001
Create Date: 2025-01-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create dynamic_tools table
    op.create_table(
        'dynamic_tools',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tool_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=True),
        sa.Column('agno_class', sa.String(length=255), nullable=False),
        sa.Column('module_path', sa.String(length=500), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('icon', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tool_id'),
        schema='ai'
    )
    
    # Create indexes
    op.create_index('idx_dynamic_tools_active', 'dynamic_tools', ['is_active'], schema='ai')
    op.create_index('idx_dynamic_tools_class', 'dynamic_tools', ['agno_class'], schema='ai')
    op.create_index('idx_dynamic_tools_category', 'dynamic_tools', ['category'], schema='ai')
    
    # Данные будут добавлены отдельно после создания таблицы


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_dynamic_tools_category', table_name='dynamic_tools', schema='ai')
    op.drop_index('idx_dynamic_tools_class', table_name='dynamic_tools', schema='ai')
    op.drop_index('idx_dynamic_tools_active', table_name='dynamic_tools', schema='ai')
    
    # Drop table
    op.drop_table('dynamic_tools', schema='ai') 