"""
Сервис для управления MCP серверами.
CRUD операции с таблицей mcp_servers.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db.models import MCPServer
from db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)


class MCPService:
    """CRUD сервис для MCP серверов"""
    
    def __init__(self):
        self.db_session = SessionLocal
    
    def get_all_active_servers(self) -> List[MCPServer]:
        """Получить все активные MCP серверы"""
        with self.db_session() as session:
            return session.query(MCPServer).filter(
                MCPServer.is_active == True
            ).order_by(MCPServer.created_at.desc()).all()
    
    def get_server_by_id(self, server_id: str) -> Optional[MCPServer]:
        """Получить MCP сервер по ID"""
        with self.db_session() as session:
            return session.query(MCPServer).filter(
                and_(
                    MCPServer.server_id == server_id,
                    MCPServer.is_active == True
                )
            ).first()
    
    def get_servers_by_transport(self, transport: str) -> List[MCPServer]:
        """Получить MCP серверы по типу транспорта"""
        with self.db_session() as session:
            return session.query(MCPServer).filter(
                and_(
                    MCPServer.transport == transport,
                    MCPServer.is_active == True
                )
            ).order_by(MCPServer.name).all()
    
    def create_server(self, server_data: Dict[str, Any]) -> MCPServer:
        """Создать новый MCP сервер"""
        with self.db_session() as session:
            server = MCPServer(
                server_id=server_data['server_id'],
                name=server_data['name'],
                description=server_data.get('description'),
                command=server_data.get('command'),
                url=server_data.get('url'),
                transport=server_data.get('transport', 'stdio'),
                env_config=server_data.get('env_config'),
                is_active=server_data.get('is_active', True)
            )
            
            session.add(server)
            session.commit()
            session.refresh(server)
            
            # Инвалидируем кэш
            self._invalidate_cache(server_data['server_id'])
            
            logger.info(f"Создан MCP сервер: {server_data['server_id']} ({server_data.get('transport', 'stdio')})")
            return server
    
    def update_server(self, server_id: str, server_data: Dict[str, Any]) -> Optional[MCPServer]:
        """Обновить MCP сервер"""
        with self.db_session() as session:
            server = session.query(MCPServer).filter(
                and_(
                    MCPServer.server_id == server_id,
                    MCPServer.is_active == True
                )
            ).first()
            
            if not server:
                return None
            
            # Обновляем поля
            for key, value in server_data.items():
                if hasattr(server, key) and key != 'server_id':  # ID не изменяем
                    setattr(server, key, value)
            
            session.commit()
            session.refresh(server)
            
            # Инвалидируем кэш
            self._invalidate_cache(server_id)
            
            logger.info(f"Обновлен MCP сервер: {server_id}")
            return server
    
    def delete_server(self, server_id: str) -> bool:
        """Удалить MCP сервер (soft delete)"""
        with self.db_session() as session:
            server = session.query(MCPServer).filter(
                and_(
                    MCPServer.server_id == server_id,
                    MCPServer.is_active == True
                )
            ).first()
            
            if not server:
                return False
            
            server.is_active = False
            session.commit()
            
            # Инвалидируем кэш
            self._invalidate_cache(server_id)
            
            logger.info(f"Удален MCP сервер: {server_id}")
            return True
    
    async def test_server_connection(self, server_id: str) -> Dict[str, Any]:
        """Протестировать подключение к MCP серверу"""
        try:
            server = self.get_server_by_id(server_id)
            if not server:
                return {'success': False, 'error': 'MCP сервер не найден'}
            
            from .mcp_provider import MCPProvider
            
            # Тестируем подключение
            result = await MCPProvider.test_mcp_connection(server.to_dict())
            
            logger.info(f"Тест подключения MCP сервера '{server_id}': {'успешно' if result['success'] else 'ошибка'}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка тестирования MCP сервера '{server_id}': {e}")
            return {
                'success': False,
                'server_id': server_id,
                'error': str(e)
            }
    
    async def get_server_tools(self, server_id: str) -> Dict[str, Any]:
        """Получить список инструментов MCP сервера"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            
            # Создаем экземпляр MCP подключения
            mcp_instance = await dynamic_tool_service._create_mcp_instance_async(
                self.get_server_by_id(server_id), {}
            )
            
            if not mcp_instance:
                return {'success': False, 'error': 'Не удалось подключиться к MCP серверу'}
            
            # Извлекаем информацию об инструментах
            tools_info = []
            for func_name, func in mcp_instance.functions.items():
                tools_info.append({
                    'name': func_name,
                    'description': getattr(func, 'description', None),
                    'parameters': getattr(func, 'parameters', {})
                })
            
            # Закрываем подключение
            from .mcp_provider import MCPProvider
            await MCPProvider.close_mcp_instance(mcp_instance)
            
            return {
                'success': True,
                'server_id': server_id,
                'tools': tools_info,
                'tools_count': len(tools_info)
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения инструментов MCP сервера '{server_id}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def execute_server_tool(self, server_id: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить инструмент MCP сервера"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            
            # Создаем экземпляр MCP подключения
            mcp_instance = await dynamic_tool_service._create_mcp_instance_async(
                self.get_server_by_id(server_id), {}
            )
            
            if not mcp_instance:
                return {'success': False, 'error': 'Не удалось подключиться к MCP серверу'}
            
            # Проверяем наличие инструмента
            if tool_name not in mcp_instance.functions:
                available_tools = list(mcp_instance.functions.keys())
                await MCPProvider.close_mcp_instance(mcp_instance)
                return {
                    'success': False,
                    'error': f'Инструмент "{tool_name}" не найден',
                    'available_tools': available_tools
                }
            
            # Выполняем инструмент
            function = mcp_instance.functions[tool_name]
            result = await function.entrypoint(**parameters)
            
            # Закрываем подключение
            from .mcp_provider import MCPProvider
            await MCPProvider.close_mcp_instance(mcp_instance)
            
            return {
                'success': True,
                'server_id': server_id,
                'tool_name': tool_name,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Ошибка выполнения инструмента '{tool_name}' MCP сервера '{server_id}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_server_config(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидировать конфигурацию MCP сервера"""
        errors = []
        
        # Проверяем обязательные поля
        required_fields = ['server_id', 'name']
        for field in required_fields:
            if not server_data.get(field):
                errors.append(f"Поле '{field}' обязательно")
        
        transport = server_data.get('transport', 'stdio')
        
        # Проверяем параметры в зависимости от транспорта
        if transport == 'stdio':
            if not server_data.get('command'):
                errors.append("Для stdio транспорта требуется команда")
        elif transport in ['sse', 'streamable-http']:
            if not server_data.get('url'):
                errors.append(f"Для {transport} транспорта требуется URL")
        else:
            errors.append(f"Неподдерживаемый транспорт: {transport}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    async def create_tool_instance_async(self, server_id: str, config: Dict[str, Any] = None) -> Optional[Any]:
        """✅ ПРАВИЛЬНЫЙ асинхронный метод создания MCP инструмента"""
        try:
            # Получаем данные сервера из БД
            server_data = self.get_server_by_id(server_id)
            
            if not server_data:
                logger.error(f"MCP сервер '{server_id}' не найден в БД")
                return None
            
            if not server_data.is_active:
                logger.error(f"MCP сервер '{server_id}' отключен")
                return None
            
            # Импортируем provider
            from .mcp_provider import MCPProvider
            
            # ✅ Создаем и ИНИЦИАЛИЗИРУЕМ MCPTools
            mcp_tools = await MCPProvider.create_mcp_instance(server_data.to_dict())
            
            logger.info(f"✅ MCP инструмент '{server_id}' создан успешно")
            return mcp_tools
            
        except Exception as e:
            logger.error(f"Ошибка создания MCP инструмента '{server_id}': {e}")
            return None
    
    def create_tool_instance(self, server_id: str, config: Dict[str, Any] = None) -> Optional[Any]:
        """❌ УСТАРЕВШИЙ синхронный метод - не используйте для MCP"""
        logger.warning(f"⚠️ Попытка синхронного создания MCP инструмента '{server_id}' - используйте create_tool_instance_async()")
        return None
    
    def _invalidate_cache(self, server_id: str):
        """Инвалидировать кэш сервера"""
        try:
            from db.services.dynamic_tool_service import dynamic_tool_service
            dynamic_tool_service.invalidate_tool_cache(server_id)
        except Exception as e:
            logger.warning(f"Ошибка инвалидации кэша для '{server_id}': {e}")


# Глобальный экземпляр сервиса
mcp_service = MCPService() 