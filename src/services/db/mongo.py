"""Service for handling MongoDB operations."""

from pymongo import MongoClient

MONGO_URL = "mongodb://root:root@localhost:27017/"


class ServiceMongo:
    """ServiceMongo."""

    @staticmethod
    def import_data(data: dict) -> None:
        """Import data into Mongo."""
        client = MongoClient(MONGO_URL)
        fisheyesea = client.get_database("fisheyesea")
        fishingefforts = fisheyesea.get_collection("fishingefforts")
        fishingefforts.insert_many(data)

    @staticmethod
    def clean_data() -> None:
        """Clean data in Mongo."""
        client = MongoClient(MONGO_URL)
        fisheyesea = client.get_database("fisheyesea")
        fishingefforts = fisheyesea.get_collection("fishingefforts")
        fishingefforts.delete_many({})

    @staticmethod
    def get_data() -> list[dict]:
        """Get data from Mongo."""
        client = MongoClient(MONGO_URL)
        fisheyesea = client.get_database("fisheyesea")
        fishingefforts = fisheyesea.get_collection("fishingefforts")
        return fishingefforts.find({}).to_list()
