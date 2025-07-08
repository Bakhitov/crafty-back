"""
Провайдер для кастомных Python инструментов.
✅ ПРАВИЛЬНАЯ интеграция с Agno Toolkit согласно плану.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from agno.tools.toolkit import Toolkit
import ast
import logging

logger = logging.getLogger(__name__)


class CustomToolProvider:
    """Легковесный провайдер кастомных инструментов"""
    
    @staticmethod
    def validate_code(code: str) -> bool:
        """Простая и эффективная валидация"""
        try:
            compile(code, '<string>', 'exec')
            
            # Проверка на опасные конструкции
            dangerous = [
                'import os', 'import sys', 'import subprocess',
                'exec(', 'eval(', '__import__', 'open('
            ]
            
            return not any(pattern in code for pattern in dangerous)
        except SyntaxError:
            return False
    
    @staticmethod
    def create_tool_instance(tool_id: str, name: str, source_code: str, 
                           description: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """Создать экземпляр кастомного инструмента"""
        return CustomToolkit(
            tool_id=tool_id,
            name=name,
            source_code=source_code,
            description=description,
            config=config or {}
        )
    
    @staticmethod
    def extract_functions_from_code(code: str) -> List[Dict[str, Any]]:
        """Извлечение функций из кода через AST"""
        tree = ast.parse(code)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node) or f"Функция {node.name}",
                    'parameters': CustomToolProvider._extract_parameters(node)
                }
                functions.append(func_info)
        
        return functions
    
    @staticmethod
    def _extract_parameters(func_node: ast.FunctionDef) -> Dict[str, Any]:
        """Простое извлечение параметров"""
        params = {
            'type': 'object',
            'properties': {},
            'required': []
        }
        
        for arg in func_node.args.args:
            if arg.arg != 'self':
                params['properties'][arg.arg] = {
                    'type': 'string',
                    'description': f'Параметр {arg.arg}'
                }
                params['required'].append(arg.arg)
        
        return params


class CustomToolkit(Toolkit):
    """✅ ПРАВИЛЬНАЯ интеграция с Agno Toolkit согласно плану"""
    
    def __init__(self, tool_id: str, name: str, source_code: str, 
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        
        self.tool_id = tool_id
        self.source_code = source_code
        self.config = config or {}
        
        # Валидация кода
        if not CustomToolProvider.validate_code(source_code):
            raise ValueError("Небезопасный код в кастомном инструменте")
        
        # ✅ ИЗВЛЕКАЕМ ФУНКЦИИ из кода ПЕРЕД инициализацией Toolkit
        functions = self._extract_and_create_functions()
        
        # ✅ ПРАВИЛЬНАЯ инициализация Agno Toolkit согласно плану
        super().__init__(
            name=name,
            tools=functions,  # ✅ Передаем функции в tools
            instructions=description,
            auto_register=True,  # ✅ Позволяем Agno автоматически зарегистрировать
            **kwargs
        )
        
        logger.info(f"✅ Создан кастомный toolkit '{name}' с {len(functions)} функциями")
    
    def _extract_and_create_functions(self) -> List[callable]:
        """✅ Создание и возврат функций из кода для Agno"""
        # Безопасное выполнение кода
        safe_globals = {
            '__builtins__': {
                'len': len, 'str': str, 'int': int, 'float': float,
                'bool': bool, 'list': list, 'dict': dict, 'tuple': tuple,
                'range': range, 'enumerate': enumerate, 'zip': zip,
                'min': min, 'max': max, 'sum': sum, 'abs': abs,
                'round': round, 'all': all, 'any': any,
                'Exception': Exception, 'ValueError': ValueError,
                'TypeError': TypeError, 'KeyError': KeyError,
            }
        }
        
        # Добавляем конфигурацию как доступную переменную
        safe_globals['config'] = self.config
        
        local_vars = {}
        try:
            exec(self.source_code, safe_globals, local_vars)
        except Exception as e:
            raise ValueError(f"Ошибка выполнения кода: {e}")
        
        # ✅ Возвращаем СПИСОК ФУНКЦИЙ для Agno
        functions = []
        for name, obj in local_vars.items():
            if callable(obj) and not name.startswith('_'):
                functions.append(obj)
        
        if not functions:
            raise ValueError("В коде не найдено ни одной функции")
        
        return functions


class ToolCache:
    """Кэш для инструментов с автоматической инвалидацией"""
    
    def __init__(self, ttl_seconds: int = 60):
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, tool_id: str) -> Optional[Any]:
        """Получить инструмент из кэша"""
        if tool_id in self._cache:
            tool, cached_time = self._cache[tool_id]
            if datetime.now() - cached_time < self._ttl:
                return tool
            else:
                # Удаляем устаревший элемент
                del self._cache[tool_id]
        return None
    
    def set(self, tool_id: str, tool: Any):
        """Сохранить инструмент в кэш"""
        self._cache[tool_id] = (tool, datetime.now())
    
    def invalidate(self, tool_id: str):
        """Инвалидировать конкретный инструмент"""
        self._cache.pop(tool_id, None)
        logger.info(f"Кэш инструмента '{tool_id}' инвалидирован")
    
    def invalidate_all(self):
        """Очистить весь кэш"""
        self._cache.clear()
        logger.info("Весь кэш инструментов очищен")
    
    def cleanup_expired(self) -> int:
        """Удалить устаревшие элементы из кэша"""
        current_time = datetime.now()
        expired_keys = [
            key for key, (_, cached_time) in self._cache.items()
            if current_time - cached_time >= self._ttl
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)


# Глобальный кэш для инструментов
tool_cache = ToolCache(ttl_seconds=60) 