from .mcp_client import client


# flights_with_airline
# historical_flights_by_date
# flight_arrival_departure_schedule
# future_flights_arrival_departure_schedule
# random_aircraft_type
# random_airplanes_detailed_info
# random_countries_detailed_info
# random_cities_detailed_info
# list_airports
# list_airlines
# list_routes
# list_taxes

async def avaitation_tool():
    tools = await client.get_tools(server_name='Aviationstack_MCP')
    avaitation_tool = [
        tool for tool in tools
    ]

    return avaitation_tool



    

# if __name__ == "__main__":
#     asyncio.run(avaitation_tool())