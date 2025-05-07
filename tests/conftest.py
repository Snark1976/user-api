import pytest
import pytest_asyncio
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, AsyncSessionConfig
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from litestar.testing import AsyncTestClient

from user_api.main import create_app

load_dotenv()

@pytest.fixture(scope="session")
def postgres_container():
    # Create a PostgreSQL container using testcontainers for the test session
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest_asyncio.fixture
async def app_client(postgres_container):
    # Construct the database connection string from the PostgreSQL container
    raw_connection_url = postgres_container.get_connection_url()
    scheme, rest = raw_connection_url.split("://", 1)
    db_connection_string = f"postgresql+asyncpg://{rest}"

    # Configure SQLAlchemy with autocommit enabled
    db_config = SQLAlchemyAsyncConfig(
        connection_string=db_connection_string,
        session_config=AsyncSessionConfig(expire_on_commit=False),
        create_all=True,
        before_send_handler="autocommit"
    )

    # Create the Litestar app with the specified database configuration
    test_app = create_app(db_config)

    # Create an async engine for manual database operations
    engine = create_async_engine(db_connection_string)
    test_app.state["db_engine"] = engine

    # Retrieve the SQLAlchemy plugin from the app
    sqlalchemy_plugin = test_app.plugins.get(SQLAlchemyPlugin)
    if sqlalchemy_plugin is None:
        raise ValueError("SQLAlchemyPlugin not found")

    # Extract the SQLAlchemy configuration
    config = sqlalchemy_plugin.config
    if isinstance(config, list):
        if not config:
            raise ValueError("Config is empty")
        config = config[0]

    # Create all database tables before running tests
    async with engine.begin() as conn:
        await conn.run_sync(config.metadata.create_all)

    yield test_app

    # Drop all database tables after tests are complete
    async with engine.begin() as conn:
        await conn.run_sync(config.metadata.drop_all)

    # Dispose of the engine to clean up resources
    await engine.dispose()

@pytest_asyncio.fixture
async def client(app_client):
    # Provide an AsyncTestClient for interacting with the Litestar app during tests
    async with AsyncTestClient(app=app_client) as client:
        yield client