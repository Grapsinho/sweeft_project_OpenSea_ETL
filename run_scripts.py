from database_app.models import Collection, Cars

# i created a table collection
#Collection.create_table()

# Collection.remove_columns("new_column")

records = Collection.filter(owner="0x05374ebbc828df9e3c6a989d7ef7c0c30a4349b9").limit(2)

for i in records:
    print(i.name)
    print(i.contracts)

    print("\n")
    print("---- next ----")

# for i in collections_instance:
#     print(i.name)


# new_collection = Collection(
#     collection="Art NFTs",
#     name="Modern Art Collection",
#     description="A collection of modern NFT artworks.",
#     image_url="https://example.com/image.jpg",
#     owner="0x123456...",
#     twitter_username="nft_artist",
#     contracts="[{\"address\": \"0x123456...\", \"chain\": \"ethereum\"}]"
# )

# new_collection.save()

# collections = Collection.all()

# for i in collections:
#     print(f"name: {i.name}")



# populate json files
# load database

# from handle_etl.etl_pipeline import run_etl

# if __name__ == "__main__":
#     run_etl()



#################### testing delete method ########################

#print(Cars.all())