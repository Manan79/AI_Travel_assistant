from langchain_core.tools import tool
import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from Travel_AI.tools.mcp_client import client
import asyncio

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

    results = []
    response = await search_tool.ainvoke(
        {"query": query.strip(), "max_results": max_results}
    )
    results_list = response[0].get("result", []) if response else []

    for i, r in enumerate(results_list, 1):
        title = r.get("title", "Unknown")
        url = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)


