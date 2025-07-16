from enum import Enum
from io import BytesIO
from logging import getLogger
from typing import AsyncGenerator, List, Optional, Dict, Any, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Query
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from db.services.dynamic_agent_service import dynamic_agent_service
from db.models import DynamicAgent, ModelConfig, ToolsConfig, MemoryConfig, KnowledgeConfig, StorageConfig, ReasoningConfig, TeamConfig, AgentSettings

import asyncio
import concurrent.futures
import json
import logging

# Agno helpers for sessions
from agno.app.playground.operator import get_session_title
from agno.app.playground.schemas import AgentSessionsResponse, AgentRenameRequest
from agno.storage.session.agent import AgentSession
from agno.app.playground.schemas import MemoryResponse  # Добавлено для ответа воспоминаний

logger = getLogger(__name__)

######################################################
## Routes for the Dynamic Agent Interface
######################################################

agents_router = APIRouter(prefix="/agents", tags=["Agents"])


class Model(str, Enum):
    gpt_4_1 = "gpt-4.1"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    o3_mini = "o3-mini"
    claude_opus_4_20250514 = "claude-opus-4-20250514"
    claude_sonnet_4_20250514 = "claude-sonnet-4-20250514"
    claude_3_7_sonnet_20250219 = "claude-3-7-sonnet-20250219"
    claude_3_5_sonnet_20241022 = "claude-3-5-sonnet-20241022"
    claude_3_5_haiku_20241022 = "claude-3-5-haiku-20241022"
    claude_3_opus_20240229 = "claude-3-opus-20240229"
    deepseek_chat = "deepseek-chat"
    deepseek_reasoner = "deepseek-reasoner"
    deepseek_r1_distill_llama_70b = "deepseek-r1-distill-llama-70b"
    gemini_2_5_pro = "gemini-2.5-pro"
    gemini_2_5_flash = "gemini-2.5-flash"
    gemini_2_5_flash_lite_preview_06_17 = "gemini-2.5-flash-lite-preview-06-17"
    llama_3_3_70b_versatile = "llama-3.3-70b-versatile"
    llama_3_1_8b_instant = "llama-3.1-8b-instant"
    grok_3_latest = "grok-3-latest"
    grok_3_fast_latest = "grok-3-fast-latest"
    grok_3_mini_latest = "grok-3-mini-latest"


class AgentResponse(BaseModel):
    """Модель ответа для агента с полной конфигурацией"""
    id: int
    name: str
    agent_id: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    is_active: bool
    is_active_api: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Основные конфигурации (соответствуют полям БД)
    model_configuration: Optional[Dict[str, Any]] = None
    tools_config: Optional[Dict[str, Any]] = None
    knowledge_config: Optional[Dict[str, Any]] = None
    memory_config: Optional[Dict[str, Any]] = None
    storage_config: Optional[Dict[str, Any]] = None
    reasoning_config: Optional[Dict[str, Any]] = None
    team_config: Optional[Dict[str, Any]] = None
    
    # Дополнительные конфигурации (из settings)
    system_message_config: Optional[Dict[str, Any]] = None
    user_message_config: Optional[Dict[str, Any]] = None
    context_config: Optional[Dict[str, Any]] = None
    history_config: Optional[Dict[str, Any]] = None
    response_config: Optional[Dict[str, Any]] = None
    streaming_config: Optional[Dict[str, Any]] = None
    debug_config: Optional[Dict[str, Any]] = None
    extra_config: Optional[Dict[str, Any]] = None
    config_version: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # Полные settings для дополнительных параметров
    settings: Optional[Dict[str, Any]] = None


