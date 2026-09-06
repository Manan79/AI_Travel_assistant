import os
import httpx
from dotenv import load_dotenv
import asyncio
from langchain_core.tools import tool
import json
load_dotenv()

import requests


async def get_station_code(station: str):
    with open(r"Travel_AI\tools\indian_railway_stations.json", "r", encoding="utf-8") as f:
        stations_list = json.load(f)

    stations = {
        station["name"].strip(): station["code"]
        for station in stations_list
    }
    code = stations[station]

    return code


@tool
async def get_train_details(
    boarding_station: str,
    destination_station: str
):
    """Return Indian trains running between two stations and this tool only expects the Railway station codes.
       Use this tool for retrieving the indian railways data only
    """

    bs = await get_station_code(boarding_station)
    ds = await get_station_code(destination_station)

    print(f"Finding Trains between {bs} to {ds}")

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"https://api.railradar.in/v1/trains/between/"
            f"{bs}/{ds}",
            headers={
                "Authorization": os.environ["RAILRADAR_API_KEY"]
            }
        )

        response.raise_for_status()

        data = response.json()

        trains = data['data']['trains']
        result = []

        for train in trains:
            result.append({
            "train_number": train["train"]["number"],
            "train_name": train["train"]["name"],
            "train_type": train["train"]["type"],
            "departure": train["from"]["departure"],
            "arrival": train["to"]["arrival"],
            "duration": train["duration"],
            "distance": train["distance"],
            "running_days": train["train"]["runDays"]
        })
        
        return result

# if __name__ == "__main__":
#     asyncio.run(
#         get_train_details(
#             boarding_station = 'Jalandhar City',
#             destination_station = "Delhi"
#         )
#     )
