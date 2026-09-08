import asyncio
import sys
from pathlib import Path
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from typing import Annotated , List
from langgraph.graph import add_messages
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.prebuilt.tool_node import tools_condition
from Travel_AI.src.initial_agent import processing_query
from Travel_AI.src.react_agent import react_agent, all_tools
from Travel_AI.agents.iternary_agent import iternary_agent


load_dotenv()


class MainWorkflow(TypedDict):
    user_query: str
    boarding_station: str
    destination_station: str
    number_guest: int
    duration: int
    transport: str
    place_selection: str
    hotel_agent_response: str
    route_selection: str
    itinerary: str
    messages: Annotated[list, add_messages]



def build_workflow():
    graph = StateGraph(MainWorkflow)
    graph.add_node("Query Processor", processing_query)
    graph.add_node("Brain Agent" , react_agent)
    graph.add_node("tools", ToolNode(all_tools))
    graph.add_node("Iternary_agent" , iternary_agent)


    graph.add_edge(START , "Query Processor")
    graph.add_edge("Query Processor" , "Brain Agent")

    graph.add_conditional_edges(
    "Brain Agent",
    tools_condition,  # Routes to "tools" or "__end__"
    {
        "tools": "tools",
        "__end__": "Iternary_agent"
    }
)   
    # graph.add_edge("Brain Agent" , "Iternary_agent")
    graph.add_edge("tools", "Brain Agent")
    graph.add_edge("Iternary_agent" , END)


    checkpointer = InMemorySaver()
    
    return graph.compile(checkpointer= checkpointer)


async def workflow_invoke():
    
    workflow = build_workflow()
    config = {"configurable": {"thread_id": "3"}}
    result = await workflow.ainvoke({
            "user_query": "Hi, Plan a trip guide for from Mumbai to Switzerland for 5 days for 2 persons. ",
        },
            config = config
        )

    print(result['itinerary'])

if __name__ == "__main__":
    asyncio.run(workflow_invoke())
    # graph = graph.compile()
    # graph_image = graph.get_graph().draw_mermaid_png()

    # with open("travel_ai_graph.png", "wb") as f:
    #     f.write(graph_image)

