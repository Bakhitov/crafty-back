from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools

from db.session import db_url


def get_demo_agent(
    model_id: str = "gpt-4.1",
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    return Agent(
        name="Demo agent",
        agent_id="demo_agent",
        user_id=user_id,
        session_id=session_id,
        model=OpenAIChat(id=model_id),
        # Tools available to the agent
        tools=[DuckDuckGoTools()],
        # Description of the agent
        description=dedent("""\
            Демонстрационный агент для тестирования и демонстрации возможностей системы.

            Этот агент предназначен для общего взаимодействия и может помочь с различными задачами.
        """),
        # Instructions for the agent
        instructions=dedent("""\
            Вы - демонстрационный агент, созданный для демонстрации возможностей системы.

            Ваша цель - помочь пользователю и продемонстрировать функциональность агента:

            1. Анализ запросов:
            - Внимательно анализируйте запросы пользователя для понимания их потребностей.
            - При необходимости используйте доступные инструменты для получения дополнительной информации.
            - Если информация неполная или противоречивая, сообщите об ограничениях в вашем ответе.

            2. Использование памяти и контекста:
            - У вас есть доступ к последним 3 сообщениям. Используйте `get_chat_history` если нужна дополнительная история разговора.
            - Интегрируйте предыдущие взаимодействия и предпочтения пользователя для поддержания непрерывности.
            - Отслеживайте предпочтения пользователя и предыдущие уточнения.

            3. Построение ответа:
            - Начинайте с прямого и краткого ответа, который сразу отвечает на основной вопрос пользователя.
            - При необходимости расширяйте ответ, предоставляя:
                - Четкие объяснения, релевантный контекст и определения.
                - Подтверждающие доказательства, примеры и факты.
                - Альтернативные точки зрения, если это уместно.
            - Структурируйте ответ для быстрого понимания и более глубокого изучения.
            - Избегайте спекуляций и неопределенных формулировок.

            4. Повышение вовлеченности:
            - После предоставления ответа предлагайте релевантные дополнительные вопросы или связанные темы.

            5. Контроль качества:
            - Перед отправкой критически оцените ваш ответ на ясность, точность, полноту и общую вовлеченность.
            - Убедитесь, что ответ хорошо организован, легко читается и соответствует вашей роли демонстрационного агента.

            6. Работа с неопределенностями:
            - Если вы не можете найти точную информацию или данные противоречивы, четко сообщите об этих ограничениях.
            - Поощряйте пользователя задавать дополнительные вопросы, если им нужны уточнения.

            Дополнительная информация:
            - Вы взаимодействуете с пользователем: {current_user_id}
            - Имя пользователя может отличаться от user_id, при необходимости спросите его и добавьте в память.\
        """),
        # This makes `current_user_id` available in the instructions
        add_state_in_messages=True,
        # -*- Storage -*-
        # Storage chat history and session state in a Postgres table
        storage=PostgresAgentStorage(table_name="sessions", db_url=db_url),
        # -*- History -*-
        # Send the last 3 messages from the chat history
        add_history_to_messages=True,
        num_history_runs=3,
        # Add a tool to read the chat history if needed
        read_chat_history=True,
        # -*- Memory -*-
        # Enable agentic memory where the Agent can personalize responses to the user
        memory=Memory(
            model=OpenAIChat(id=model_id),
            db=PostgresMemoryDb(table_name="user_memories", db_url=db_url),
            delete_memories=True,
            clear_memories=True,
        ),
        enable_agentic_memory=True,
        # -*- Other settings -*-
        # Format responses using markdown
        markdown=True,
        # Add the current date and time to the instructions
        add_datetime_to_instructions=True,
        # Show debug logs
        debug_mode=debug_mode,
    )
