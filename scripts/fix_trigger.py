#!/usr/bin/env python3
"""
Скрипт для исправления триггера кэш-инвалидации
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import psycopg
from db.url import get_db_url

def fix_trigger():
    """Исправляет функцию триггера кэш-инвалидации"""
    
    try:
        # Устанавливаем переменные окружения
        os.environ["DB_URL"] = "postgresql://postgres:Ginifi51!@db.wyehpfzafbjfvyjzgjss.supabase.co:5432/postgres"
        
        # Получаем URL БД
        db_url = get_db_url()
        print(f"🔗 Подключение к БД: {db_url[:50]}...")
        
        # Для psycopg нужен обычный postgresql:// URL
        if db_url.startswith("postgresql+psycopg://"):
            db_url = db_url.replace("postgresql+psycopg://", "postgresql://", 1)
        
        # Подключаемся к БД
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                print("🗑️ Удаляю старые триггеры...")
                
                # Удаляем старые триггеры
                cur.execute("DROP TRIGGER IF EXISTS tools_cache_invalidation_trigger ON tools;")
                cur.execute("DROP TRIGGER IF EXISTS agents_cache_invalidation_trigger ON agents;")
                cur.execute("DROP FUNCTION IF EXISTS notify_cache_invalidation();")
                
                print("🔧 Создаю новую функцию триггера...")
                
                # Создаем новую функцию
                fix_sql = """
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
                            'agent_id', CASE WHEN TG_TABLE_NAME = 'agents' THEN NEW.agent_id::text ELSE NULL END
                        );
                        PERFORM pg_notify('cache_invalidation', payload::text);
                        RETURN NEW;
                        
                    ELSIF TG_OP = 'DELETE' THEN
                        payload = json_build_object(
                            'operation', 'DELETE',
                            'table', TG_TABLE_NAME,
                            'id', OLD.id::text,
                            'agent_id', CASE WHEN TG_TABLE_NAME = 'agents' THEN OLD.agent_id::text ELSE NULL END
                        );
                        PERFORM pg_notify('cache_invalidation', payload::text);
                        RETURN OLD;
                        
                    END IF;
                    
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;
                """
                
                cur.execute(fix_sql)
                
                print("🔧 Создаю новые триггеры...")
                
                # Создаем триггеры заново
                cur.execute("""
                    CREATE TRIGGER agents_cache_invalidation_trigger
                    AFTER INSERT OR DELETE ON agents
                    FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();
                """)
                
                cur.execute("""
                    CREATE TRIGGER tools_cache_invalidation_trigger
                    AFTER INSERT OR DELETE ON tools
                    FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();
                """)
                
                conn.commit()
                print("✅ Триггеры успешно пересозданы!")
                return True
                
    except Exception as e:
        print(f"❌ Ошибка исправления триггера: {e}")
        return False

if __name__ == "__main__":
    success = fix_trigger()
    sys.exit(0 if success else 1) 