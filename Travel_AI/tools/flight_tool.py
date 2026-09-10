<<<<<<< HEAD
import re
from datetime import datetime

from langchain_core.tools import tool
=======
from langchain_core.tools import tool

>>>>>>> main
from .mcp_client import client

# ==========================================
# AviationStack MCP tools
# ==========================================

<<<<<<< HEAD
aviation_tools = {}


async def initialize_aviation_tools():
    global aviation_tools

    if aviation_tools:
        return

    # Load only AviationStack.
    # Tavily and Weather will not be initialized here.
    tools = await client.get_tools(
        server_name="Aviationstack_MCP"
    )

    aviation_tools = {
        tool.name: tool
        for tool in tools
    }

    if not aviation_tools:
        raise RuntimeError(
            "AviationStack MCP connected but "
            "returned no tools."
        )


async def aviation_mcp_call(
    tool_name: str,
    tool_args: dict = None
):
    await initialize_aviation_tools()

    tool = aviation_tools.get(tool_name)

    if tool is None:
        available_tools = ", ".join(
            sorted(aviation_tools.keys())
        )

        raise ValueError(
            f"AviationStack tool '{tool_name}' "
            "was not found. "
            f"Available tools: "
            f"{available_tools or 'none'}"
        )

    result = await tool.ainvoke(
        tool_args or {}
    )

    return result
=======
@tool
async def search_flights(
    departure_airport: str,
    arrival_airport: str,
    limit: int = 10,
):
    """Find flight routes between two airports.

    Use three-letter IATA airport codes, for example DEL for New Delhi
    and IXJ for Jammu. This tool returns route data from Aviationstack.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")

    aviation_tools = await client.get_tools(server_name="Aviationstack_MCP")
    route_tool = next(
        (tool for tool in aviation_tools if tool.name == "list_routes"),
        None,
    )
>>>>>>> main

    if route_tool is None:
        raise RuntimeError("Aviationstack MCP does not provide the list_routes tool")

<<<<<<< HEAD



@tool
async def list_airports():
    """Call this tool to get the list of airports"""
    return await aviation_mcp_call("list_airports")


@tool
async def list_airlines():
    """Call This tool to get list of airplines"""
    return await aviation_mcp_call("list_airlines")
=======
    return await route_tool.ainvoke(
        {
            "dep_iata": departure_airport.strip().upper(),
            "arr_iata": arrival_airport.strip().upper(),
            "limit": limit,
        }
    )
>>>>>>> main
