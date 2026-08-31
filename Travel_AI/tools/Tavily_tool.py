import asyncio
# from dotenv import load_dotenv
# import os
from mcp_client import client


async def tavily_search():

    tools = await client.get_tools()

    search_tool = next(
        t for t in tools
            if t.name == 'tavily_search'
    )

    result = await search_tool.ainvoke({'query': "latest AI developments"})

    print(result)

if __name__ == "__main__":
    asyncio.run(tavily_search())