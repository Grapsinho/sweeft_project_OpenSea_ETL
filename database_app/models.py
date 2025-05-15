from .base_model import Model
from typing import Optional

class Collection(Model):
    id: Optional[int]  # ID is an integer but optional (since new objects won’t have it)
    collection: str
    name: str
    description: str
    image_url: str
    owner: str
    twitter_username: str
    contracts: dict

# to test things
class Cars(Model):
    name: str
    description: str