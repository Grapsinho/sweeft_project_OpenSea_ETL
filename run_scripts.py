from database_app.models import Collection

# i created a table collection
#Collection.create_table()

# new_collection = Collection(
#     collection="Art NFTs",
#     name="Modern Art Collection",
#     description="A collection of modern NFT artworks.",
#     image_url="https://example.com/image.jpg",
#     owner="0x123456...",
#     twitter_username="nft_artist",
#     contracts={"main": "0xabcdef..."}
# )

# new_collection.save()

collections = Collection.filter(limit=2, order_by="name", name__icontains="100")

for i in collections:
    print(f"name: {i.name}")



# from handle_etl.etl_pipeline import run_etl

# if __name__ == "__main__":
#     run_etl()

# all_coll = Collection.all()

# for i in all_coll:
#     print(f"name: {i.name}")
#     print(f"chain: {i.contracts[0]["chain"]}")