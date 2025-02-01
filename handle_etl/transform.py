import json

DATA_LAKE_PATH = "data_lake/raw_data.json"

def load_raw_data():
    """Load the raw data from JSON file."""
    try:
        with open(DATA_LAKE_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return raw_data
    except Exception as e:
        print(f"Error loading raw data: {e}")
        return []


def filter_ethereum_collections(collections):
    """Filter collections that belong to the Ethereum blockchain."""
    return [
        col for col in collections 
        if col.get("contracts") and col["contracts"][0].get("chain") == "ethereum"
    ]


def transform_collection_data(collections):
    """Transform raw data into structured format for database insertion."""
    transformed_data = []

    for col in collections:
        transformed_data.append({
            "collection": col.get("collection", "unknown"),
            "name": col.get("name", "No Name"),
            "description": col.get("description", "No description available."),
            "image_url": col.get("image_url", "static/images/default.jpg"),
            "owner": col.get("owner", "Unknown"),
            "twitter_username": col.get("twitter_username", "N/A"),
            "contracts": col.get("contracts", {})
        })

    return transformed_data

def save_transformed_data(transformed_data, output_path="data_lake/cleaned_data.json"):
    """Save cleaned data to a JSON file before loading into the database."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed_data, f, indent=4)
    print(f"Transformed data saved to {output_path}")

def transform_data():
    """Full transformation process: Load, filter, transform, and save data."""
    raw_data = load_raw_data()  # Step 1: Load raw JSON
    eth_collections = filter_ethereum_collections(raw_data)  # Step 2: Filter ETH collections
    transformed_data = transform_collection_data(eth_collections)  # Step 3: Clean & transform
    save_transformed_data(transformed_data)  # Step 4: Save cleaned data
    return transformed_data

if __name__ == "__main__":
    transformed_collections = transform_data()
    print(f"🚀 Transformed {len(transformed_collections)} Ethereum collections ready for database insertion!")