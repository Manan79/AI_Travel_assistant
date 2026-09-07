import os
import httpx
from dotenv import load_dotenv
import asyncio
from langchain_core.tools import tool
import json
load_dotenv()




@tool
async def get_train_details(
    boarding_station: str,
    destination_station: str
):
    """Return Indian trains running between two stations.
       Use this tool for retrieving the indian railways data only


    args:
        Accepts the station codes only
    """

    bs = boarding_station
    ds = destination_station

    print(f"Finding Trains between {bs} to {ds}")

    async with httpx.AsyncClient(timeout=30.0) as client:

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

