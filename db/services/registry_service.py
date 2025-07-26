"""
Сервис для работы с реестрами моделей, агентов и хуков.
Обеспечивает управление сложными объектами через ссылки.
"""

from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_
import importlib
import logging

from db.models import ModelRegistryTable, AgentRegistryTable, HookRegistryTable, ModelConfig
from db.registry_models import ModelRegistry, AgentRegistry, HookRegistry
from db.session import SessionLocal

logger = logging.getLogger(__name__)


class RegistryService:
    """Сервис для работы с реестрами"""
    
    def __init__(self):
        self.db_session = SessionLocal
    
    # === РЕЕСТР МОДЕЛЕЙ ===
    
    def get_model_by_id(self, registry_id: str) -> Optional[ModelRegistryTable]:
        """Получить модель из реестра по ID"""
        with self.db_session() as session:
            return session.query(ModelRegistryTable).filter(
                and_(
                    ModelRegistryTable.registry_id == registry_id,
                    ModelRegistryTable.is_active == True
                )
            ).first()
    
    def get_all_models(self) -> List[ModelRegistryTable]:
        """Получить все активные модели из реестра"""
        with self.db_session() as session:
            return session.query(ModelRegistryTable).filter(
                ModelRegistryTable.is_active == True
            ).order_by(ModelRegistryTable.created_at.desc()).all()
    
    def create_model_registry(self, registry_data: Dict[str, Any]) -> ModelRegistryTable:
        """Создать новую модель в реестре"""
        with self.db_session() as session:
            model_entry = ModelRegistryTable(
                registry_id=registry_data['registry_id'],
                name=registry_data['name'],
                description=registry_data.get('description'),
                model_config=registry_data['config_data'],
                is_active=registry_data.get('is_active', True),
                tags=registry_data.get('tags', [])
            )
            
            session.add(model_entry)
            session.commit()
            session.refresh(model_entry)
            return model_entry
    
    def resolve_model_reference(self, model_ref: Union[str, ModelConfig, Dict[str, Any]]) -> Optional[Any]:
        """
        Разрешить ссылку на модель в agno.Model объект
        """
        try:
            if isinstance(model_ref, str):
                # Ссылка на модель из реестра
                model_entry = self.get_model_by_id(model_ref)
                if not model_entry:
                    logger.error(f"Модель '{model_ref}' не найдена в реестре")
                    return None
                
                model_config = model_entry.get_model_config()
                if not model_config:
                    logger.error(f"Некорректная конфигурация модели '{model_ref}'")
                    return None
                
                return self._create_agno_model_instance(model_config)
                
            elif isinstance(model_ref, dict):
                # Встроенная конфигурация модели
                model_config = ModelConfig(**model_ref)
                return self._create_agno_model_instance(model_config)
                
            elif isinstance(model_ref, ModelConfig):
                # Готовая Pydantic модель
                return self._create_agno_model_instance(model_ref)
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка разрешения ссылки на модель: {e}")
            return None
    
    def _create_agno_model_instance(self, model_config: ModelConfig) -> Optional[Any]:
        """Создать экземпляр agno.Model из конфигурации"""
        try:
            # Импортируем нужный класс модели в зависимости от провайдера
            provider = model_config.provider or "openai"
            
            if provider.lower() in {"openai", "azure"}:
                from agno.models.openai import OpenAIChat
                return OpenAIChat(**model_config.dict(exclude_none=True))
            elif provider.lower() == "anthropic":
                from agno.models.anthropic import AnthropicChat
                return AnthropicChat(**model_config.dict(exclude_none=True))
            elif provider.lower() == "google":
                from agno.models.google import GoogleChat
                return GoogleChat(**model_config.dict(exclude_none=True))
            else:
                # Fallback к OpenAI
                from agno.models.openai import OpenAIChat
                return OpenAIChat(**model_config.dict(exclude_none=True))
                
        except Exception as e:
            logger.error(f"Ошибка создания экземпляра модели: {e}")
            return None
    
    # === РЕЕСТР АГЕНТОВ ===
    
    def get_agent_by_id(self, registry_id: str) -> Optional[AgentRegistryTable]:
        """Получить агента из реестра по ID"""
        with self.db_session() as session:
            return session.query(AgentRegistryTable).filter(
                and_(
                    AgentRegistryTable.registry_id == registry_id,
                    AgentRegistryTable.is_active == True
                )
            ).first()
    
    def get_all_agents(self) -> List[AgentRegistryTable]:
        """Получить всех активных агентов из реестра"""
        with self.db_session() as session:
            return session.query(AgentRegistryTable).filter(
                AgentRegistryTable.is_active == True
            ).order_by(AgentRegistryTable.created_at.desc()).all()
    
    def create_agent_registry(self, registry_data: Dict[str, Any]) -> AgentRegistryTable:
        """Создать нового агента в реестре"""
        with self.db_session() as session:
            agent_entry = AgentRegistryTable(
                registry_id=registry_data['registry_id'],
                name=registry_data['name'],
                description=registry_data.get('description'),
                agent_config=registry_data['agent_config'],
                is_active=registry_data.get('is_active', True),
                tags=registry_data.get('tags', [])
            )
            
            session.add(agent_entry)
            session.commit()
            session.refresh(agent_entry)
            return agent_entry
    
    def resolve_agent_reference(self, agent_ref: Union[str, Dict[str, Any]]) -> Optional[Any]:
        """
        Разрешить ссылку на агента в agno.Agent объект.
        ВНИМАНИЕ: Может вызвать циклическую зависимость!
        """
        try:
            if isinstance(agent_ref, str):
                # Ссылка на агента из реестра
                agent_entry = self.get_agent_by_id(agent_ref)
                if not agent_entry:
                    logger.error(f"Агент '{agent_ref}' не найден в реестре")
                    return None
                
                # Создаем упрощенного агента из конфигурации
                return self._create_simple_agent_instance(agent_entry.agent_config)
                
            elif isinstance(agent_ref, dict):
                # Встроенная конфигурация агента
                return self._create_simple_agent_instance(agent_ref)
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка разрешения ссылки на агента: {e}")
            return None
    
    def _create_simple_agent_instance(self, agent_config: Dict[str, Any]) -> Optional[Any]:
        """Создать упрощенный экземпляр agno.Agent из конфигурации"""
        try:
            from agno.agent.agent import Agent
            
            # Базовые параметры для агента
            basic_params = {
                'name': agent_config.get('name'),
                'description': agent_config.get('description'),
                'instructions': agent_config.get('instructions'),
            }
            
            # Модель (может быть ссылкой)
            if 'model' in agent_config:
                model_instance = self.resolve_model_reference(agent_config['model'])
                if model_instance:
                    basic_params['model'] = model_instance
            
            return Agent(**{k: v for k, v in basic_params.items() if v is not None})
            
        except Exception as e:
            logger.error(f"Ошибка создания экземпляра агента: {e}")
            return None
    
    # === РЕЕСТР ХУКОВ ===
    
    def get_hook_by_id(self, registry_id: str) -> Optional[HookRegistryTable]:
        """Получить хук из реестра по ID"""
        with self.db_session() as session:
            return session.query(HookRegistryTable).filter(
                and_(
                    HookRegistryTable.registry_id == registry_id,
                    HookRegistryTable.is_active == True
                )
            ).first()
    
    def get_all_hooks(self) -> List[HookRegistryTable]:
        """Получить все активные хуки из реестра"""
        with self.db_session() as session:
            return session.query(HookRegistryTable).filter(
                HookRegistryTable.is_active == True
            ).order_by(HookRegistryTable.created_at.desc()).all()
    
    def get_hooks_by_type(self, hook_type: str) -> List[HookRegistryTable]:
        """Получить хуки по типу"""
        with self.db_session() as session:
            return session.query(HookRegistryTable).filter(
                and_(
                    HookRegistryTable.hook_type == hook_type,
                    HookRegistryTable.is_active == True
                )
            ).order_by(HookRegistryTable.created_at.desc()).all()
    
    def create_hook_registry(self, registry_data: Dict[str, Any]) -> HookRegistryTable:
        """Создать новый хук в реестре"""
        with self.db_session() as session:
            hook_entry = HookRegistryTable(
                registry_id=registry_data['registry_id'],
                name=registry_data['name'],
                description=registry_data.get('description'),
                hook_type=registry_data['hook_type'],
                module_path=registry_data['module_path'],
                function_name=registry_data['function_name'],
                config=registry_data.get('config'),
                is_active=registry_data.get('is_active', True),
                tags=registry_data.get('tags', [])
            )
            
            session.add(hook_entry)
            session.commit()
            session.refresh(hook_entry)
            return hook_entry
    
    def resolve_hook_reference(self, hook_ref: Union[str, Dict[str, Any]]) -> Optional[callable]:
        """
        Разрешить ссылку на хук в callable функцию
        """
        try:
            if isinstance(hook_ref, str):
                # Ссылка на хук из реестра
                hook_entry = self.get_hook_by_id(hook_ref)
                if not hook_entry:
                    logger.error(f"Хук '{hook_ref}' не найден в реестре")
                    return None
                
                return self._load_hook_function(
                    hook_entry.module_path,
                    hook_entry.function_name,
                    hook_entry.config or {}
                )
                
            elif isinstance(hook_ref, dict):
                # Встроенная конфигурация хука
                return self._load_hook_function(
                    hook_ref['module_path'],
                    hook_ref['function_name'],
                    hook_ref.get('config', {})
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка разрешения ссылки на хук: {e}")
            return None
    
    def _load_hook_function(self, module_path: str, function_name: str, config: Dict[str, Any]) -> Optional[callable]:
        """Динамически загрузить функцию хука"""
        try:
            # Импорт модуля
            module = importlib.import_module(module_path)
            
            # Получение функции
            if not hasattr(module, function_name):
                logger.error(f"Функция '{function_name}' не найдена в модуле '{module_path}'")
                return None
            
            hook_function = getattr(module, function_name)
            
            # Проверяем что это callable
            if not callable(hook_function):
                logger.error(f"'{function_name}' в модуле '{module_path}' не является функцией")
                return None
            
            # Если есть конфигурация, можем обернуть функцию
            if config:
                def configured_hook(*args, **kwargs):
                    return hook_function(*args, config=config, **kwargs)
                return configured_hook
            
            return hook_function
            
        except ImportError as e:
            logger.error(f"Ошибка импорта модуля '{module_path}': {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка загрузки функции хука: {e}")
            return None
    
    def resolve_tool_hooks_list(self, tool_hooks_config: Optional[List[Dict[str, Any]]]) -> List[callable]:
        """
        Разрешить список конфигураций хуков в список callable функций
        """
        if not tool_hooks_config:
            return []
        
        resolved_hooks = []
        
        for hook_config in tool_hooks_config:
            if isinstance(hook_config, dict):
                # Прямая конфигурация хука
                hook_function = self.resolve_hook_reference(hook_config)
                if hook_function:
                    resolved_hooks.append(hook_function)
            elif isinstance(hook_config, str):
                # ID хука из реестра
                hook_function = self.resolve_hook_reference(hook_config)
                if hook_function:
                    resolved_hooks.append(hook_function)
        
        return resolved_hooks


# Глобальный экземпляр сервиса
registry_service = RegistryService() 