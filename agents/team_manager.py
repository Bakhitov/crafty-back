"""
Менеджер команд агентов для динамических агентов.
Позволяет создавать команды через agent_id ссылки.
"""

from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from agno.agent import Agent
from agno.utils.log import log_warning, log_debug

from agents.agent_cache import agent_cache


class TeamManager:
    """Управление командами динамических агентов"""
    
    def __init__(self, db: Session):
        self.db = db
        self._team_cache: Dict[str, List[Agent]] = {}
    
    def build_team(
        self, 
        team_config: List[str], 
        user_id: Optional[str] = None,
        debug_mode: bool = True
    ) -> List[Agent]:
        """
        Создать команду агентов по списку agent_id
        
        Args:
            team_config: Список agent_id для команды
            user_id: ID пользователя для контекста
            debug_mode: Режим отладки
            
        Returns:
            Список Agent объектов
        """
        if not team_config:
            return []
        
        # Кэш-ключ для команды
        cache_key = f"{sorted(team_config)}:{user_id}:{debug_mode}"
        
        if cache_key in self._team_cache:
            log_debug(f"Team cache hit: {cache_key}")
            return self._team_cache[cache_key]
        
        team_agents = []
        for agent_id in team_config:
            try:
                # Используем функцию get_agent с отложенным импортом
                # чтобы избежать циклических импортов
                agent = self._get_agent_safe(
                    agent_id=agent_id,
                    user_id=user_id,
                    debug_mode=debug_mode
                )
                if agent:
                    team_agents.append(agent)
            except Exception as e:
                log_warning(f"Failed to load team member {agent_id}: {e}")
                continue
        
        # Кэшируем команду только если она не пустая
        if team_agents:
            self._team_cache[cache_key] = team_agents
            log_debug(f"Team cached: {len(team_agents)} agents for key {cache_key}")
        
        return team_agents
    
    def _get_agent_safe(self, agent_id: str, user_id: Optional[str], debug_mode: bool) -> Optional[Agent]:
        """
        Безопасное получение агента с избежанием циклических импортов
        """
        try:
            # Отложенный импорт для избежания циклических зависимостей
            from agents.selector import get_agent
            return get_agent(
                agent_id=agent_id,
                user_id=user_id,
                debug_mode=debug_mode,
                db=self.db
            )
        except ImportError as e:
            log_warning(f"Import error when loading agent {agent_id}: {e}")
            return None
        except Exception as e:
            log_warning(f"Error loading agent {agent_id}: {e}")
            return None
    
    def invalidate_team_cache(self, agent_id: str):
        """
        Инвалидировать кэш команд при изменении агента
        
        Args:
            agent_id: ID агента, который изменился
        """
        keys_to_remove = []
        for cache_key in self._team_cache.keys():
            # Проверяем, содержит ли ключ кэша измененный agent_id
            team_agents_str = cache_key.split(':')[0]  # "['agent1', 'agent2']"
            if agent_id in team_agents_str:
                keys_to_remove.append(cache_key)
        
        for key in keys_to_remove:
            del self._team_cache[key]
            log_debug(f"Invalidated team cache key: {key}")
    
    def clear_cache(self):
        """Очистить весь кэш команд"""
        cleared_count = len(self._team_cache)
        self._team_cache.clear()
        log_debug(f"Cleared {cleared_count} team cache entries")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Получить статистику кэша команд"""
        return {
            "cached_teams": len(self._team_cache),
            "total_agents_cached": sum(len(team) for team in self._team_cache.values())
        }


# Глобальный кэш менеджеров команд по сессии БД
_team_managers: Dict[int, TeamManager] = {}


def get_team_manager(db: Session) -> TeamManager:
    """
    Получить Team Manager для сессии БД
    
    Args:
        db: Сессия базы данных
        
    Returns:
        Экземпляр TeamManager для данной сессии
    """
    db_id = id(db)
    if db_id not in _team_managers:
        _team_managers[db_id] = TeamManager(db)
        log_debug(f"Created new TeamManager for DB session {db_id}")
    return _team_managers[db_id]


def invalidate_team_caches(agent_id: str):
    """
    Инвалидировать кэши команд во всех менеджерах
    
    Args:
        agent_id: ID агента, который изменился
    """
    for manager in _team_managers.values():
        manager.invalidate_team_cache(agent_id)


def clear_all_team_caches():
    """Очистить все кэши команд"""
    for manager in _team_managers.values():
        manager.clear_cache()


def get_all_cache_stats() -> Dict[str, Dict[str, int]]:
    """Получить статистику всех кэшей команд"""
    stats = {}
    for db_id, manager in _team_managers.items():
        stats[f"db_session_{db_id}"] = manager.get_cache_stats()
    return stats 