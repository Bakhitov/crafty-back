"""
Сервис для управления кастомными Python инструментами.
CRUD операции с таблицей custom_tools.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db.models import CustomTool
from db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)


class CustomToolService:
    """CRUD сервис для кастомных инструментов"""
    
    def __init__(self):
        self.db_session = SessionLocal
    
    def get_all_active_tools(self) -> List[CustomTool]:
        """Получить все активные кастомные инструменты"""
        with self.db_session() as session:
            return session.query(CustomTool).filter(
                CustomTool.is_active == True
            ).order_by(CustomTool.created_at.desc()).all()
    
    def get_tool_by_id(self, tool_id: str) -> Optional[CustomTool]:
        """Получить кастомный инструмент по ID"""
        with self.db_session() as session:
            return session.query(CustomTool).filter(
                and_(
                    CustomTool.tool_id == tool_id,
                    CustomTool.is_active == True
                )
            ).first()
    
    def create_tool(self, tool_data: Dict[str, Any]) -> CustomTool:
        """Создать новый кастомный инструмент"""
        with self.db_session() as session:
            tool = CustomTool(
                tool_id=tool_data['tool_id'],
                name=tool_data['name'],
                description=tool_data.get('description'),
                source_code=tool_data['source_code'],
                config=tool_data.get('config', {}),
                is_active=tool_data.get('is_active', True)
            )
            
            session.add(tool)
            session.commit()
            session.refresh(tool)
            
            # Инвалидируем кэш
            self._invalidate_cache(tool_data['tool_id'])
            
            logger.info(f"Создан кастомный инструмент: {tool_data['tool_id']}")
            return tool
    
    def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Optional[CustomTool]:
        """Обновить кастомный инструмент"""
        with self.db_session() as session:
            tool = session.query(CustomTool).filter(
                and_(
                    CustomTool.tool_id == tool_id,
                    CustomTool.is_active == True
                )
            ).first()
            
            if not tool:
                return None
            
            # Обновляем поля
            for key, value in tool_data.items():
                if hasattr(tool, key) and key != 'tool_id':  # ID не изменяем
                    setattr(tool, key, value)
            
            session.commit()
            session.refresh(tool)
            
            # Инвалидируем кэш
            self._invalidate_cache(tool_id)
            
            logger.info(f"Обновлен кастомный инструмент: {tool_id}")
            return tool
    
    def delete_tool(self, tool_id: str) -> bool:
        """Удалить кастомный инструмент (soft delete)"""
        with self.db_session() as session:
            tool = session.query(CustomTool).filter(
                and_(
                    CustomTool.tool_id == tool_id,
                    CustomTool.is_active == True
                )
            ).first()
            
            if not tool:
                return False
            
            tool.is_active = False
            session.commit()
            
            # Инвалидируем кэш
            self._invalidate_cache(tool_id)
            
            logger.info(f"Удален кастомный инструмент: {tool_id}")
            return True
    
    def test_tool_code(self, source_code: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Протестировать код инструмента без сохранения в БД"""
        try:
            from .custom_tool_provider import CustomToolkit
            
            # Создаем временный экземпляр для тестирования
            test_toolkit = CustomToolkit(
                tool_id="test_tool",
                name="Test Tool",
                source_code=source_code,
                description="Тестовый инструмент",
                config=config or {}
            )
            
            # Извлекаем информацию о функциях
            functions_info = []
            for func_name, func in test_toolkit.functions.items():
                functions_info.append({
                    'name': func_name,
                    'description': getattr(func, 'description', None),
                    'parameters': getattr(func, 'parameters', {})
                })
            
            return {
                'success': True,
                'functions': functions_info,
                'functions_count': len(functions_info)
            }
            
        except Exception as e:
            logger.error(f"Ошибка тестирования кода: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_tool_functions(self, tool_id: str) -> Dict[str, Any]:
        """Получить список функций кастомного инструмента"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            
            # Создаем экземпляр инструмента
            tool_instance = dynamic_tool_service.create_tool_instance(tool_id)
            
            if not tool_instance:
                return {'success': False, 'error': 'Инструмент не найден'}
            
            # Извлекаем информацию о функциях
            functions_info = []
            for func_name, func in tool_instance.functions.items():
                functions_info.append({
                    'name': func_name,
                    'description': getattr(func, 'description', None),
                    'parameters': getattr(func, 'parameters', {})
                })
            
            return {
                'success': True,
                'tool_id': tool_id,
                'functions': functions_info,
                'functions_count': len(functions_info)
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения функций инструмента '{tool_id}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_tool_function(self, tool_id: str, function_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить функцию кастомного инструмента"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            
            # Создаем экземпляр инструмента
            tool_instance = dynamic_tool_service.create_tool_instance(tool_id)
            
            if not tool_instance:
                return {'success': False, 'error': 'Инструмент не найден'}
            
            # Проверяем наличие функции
            if function_name not in tool_instance.functions:
                return {
                    'success': False, 
                    'error': f'Функция "{function_name}" не найдена',
                    'available_functions': list(tool_instance.functions.keys())
                }
            
            # Выполняем функцию
            function = tool_instance.functions[function_name]
            result = function.entrypoint(**parameters)
            
            return {
                'success': True,
                'tool_id': tool_id,
                'function_name': function_name,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Ошибка выполнения функции '{function_name}' инструмента '{tool_id}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_tool_instance(self, tool_id: str, config: Dict[str, Any] = None) -> Optional[Any]:
        """Создать экземпляр кастомного инструмента"""
        try:
            # Получаем данные инструмента из БД
            tool_data = self.get_tool_by_id(tool_id)
            
            if not tool_data:
                logger.error(f"Кастомный инструмент '{tool_id}' не найден в БД")
                return None
            
            if not tool_data.is_active:
                logger.error(f"Кастомный инструмент '{tool_id}' отключен")
                return None
            
            # Импортируем provider
            from .custom_tool_provider import CustomToolProvider
            
            # Создаем экземпляр через provider
            tool_instance = CustomToolProvider.create_tool_instance(
                tool_id=tool_data.tool_id,
                name=tool_data.name,
                source_code=tool_data.source_code,
                description=tool_data.description or "Кастомный инструмент",
                config={**(tool_data.config or {}), **(config or {})}
            )
            
            logger.info(f"✅ Создан кастомный инструмент: {tool_id}")
            return tool_instance
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания кастомного инструмента '{tool_id}': {e}")
            return None
    
    def _invalidate_cache(self, tool_id: str):
        """Инвалидировать кэш инструмента"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            dynamic_tool_service.invalidate_tool_cache(tool_id)
        except Exception as e:
            logger.warning(f"Ошибка инвалидации кэша для '{tool_id}': {e}")


# Глобальный экземпляр сервиса
custom_tool_service = CustomToolService() 