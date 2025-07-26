"""
005_create_registries

Создание таблиц для реестров моделей, агентов и хуков.
Обеспечивает поддержку сложных объектов через ссылки.

Создан: 2024-01-XX
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    """Создание таблиц для реестров"""
    
    # === РЕЕСТР МОДЕЛЕЙ ===
    op.create_table(
        'model_registry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registry_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registry_id'),
        schema='ai'
    )
    
    # Индексы для model_registry
    op.create_index('ix_model_registry_is_active', 'model_registry', ['is_active'], schema='ai')
    op.create_index('ix_model_registry_name', 'model_registry', ['name'], schema='ai')
    op.create_index('ix_model_registry_created_at', 'model_registry', ['created_at'], schema='ai')
    
    # === РЕЕСТР АГЕНТОВ ===
    op.create_table(
        'agent_registry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registry_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('agent_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registry_id'),
        schema='ai'
    )
    
    # Индексы для agent_registry
    op.create_index('ix_agent_registry_is_active', 'agent_registry', ['is_active'], schema='ai')
    op.create_index('ix_agent_registry_name', 'agent_registry', ['name'], schema='ai')
    op.create_index('ix_agent_registry_created_at', 'agent_registry', ['created_at'], schema='ai')
    
    # === РЕЕСТР ХУКОВ ===
    op.create_table(
        'hook_registry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registry_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('hook_type', sa.String(length=50), nullable=False),
        sa.Column('module_path', sa.String(length=500), nullable=False),
        sa.Column('function_name', sa.String(length=255), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registry_id'),
        schema='ai'
    )
    
    # Индексы для hook_registry
    op.create_index('ix_hook_registry_is_active', 'hook_registry', ['is_active'], schema='ai')
    op.create_index('ix_hook_registry_hook_type', 'hook_registry', ['hook_type'], schema='ai')
    op.create_index('ix_hook_registry_name', 'hook_registry', ['name'], schema='ai')
    op.create_index('ix_hook_registry_created_at', 'hook_registry', ['created_at'], schema='ai')
    
    # === ТРИГГЕРЫ ДЛЯ ОБНОВЛЕНИЯ updated_at ===
    
    # Триггер для model_registry
    op.execute("""
        CREATE OR REPLACE FUNCTION ai.update_model_registry_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER model_registry_updated_at_trigger
        BEFORE UPDATE ON ai.model_registry
        FOR EACH ROW EXECUTE FUNCTION ai.update_model_registry_updated_at();
    """)
    
    # Триггер для agent_registry
    op.execute("""
        CREATE OR REPLACE FUNCTION ai.update_agent_registry_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER agent_registry_updated_at_trigger
        BEFORE UPDATE ON ai.agent_registry
        FOR EACH ROW EXECUTE FUNCTION ai.update_agent_registry_updated_at();
    """)
    
    # Триггер для hook_registry
    op.execute("""
        CREATE OR REPLACE FUNCTION ai.update_hook_registry_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER hook_registry_updated_at_trigger
        BEFORE UPDATE ON ai.hook_registry
        FOR EACH ROW EXECUTE FUNCTION ai.update_hook_registry_updated_at();
    """)


def downgrade():
    """Удаление таблиц реестров"""
    
    # Удаляем таблицы (триггеры и функции удалятся автоматически)
    op.drop_table('hook_registry', schema='ai')
    op.drop_table('agent_registry', schema='ai')
    op.drop_table('model_registry', schema='ai')
    
    # Удаляем функции триггеров
    op.execute("DROP FUNCTION IF EXISTS ai.update_model_registry_updated_at() CASCADE;")
    op.execute("DROP FUNCTION IF EXISTS ai.update_agent_registry_updated_at() CASCADE;")
    op.execute("DROP FUNCTION IF EXISTS ai.update_hook_registry_updated_at() CASCADE;") 