import json
import os
from pathlib import Path
import httpx
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()

STATIONS_FILE = Path(__file__).with_name("indian_railway_stations.json")

@tool
async def get_train_details(
    boarding_station: str,
    destination_station: str
):
    """Find Indian trains availble between the two station 
    
    args:
    It accepts the station codes instead of station names.
    for ex Jalandhar city -> JUC
    """

    bs = boarding_station
    ds = destination_station
    api_key = os.environ.get("RAILRADAR_API_KEY")
    if not api_key:
        raise RuntimeError("RAILRADAR_API_KEY is not configured")

    print(f"Finding Trains between {bs} to {ds}")

    async with httpx.AsyncClient(timeout=30.0) as client:

        response = await client.get(
            f"https://api.railradar.in/v1/trains/between/"
            f"{bs}/{ds}",
            headers={
                "Authorization": api_key
            }
        )

        response.raise_for_status()

        data = response.json()

        trains = data.get("data", {}).get("trains", [])
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

