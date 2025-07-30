"""add_cache_invalidation_triggers

Revision ID: 4697822e380c
Revises: c7dd7b0ce41c
Create Date: 2025-07-30 16:34:27.320271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4697822e380c'
down_revision: Union[str, None] = 'c7dd7b0ce41c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Добавляет специальные триггеры для автоматической инвалидации кэша.
    
    Эти триггеры будут:
    1. При INSERT - инвалидировать кэш списка агентов/инструментов
    2. При DELETE - инвалидировать конкретные записи в кэше
    3. Работать через NOTIFY механизм PostgreSQL
    """
    
    # 1. Функция для отправки уведомлений об изменениях кэша
    op.execute("""
        CREATE OR REPLACE FUNCTION notify_cache_invalidation()
        RETURNS TRIGGER AS $$
        DECLARE
            payload JSON;
        BEGIN
            -- Формируем payload в зависимости от операции
            IF TG_OP = 'INSERT' THEN
                payload = json_build_object(
                    'operation', 'INSERT',
                    'table', TG_TABLE_NAME,
                    'id', NEW.id::text,
                    'agent_id', CASE WHEN TG_TABLE_NAME = 'agents' THEN NEW.agent_id ELSE NULL END
                );
                -- Уведомляем о необходимости обновить список агентов/инструментов
                PERFORM pg_notify('cache_invalidation', payload::text);
                RETURN NEW;
                
            ELSIF TG_OP = 'DELETE' THEN
                payload = json_build_object(
                    'operation', 'DELETE',
                    'table', TG_TABLE_NAME,
                    'id', OLD.id::text,
                    'agent_id', CASE WHEN TG_TABLE_NAME = 'agents' THEN OLD.agent_id ELSE NULL END
                );
                -- Уведомляем о необходимости инвалидировать конкретную запись
                PERFORM pg_notify('cache_invalidation', payload::text);
                RETURN OLD;
                
            END IF;
            
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 2. Триггеры для таблицы agents
    op.execute("""
        CREATE TRIGGER agents_cache_invalidation_trigger
        AFTER INSERT OR DELETE ON agents
        FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();
    """)
    
    # 3. Триггеры для таблицы tools  
    op.execute("""
        CREATE TRIGGER tools_cache_invalidation_trigger
        AFTER INSERT OR DELETE ON tools
        FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();
    """)


def downgrade() -> None:
    """Удаляет триггеры инвалидации кэша"""
    
    # Удаляем триггеры
    op.execute("DROP TRIGGER IF EXISTS tools_cache_invalidation_trigger ON tools;")
    op.execute("DROP TRIGGER IF EXISTS agents_cache_invalidation_trigger ON agents;")
    
    # Удаляем функцию
    op.execute("DROP FUNCTION IF EXISTS notify_cache_invalidation();")
