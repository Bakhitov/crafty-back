"""
Провайдер для MCP серверов.
✅ ПРАВИЛЬНОЕ использование существующего Agno MCPTools согласно плану.
"""

from typing import Dict, Any, Optional
from agno.tools.mcp import MCPTools
import logging

logger = logging.getLogger(__name__)


class MCPProvider:
    """✅ Провайдер для динамических MCP серверов через стандартный Agno MCPTools"""
    
    @staticmethod
    async def create_mcp_instance(server_data: Dict[str, Any], **kwargs) -> MCPTools:
        """✅ ПРАВИЛЬНОЕ создание MCPTools из конфигурации БД согласно Agno API"""
        
        server_id = server_data['server_id']
        transport = server_data.get('transport', 'stdio')
        
        # ✅ ПРАВИЛЬНЫЕ параметры MCPTools согласно Agno API
        mcp_params = {
            'transport': transport,
            **kwargs  # Дополнительные параметры от пользователя
        }
        
        # ✅ Настройка параметров согласно Agno MCPTools API
        if transport == 'stdio':
            if not server_data.get('command'):
                raise ValueError(f"Для MCP сервера '{server_id}' с транспортом 'stdio' требуется команда")
            
            mcp_params['command'] = server_data['command']
            
            # Добавляем переменные окружения если есть
            if server_data.get('env_config'):
                mcp_params['env'] = server_data['env_config']
                
        elif transport in ['sse', 'streamable-http']:
            if not server_data.get('url'):
                raise ValueError(f"Для MCP сервера '{server_id}' с транспортом '{transport}' требуется URL")
            
            mcp_params['url'] = server_data['url']
            
        else:
            raise ValueError(f"Неподдерживаемый транспорт: {transport}")
        
        logger.info(f"Создание MCP подключения '{server_id}' через {transport}")
        
        # timeout_seconds определяет лимит ожидания handshake (по умолчанию 5 с).
        if 'timeout_seconds' not in mcp_params:
            mcp_params['timeout_seconds'] = 10

        # ✅ Создаем MCPTools через стандартный Agno API
        mcp_tools = MCPTools(**mcp_params)
        
        # ✅ Используем async context manager для инициализации
        # Инициализируем подключение, но не используем полный context manager здесь
        # так как экземпляр будет возвращен для дальнейшего использования
        await mcp_tools.__aenter__()
        
        logger.info(f"✅ MCP сервер '{server_id}' подключен, доступно {len(mcp_tools.functions)} функций")
        
        return mcp_tools
    
    @staticmethod
    async def test_mcp_connection(server_data: Dict[str, Any]) -> Dict[str, Any]:
        """Тестировать подключение к MCP серверу"""
        try:
            # Создаем временное подключение
            mcp_tools = await MCPProvider.create_mcp_instance(server_data)
            
            # Получаем информацию о доступных инструментах
            available_tools = []
            for func_name, func in mcp_tools.functions.items():
                available_tools.append({
                    'name': func_name,
                    'description': getattr(func, 'description', None),
                    'parameters': getattr(func, 'parameters', {})
                })
            
            # ✅ ПРАВИЛЬНОЕ закрытие подключения
            await mcp_tools.__aexit__(None, None, None)
            
            return {
                'success': True,
                'server_id': server_data['server_id'],
                'transport': server_data['transport'],
                'tools_count': len(available_tools),
                'tools': available_tools
            }
            
        except Exception as e:
            logger.error(f"Ошибка подключения к MCP серверу '{server_data.get('server_id')}': {e}")
            return {
                'success': False,
                'server_id': server_data.get('server_id'),
                'error': str(e)
            }
    
    @staticmethod
    async def close_mcp_instance(mcp_tools: MCPTools):
        """✅ Корректно закрыть MCP подключение"""
        try:
            await mcp_tools.__aexit__(None, None, None)
            logger.info(f"MCP подключение '{mcp_tools.name}' закрыто")
        except Exception as e:
            logger.error(f"Ошибка закрытия MCP подключения: {e}") 