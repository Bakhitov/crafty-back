"""add_agno_native_fields_to_agents

Revision ID: f3a8b9c2d1e4
Revises: 4697822e380c
Create Date: 2025-01-30 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a8b9c2d1e4'
down_revision: Union[str, None] = '4697822e380c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавляет нативные поля Agno (goal, expected_output, role) в таблицу agents"""
    
    # Добавляем новые поля в таблицу agents
    op.add_column('agents', sa.Column('goal', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('expected_output', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('role', sa.String(255), nullable=True))


def downgrade() -> None:
    """Удаляет нативные поля Agno из таблицы agents"""
    
    # Удаляем поля из таблицы agents
    op.drop_column('agents', 'role')
    op.drop_column('agents', 'expected_output')
    op.drop_column('agents', 'goal') 