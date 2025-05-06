from litestar import Litestar
from src.user_api.controllers.user import UserController
from src.user_api.config.settings import get_app_config, get_openapi_config

sqlalchemy_plugin = get_app_config()

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin],
    openapi_config=get_openapi_config(),
)