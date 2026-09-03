import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.Tavily_tool import tavily_search
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
import asyncio
from dotenv import load_dotenv
from typing import List , Optional
from pydantic import BaseModel , Field
from datetime import date, timedelta
load_dotenv()

LLM = ChatOpenRouter(model = 'minimax/minimax-m2.7:free')

class TransportOption(BaseModel):
    mode: str = Field(description="Bus, train, taxi, cab, etc.")
    travel_time_minutes: Optional[int] = None
    one_way_cost_inr: Optional[float] = None
    round_trip_cost_inr: Optional[float] = None


class Place(BaseModel):
    name: str
    category: str
    description: str
    distance_km: Optional[float] = None
    transport: List[TransportOption] = []


class PlaceFinderOutput(BaseModel):
    destination: str
    places_in_destination: List[Place]
    nearby_places: List[Place]

async def place_finder_llm():
    tools = await tavily_search()

    result = await tools[0].ainvoke({
        "query": "top tourist places in Amritsar"
    })
    structured_llm = LLM.with_structured_output(PlaceFinderOutput)

    structured_result = await structured_llm.ainvoke(
        f"""
        Extract place information from the following search results
        and fill the output schema.

        SEARCH RESULTS:
        {result}
        """
    )

    print(structured_result)





if __name__ == "__main__":
    asyncio.run(place_finder_llm())