from langchain_core.tools import tool
import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from Travel_AI.tools.mcp_client import client
import asyncio

# Cache Tavily MCP tool discovery once per process so we do not reload
# the remote MCP server registry for every search request.
TAVILY_SEARCH_TOOL = None


async def _get_tavily_search_tool():
    global TAVILY_SEARCH_TOOL

    if TAVILY_SEARCH_TOOL is not None:
        return TAVILY_SEARCH_TOOL

    tools = await client.get_tools(server_name="Tavily_MCP")
    search_tool = next(
        (tool_obj for tool_obj in tools if tool_obj.name == "tavily_search"),
        None,
    )

    if search_tool is None:
        raise RuntimeError("Tavily MCP does not provide the tavily_search tool")

    TAVILY_SEARCH_TOOL = search_tool
    return search_tool


@tool
async def tavily_search(query: str, max_results: int = 5):
    """Search the web for hotels, places, and travel information."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be at least 1")

    search_tool = await _get_tavily_search_tool()

    results = []
    response = await search_tool.ainvoke(
        {"query": query.strip(), "max_results": max_results}
    )
    results_list = response[0].get("result", []) if response else []

    for i, r in enumerate(results_list, 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)


