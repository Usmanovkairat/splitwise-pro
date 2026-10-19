import os
from sqlalchemy import create_engine, event

DEFAULT_URL = "sqlite:///./backend/splitwise.db"


def make_engine(url=None):
    url = url or os.getenv("DATABASE_URL", DEFAULT_URL)
    kwargs = (
        {"connect_args": {"check_same_thread": False, "timeout": 30}}
        if url.startswith("sqlite:")
        else {}
    )
    engine = create_engine(url, **kwargs)
    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine
