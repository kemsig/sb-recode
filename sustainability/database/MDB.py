from pymongo import MongoClient
import config
from database.AbstractDatabase import Database

class MongoDatabase(Database):
    """
    Implements a MongoDB database.
    User data is stored in the "users" collection of the "sustain_db" database.
    """
    def __init__(self, uri: str = config.MONGO_URI, db_name: str = "sustain_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.users = self.db["users"]

    def add_points(self, user_id: int, points: int) -> bool:
        try:
            user = self.users.find_one({"user_id": user_id})
            if user:
                new_points_cur = user.get("points_cur", 0) + points
                new_points_total = user.get("points_total", 0) + (points if points > 0 else 0)
                self.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"points_cur": new_points_cur, "points_total": new_points_total}}
                )
            else:
                points_total = points if points > 0 else 0
                self.users.insert_one({
                    "user_id": user_id,
                    "points_cur": points,
                    "points_total": points_total
                })
            return False  # success
        except Exception as e:
            print(f"MongoDatabase.add_points error: {e}")
            return True   # error

    def get_user_info(self, user_id: int) -> dict:
        try:
            user = self.users.find_one({"user_id": user_id})
            return user if user else None
        except Exception as e:
            print(f"MongoDatabase.get_user_info error: {e}")
            return None

    def shutdown(self):
        """
        Closes the MongoDB client connection.
        """
        self.client.close()

