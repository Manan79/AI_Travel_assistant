import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.flight_tool import avaitation_tool
from Travel_AI.tools.railway_tool import get_train_details
from Travel_AI.tools.Tavily_tool import tavily_search
import asyncio


async def all_tools():
    tavily_tool = await tavily_search()
    avaitation = await avaitation_tool()
    railway = [get_train_details]

    all_tools = tavily_tool + avaitation + railway
    print(all_tools)


if __name__ == "__main__":
    asyncio.run(all_tools())