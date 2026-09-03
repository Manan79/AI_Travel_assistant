import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.Tavily_tool import tavily_search
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
import asyncio
from dotenv import load_dotenv
from datetime import date, timedelta
load_dotenv()

LLM = ChatOpenRouter(model = 'minimax/minimax-m2.7:free')

HOTEL_SELECTION_PROMPT = """
You are a hotel search agent.

Extract from the user's request:
- destination/location
- number of guests
- rooms = number of guests / 2 
- preferences (budget, rating, amenities, etc.)

Rules:
- Do not ask for information already provided.
- Ask only for genuinely required missing information.
- Use the hotel search tool when enough information is available.
- Respect the user's preferences when ranking hotels.
- Never invent hotel details, prices, ratings, or availability.
- Return the best matching options concisely with name, price, url , rating, location, and key features.
- Suggest atmost 5 hotels
"""

async def hotel_search_llm():
    tools = await tavily_search()


    agent = create_agent(
        model = LLM,
        tools=  tools,
        system_prompt = HOTEL_SELECTION_PROMPT
    )

    response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": f"Hi, I am looking for the hotels in Mysore near railway station for 1 person "}]},
)
    print("===== FINAL MESSAGE =====")
    print(response["messages"][-1].content)





if __name__ == "__main__":
    asyncio.run(hotel_search_llm())