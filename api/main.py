import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.v1_router import v1_router
from api.settings import api_settings


def create_app() -> FastAPI:
    """Create a FastAPI App"""

    # Create FastAPI App
    app: FastAPI = FastAPI(
        title=api_settings.title,
        version=api_settings.version,
        docs_url="/docs" if api_settings.docs_enabled else None,
        redoc_url="/redoc" if api_settings.docs_enabled else None,
        openapi_url="/openapi.json" if api_settings.docs_enabled else None,
    )

    # Add v1 router
    app.include_router(v1_router)

    # Add Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# Create a FastAPI app
app = create_app()

@app.on_event("startup")
async def startup_event():
    """Инициализация при старте приложения"""
    print("🚀 Starting Agent API...")
    
    # ⚡ ОПТИМИЗАЦИЯ: Предварительная загрузка кэша популярных агентов
    try:
        from db.services.dynamic_agent_service import dynamic_agent_service
        # Загружаем кэш для всех активных агентов в фоновом режиме
        asyncio.create_task(_preload_cache_background())
    except Exception as e:
        print(f"⚠️ Не удалось предварительно загрузить кэш: {e}")

async def _preload_cache_background():
    """Фоновая загрузка кэша агентов"""
    try:
        import time
        await asyncio.sleep(2)  # Ждём запуска сервера
        
        start_time = time.time()
        from db.services.dynamic_agent_service import dynamic_agent_service
        dynamic_agent_service.preload_agent_cache()
        
        end_time = time.time()
        print(f"⚡ Кэш агентов предварительно загружен за {end_time - start_time:.2f} секунд")
        
    except Exception as e:
        print(f"⚠️ Ошибка фоновой загрузки кэша: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при остановке приложения"""
    print("🛑 Shutting down Agent API...")
