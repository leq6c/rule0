from langgraph.graph.graph import Graph
from rule0.agents import AdminAgent, JudgeAgent, ParticipantAgent
from rule0.orchestrator.state import State


class AgentConfig:
    name: str
    role: str
    basis: str
    verbal: str


class Builder:
    def __init__(self, topic: str, agents: list[AgentConfig], prompts: dict[str, str]):
        self.topic = topic
        self.agents = agents
        self.prompts = prompts
        self.debug = False

    def router(state: State) -> str:
        return "end" if state.exited else state.next_speaker

    def admin_router(state: State) -> str:
        return "end" if state.exited else "judge"

    def build(self) -> Graph:
        admin_agent = AdminAgent(self.debug)
        judge_agent = JudgeAgent(self.debug)

        participants = []
        for agent in self.agents:
            participants.append(ParticipantAgent(agent.name, agent.basis, self.debug))

        workflow = Graph()

        workflow.add_node("admin", admin_agent.run)
        workflow.add_node("judge", judge_agent.run)
        for participant in participants:
            workflow.add_node(participant.name, participant.run)
        workflow.add_node("end", lambda state: state)

        workflow.add_conditional_edges("admin", self.admin_router)
        workflow.add_conditional_edges("judge", self.router)
        for participant in participants:
            workflow.add_edge(participant.name, "judge")

        workflow.set_entry_point("admin")
        workflow.set_finish_point("end")

        return workflow
