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
async def workflow_invoke(user_query: str, thread_id: str):
    workflow = build_workflow()
    initial_state = {"user_query": user_query, "messages": []}

    graph_config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await workflow.ainvoke(initial_state, config=graph_config)
    return result

# if __name__ == "__main__":
#     asyncio.run(workflow_invoke(user_query = "Hi Plan a solo trip for 5 days from New Delhi to Mumbai",
#     thread_id = "45"
#     ))

# ====== Enable Streaming ========
# async def workflow_invoke(user_query: str , config: str):
#     workflow = build_workflow()
   
#     initial_state = {
#         "user_query": user_query,
#         "messages": [],
#     }
#     # async for chunk in workflow.astream(
#     #     initial_state,
#     #     config=config,
#     #     stream_mode="messages",
#     # ):
#     #    message, metadata = chunk
#     #    print (message.content, end="", flush=True)
#     configs = {
#         "configurable": {
#             "thread_id": config
#         }
#     }
    # result = await workflow.ainvoke(initial_state, config=configs)