import asyncio
import sys
from pathlib import Path
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from Travel_AI.agents.hotel_agent import hotel_search_llm
from Travel_AI.agents.place_finder import place_finder_llm
from Travel_AI.agents.route_agent import route_llm
from Travel_AI.agents.iternary_agent import iternary_agent
from Travel_AI.src.initial_agent import processing_query

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



def build_workflow():
    graph = StateGraph(MainWorkflow)
    graph.add_node("Query Processor", processing_query)
    graph.add_node("Hotel Searching Agent", hotel_search_llm)
    graph.add_node("Place Finder Agent", place_finder_llm)
    graph.add_node("Route Decider Agent", route_llm)
    graph.add_node("Itinerary Generator Agent", iternary_agent)
    graph.add_edge(START, "Query Processor")
    graph.add_edge("Query Processor", "Hotel Searching Agent")
    graph.add_edge("Query Processor", "Place Finder Agent")
    graph.add_edge("Query Processor", "Route Decider Agent")
    graph.add_edge("Route Decider Agent", "Itinerary Generator Agent")
    graph.add_edge("Place Finder Agent", "Itinerary Generator Agent")
    graph.add_edge("Hotel Searching Agent", "Itinerary Generator Agent")
    graph.add_edge("Itinerary Generator Agent", END)
    checkpointer = InMemorySaver()
    
    return graph.compile(checkpointer= checkpointer)


async def workflow_invoke():
    
    workflow = build_workflow()
    config = {"configurable": {"thread_id": "3"}}
    result = await workflow.ainvoke({
            "user_query": "Hi I planning a trip of USA from India alone for 7 days",
        },
            config = config
        )

    print(result['itinerary'])

if __name__ == "__main__":
    asyncio.run(workflow_invoke())
