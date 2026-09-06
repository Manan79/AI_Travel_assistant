import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.Tavily_tool import tavily_search
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
import asyncio
from dotenv import load_dotenv
# from datetime import date, timedelta
load_dotenv()

LLM = ChatOpenRouter(model = 'minimax/minimax-m2.7:free')

HOTEL_SELECTION_PROMPT = """
You are a hotel search agent.

Extract from the user's request:
- destination/location
- number of guests
- rooms = number of guests / 2 
- number of days (optional)
- preferences (budget, rating, amenities, etc.)

Rules:
- Do not ask for information already provided.
- Ask only for genuinely required missing information.
- Use the hotel search tool when enough information is available.
- Calculate the final budget like number of days x per night stay.
- Respect the user's preferences when ranking hotels.
- Never invent hotel details, prices, ratings, or availability.
- Return the best matching options concisely with name, price, url , rating, location, and key features.
- Suggest atmost 5 hotels
"""

async def hotel_search_llm(state):

    print("===== Hotel Agent Started =====")

    tools = await tavily_search()


    agent = create_agent(
        model = LLM,
        tools=  tools,
        system_prompt = HOTEL_SELECTION_PROMPT
    )

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Place: {state['destination_station']}\n"
                        f"Number of days: {state['duration']}\n"
                        f"Number of guests: {state['number_guest']}"
                    ),
                }
            ]
        }
    )
    print("===== Hotel Agent Result =====")
    # return (response["messages"][-1].content)
    return {'hotel_agent_response': str(response["messages"][-1].content)}






# if __name__ == "__main__":
#     asyncio.run(hotel_search_llm())