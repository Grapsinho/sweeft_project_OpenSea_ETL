import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENSEA_API_KEY = os.getenv("OPENSEA_API_KEY")

HEADERS = {"Accept": "application/json", "X-API-KEY": OPENSEA_API_KEY}
BASE_URL = "https://api.opensea.io/api/v2/collections"
DATA_LAKE_PATH = "data_lake/raw_data.json"

def fetch_collections(limit=100, max_pages=5):
    """
    Extract collections data from OpenSea API.
    """
    collections = []
    next_cursor = None

    # with this we only fetch number of pages that are specified in max_pages
    for _ in range(max_pages):
        params = {"limit": limit}
        if next_cursor:
            params["next"] = next_cursor

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        
        # error handling
        if response.status_code == 429:
            print("Rate limit error! Wait for 10 seconds...")
            time.sleep(10)
            continue
        elif response.status_code != 200:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

        # adding data in our list
        data = response.json()
        collections.extend(data.get("collections", []))
        
        # stop if there is no more data
        next_cursor = data.get("next")
        if not next_cursor:
            break

    # save data in json file
    with open(DATA_LAKE_PATH, "w", encoding="utf-8") as f:
        json.dump(collections, f, indent=4)

    return collections

if __name__ == "__main__":
    collections_data = fetch_collections()
    print(f"Extracted {len(collections_data)} collections and saved raw data.")
