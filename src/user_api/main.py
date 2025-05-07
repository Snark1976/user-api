from litestar import Litestar
from src.user_api.controllers.user import UserController
from src.user_api.config.settings import get_openapi_config, get_db_config
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig
from typing import Optional

def create_app(db_config: Optional[SQLAlchemyAsyncConfig] = None) -> Litestar:
    if db_config is None:
        db_config = get_db_config()
    return Litestar(
        route_handlers=[UserController],
        plugins=[SQLAlchemyPlugin(config=db_config)],
        openapi_config=get_openapi_config(),
    )

app = create_app()