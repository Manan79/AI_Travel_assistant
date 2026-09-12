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



load_dotenv()


class MainWorkflow(TypedDict):
    user_query: str
    boarding_station: str
    destination_station: str
    number_guest: int
    duration: int
    itinerary: str
    messages: Annotated[list, add_messages]
    country: str
    brain_agent_response: str
