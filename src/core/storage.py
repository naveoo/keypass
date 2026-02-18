import sqlite3
from src.core.crypto import get_db_path, encrypt_password, decrypt_password


class Database:
    """Gestionnaire de la base de données des mots de passe."""

    TABLE_NAME = "passwords"

    def __init__(self, derived_key: bytes):
        self.key = derived_key
        self._db_path = get_db_path()
        self._connect()

    # ------------------------------------------------------------------
    # Connexion & cycle de vie
    # ------------------------------------------------------------------

    def _connect(self) -> None:
        """Ouvre la connexion et crée la table si nécessaire."""
        try:
            self.conn = sqlite3.connect(str(self._db_path))
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application TEXT NOT NULL,
                    userid TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(
                f"Erreur lors de l'initialisation de la base de données : {e}"
            )

    def close(self) -> None:
        """Ferme la connexion à la base de données."""
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close()

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------

    def get_applications(self) -> list[str]:
        """Retourne la liste des applications enregistrées (sans doublon)."""
        try:
            self.cursor.execute(
                f"SELECT DISTINCT application FROM {self.TABLE_NAME}"
            )
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur lors de la récupération des applications : {e}")

    def get_info(self, application: str) -> list[tuple[str, str]]:
        """Retourne les (userid, mot_de_passe_déchiffré) pour une application."""
        try:
            self.cursor.execute(
                f"SELECT userid, password FROM {self.TABLE_NAME} WHERE application = ?",
                (application,),
            )
            rows = self.cursor.fetchall()
            return [(uid, decrypt_password(pwd, self.key)) for uid, pwd in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur lors de la récupération des informations : {e}")
        except Exception as e:
            raise RuntimeError(f"Erreur de déchiffrement : {e}")

    def get_users_for_application(self, application: str) -> list[str]:
        """Retourne les utilisateurs distincts pour une application."""
        try:
            self.cursor.execute(
                f"SELECT DISTINCT userid FROM {self.TABLE_NAME} WHERE application = ?",
                (application,),
            )
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur lors de la récupération des utilisateurs : {e}")

    # ------------------------------------------------------------------
    # Écriture
    # ------------------------------------------------------------------

    def insert(self, application: str, userid: str, password: str) -> None:
        """Insère un nouveau mot de passe chiffré."""
        encrypted_password = encrypt_password(password, self.key)
        try:
            self.cursor.execute(
                f"INSERT INTO {self.TABLE_NAME} (application, userid, password) VALUES (?, ?, ?)",
                (application, userid, encrypted_password),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur lors de l'insertion : {e}")

    def delete_entry_by_app_and_user(self, application: str, userid: str) -> None:
        """Supprime une entrée par application et utilisateur."""
        try:
            self.cursor.execute(
                f"SELECT id FROM {self.TABLE_NAME} WHERE application = ? AND userid = ?",
                (application, userid),
            )
            result = self.cursor.fetchone()

            if result is None:
                raise ValueError(
                    f"Aucune entrée trouvée pour '{application}' avec l'utilisateur '{userid}'."
                )

            self.cursor.execute(
                f"DELETE FROM {self.TABLE_NAME} WHERE id = ?",
                (result[0],),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erreur base de données : {e}")
