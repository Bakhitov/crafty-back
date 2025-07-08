"""
Простой сервис для управления динамическими инструментами.
Только CRUD операции, без избыточной сложности.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.models import DynamicTool, CustomTool, MCPServer
from db.session import SessionLocal

class DynamicToolService:
    """Простой CRUD сервис для динамических инструментов"""
    
    def __init__(self):
        self.db_session = SessionLocal
    
    def get_all_active_tools(self) -> List[DynamicTool]:
        """Получить все активные инструменты"""
        with self.db_session() as session:
            return session.query(DynamicTool).filter(
                DynamicTool.is_active == True
            ).order_by(DynamicTool.created_at.desc()).all()
    
    def get_tool_by_id(self, tool_id: str) -> Optional[DynamicTool]:
        """Получить инструмент по ID"""
        with self.db_session() as session:
            return session.query(DynamicTool).filter(
                and_(
                    DynamicTool.tool_id == tool_id,
                    DynamicTool.is_active == True
                )
            ).first()
    
    def get_tools_by_ids(self, tool_ids: List[str]) -> List[DynamicTool]:
        """Получить инструменты по списку ID"""
        if not tool_ids:
            return []
        
        with self.db_session() as session:
            return session.query(DynamicTool).filter(
                and_(
                    DynamicTool.tool_id.in_(tool_ids),
                    DynamicTool.is_active == True
                )
            ).all()
    
    def create_tool(self, tool_data: Dict[str, Any]) -> DynamicTool:
        """Создать новый инструмент"""
        with self.db_session() as session:
            tool = DynamicTool(
                tool_id=tool_data['tool_id'],
                name=tool_data['name'],
                display_name=tool_data.get('display_name'),
                agno_class=tool_data['agno_class'],
                module_path=tool_data['module_path'],
                config=tool_data.get('config', {}),
                description=tool_data.get('description'),
                category=tool_data.get('category'),
                icon=tool_data.get('icon'),
                is_active=tool_data.get('is_active', True)
            )
            
            session.add(tool)
            session.commit()
            session.refresh(tool)
            return tool
    
    def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Optional[DynamicTool]:
        """Обновить инструмент"""
        with self.db_session() as session:
            tool = session.query(DynamicTool).filter(
                and_(
                    DynamicTool.tool_id == tool_id,
                    DynamicTool.is_active == True
                )
            ).first()
            
            if not tool:
                return None
            
            for key, value in tool_data.items():
                if hasattr(tool, key):
                    setattr(tool, key, value)
            
            session.commit()
            session.refresh(tool)
            return tool
    
    def delete_tool(self, tool_id: str) -> bool:
        """Удалить инструмент (soft delete)"""
        with self.db_session() as session:
            tool = session.query(DynamicTool).filter(
                and_(
                    DynamicTool.tool_id == tool_id,
                    DynamicTool.is_active == True
                )
            ).first()
            
            if not tool:
                return False
            
            tool.is_active = False
            session.commit()
            return True
    
    def get_tools_by_category(self, category: str) -> List[DynamicTool]:
        """Получить инструменты по категории"""
        with self.db_session() as session:
            return session.query(DynamicTool).filter(
                and_(
                    DynamicTool.category == category,
                    DynamicTool.is_active == True
                )
            ).order_by(DynamicTool.name).all()
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ КАСТОМНЫХ ИНСТРУМЕНТОВ ===
    
    def get_custom_tool(self, tool_id: str) -> Optional[CustomTool]:
        """Получить кастомный инструмент из БД"""
        with self.db_session() as session:
            return session.query(CustomTool).filter(
                and_(
                    CustomTool.tool_id == tool_id,
                    CustomTool.is_active == True
                )
            ).first()
    
    def get_all_custom_tools(self) -> List[CustomTool]:
        """Получить все активные кастомные инструменты"""
        with self.db_session() as session:
            return session.query(CustomTool).filter(
                CustomTool.is_active == True
            ).order_by(CustomTool.created_at.desc()).all()
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ MCP СЕРВЕРОВ ===
    
    def get_mcp_server(self, server_id: str) -> Optional[MCPServer]:
        """Получить MCP сервер из БД"""
        with self.db_session() as session:
            return session.query(MCPServer).filter(
                and_(
                    MCPServer.server_id == server_id,
                    MCPServer.is_active == True
                )
            ).first()
    
    def get_all_mcp_servers(self) -> List[MCPServer]:
        """Получить все активные MCP серверы"""
        with self.db_session() as session:
            return session.query(MCPServer).filter(
                MCPServer.is_active == True
            ).order_by(MCPServer.created_at.desc()).all()
    
    # === ГЛАВНЫЙ МЕТОД ДЛЯ СОЗДАНИЯ ЛЮБОГО ИНСТРУМЕНТА ===
    
    def create_tool_instance(self, tool_id: str, config: Dict[str, Any] = None) -> Optional[Any]:
        """
        Единая точка создания ЛЮБОГО инструмента:
        1. Стандартные Agno инструменты (dynamic_tools)
        2. Кастомные Python инструменты (custom_tools) 
        3. MCP серверы (mcp_servers)
        """
        if config is None:
            config = {}
        
        try:
            # Используем кэш для оптимизации
            from .custom_tool_provider import tool_cache
            
            # Проверяем кэш
            cached_tool = tool_cache.get(tool_id)
            if cached_tool:
                return cached_tool
            
            # 1. Проверяем стандартные Agno инструменты (УЖЕ РАБОТАЕТ)
            agno_tool_data = self.get_tool_by_id(tool_id)
            if agno_tool_data:
                tool_instance = self._create_agno_tool_instance(agno_tool_data.to_dict(), config)
                if tool_instance:
                    tool_cache.set(tool_id, tool_instance)
                    return tool_instance
            
            # 2. Проверяем кастомные Python инструменты (НОВОЕ)
            custom_tool = self.get_custom_tool(tool_id)
            if custom_tool:
                tool_instance = self._create_custom_tool_instance(custom_tool, config)
                if tool_instance:
                    tool_cache.set(tool_id, tool_instance)
                    return tool_instance
            
            # 3. Проверяем MCP серверы (НОВОЕ)
            mcp_server = self.get_mcp_server(tool_id)
            if mcp_server:
                # MCP - асинхронный, возвращаем coroutine
                return self._create_mcp_instance_async(mcp_server, config)
            
            return None
            
        except Exception as e:
            print(f"Ошибка создания инструмента '{tool_id}': {e}")
            return None
    
    def _create_custom_tool_instance(self, custom_tool: CustomTool, config: Dict[str, Any]) -> Any:
        """Создать экземпляр кастомного инструмента"""
        from .custom_tool_provider import CustomToolkit
        
        return CustomToolkit(
            tool_id=custom_tool.tool_id,
            name=custom_tool.name,
            source_code=custom_tool.source_code,
            description=custom_tool.description,
            config={**(custom_tool.config or {}), **config}
        )
    
    async def _create_mcp_instance_async(self, mcp_server: MCPServer, config: Dict[str, Any]) -> Any:
        """Создать экземпляр MCP сервера (асинхронно)"""
        from .mcp_provider import MCPProvider
        
        server_data = mcp_server.to_dict()
        return await MCPProvider.create_mcp_instance(server_data, **config)
    
    def _create_agno_tool_instance(self, tool_data: Dict[str, Any], config: Dict[str, Any]) -> Optional[Any]:
        """
        Создать экземпляр Agno инструмента по данным из БД.
        ДИНАМИЧЕСКИЙ ИМПОРТ ИЗ БД - поддержка всех 86+ классов.
        """
        try:
            if not tool_data.get('is_active', True):
                print(f"Инструмент '{tool_data['tool_id']}' отключен")
                return None
            
            # === ДИНАМИЧЕСКИЙ ИМПОРТ ===
            agno_class = tool_data['agno_class']
            module_path = tool_data['module_path']
            
            # Импорт модуля
            import importlib
            module = importlib.import_module(module_path)
            
            # Получение класса из модуля
            if not hasattr(module, agno_class):
                print(f"Класс '{agno_class}' не найден в модуле '{module_path}'")
                return None
            
            tool_class = getattr(module, agno_class)
            
            # === СОЗДАНИЕ ЭКЗЕМПЛЯРА ===
            # Объединение конфигурации из БД и переданной конфигурации
            final_config = {**(tool_data.get('config') or {}), **config}
            
            # Создание экземпляра инструмента
            tool_instance = tool_class(**final_config)
            
            print(f"✅ Создан инструмент: {agno_class} из {module_path}")
            return tool_instance
            
        except ImportError as e:
            print(f"❌ Ошибка импорта модуля '{module_path}': {e}")
            return None
        except AttributeError as e:
            print(f"❌ Класс '{agno_class}' не найден в модуле '{module_path}': {e}")
            return None
        except TypeError as e:
            print(f"❌ Ошибка создания экземпляра '{agno_class}': {e}")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка при создании инструмента '{tool_data['tool_id']}': {e}")
            return None
    
    # === МЕТОДЫ ИНВАЛИДАЦИИ КЭША ===
    
    def invalidate_tool_cache(self, tool_id: str):
        """Инвалидировать кэш конкретного инструмента"""
        from .custom_tool_provider import tool_cache
        tool_cache.invalidate(tool_id)
    
    def invalidate_all_tool_cache(self):
        """Очистить весь кэш инструментов"""
        from .custom_tool_provider import tool_cache
        tool_cache.invalidate_all()
    
    def cleanup_expired_cache(self) -> int:
        """Очистить устаревшие элементы кэша"""
        from .custom_tool_provider import tool_cache
        return tool_cache.cleanup_expired()

    def get_available_agno_classes(self) -> List[str]:
        """Получить полный список доступных классов Agno инструментов (101 класс)"""
        return [
            # A-C
            "AWSLambdaTools", "AgentQLTools", "AirflowTools", "ApifyTools", "ArxivTools",
            "AzureOpenAITools", "BaiduSearchTools", "BraveSearchTools", "BrightDataTools",
            "BrowserbaseTools", "CalComTools", "CalculatorTools", "CartesiaTools",
            "ClickUpTools", "ConfluenceTools", "Crawl4aiTools", "CsvTools", "CustomApiTools",
            
            # D-F
            "DalleTools", "DaytonaTools", "DesiVocalTools", "DiscordTools", "DockerTools",
            "DuckDbTools", "DuckDuckGoTools", "E2BTools", "ElevenLabsTools", "EmailTools",
            "ExaTools", "FalTools", "FileTools", "FinancialDatasetsTools", "FirecrawlTools",
            
            # G-J  
            "GeminiTools", "GiphyTools", "GithubTools", "GmailTools", "GoogleBigQueryTools",
            "GoogleCalendarTools", "GoogleMapTools", "GoogleSearchTools", "GoogleSheetsTools",
            "GroqTools", "HackerNewsTools", "JinaReaderTools", "JinaReaderToolsConfig", "JiraTools",
            
            # K-M
            "KnowledgeTools", "LinearTools", "LocalFileSystemTools", "LumaLabTools",
            "MCPTools", "MLXTranscribeTools", "Mem0Tools", "ModelsLabTools", "MoviePyVideoTools",
            "MultiMCPTools",
            
            # N-P
            "NebiusTools", "Newspaper4kTools", "NewspaperTools", "OpenAITools", "OpenBBTools",
            "OpenCVTools", "OpenWeatherTools", "PandasTools", "PostgresTools", "PubmedTools",
            "PythonTools",
            
            # R-S
            "ReasoningTools", "RedditTools", "ReplicateTools", "ResendTools", "SQLTools",
            "ScrapeGraphTools", "SerpApiTools", "SerperTools", "ShellTools", "SlackTools",
            "SleepTools", "SpiderTools",
            
            # T-W
            "TavilyTools", "TelegramTools", "ThinkingTools", "TodoistTools", "TrelloTools",
            "TwilioTools", "UserControlFlowTools", "VisualizationTools", "WebBrowserTools",
            "WebTools", "WebexTools", "WebsiteTools", "WhatsAppTools", "WikipediaTools",
            
            # X-Z
            "XTools", "YFinanceTools", "YouTubeTools", "ZendeskTools", "ZepAsyncTools",
            "ZepTools", "ZoomTools"
        ]

# Глобальный экземпляр сервиса
dynamic_tool_service = DynamicToolService() 