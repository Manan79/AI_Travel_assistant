import asyncio
from .mcp_client import client

async def tavily_search():
    """ Search tool used to seach information accross the web  """

    tools = await client.get_tools()

    search_tool = next(
        t for t in tools
            if t.name == 'tavily_search'
    )

    return [search_tool] 

# if __name__ == "__main__":
#     asyncio.run(tavily_search())