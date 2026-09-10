from langgraph.graph import END, START, StateGraph
import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from langsmith import traceable
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.prebuilt.tool_node import tools_condition
from Travel_AI.src.initial_agent import processing_query
from Travel_AI.src.react_agent import react_agent, all_tools
from Travel_AI.agents.iternary_agent import iternary_generator
from Travel_AI.src.main_state import MainWorkflow
from langgraph.checkpoint.memory import InMemorySaver
import asyncio


def build_workflow():
    graph = StateGraph(MainWorkflow)
    graph.add_node("Query Processor", processing_query)
    graph.add_node("Brain Agent", react_agent)
    graph.add_node("tools", ToolNode(all_tools))
    graph.add_node("Iternary_agent", iternary_generator)

    graph.add_edge(START, "Query Processor")
    graph.add_edge("Query Processor", "Brain Agent")

    graph.add_conditional_edges(
        "Brain Agent",
        tools_condition,
        {
            "tools": "tools",
            "__end__": "Iternary_agent",
        },
    )

    graph.add_edge("tools", "Brain Agent")
    graph.add_edge("Iternary_agent", END)

    checkpointer = InMemorySaver()
    return graph.compile(checkpointer=checkpointer)


@traceable
async def workflow_invoke():
    workflow = build_workflow()
    config = {"configurable": {"thread_id": "10"}}

    initial_state = {
        "user_query": "Hi, plan a trip from Mumbai to Australia for 5 days for 2 person starting",
        "messages": [],
    }

    async for chunk in workflow.astream(
        initial_state,
        config=config,
        stream_mode="messages",
    ):
        message, metadata = chunk
        print(message.content, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(workflow_invoke())
    # graph = graph.compile()
    # graph_image = graph.get_graph().draw_mermaid_png()

    # with open("travel_ai_graph.png", "wb") as f:
    #     f.write(graph_image)