class CreateAgentRequest(BaseModel):
    """Модель запроса для создания агента"""
    name: str
    agent_id: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    
    # Основные конфигурации (соответствуют полям БД)
    model_configuration: Optional[Dict[str, Any]] = None
    tools_config: Optional[Dict[str, Any]] = None
    knowledge_config: Optional[Dict[str, Any]] = None
    memory_config: Optional[Dict[str, Any]] = None
    storage_config: Optional[Dict[str, Any]] = None
    reasoning_config: Optional[Dict[str, Any]] = None
    team_config: Optional[Dict[str, Any]] = None
    
    # Дополнительные конфигурации (будут сохранены в settings)
    system_message_config: Optional[Dict[str, Any]] = None
    user_message_config: Optional[Dict[str, Any]] = None
    context_config: Optional[Dict[str, Any]] = None
    history_config: Optional[Dict[str, Any]] = None
    response_config: Optional[Dict[str, Any]] = None
    streaming_config: Optional[Dict[str, Any]] = None
    debug_config: Optional[Dict[str, Any]] = None
    extra_config: Optional[Dict[str, Any]] = None
    config_version: Optional[str] = "1.0"
    tags: Optional[List[str]] = None
    
    # ✅ ИЗМЕНЕНО: унифицируем имя поля на 'settings'
    settings: Optional[Dict[str, Any]] = None


class UpdateAgentRequest(BaseModel):
    """Модель запроса для обновления агента"""
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    
    # Основные конфигурации (соответствуют полям БД)
    model_configuration: Optional[Dict[str, Any]] = None
    tools_config: Optional[Dict[str, Any]] = None
    knowledge_config: Optional[Dict[str, Any]] = None
    memory_config: Optional[Dict[str, Any]] = None
    storage_config: Optional[Dict[str, Any]] = None
    reasoning_config: Optional[Dict[str, Any]] = None
    team_config: Optional[Dict[str, Any]] = None
    
    # Дополнительные конфигурации (будут сохранены в settings)
    system_message_config: Optional[Dict[str, Any]] = None
    user_message_config: Optional[Dict[str, Any]] = None
    context_config: Optional[Dict[str, Any]] = None
    history_config: Optional[Dict[str, Any]] = None
    response_config: Optional[Dict[str, Any]] = None
    streaming_config: Optional[Dict[str, Any]] = None
    debug_config: Optional[Dict[str, Any]] = None
    extra_config: Optional[Dict[str, Any]] = None
    config_version: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # ✅ ИЗМЕНЕНО: унифицируем имя поля на 'settings'
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_active_api: Optional[bool] = None


def _build_agent_response(agent: DynamicAgent) -> AgentResponse:
    """Построить полный ответ агента со всеми конфигурациями"""
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        agent_id=agent.agent_id,
        description=agent.description,
        instructions=agent.instructions,
        is_active=agent.is_active,
        is_active_api=agent.is_active_api,
        created_at=agent.created_at.isoformat() if agent.created_at else None,
        updated_at=agent.updated_at.isoformat() if agent.updated_at else None,
        
        # Основные конфигурации
        model_configuration=agent.model_configuration,
        tools_config=agent.tools_config,
        knowledge_config=agent.knowledge_config,
        memory_config=agent.memory_config,
        storage_config=agent.storage_config,
        reasoning_config=agent.reasoning_config,
        team_config=agent.team_config,
        
        # Дополнительные конфигурации из settings
        system_message_config=agent.get_system_message_config(),
        user_message_config=agent.get_user_message_config(),
        context_config=agent.get_context_config(),
        history_config=agent.get_history_config(),
        response_config=agent.get_response_config(),
        streaming_config=agent.get_streaming_config(),
        debug_config=agent.get_debug_config(),
        extra_config=agent.get_extra_config(),
        config_version=agent.get_config_version(),
        tags=agent.get_tags(),
        
        # Полные settings для дополнительных параметров
        settings=agent.settings
    )


