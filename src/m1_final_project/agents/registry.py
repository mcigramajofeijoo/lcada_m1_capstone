from m1_final_project.agents.fact_agent.build import build_fact_agent
from m1_final_project.agents.poster_agent.build import build_poster_agent


class AgentRegistry:
    def __init__(self):
        self.fact_agent = None
        self.poster_agent = None

    def build(self):
        self.fact_agent = build_fact_agent()
        self.poster_agent = build_poster_agent()


agent_registry = AgentRegistry()
