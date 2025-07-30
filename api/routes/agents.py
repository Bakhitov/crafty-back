from enum import Enum
from logging import getLogger
from typing import AsyncGenerator, List, Optional
import json
import time

from agno.agent import Agent, AgentKnowledge
from agno.media import Image, Audio, Video, File as FileMedia
from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agents.agno_assist import get_agno_assist_knowledge
from agents.selector import AgentType, get_agent, get_available_agents
from api.utils.file_processing import process_files
from db.session import get_db

logger = getLogger(__name__)

######################################################
## Routes for the Agent Interface
######################################################

agents_router = APIRouter(prefix="/agents", tags=["Agents"])


@agents_router.get("", response_model=List[str])
async def list_agents(db: Session = Depends(get_db)):
    """
    Возвращает список всех доступных агентов (статических + динамических).

    Returns:
        List[str]: List of agent identifiers
    """
    return get_available_agents(db)


async def chat_response_streamer(
    agent: Agent, 
    message: str,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    images: Optional[List[Image]] = None,
    audio: Optional[List[Audio]] = None,
    videos: Optional[List[Video]] = None,
    files: Optional[List[FileMedia]] = None,
) -> AsyncGenerator:
    """
    Stream agent responses chunk by chunk with full events and media support.

    Args:
        agent: The agent instance to interact with
        message: User message to process
        session_id: Session ID (optional)
        user_id: User ID (optional)
        images: List of input images (optional)
        audio: List of input audio files (optional)
        videos: List of input video files (optional)
        files: List of input files (optional)

    Yields:
        Full JSON events from the agent response
    """
    try:
        run_response = await agent.arun(
            message,
            session_id=session_id,
            user_id=user_id,
            images=images,
            audio=audio,
            videos=videos,
            files=files,
            stream=True,
            stream_intermediate_steps=True,  # ← КРИТИЧНО! Все события
        )
        async for chunk in run_response:
            # ✅ ПОЛНЫЕ события в JSON + медиа обработка
            if hasattr(chunk, 'to_json'):
                chunk_dict = json.loads(chunk.to_json())
                
                # Обработка медиа в событиях (если есть)
                if chunk_dict.get('event') == 'ToolCallCompleted':
                    # ToolCallCompletedEvent может содержать images, videos, audio
                    process_event_media(chunk_dict)
                elif chunk_dict.get('event') == 'RunResponseContent':
                    # RunResponseContentEvent может содержать image, response_audio
                    process_event_media(chunk_dict)
                elif chunk_dict.get('event') == 'RunCompleted':
                    # RunResponseCompletedEvent может содержать images, videos, audio, response_audio
                    process_event_media(chunk_dict)
                
                yield json.dumps(chunk_dict)
            else:
                yield chunk.content  # Fallback
    except Exception as e:
        # ✅ ПРАВИЛЬНАЯ обработка ошибок (изолированно от agno)
        error_dict = {
            "event": "RunError",
            "content": str(e),
            "agent_id": getattr(agent, 'agent_id', ''),
            "created_at": int(time.time())
        }
        yield json.dumps(error_dict)


def process_event_media(event_dict):
    """Обрабатывает медиа контент в событиях"""
    # Обработка изображений в событии
    if event_dict.get('images'):
        for img in event_dict['images']:
            # Медиа от инструментов или модели
            pass
    
    # Обработка аудио в событии  
    if event_dict.get('audio'):
        for audio in event_dict['audio']:
            pass
    
    # Обработка видео в событии
    if event_dict.get('videos'):
        for video in event_dict['videos']:
            pass
    
    # image в RunResponseContentEvent
    if event_dict.get('image'):
        pass
    
    # response_audio в событиях
    if event_dict.get('response_audio'):
        pass


