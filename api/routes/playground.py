from agno.playground import Playground

from agents.agno_assist import get_agno_assist
from agents.finance_agent import get_finance_agent
from agents.demo_agent import get_demo_agent

######################################################
## Routes for the Playground Interface
######################################################

# Get Agents to serve in the playground
demo_agent = get_demo_agent(debug_mode=True)
agno_assist = get_agno_assist(debug_mode=True)
finance_agent = get_finance_agent(debug_mode=True)

# Create a playground instance
playground = Playground(agents=[demo_agent, agno_assist, finance_agent])

# Get the router for the playground
playground_router = playground.get_async_router()
