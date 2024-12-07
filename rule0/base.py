from langgraph.graph.graph import Graph

from .agents import AdminAgent, JudgeAgent, ParticipantAgent
from .prompts.loader import load_prompt
from .world.state import State


def router(state: State) -> str:
    return "end" if state.exited else state.next_speaker


def admin_router(state: State) -> str:
    return "end" if state.exited else "judge"


class BaseAgent:
    def __init__(self):
        pass

    def run(self, debug: bool = False):
        # agents
        admin = AdminAgent(debug)
        judge = JudgeAgent(debug)

        participants = []
        """
        for i in range(2):
            participants.append(ParticipantAgent(f"name_{i}", "law"))
        """
        participants.append(ParticipantAgent("name_1", "I like pizza", debug))
        participants.append(ParticipantAgent("name_2", "I like sushi", debug))
        for i in range(3):
            participants.append(ParticipantAgent(f"voter_{i+1}", "equal", debug))

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
        initial_note = load_prompt("state", "default")
        state = State(note=initial_note)

        # Run the workflow
        state = chain.invoke(state, debug=False, config={"recursion_limit": 500})

        return state
