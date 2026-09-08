import re
from datetime import datetime

from langchain_core.tools import tool
from .mcp_client import client


async def get_data(
    tool_name : str,
    tool_args: dict = None
):
    aviation_tools = await client.get_tools(server_name="Aviationstack_MCP")

    avaitation = next(
        t for t in aviation_tools
        if t.name == tool_name
    )
    result = await avaitation.ainvoke(
        tool_args or {}
    )

    return result


async def _airport_code(airport: str) -> str:
    airport = airport.strip().upper()
    if re.fullmatch(r"[A-Z]{3}", airport):
        return airport
    raise ValueError(
        f"'{airport}' is not an IATA airport code. Provide a three-letter "
        "IATA code because this Aviationstack plan does not allow airport lookup."
    )

@tool
async def search_flights(
    departure_airport: str,
    arrival_airport: str,
    travel_date: str,
    limit: int = 10,
):
    """Find flights between two airports on a specific date.

    Use three-letter IATA airport codes, such as BOM or BKK. Airport-name
    lookup is unavailable on the current Aviationstack plan.
    """
    if not departure_airport.strip() or not arrival_airport.strip():
        raise ValueError("Both departure_airport and arrival_airport are required")
    try:
        datetime.strptime(travel_date, "%Y-%m-%d")
    except (TypeError, ValueError) as error:
        raise ValueError("travel_date must use YYYY-MM-DD format") from error
    if limit < 1:
        raise ValueError("limit must be at least 1")

    departure_code = await _airport_code(departure_airport)
    arrival_code = await _airport_code(arrival_airport)
    flight_data = await get_data(
        "historical_flights_by_date",
        {
            "flight_date": travel_date,
            "number_of_flights": limit,
            "dep_iata": departure_code,
            "arr_iata": arrival_code,
        },
    )

    return {
        "departure_airport": departure_code,
        "arrival_airport": arrival_code,
        "travel_date": travel_date,
        "flight_data": flight_data,
    }