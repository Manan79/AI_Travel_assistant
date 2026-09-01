from mcp_client import client
import asyncio


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

async def gettools():

    tools = await client.get_tools(server_name='Aviationstack_MCP')
    flights_with_airline_tool = next(
        t for t in tools
            if t.name == 'flights_with_airline'
    )

    result = await flights_with_airline_tool.ainvoke({'airline_name': 'Indigo' , 'number_of_flights': 20})
    print(result)



    

if __name__ == "__main__":
    asyncio.run(gettools())