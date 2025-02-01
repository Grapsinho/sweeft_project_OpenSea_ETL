from database_app.models import Collection

# i created a table collection
# Collection.create_table()

new_collection = Collection(
    collection="Art NFTs",
    name="Modern Art Collection",
    description="A collection of modern NFT artworks.",
    image_url="https://example.com/image.jpg",
    owner="0x123456...",
    twitter_username="nft_artist",
    contracts={"main": "0xabcdef..."}
)

new_collection.save()