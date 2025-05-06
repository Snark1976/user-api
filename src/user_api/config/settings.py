from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from litestar.openapi import OpenAPIConfig
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, AsyncSessionConfig
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv("DATABASE_URL")
if not connection_string:
    raise ValueError("DATABASE_URL is not set in .env file")

def get_app_config() -> SQLAlchemyPlugin:
    """Configure SQLAlchemy plugin for PostgreSQL."""
    return SQLAlchemyPlugin(config=get_db_config())

def get_openapi_config() -> OpenAPIConfig:
    """Configure Swagger UI."""
    return OpenAPIConfig(title="User API", version="1.0.0")

def get_db_config() -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=connection_string,
        before_send_handler="autocommit",
        session_config=AsyncSessionConfig(expire_on_commit=False),
        create_all=False,
    )