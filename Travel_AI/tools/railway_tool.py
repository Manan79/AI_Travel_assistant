import os
import httpx
from dotenv import load_dotenv
import asyncio
from langchain_core.tools import tool
load_dotenv()


@tool
async def get_train_details(
    boarding_station: str,
    destination_station: str
):
    """Return Indian trains running between two stations.
       Use this tool for retrieving the indian railways data only
    """

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"https://api.railradar.in/v1/trains/between/"
            f"{boarding_station}/{destination_station}",
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
#     asyncio.run(get_train_details(
#         boarding_station = 'JUC', destination_station = 'NDLS'
#     ))