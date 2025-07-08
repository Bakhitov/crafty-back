from os import getenv


def get_db_url() -> str:
    # Check if direct DB_URL is provided
    db_url = getenv("DB_URL")
    if db_url:
        # Add schema parameter if specified
        db_scheme = getenv("DB_SCHEME", "ai")
        if db_scheme and db_scheme != "public":
            if "?" in db_url:
                db_url += f"&options=-c search_path={db_scheme}"
            else:
                db_url += f"?options=-c search_path={db_scheme}"
        return db_url
    
    # Build URL from individual components (backward compatibility)
    db_driver = getenv("DB_DRIVER", "postgresql+psycopg")
    db_user = getenv("DB_USER")
    db_pass = getenv("DB_PASS")
    db_host = getenv("DB_HOST")
    db_port = getenv("DB_PORT")
    db_database = getenv("DB_DATABASE")
    db_scheme = getenv("DB_SCHEME", "ai")
    
    url = "{}://{}{}@{}:{}/{}".format(
        db_driver,
        db_user,
        f":{db_pass}" if db_pass else "",
        db_host,
        db_port,
        db_database,
    )
    
    # Add schema parameter if specified and not public
    if db_scheme and db_scheme != "public":
        url += f"?options=-c search_path={db_scheme}"
    
    return url
