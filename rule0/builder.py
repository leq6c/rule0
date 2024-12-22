from typing import Generator

from langgraph.graph.graph import Graph

from rule0.agents import AdminAgent, JudgeAgent, ParticipantAgent
from rule0.orchestrator.state import State
from rule0.prompts.note import NotePrompt


class AgentConfig:
    def __init__(self, name: str, role: str, basis: str, verbal: str):
        self.name = name
        self.role = role
        self.basis = basis
        self.verbal = verbal
    
    @staticmethod
    def decode(data: dict) -> "AgentConfig":
        return AgentConfig(data["name"], data["role"], data["basis"], data["verbal"])

class Log:
    def __init__(self, sender: str, action: str, message: str):
        self.sender = sender
        self.action = action
        self.message = message
    
    def __repr__(self) -> str:
        return f"{self.sender}: {self.action} {self.message}"

class Builder:
    def __init__(self, topic: str, agents: list[AgentConfig], prompts: dict[str, str], debug: bool = False):
        self.topic = topic
        self.agents = agents
        self.prompts = prompts
        self.debug = debug

    def router(self, state: State) -> str:
        return "end" if state.exited else state.next_speaker

    def admin_router(self, state: State) -> str:
        return "end" if state.exited else "judge"

    def build_workflow(self) -> Graph:
        admin_agent = AdminAgent(self.debug)
        judge_agent = JudgeAgent(self.debug)

        participants = []
        for agent in self.agents:
            participants.append(ParticipantAgent(agent.name, agent.role, agent.basis, self.debug))

        workflow = Graph()

        # default nodes
        workflow.add_node("admin", admin_agent.run)
        workflow.add_node("judge", judge_agent.run)

        # user defined participant nodes
        for participant in participants:
            workflow.add_node(participant.name, participant.run)

        # end node to finish the workflow
        workflow.add_node("end", lambda state: state)

        # default edges
        workflow.add_conditional_edges("admin", self.admin_router)
        workflow.add_conditional_edges("judge", self.router)

        # connecting participant nodes to judge node
        for participant in participants:
            workflow.add_edge(participant.name, "judge")

        # set entry and finish points
        workflow.set_entry_point("admin")
        workflow.set_finish_point("end")

        return workflow
    
    def state_to_result(self, state: State) -> list[Log]:
        logs = []
        for action in state.history:
            logs.append(Log(action.sender, action.action.value, action.args))
        return logs
    
    def run(self) -> Generator[list[Log], None, None]:
        workflow = self.build_workflow()
        chain = workflow.compile()
        note_prompt = NotePrompt()
        note = note_prompt.apply(self.topic, self.agents)
        state = State(note=note)
        last_result_str = ""
        for _ in chain.stream(state, stream_mode="updates", debug=self.debug, config={"recursion_limit": 500}):
            result = self.state_to_result(state)
            result_str = "\n".join([repr(log) for log in result])
            if result_str != last_result_str:
                yield result
                last_result_str = result_str
