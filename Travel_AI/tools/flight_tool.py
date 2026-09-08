from langchain_core.tools import tool

from .mcp_client import client


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

    if route_tool is None:
        raise RuntimeError("Aviationstack MCP does not provide the list_routes tool")

    return await route_tool.ainvoke(
        {
            "dep_iata": departure_airport.strip().upper(),
            "arr_iata": arrival_airport.strip().upper(),
            "limit": limit,
        }
    )