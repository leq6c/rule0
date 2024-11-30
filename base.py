from .prompts.loader import load_prompt
from .agents import AdminAgent, JudgeAgent, ParticipantAgent
from .agents.state import State
from .prompts.loader import load_prompt

from langgraph.graph.graph import Graph

def router(state: State) -> str:
    return state.next_speaker

def admin_router(state: State) -> str:
    return "end" if state.exited else "judge"

class BaseAgent:
    def __init__(self):
        pass

    def run(self):
        # agents
        admin = AdminAgent()
        judge = JudgeAgent()

        participants = []
        for i in range(1):
            participants.append(ParticipantAgent(f"name_{i}", "law"))
        
        workflow = Graph()

        # nodes
        workflow.add_node("admin", admin.run)
        workflow.add_node("judge", judge.run)
        for participant in participants:
            workflow.add_node(participant.name, participant.run)
        workflow.add_node("end", lambda state: state)
        
        # edges
        workflow.add_conditional_edges("admin", admin_router)
        workflow.add_conditional_edges("judge", router)
        for participant in participants:
            workflow.add_edge(participant.name, "judge")
        
        # set entry and finish points
        workflow.set_entry_point("admin")
        workflow.set_finish_point("end")
        
        # Compile the workflow
        chain = workflow.compile()

        # Load initial note
        initial_note = load_prompt("state/default.md")
        state = State(note=initial_note)

        # Run the workflow
        state = chain.invoke(state)

        return state