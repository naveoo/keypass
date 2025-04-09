import sqlite3
from pathlib import Path

class Database:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.DB_PATH = BASE_DIR / "db" / "database.db"
        self.PASSWORD_TABLE_NAME = "passwords"

        if not self.DB_PATH.parent.exists():
            self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.conn = sqlite3.connect(self.DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.PASSWORD_TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application TEXT NOT NULL,
                    userid TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError("An error occurred while initializing the database.")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def get_applications(self):
        try:
            self.cursor.execute(f"SELECT application FROM {self.PASSWORD_TABLE_NAME}")
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            raise RuntimeError("An error occurred while fetching applications.")

    def get_info(self, application: str):
        assert application != ""
        try:
            self.cursor.execute(f"""
                SELECT userid, password FROM {self.PASSWORD_TABLE_NAME}
                WHERE application = ?
            """, (application,))
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise RuntimeError("An error occurred while fetching the information.")

    def insert(self, values: tuple):
        for value in values:
            assert type(value) == str
            assert value != ""
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.PASSWORD_TABLE_NAME} (application, userid, password)
                VALUES (?, ?, ?)
            """, values)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error during insertion: {e}")
            raise RuntimeError("An error occurred while inserting data.")

    def delete_entry_by_id(self, entry_id: str):
        assert entry_id != ""
        try:
            self.cursor.execute(f"""
                DELETE FROM {self.PASSWORD_TABLE_NAME}
                WHERE id = ?
            """, (entry_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError("An error occurred while deleting the entry.")