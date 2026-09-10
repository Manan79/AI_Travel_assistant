import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.Tavily_tool import tavily_search
from langchain_openrouter import ChatOpenRouter
import asyncio
import json
from dotenv import load_dotenv
from typing import List , Optional
from pydantic import BaseModel , Field, model_validator
load_dotenv()

LLM = ChatOpenRouter(model = 'gpt-4o-mini')

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

    @model_validator(mode="before")
    @classmethod
    def decode_json_lists(cls, values):
        if not isinstance(values, dict):
            return values

        for field_name in ("places_in_destination", "nearby_places"):
            field_value = values.get(field_name)
            if isinstance(field_value, str):
                try:
                    values[field_name] = json.loads(field_value)
                except json.JSONDecodeError:
                    pass
        return values

async def place_finder_llm(state):

    print("===== Place Finder Started =====")

    tools = await tavily_search()

    result = await tools[0].ainvoke({
        "query": state['destination_station']
    })
    structured_llm = LLM.with_structured_output(PlaceFinderOutput)

    structured_result = await structured_llm.ainvoke(
        f"""
        Extract place information from the following search results
        and fill the output schema.

        SEARCH RESULTS:
        {result}

        Number of days:
        {state['duration']}
        """
    )

    return {"place_selection" : str(structured_result)}
    