@agents_router.post("/{agent_id}/runs", status_code=status.HTTP_200_OK)
async def create_agent_run(
    agent_id: str,
    message: str = Form(...),
    stream: bool = Form(True),
    model: str = Form("gpt-4.1-mini-2025-04-14"),
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),  # ← ФАЙЛЫ
    db: Session = Depends(get_db)
):
    """
    Отправляет сообщение агенту любого типа (статический или динамический) с поддержкой файлов.

    Args:
        agent_id: ID агента для взаимодействия
        message: Сообщение пользователя
        stream: Потоковый ответ (по умолчанию True)
        model: Модель для использования (по умолчанию gpt-4.1)
        session_id: ID сессии (опционально)
        user_id: ID пользователя (опционально)
        files: Список загружаемых файлов (опционально)
        db: Сессия БД

    Returns:
        Потоковый ответ или полный ответ агента с поддержкой медиа
    """
    logger.debug(f"Agent run: agent_id={agent_id}, message={message[:50]}..., files_count={len(files) if files else 0}")

    # Обработка файлов (1 строка)
    images, audios, videos, input_files = process_files(files)
    
    # Получение агента (как было)
    try:
        agent: Agent = get_agent(
            model_id=model,
            agent_id=agent_id,
            user_id=user_id,
            session_id=session_id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    if stream:
        return StreamingResponse(
            chat_response_streamer(
                agent, message,
                session_id=session_id,
                user_id=user_id,
                images=images if images else None,
                audio=audios if audios else None,
                videos=videos if videos else None,
                files=input_files if input_files else None,
            ),
            media_type="text/event-stream",
        )
    else:
        response = await agent.arun(
            message,
            session_id=session_id,
            user_id=user_id,
            images=images if images else None,
            audio=audios if audios else None,
            videos=videos if videos else None,
            files=input_files if input_files else None,
            stream=False,
        )
        # ✅ ПОЛНАЯ структура вместо только content
        return response.to_dict() if hasattr(response, 'to_dict') else response.content


@agents_router.post("/{agent_id}/runs/{run_id}/continue", status_code=status.HTTP_200_OK)
async def continue_agent_run(
    agent_id: str,
    run_id: str,
    tools: str = Form(...),  # JSON string
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    stream: bool = Form(True),
    db: Session = Depends(get_db)
):
    """
    Продолжает выполнение приостановленного агента с обновленными инструментами.

    Args:
        agent_id: ID агента для продолжения
        run_id: ID выполнения для продолжения
        tools: JSON строка с обновленными инструментами
        session_id: ID сессии (опционально)
        user_id: ID пользователя (опционально)
        stream: Потоковый ответ (по умолчанию True)
        db: Сессия БД

    Returns:
        Потоковый ответ или полный ответ продолжения выполнения
    """
    logger.debug(f"Continue run: agent_id={agent_id}, run_id={run_id}, tools={tools[:100]}...")

    # Обработка tools как в playground агно
    try:
        tools_data = json.loads(tools) if tools else []
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in tools field")
    
    # Конвертация в ToolExecution объекты (как в agno playground)
    # Агно требует updated_tools для continue, используем пустой список если не указаны
    try:
        from agno.models.response import ToolExecution
        if tools_data:
            updated_tools = [ToolExecution.from_dict(tool) for tool in tools_data]
        else:
            updated_tools = []  # Пустой список вместо None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid structure or content for tools: {str(e)}")
    
    # Получение агента (наша логика)
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, user_id=user_id, session_id=session_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    # Используем agno continue если есть, fallback если нет
    if hasattr(agent, 'acontinue_run'):
        if stream:
            return StreamingResponse(
                continue_response_streamer(agent, run_id, updated_tools, session_id, user_id),
                media_type="text/event-stream",
            )
        else:
            try:
                response = await agent.acontinue_run(
                    run_id=run_id,
                    updated_tools=updated_tools,
                    session_id=session_id,
                    user_id=user_id,
                    stream=False,
                )
                return response.to_dict() if hasattr(response, 'to_dict') else response.content
            except RuntimeError as e:
                if "No runs found for run ID" in str(e):
                    raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
                raise HTTPException(status_code=500, detail=f"Continue run failed: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Continue run error: {str(e)}")
    else:
        raise HTTPException(status_code=501, detail="Continue run not supported by this agent")


# Простой стример для continue (копия основного стримера)
async def continue_response_streamer(agent, run_id, updated_tools, session_id, user_id):
    """Стример для продолжения выполнения агента"""
    try:
        continue_response = await agent.acontinue_run(
            run_id=run_id,
            updated_tools=updated_tools,
            session_id=session_id,
            user_id=user_id,
            stream=True,
            stream_intermediate_steps=True,
        )
        async for chunk in continue_response:
            # Используем полные события как в основном стримере
            if hasattr(chunk, 'to_json'):
                chunk_dict = json.loads(chunk.to_json())
                
                # Обработка медиа в событиях continue (если есть)
                if chunk_dict.get('event') in ['ToolCallCompleted', 'RunResponseContent', 'RunCompleted']:
                    process_event_media(chunk_dict)
                
                yield json.dumps(chunk_dict)
            else:
                yield chunk.content
    except RuntimeError as e:
        if "No runs found for run ID" in str(e):
            error_dict = {
                "event": "RunError",
                "content": f"Run {run_id} not found", 
                "error_type": "NotFound",
                "created_at": int(time.time())
            }
        else:
            error_dict = {
                "event": "RunError",
                "content": f"Continue run failed: {str(e)}",
                "error_type": "RuntimeError", 
                "created_at": int(time.time())
            }
        yield json.dumps(error_dict)
    except Exception as e:
        error_dict = {
            "event": "RunError",
            "content": f"Continue run error: {str(e)}",
            "error_type": "General",
            "created_at": int(time.time())
        }
        yield json.dumps(error_dict)


# ========== SESSION & MEMORY MANAGEMENT (Фаза 3) ==========

@agents_router.get("/{agent_id}/sessions")
async def get_all_agent_sessions(
    agent_id: str, 
    user_id: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    """Получение всех сессий агента"""
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    if not hasattr(agent, 'storage') or agent.storage is None:
        raise HTTPException(status_code=404, detail="Agent does not have storage enabled.")
    
    try:
        all_sessions = agent.storage.get_all_sessions(user_id=user_id, entity_id=agent_id)
        return [
            {
                "session_id": session.session_id,
                "session_name": session.session_data.get("session_name") if session.session_data else None,
                "created_at": session.created_at,
                "title": f"Session {session.session_id[:8]}"  # Простой title без playground зависимостей
            }
            for session in all_sessions
        ]
    except HTTPException:
        raise  # Пропускаем HTTP ошибки без изменения
    except Exception as e:
        # Проверяем на ошибки "не найдено" от agno  
        error_msg = str(e).lower()
        if "404" in str(e) or "not found" in error_msg:
            raise HTTPException(status_code=404, detail="Sessions not found")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@agents_router.get("/{agent_id}/sessions/{session_id}")
async def get_agent_session(
    agent_id: str, 
    session_id: str, 
    user_id: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    """Получение конкретной сессии агента"""
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    if not hasattr(agent, 'storage') or agent.storage is None:
        raise HTTPException(status_code=404, detail="Agent does not have storage enabled.")
    
    try:
        session = agent.storage.read(session_id, user_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session.to_dict()
    except HTTPException:
        raise  # Пропускаем HTTP ошибки без изменения
    except Exception as e:
        # Проверяем на ошибки "не найдено" от agno
        error_msg = str(e).lower()
        if "404" in str(e) or "not found" in error_msg:
            raise HTTPException(status_code=404, detail="Session not found")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


class SessionRenameRequest(BaseModel):
    name: str
    user_id: Optional[str] = None


@agents_router.post("/{agent_id}/sessions/{session_id}/rename")
async def rename_agent_session(
    agent_id: str, 
    session_id: str, 
    body: SessionRenameRequest,
    db: Session = Depends(get_db)
):
    """Переименование сессии агента"""
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    if not hasattr(agent, 'storage') or agent.storage is None:
        raise HTTPException(status_code=404, detail="Agent does not have storage enabled.")
    
    try:
        if hasattr(agent, 'rename_session'):
            agent.rename_session(body.name, session_id=session_id)
            return {"message": f"Successfully renamed session {session_id}"}
        else:
            raise HTTPException(status_code=501, detail="Session renaming not supported by this agent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming session: {str(e)}")


@agents_router.delete("/{agent_id}/sessions/{session_id}")
async def delete_agent_session(
    agent_id: str, 
    session_id: str, 
    user_id: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    """Удаление сессии агента"""
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    if not hasattr(agent, 'storage') or agent.storage is None:
        raise HTTPException(status_code=404, detail="Agent does not have storage enabled.")
    
    try:
        agent.delete_session(session_id)
        return {"message": f"Successfully deleted session {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


@agents_router.get("/{agent_id}/memories")
async def get_agent_memories(
    agent_id: str, 
    user_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Получение памяти агента для пользователя"""
    try:
        agent = get_agent(model_id="gpt-4.1-mini-2025-04-14", agent_id=agent_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    if not hasattr(agent, 'memory') or agent.memory is None:
        raise HTTPException(status_code=404, detail="Agent does not have memory enabled.")
    
    try:
        # Простая реализация без зависимостей от playground
        if hasattr(agent.memory, 'get_user_memories'):
            memories = agent.memory.get_user_memories(user_id=user_id)
            return [
                {
                    "memory": memory.memory if hasattr(memory, 'memory') else str(memory),
                    "topics": memory.topics if hasattr(memory, 'topics') else [],
                    "last_updated": memory.last_updated if hasattr(memory, 'last_updated') else None
                }
                for memory in memories
            ]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memories: {str(e)}")


@agents_router.post("/{agent_id}/knowledge/load", status_code=status.HTTP_200_OK)
async def load_agent_knowledge(agent_id: str):  # Изменил тип на str
    """
    Загружает базу знаний для конкретного агента.
    Пока поддерживается только для статических агентов.

    Args:
        agent_id: ID агента для загрузки знаний.

    Returns:
        Сообщение об успехе если база знаний загружена.
    """
    agent_knowledge: Optional[AgentKnowledge] = None

    if agent_id == AgentType.AGNO_ASSIST.value:
        agent_knowledge = get_agno_assist_knowledge()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent {agent_id} does not have a knowledge base.",
        )

    try:
        await agent_knowledge.aload(upsert=True)
    except Exception as e:
        logger.error(f"Error loading knowledge base for {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load knowledge base for {agent_id}.",
        )

    return {"message": f"Knowledge base for {agent_id} loaded successfully."}
