import sqlite3
import os
import config
from database.AbstractDatabase import Database


class LocalDatabase(Database):
    """
    Implements a local SQLite database.
    The database file (by default, "local.db") stores a table "users" with:
        user_id INTEGER PRIMARY KEY,
        points_cur INTEGER NOT NULL,
        points_total INTEGER NOT NULL
    """
    def __init__(self, db_file: str = "local.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    points_cur INTEGER NOT NULL,
                    points_total INTEGER NOT NULL
                );
            """)

    def add_points(self, user_id: int, points: int) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if row:
                new_points_cur = row["points_cur"] + points
                new_points_total = row["points_total"] + (points if points > 0 else 0)
                cur.execute(
                    "UPDATE users SET points_cur = ?, points_total = ? WHERE user_id = ?",
                    (new_points_cur, new_points_total, user_id)
                )
            else:
                points_total = points if points > 0 else 0
                cur.execute(
                    "INSERT INTO users (user_id, points_cur, points_total) VALUES (?, ?, ?)",
                    (user_id, points, points_total)
                )
            self.conn.commit()
            return False  # indicates success
        except Exception as e:
            print(f"LocalDatabase.add_points error: {e}")
            return True   # indicates error

    def get_user_info(self, user_id: int) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if row:
                return {
                    "user_id": row["user_id"],
                    "points_cur": row["points_cur"],
                    "points_total": row["points_total"]
                }
            else:
                # User not found: initialize with 0 points
                cur.execute(
                    "INSERT INTO users (user_id, points_cur, points_total) VALUES (?, ?, ?)",
                    (user_id, 0, 0)
                )
                self.conn.commit()
                return {"user_id": user_id, "points_cur": 0, "points_total": 0}
        except Exception as e:
            print(f"LocalDatabase.get_user_info error: {e}")
            return None

    def get_leaderboard(self, limit: int = 10, offset: int = 0) -> list:
        """
        Returns a list of users ordered by total points in descending order.
        Each user is represented as a dictionary.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM users ORDER BY points_total DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cur.fetchall()
            leaderboard = []
            for row in rows:
                leaderboard.append({
                    "user_id": row["user_id"],
                    "points_cur": row["points_cur"],
                    "points_total": row["points_total"]
                })
            return leaderboard
        except Exception as e:
            print(f"LocalDatabase.get_leaderboard error: {e}")
            return []

    def shutdown(self):
        """
        Commits and closes the database connection.
        After calling shutdown(), you can access self.db_file to retrieve
        the database file and send it via DM (this step is handled by your bot logic).
        """
        self.conn.commit()
        self.conn.close()
        return self.db_file

    def check_db_size(self) -> bool:
        """
        Checks if the size of the database file does not exceed config.MAX_DB_SIZE.
        Returns True if the file size is within the limit, False otherwise.
        """
        try:
            file_size = os.path.getsize(self.db_file)
            print(file_size, config.MAX_DB_SIZE)
            return file_size <= config.MAX_DB_SIZE
        except Exception as e:
            print(f"Error checking database size: {e}")
            return False


    def remove_user(self, user_id: int) -> bool:
        """
        Removes the user record from the database.
        Returns False on success, True if an error occurred.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.conn.commit()
            return False
        except Exception as e:
            print(f"LocalDatabase.remove_user error: {e}")
            return True