def _prepare_agent_data(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Собирает все разрозненные конфигурационные поля в единый словарь 'settings'.
    Приоритет отдается более специфичным полям (например, `config_version`)
    над общим объектом `settings`.
    """
    
    # 1. Начинаем с объекта 'settings', если он был передан.
    final_settings = agent_data.pop('settings', None) or {}

    # 2. "Сплющиваем" поля-конфиги, перезаписывая значения в 'final_settings'.
    setting_keys_to_merge = [
        'system_message_config', 'user_message_config', 'context_config',
        'history_config', 'response_config', 'streaming_config',
        'debug_config', 'extra_config'
    ]
    for key in setting_keys_to_merge:
        config_dict = agent_data.pop(key, None)
        if isinstance(config_dict, dict):
            final_settings.update(config_dict)

    # 3. Переносим простые поля, перезаписывая значения в 'final_settings'.
    simple_setting_keys_to_move = ['config_version', 'tags']
    for key in simple_setting_keys_to_move:
        if key in agent_data:
            final_settings[key] = agent_data.pop(key)

    # 4. Возвращаем 'final_settings' в основной словарь.
    if final_settings:
        agent_data['settings'] = final_settings
                
    return agent_data


@agents_router.get("", response_model=List[str])
async def list_agents():
    """
    Возвращает список всех доступных ID агентов.

    Returns:
        List[str]: Список идентификаторов агентов
    """
    try:
        return dynamic_agent_service.get_available_agent_ids()
    except Exception as e:
        logger.error(f"Error getting available agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve available agents"
        )


@agents_router.get("/detailed", response_model=List[AgentResponse])
async def list_agents_detailed():
    """
    Возвращает подробную информацию о всех доступных агентах с полными конфигурациями.

    Returns:
        List[AgentResponse]: Список агентов с полной конфигурацией
    """
    try:
        agents = dynamic_agent_service.get_all_active_agents()
        return [_build_agent_response(agent) for agent in agents]
    except Exception as e:
        logger.error(f"Error getting detailed agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve detailed agent information"
        )


@agents_router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """
    Получить полную информацию о конкретном агенте включая все конфигурации.

    Args:
        agent_id: ID агента

    Returns:
        AgentResponse: Полная информация об агенте со всеми конфигурациями
    """
    try:
        agent = dynamic_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )
        
        return _build_agent_response(agent)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve agent {agent_id}"
        )


@agents_router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(request: CreateAgentRequest):
    """
    Создать нового динамического агента.

    Args:
        request: Данные для создания агента

    Returns:
        AgentResponse: Информация о созданном агенте
    """
    try:
        agent_data = request.dict(exclude_none=True)
        
        # ✅ ИСПРАВЛЕНИЕ: Собираем все настройки в один объект
        agent_data = _prepare_agent_data(agent_data)
        
        agent = dynamic_agent_service.create_agent(agent_data)
        
        return _build_agent_response(agent)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent"
        )


@agents_router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, request: UpdateAgentRequest):
    """
    Обновить существующего агента.

    Args:
        agent_id: ID агента
        request: Данные для обновления

    Returns:
        AgentResponse: Информация об обновленном агенте
    """
    try:
        agent_data = request.dict(exclude_none=True)
        
        # ✅ ИСПРАВЛЕНИЕ: Собираем все настройки в один объект
        agent_data = _prepare_agent_data(agent_data)
        
        agent = dynamic_agent_service.update_agent(agent_id, agent_data)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )
        
        return _build_agent_response(agent)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent {agent_id}"
        )


@agents_router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """
    Удалить агента (soft delete).

    Args:
        agent_id: ID агента

    Returns:
        dict: Сообщение об успешном удалении
    """
    try:
        success = dynamic_agent_service.delete_agent(agent_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )
        
        return {"message": f"Agent {agent_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent {agent_id}"
        )


async def chat_response_streamer(
    agent_response
) -> AsyncGenerator[str, None]:
    """
    Потоковая передача ответов агента по частям.
    Изолированная от конкретного фреймворка реализация.
    Поддерживает как обычные генераторы, так и async генераторы.
    """
    # Проверяем тип генератора
    if hasattr(agent_response, '__aiter__'):
        # Async генератор
        async for chunk in agent_response:
            yield f"data: {chunk}\n\n"
    elif hasattr(agent_response, '__iter__') and not isinstance(agent_response, str):
        # Обычный генератор
        for chunk in agent_response:
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0)  # Позволяем другим задачам выполняться
    else:
        # Простая строка
        yield f"data: {str(agent_response)}\n\n"


class RunRequest(BaseModel):
    """Модель запроса для запуска агента (для JSON запросов без файлов)"""

    message: str
    stream: bool = True
    model: Model = Model.gpt_4_1
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@agents_router.post("/{agent_id}/runs", status_code=status.HTTP_200_OK)
async def create_agent_run(
    agent_id: str,
    message: str = Form(...),
    stream: bool = Form(True),
    model: Model = Form(Model.gpt_4_1),
    user_id: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    stop_after_tool_call: bool = Form(False),
):
    """
    Создает и выполняет запуск агента.
    Поддерживает потоковую передачу и загрузку файлов.
    """
    # 1. Получаем агента
    agent = dynamic_agent_service.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID '{agent_id}' not found"
        )
    
    # 2. Проверяем, активен ли API для этого агента
    if not agent.is_active_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"API for agent '{agent_id}' is disabled."
        )

    # 3. Базовая валидация
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    logger.debug(f"RunRequest: agent_id={agent_id}, message={message}, stream={stream}, model={model}")

    try:
        # Выполняем агента напрямую через сервис
        agent_response = await dynamic_agent_service.run_agent(
            agent_id=agent_id,
            message=message,
            user_id=user_id,
            session_id=session_id,
            stream=stream,
            model_override=model.value if model != Model.gpt_4_1 else None,
            files=files or [],
            stop_after_tool_call=stop_after_tool_call,
        )
        
        # Обрабатываем ответ
        if isinstance(agent_response, str):
            # Синхронный ответ (ошибка или простой текст) - старый формат
            if agent_response.startswith("Ошибка") or agent_response.startswith("Агент с ID"):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=agent_response
                )
            
            if stream:
                # Для синхронного ответа в потоковом режиме
                async def single_response():
                    yield f"data: {agent_response}\n\n"
                return StreamingResponse(single_response(), media_type="text/event-stream")
            else:
                return agent_response
        elif isinstance(agent_response, dict):
            # Новый формат ответа с RunResponse объектом
            if stream:
                # Для структурированного ответа в потоковом режиме
                async def single_dict_response():
                    yield f"data: {json.dumps(agent_response)}\n\n"
                return StreamingResponse(single_dict_response(), media_type="text/event-stream")
            else:
                return agent_response
        else:
            # Потоковый ответ (AsyncGenerator)
            return StreamingResponse(
                chat_response_streamer(agent_response),
                media_type="text/event-stream"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run agent {agent_id}: {str(e)}"
        )


@agents_router.post("/{agent_id}/runs/{run_id}/continue", status_code=status.HTTP_200_OK)
async def continue_agent_run(
    agent_id: str,
    run_id: str,
    tools: str = Form(...),  # JSON string of tools
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    stream: bool = Form(True),
):
    """
    Продолжить выполнение агента с обновленными инструментами.
    Аналогично playground continue эндпоинту.

    Args:
        agent_id: ID агента
        run_id: ID запуска для продолжения
        tools: JSON строка с обновленными инструментами
        session_id: Опциональный ID сессии
        user_id: Опциональный ID пользователя
        stream: Использовать ли потоковую передачу

    Returns:
        Либо потоковый ответ, либо полный ответ агента
    """
    # Parse the JSON string manually
    try:
        tools_data = json.loads(tools) if tools else None
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in tools field")

    logger.debug(
        f"AgentContinueRunRequest: run_id={run_id} session_id={session_id} user_id={user_id} agent_id={agent_id}"
    )

    try:
        # Получаем агента для продолжения выполнения
        agent_instance = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if not agent_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )

        if session_id is None or session_id == "":
            logger.warning(
                "Continuing run without session_id. This might lead to unexpected behavior if session context is important."
            )
        else:
            logger.debug(f"Continuing run within session: {session_id}")

        # Convert tools dict to ToolExecution objects if provided
        updated_tools = None
        if tools_data:
            try:
                from agno.models.response import ToolExecution
                updated_tools = [ToolExecution.from_dict(tool) for tool in tools_data]
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid structure or content for tools: {str(e)}")

        if stream:
            # Потоковый режим
            async def continue_streamer():
                try:
                    continue_response = await agent_instance.acontinue_run(
                        run_id=run_id,
                        updated_tools=updated_tools,
                        session_id=session_id,
                        user_id=user_id,
                        stream=True,
                        stream_intermediate_steps=True,
                    )
                    async for run_response_chunk in continue_response:
                        yield f"data: {run_response_chunk.to_json()}\n\n"
                except Exception as e:
                    logger.error(f"Error in continue_streamer: {e}")
                    from agno.run.response import RunResponseErrorEvent
                    error_response = RunResponseErrorEvent(content=str(e))
                    yield f"data: {error_response.to_json()}\n\n"

            return StreamingResponse(continue_streamer(), media_type="text/event-stream")
        else:
            # Обычный режим
            run_response_obj = await agent_instance.acontinue_run(
                run_id=run_id,
                updated_tools=updated_tools,
                session_id=session_id,
                user_id=user_id,
                stream=False,
            )
            return run_response_obj.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error continuing agent run {agent_id}/{run_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to continue agent run: {str(e)}"
        )


# === Дополнительные эндпоинты для полной динамики ===

@agents_router.get("/meta/runtimes")
async def get_supported_runtimes():
    """Получить список поддерживаемых runtime"""
    try:
        return {
            "runtimes": ["agno"]  # Пока поддерживаем только Agno
        }
    except Exception as e:
        logger.error(f"Error getting supported runtimes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported runtimes"
        )


@agents_router.get("/meta/models")
async def get_supported_models(runtime: Optional[str] = None):
    """Получить список поддерживаемых моделей"""
    try:
        # Возвращаем модели из enum
        models = [model.value for model in Model]
        return {
            "runtime": runtime or "agno",
            "models": models
        }
    except Exception as e:
        logger.error(f"Error getting supported models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported models"
        )


@agents_router.get("/meta/tools")
async def get_supported_tools(runtime: Optional[str] = None):
    """Получить список поддерживаемых инструментов"""
    try:
        # Возвращаем известные Agno инструменты
        tools = [
            "DuckDuckGoTools", "YFinanceTools", "WebsiteTools", "EmailTools",
            "FileTools", "ShellTools", "PythonTools", "SqlTools", "CalculatorTools",
            "DateTimeTools", "WeatherTools", "NewsTools", "ImageTools", "AudioTools"
        ]
        return {
            "runtime": runtime or "agno",
            "tools": tools
        }
    except Exception as e:
        logger.error(f"Error getting supported tools: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported tools"
        )


@agents_router.post("/{agent_id}/validate")
async def validate_agent_config(agent_id: str):
    """Валидировать конфигурацию агента"""
    try:
        agent = dynamic_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )

        # Используем существующий метод валидации
        try:
            dynamic_agent_service._validate_agent_data(agent.to_dict())
            return {
                "valid": True,
                "errors": [],
                "agent_id": agent_id
            }
        except ValueError as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "agent_id": agent_id
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate agent {agent_id}"
        )


@agents_router.post("/{source_agent_id}/clone")
async def clone_agent(source_agent_id: str, new_agent_id: str, new_name: str):
    """Клонировать агента"""
    try:
        cloned_agent = dynamic_agent_service.clone_agent(source_agent_id, new_agent_id, new_name)
        if not cloned_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source agent with ID '{source_agent_id}' not found"
            )
        
        return _build_agent_response(cloned_agent)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cloning agent {source_agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clone agent {source_agent_id}"
        )


# === Управление кэшем ===

@agents_router.post("/cache/invalidate")
async def invalidate_all_cache():
    """Сбросить весь кэш агентов"""
    try:
        dynamic_agent_service.invalidate_all_cache()
        return {"message": "Весь кэш агентов успешно сброшен"}
    except Exception as e:
        logger.error(f"Error invalidating all cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to invalidate cache"
        )


@agents_router.post("/{agent_id}/cache/invalidate")
async def invalidate_agent_cache(agent_id: str):
    """Сбросить кэш для конкретного агента"""
    try:
        dynamic_agent_service.invalidate_agent_cache(agent_id)
        return {"message": f"Кэш агента {agent_id} успешно сброшен"}
    except Exception as e:
        logger.error(f"Error invalidating cache for agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invalidate cache for agent {agent_id}"
        )


@agents_router.post("/cache/refresh")
async def refresh_all_cache():
    """Принудительно обновить весь кэш агентов"""
    try:
        agents = dynamic_agent_service.refresh_all_cache()
        return {
            "message": "Весь кэш агентов успешно обновлен",
            "agents_count": len(agents)
        }
    except Exception as e:
        logger.error(f"Error refreshing all cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh cache"
        )


@agents_router.post("/{agent_id}/cache/refresh")
async def refresh_agent_cache(agent_id: str):
    """Принудительно обновить кэш для конкретного агента"""
    try:
        agent = dynamic_agent_service.refresh_agent_cache(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID '{agent_id}' not found"
            )
        
        return {
            "message": f"Кэш агента {agent_id} успешно обновлен",
            "agent": _build_agent_response(agent)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing cache for agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh cache for agent {agent_id}"
        )


@agents_router.get("/cache/stats")
async def get_cache_stats():
    """Получить статистику кэша агентов"""
    try:
        stats = dynamic_agent_service.get_cache_stats()
        return {
            "cache_stats": stats,
            "message": "Статистика кэша получена успешно"
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cache statistics"
        )


@agents_router.post("/cache/cleanup")
async def cleanup_expired_cache():
    """Очистить истекшие записи кэша"""
    try:
        cleaned_count = dynamic_agent_service.cleanup_expired_cache()
        return {
            "message": f"Очищено {cleaned_count} истекших записей кэша",
            "cleaned_entries": cleaned_count
        }
    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cleanup cache"
        )

# === Работа с сессиями (эквивалент Agno Playground) ===


@agents_router.get("/{agent_id}/sessions", response_model=List[AgentSessionsResponse])
async def get_all_agent_sessions(agent_id: str, user_id: Optional[str] = Query(None, min_length=1)):
    """Получить список всех сессий агента"""
    try:
        agno_agent = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if agno_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        if agno_agent.storage is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent does not have storage enabled")

        sessions: List[AgentSession] = agno_agent.storage.get_all_sessions(user_id=user_id, entity_id=agent_id)  # type: ignore
        result: List[AgentSessionsResponse] = []
        for session in sessions:
            title = get_session_title(session)
            result.append(
                AgentSessionsResponse(
                    title=title,
                    session_id=session.session_id,
                    session_name=session.session_data.get("session_name") if session.session_data else None,
                    created_at=session.created_at,
                )
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sessions for agent {agent_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve sessions")


@agents_router.get("/{agent_id}/sessions/{session_id}")
async def get_agent_session(agent_id: str, session_id: str, user_id: Optional[str] = Query(None, min_length=1)):
    """Получить конкретную сессию агента"""
    try:
        agno_agent = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if agno_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        if agno_agent.storage is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent does not have storage enabled")

        session: Optional[AgentSession] = agno_agent.storage.read(session_id, user_id)  # type: ignore
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        session_dict = session.to_dict()
        if session.memory is not None:
            runs = session.memory.get("runs")
            if runs is not None and len(runs) > 0:
                first_run = runs[0]
                if "content" in first_run or first_run.get("is_paused", False) or first_run.get("event") == "RunPaused":
                    session_dict["runs"] = []
                    for run in runs:
                        first_user_message = next(
                            (
                                msg
                                for msg in run.get("messages", [])
                                if msg.get("role") == "user" and not msg.get("from_history", False)
                            ),
                            None,
                        )
                        run.pop("memory", None)
                        session_dict["runs"].append({"message": first_user_message, "response": run})

        return session_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session {session_id} for agent {agent_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve session")


@agents_router.post("/{agent_id}/sessions/{session_id}/rename")
async def rename_agent_session(agent_id: str, session_id: str, body: AgentRenameRequest):
    """Переименовать сессию агента"""
    try:
        agno_agent = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if agno_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        if agno_agent.storage is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent does not have storage enabled")

        sessions: List[AgentSession] = agno_agent.storage.get_all_sessions(user_id=body.user_id)  # type: ignore
        for session in sessions:
            if session.session_id == session_id:
                agno_agent.rename_session(body.name, session_id=session_id)
                return JSONResponse(content={"message": f"Session {session.session_id} renamed"})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error renaming session {session_id} for agent {agent_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to rename session")


@agents_router.delete("/{agent_id}/sessions/{session_id}")
async def delete_agent_session(agent_id: str, session_id: str, user_id: Optional[str] = Query(None, min_length=1)):
    """Удалить сессию агента"""
    try:
        agno_agent = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if agno_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        if agno_agent.storage is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent does not have storage enabled")

        sessions: List[AgentSession] = agno_agent.storage.get_all_sessions(user_id=user_id, entity_id=agent_id)  # type: ignore
        for session in sessions:
            if session.session_id == session_id:
                agno_agent.delete_session(session_id)
                return JSONResponse(content={"message": f"Session {session_id} deleted"})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id} for agent {agent_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete session")


@agents_router.get("/{agent_id}/memories", response_model=List[MemoryResponse])
async def get_agent_memories(agent_id: str, user_id: str = Query(..., min_length=1)):
    """Получить воспоминания пользователя для указанного агента напрямую через Agno.

    Args:
        agent_id: ID агента
        user_id: ID пользователя, для которого запрашиваются воспоминания

    Returns:
        List[MemoryResponse]: Список воспоминаний пользователя
    """
    try:
        # Получаем инстанс агента из Agno
        agno_agent = await dynamic_agent_service.get_agent_instance_async(agent_id)
        if agno_agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        # Проверяем наличие памяти у агента
        if agno_agent.memory is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent does not have memory enabled")

        # Универсально получаем воспоминания, если метод поддерживается
        memories = []
        if hasattr(agno_agent.memory, "get_user_memories"):
            memories = agno_agent.memory.get_user_memories(user_id=user_id)  # type: ignore
        else:
            # Если метод недоступен – возвращаем пустой список
            memories = []

        # Формируем ответ
        return [
            MemoryResponse(memory=m.memory, topics=getattr(m, "topics", None), last_updated=getattr(m, "last_updated", None))  # type: ignore
            for m in memories
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting memories for agent {agent_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve agent memories")

@agents_router.post("/cache/clear")
async def clear_all_cache():
    """Алиас для /cache/invalidate – поддержка старого тест-плана."""
    return await invalidate_all_cache()

@agents_router.post("/{agent_id}/cache/clear")
async def clear_agent_cache(agent_id: str):
    """Алиас для /{agent_id}/cache/invalidate – поддержка старого тест-плана."""
    return await invalidate_agent_cache(agent_id)
