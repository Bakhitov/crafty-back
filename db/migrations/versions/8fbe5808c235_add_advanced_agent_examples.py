"""
Добавить примеры агентов с новыми возможностями:
- Tool Hooks (middleware для инструментов)
- Response Models (структурированные ответы) 
- Team Agents (команды агентов)

Демонстрирует все три доработки для 100% поддержки конфигураций Agno.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision = '8fbe5808c235'
down_revision = 'f3a8b9c2d1e4'
branch_labels = None
depends_on = None


def upgrade():
    """Добавить примеры агентов с продвинутыми возможностями"""
    
    # 1. Агент с Tool Hooks - Production-ready конфигурация
    op.execute("""
        INSERT INTO agents (
            agent_id, 
            name, 
            description, 
            model_config,
            agent_config,
            is_public
        ) VALUES (
            'production_assistant',
            'Production ассистент с мониторингом',
            'Агент с полным набором middleware для production использования',
            '{
                "provider": "openai",
                "id": "gpt-4.1-mini-2025-04-14",
                "temperature": 0.3,
                "max_tokens": 2000
            }',
            '{
                "tool_hooks": ["logging", "validation", "rate_limiting", "metrics", "error_recovery"],
                "tool_call_limit": 15,
                "show_tool_calls": true,
                "storage": {
                    "table_name": "sessions"
                },
                "history": {
                    "add_history_to_messages": true,
                    "num_history_runs": 5
                },
                "markdown": true,
                "add_datetime_to_instructions": true,
                "debug_mode": false,
                "monitoring": true
            }',
            true
        );
    """)
    
    # 2. Агент с Response Model - Структурированные ответы
    op.execute("""
        INSERT INTO agents (
            agent_id,
            name, 
            description,
            model_config,
            agent_config,
            goal,
            expected_output,
            is_public
        ) VALUES (
            'task_manager',
            'Менеджер задач',
            'Агент для управления задачами с структурированными ответами',
            '{
                "provider": "openai",
                "id": "gpt-4.1-2025-04-14",
                "temperature": 0.1
            }',
            '{
                "response_model": "TaskResult",
                "structured_outputs": true,
                "parse_response": true,
                "tool_hooks": ["logging", "validation"],
                "storage": {
                    "table_name": "sessions"
                },
                "markdown": false,
                "add_datetime_to_instructions": true
            }',
            'Создавать, обновлять и отслеживать задачи пользователя',
            'Структурированный JSON с полями success, message, status, data, timestamp',
            true
        );
    """)
    
    # 3. Агент с командой - Team Leader
    op.execute("""
        INSERT INTO agents (
            agent_id,
            name,
            description, 
            model_config,
            agent_config,
            role,
            is_public
        ) VALUES (
            'research_team_leader',
            'Лидер исследовательской команды',
            'Координирует работу команды специалистов для комплексных исследований',
            '{
                "provider": "openai",
                "id": "gpt-4.1-2025-04-14",
                "temperature": 0.5
            }',
            '{
                "team": ["web_agent", "finance_agent", "agno_assist"],
                "team_data": {
                    "project_type": "research",
                    "coordination_mode": "sequential"
                },
                "add_transfer_instructions": true,
                "team_response_separator": "\\n---\\n",
                "tool_hooks": ["logging", "metrics"],
                "storage": {
                    "table_name": "sessions"
                },
                "history": {
                    "add_history_to_messages": true,
                    "num_history_runs": 10
                },
                "markdown": true,
                "add_datetime_to_instructions": true
            }',
            'team_leader',
            true
        );
    """)
    
    # 4. Комбинированный агент - Все возможности вместе
    op.execute("""
        INSERT INTO agents (
            agent_id,
            name,
            description,
            model_config, 
            agent_config,
            goal,
            expected_output,
            role,
            is_public
        ) VALUES (
            'ultimate_assistant',
            'Универсальный ассистент',
            'Демонстрация всех возможностей: hooks, response models, team coordination',
            '{
                "provider": "openai",
                "id": "gpt-4.1-2025-04-14",
                "temperature": 0.4,
                "max_tokens": 4000
            }',
            '{
                "response_model": "QuestionAnswer",
                "structured_outputs": true,
                "tool_hooks": ["logging", "cache_5min", "validation", "metrics"],
                "team": ["web_agent", "finance_agent"],
                "team_data": {
                    "specialization": "comprehensive_assistance"
                },
                "memory": {
                    "enabled": true,
                    "table_name": "user_memories",
                    "delete_memories": false
                },
                "knowledge": {
                    "enabled": true,
                    "type": "url",
                    "urls": ["https://docs.agno.com"]
                },
                "storage": {
                    "table_name": "sessions"
                },
                "history": {
                    "add_history_to_messages": true,
                    "num_history_runs": 7
                },
                "reasoning": {
                    "enabled": true,
                    "min_steps": 2,
                    "max_steps": 5
                },
                "stream": true,
                "stream_intermediate_steps": true,
                "markdown": true,
                "add_datetime_to_instructions": true,
                "enable_agentic_memory": true,
                "add_references": true,
                "search_knowledge": true
            }',
            'Предоставлять максимально полные и структурированные ответы с использованием команды и всех доступных инструментов',
            'JSON объект QuestionAnswer с полями question, answer, confidence, sources, category',
            'universal_assistant',
            true
        );
    """)


def downgrade():
    """Удалить примеры агентов"""
    op.execute("""
        DELETE FROM agents WHERE agent_id IN (
            'production_assistant',
            'task_manager', 
            'research_team_leader',
            'ultimate_assistant'
        );
    """) 