from os import getenv


def get_db_url() -> str:
    # Проверяем, есть ли готовый URL БД
    db_url = getenv("DB_URL")
    if db_url:
        # Заменяем postgresql:// на postgresql+psycopg:// для использования psycopg (v3)
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        # Добавляем параметры подключения для стабильности
        if "?" not in db_url:
            db_url += "?connect_timeout=30&keepalives_idle=60&keepalives_interval=10&keepalives_count=3"
        
        return db_url
    
    # Если нет, собираем URL из отдельных переменных
    db_driver = getenv("DB_DRIVER", "postgresql+psycopg")
    db_user = getenv("DB_USER")
    db_pass = getenv("DB_PASSWORD")  # Изменено с DB_PASS на DB_PASSWORD
    db_host = getenv("DB_HOST")
    db_port = getenv("DB_PORT")
    db_database = getenv("DB_NAME")  # Изменено с DB_DATABASE на DB_NAME
    
    return "{}://{}{}@{}:{}/{}".format(
        db_driver,
        db_user,
        f":{db_pass}" if db_pass else "",
        db_host,
        db_port,
        db_database,
    )
