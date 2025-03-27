from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def add_points(self, user_id: int, points: int) -> bool:
        """
        Add (or subtract) points for a user.
        Return False on success, True if there was an error.
        """
        pass

    @abstractmethod
    def get_user_info(self, user_id: int) -> dict:
        """
        Retrieve user info as a dictionary.
        Return None if the user is not found or on error.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Shutdown routine. For a local database this might close the connection
        and return the file path of the .db file so that it can be DM'd.
        For MongoDB, it might simply close the connection.
        """
        pass

    @abstractmethod
    def get_leaderboard(self):
        pass

    @abstractmethod
    def remove_user(self, user_id: int):
        pass
