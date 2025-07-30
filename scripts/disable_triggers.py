#!/usr/bin/env python3
import os
import sys
sys.path.append('.')
from dotenv import load_dotenv
load_dotenv()
import psycopg
from db.url import get_db_url

os.environ['DB_URL'] = 'postgresql://postgres:Ginifi51!@db.wyehpfzafbjfvyjzgjss.supabase.co:5432/postgres'
db_url = get_db_url().replace('postgresql+psycopg://', 'postgresql://')

with psycopg.connect(db_url) as conn:
    with conn.cursor() as cur:
        print('🔧 Временно отключаю триггеры...')
        cur.execute('DROP TRIGGER IF EXISTS tools_cache_invalidation_trigger ON tools;')
        cur.execute('DROP TRIGGER IF EXISTS agents_cache_invalidation_trigger ON agents;')
        conn.commit()
        print('✅ Триггеры отключены') 