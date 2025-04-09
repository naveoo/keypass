import sqlite3
from pathlib import Path
from src.core.crypto import encrypt_password, decrypt_password

class Database:
    def __init__(self, derived_key: bytes):
        self.key = derived_key
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
        except sqlite3.Error:
            raise RuntimeError("Une erreur est survenue lors de l'initialisation de la base de données.")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def get_applications(self):
        try:
            self.cursor.execute(f"SELECT application FROM {self.PASSWORD_TABLE_NAME}")
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error:
            raise RuntimeError("Erreur lors de la récupération des applications.")

    def get_info(self, application: str):
        try:
            self.cursor.execute(f"""
                SELECT userid, password FROM {self.PASSWORD_TABLE_NAME}
                WHERE application = ?
            """, (application,))
            rows = self.cursor.fetchall()
            return [(uid, decrypt_password(pwd, self.key)) for uid, pwd in rows]
        except sqlite3.Error:
            raise RuntimeError("Erreur lors de la récupération des informations.")
        except Exception as e:
            raise RuntimeError(f"Erreur de déchiffrement : {e}")

    def get_users_for_application(self, application: str):
        try:
            self.cursor.execute(f"""
                SELECT DISTINCT userid FROM {self.PASSWORD_TABLE_NAME} WHERE application = ?
            """, (application,))
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]  # Retourne la liste des utilisateurs pour cette application
        except sqlite3.Error:
            raise RuntimeError("Une erreur est survenue lors de la récupération des utilisateurs.")

    def insert(self, values: tuple):
        application, userid, password = values
        encrypted_password = encrypt_password(password, self.key)
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.PASSWORD_TABLE_NAME} (application, userid, password)
                VALUES (?, ?, ?)
            """, (application, userid, encrypted_password))
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur lors de l'insertion : {e}")

    def delete_entry_by_app_and_user(self, application: str, userid: str):
        try:
            self.cursor.execute(f"""
                SELECT id FROM {self.PASSWORD_TABLE_NAME}
                WHERE application = ? AND userid = ?
            """, (application, userid))
            result = self.cursor.fetchone()

            if result is None:
                raise ValueError(f"Aucune entrée trouvée pour '{application}' avec l'utilisateur '{userid}'.")

            self.cursor.execute(f"""
                DELETE FROM {self.PASSWORD_TABLE_NAME} WHERE id = ?
            """, (result[0],))
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur base de données : {e}")
        except ValueError as e:
            raise e
