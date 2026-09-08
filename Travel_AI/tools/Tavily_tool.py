from langchain_core.tools import tool

from .mcp_client import client

@tool
async def tavily_search(query: str, max_results: int = 5):
    """Search the web for hotels, places, and travel information."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be at least 1")

    tools = await client.get_tools(server_name="Tavily_MCP")
    search_tool = next(
        (tool for tool in tools if tool.name == "tavily_search"),
        None,
    )

    if search_tool is None:
        raise RuntimeError("Tavily MCP does not provide the tavily_search tool")
    print("Tavily Tool has been called")
    return await search_tool.ainvoke(
        {"query": query.strip(), "max_results": max_results}
    )