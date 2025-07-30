#!/usr/bin/env python3
"""
Скрипт для проверки состояния базы данных Agent-API
Выводит данные в формате JSON
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

def get_db_connection():
    """Создает подключение к базе данных из переменных окружения"""
    try:
        # Получаем переменные из .env файла
        db_url = os.getenv('DB_URL')
        if db_url:
            return psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        
        # Альтернативно - по отдельным параметрам
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
        }
        
        return psycopg2.connect(**conn_params, cursor_factory=RealDictCursor)
        
    except Exception as e:
        print(json.dumps({"error": f"Database connection failed: {e}"}))
        sys.exit(1)

def get_all_tables(cursor) -> List[Dict[str, Any]]:
    """Получает список всех таблиц в схеме public"""
    cursor.execute("""
        SELECT 
            schemaname,
            tablename,
            hasindexes,
            hastriggers,
            hasrules
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    
    tables = cursor.fetchall()
    tables_data = []
    
    for table in tables:
        schema = table['schemaname']
        name = table['tablename']
        
        # Получаем количество записей
        try:
            cursor.execute(f'SELECT COUNT(*) as count FROM "{schema}"."{name}";')
            count_result = cursor.fetchone()
            count = count_result['count'] if count_result else 0
        except Exception as e:
            count = f"Error: {e}"
        
        # Получаем размер таблицы
        try:
            cursor.execute(f"""
                SELECT pg_size_pretty(pg_total_relation_size('"{schema}"."{name}"')) as size;
            """)
            size_result = cursor.fetchone()
            size = size_result['size'] if size_result else 'Unknown'
        except Exception as e:
            size = f"Error: {e}"
        
        table_info = {
            "name": name,
            "schema": schema,
            "count": count,
            "size": size,
            "has_indexes": table['hasindexes'],
            "has_triggers": table['hastriggers'],
            "has_rules": table['hasrules']
        }
        
        tables_data.append(table_info)
    
    return tables_data

def check_agents(cursor) -> List[Dict[str, Any]]:
    """Проверяет всех агентов в базе данных"""
    # Проверяем существование таблицы agents в схеме public
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'agents'
        );
    """)
    
    result = cursor.fetchone()
    if not result['exists']:
        return []
    
    # Получаем всех агентов
    cursor.execute("""
        SELECT 
            agent_id,
            name,
            description,
            model_config,
            system_instructions,
            tool_ids,
            is_active,
            is_public,
            user_id,
            company_id,
            photo,
            category,
            created_at,
            updated_at
        FROM agents
        ORDER BY created_at DESC;
    """)
    
    agents = cursor.fetchall()
    agents_data = []
    
    for agent in agents:
        agent_data = {
            "agent_id": agent['agent_id'],
            "name": agent['name'],
            "description": agent['description'],
            "model_config": agent['model_config'],
            "system_instructions": agent['system_instructions'],
            "tool_ids": agent['tool_ids'],
            "is_active": agent['is_active'],
            "is_public": agent['is_public'],
            "user_id": agent['user_id'],
            "company_id": str(agent['company_id']) if agent['company_id'] else None,
            "photo": agent['photo'],
            "category": agent['category'],
            "created_at": agent['created_at'].isoformat() if agent['created_at'] else None,
            "updated_at": agent['updated_at'].isoformat() if agent['updated_at'] else None,
            "instructions_count": len(agent['system_instructions']) if agent['system_instructions'] else 0,
            "tools_count": len(agent['tool_ids']) if agent['tool_ids'] else 0
        }
        
        agents_data.append(agent_data)
    
    return agents_data

def check_tools(cursor) -> List[Dict[str, Any]]:
    """Проверяет все инструменты в базе данных"""
    # Проверяем существование таблицы tools в схеме public
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'tools'
        );
    """)
    
    result = cursor.fetchone()
    if not result['exists']:
        return []
    
    # Получаем все инструменты
    cursor.execute("""
        SELECT 
            id,
            name,
            type,
            description,
            configuration,
            is_public,
            company_id,
            user_id,
            display_name,
            category,
            is_active,
            created_at,
            updated_at
        FROM tools
        ORDER BY type, name;
    """)
    
    tools = cursor.fetchall()
    tools_data = []
    
    for tool in tools:
        tool_data = {
            "id": str(tool['id']),
            "name": tool['name'],
            "type": tool['type'],
            "description": tool['description'],
            "configuration": tool['configuration'],
            "is_public": tool['is_public'],
            "company_id": str(tool['company_id']) if tool['company_id'] else None,
            "user_id": str(tool['user_id']) if tool['user_id'] else None,
            "display_name": tool['display_name'],
            "category": tool['category'],
            "is_active": tool['is_active'],
            "created_at": tool['created_at'].isoformat() if tool['created_at'] else None,
            "updated_at": tool['updated_at'].isoformat() if tool['updated_at'] else None
        }
        
        tools_data.append(tool_data)
    
    return tools_data

