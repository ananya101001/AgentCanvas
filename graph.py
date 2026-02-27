from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from crew.crew_logic import run_planning_crew, run_development_crew, run_qa_crew
from tools.file_writer import save_html_file

# ── State Definition ───────────────────────────────────────────
class GraphState(TypedDict):
    user_prompt:        str
    wireframe_and_copy: dict
    raw_code:           str
    qa_feedback:        List[str]
    iteration_count:    int
    final_status:       str

# ── Node Functions ─────────────────────────────────────────────

def planning_node(state: GraphState) -> GraphState:
    print("\n🧠 PM Agent is planning the page...")
    wireframe = run_planning_crew(state["user_prompt"])
    return {**state, "wireframe_and_copy": wireframe}


def development_node(state: GraphState) -> GraphState:
    print(f"\n💻 Developer Agent is writing code (iteration {state['iteration_count'] + 1})...")
    code = run_development_crew(
        wireframe=state["wireframe_and_copy"],
        qa_feedback=state["qa_feedback"]
    )
    return {
        **state,
        "raw_code": code,
        "iteration_count": state["iteration_count"] + 1
    }


def qa_node(state: GraphState) -> GraphState:
    print("\n🔍 QA Agent is reviewing the code...")
    feedback = run_qa_crew(state["raw_code"])

    if feedback.upper() == "PASS":
        return {**state, "qa_feedback": [], "final_status": "Success"}
    else:
        # Split numbered bug list into a clean Python list
        bugs = [line.strip() for line in feedback.split("\n") if line.strip()]
        return {**state, "qa_feedback": bugs, "final_status": "Pending"}


def output_node(state: GraphState) -> GraphState:
    print(f"\n✅ Saving final page... Status: {state['final_status']}")
    save_html_file(state["raw_code"])
    return state


# ── Conditional Router (The QA Loop) ──────────────────────────
def qa_router(state: GraphState) -> str:
    if state["final_status"] == "Success":
        print("✅ QA Passed! Moving to output.")
        return "output"

    elif state["iteration_count"] >= 3:
        print("⚠️  Max iterations reached. Saving best available code.")
        state["final_status"] = "Failed_QA"
        return "output"

    else:
        print(f"🔁 Bugs found. Sending back to Developer. (Attempt {state['iteration_count']}/3)")
        return "developer"


# ── Build the Graph ────────────────────────────────────────────
def build_graph():
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("planner",   planning_node)
    graph.add_node("developer", development_node)
    graph.add_node("qa",        qa_node)
    graph.add_node("output",    output_node)

    # Define edges (the flow)
    graph.set_entry_point("planner")
    graph.add_edge("planner",   "developer")
    graph.add_edge("developer", "qa")

    # The conditional router — this is the QA loop
    graph.add_conditional_edges(
        "qa",           # from this node
        qa_router,      # use this function to decide
        {
            "developer": "developer",   # loop back
            "output":    "output"       # move forward
        }
    )

    graph.add_edge("output", END)

    return graph.compile()