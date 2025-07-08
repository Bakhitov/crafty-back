from fastapi import APIRouter

from .agents import agents_router
from .health import health_router
from .playground import playground_router
from .tools import tools_router
from .custom_tools import custom_tools_router
from .mcp_tools import mcp_tools_router

v1_router = APIRouter(prefix="/v1")

# Подключаем все роутеры
# ВАЖНО: более специфичные роутеры должны быть зарегистрированы раньше общих
v1_router.include_router(health_router)
v1_router.include_router(agents_router)
v1_router.include_router(playground_router)
v1_router.include_router(custom_tools_router)  # Специфичный роутер раньше
v1_router.include_router(mcp_tools_router)     # Специфичный роутер раньше
v1_router.include_router(tools_router)         # Общий роутер в конце