def check_sessions(cursor) -> List[Dict[str, Any]]:
    """Проверяет таблицы сессий в схеме public"""
    # Ищем таблицы с 'sessions' в названии только в схеме public
    cursor.execute("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename LIKE '%sessions%'
        ORDER BY tablename;
    """)
    
    session_table_names = cursor.fetchall()
    
    if not session_table_names:
        return []
    
    session_tables_data = []
    
    for table_info in session_table_names:
        name = table_info['tablename']
        
        try:
            # Получаем количество записей
            cursor.execute(f'SELECT COUNT(*) as count FROM "{name}";')
            count_result = cursor.fetchone()
            count = count_result['count'] if count_result else 0
            
            table_data = {
                "name": name,
                "count": count,
                "recent_sessions": []
            }
            
            if count > 0:
                # Получаем последние сессии
                cursor.execute(f"""
                    SELECT 
                        session_id,
                        user_id,
                        created_at
                    FROM "{name}"
                    ORDER BY created_at DESC
                    LIMIT 3;
                """)
                recent_sessions = cursor.fetchall()
                
                for session in recent_sessions:
                    session_data = {
                        "session_id": session['session_id'],
                        "user_id": session.get('user_id'),
                        "created_at": session.get('created_at').isoformat() if session.get('created_at') else None
                    }
                    table_data["recent_sessions"].append(session_data)
            
            session_tables_data.append(table_data)
            
        except Exception:
            continue
    
    return session_tables_data

def check_migrations(cursor) -> Dict[str, Any]:
    """Проверяет состояние миграций Alembic"""
    # Проверяем таблицу alembic_version
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'alembic_version'
        );
    """)
    
    result = cursor.fetchone()
    migration_data = {"exists": result["exists"]}
    
    if not result["exists"]:
        migration_data["version"] = None
        return migration_data
    
    # Получаем текущую версию
    cursor.execute("SELECT version_num FROM public.alembic_version;")
    version_result = cursor.fetchone()
    
    if version_result:
        migration_data["version"] = version_result['version_num']
    else:
        migration_data["version"] = None
    
    return migration_data

def main():
    """Основная функция проверки базы данных"""
    # Подключение к БД
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Получаем информацию о БД
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()['version']
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()['current_database']
        cursor.execute("SELECT current_schema();")
        current_schema = cursor.fetchone()['current_schema']
        
        # Проверяем все компоненты
        migrations = check_migrations(cursor)
        tables = get_all_tables(cursor)
        agents = check_agents(cursor)
        tools = check_tools(cursor)
        session_tables = check_sessions(cursor)
        
        # Выводим все данные в JSON формате
        result = {
            "timestamp": datetime.now().isoformat(),
            "database_info": {
                "version": db_version.split(',')[0],
                "name": db_name,
                "schema": current_schema
            },
            "migrations": migrations,
            "tables": tables,
            "agents": agents,
            "tools": tools,
            "session_tables": session_tables,
            "summary": {
                "tables_count": len(tables),
                "agents_count": len(agents),
                "tools_count": len(tools),
                "session_tables_count": len(session_tables)
            }
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": f"Database check failed: {e}"}))
        return 1
    
    finally:
        cursor.close()
        conn.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 