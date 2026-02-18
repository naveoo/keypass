import sys
import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode


# ---------------------------------------------------------------------------
# Paths helpers (centralisés ici pour éviter la duplication)
# ---------------------------------------------------------------------------

def get_app_base_path() -> Path:
    """Retourne le dossier racine de l'application.

    En mode PyInstaller, c'est le dossier contenant l'exécutable.
    En mode développement, c'est le dossier parent de ``src/``.
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent  # keypass/


def get_user_data_dir() -> Path:
    """Retourne le dossier de données utilisateur pour le mode packagé."""
    user_data_dir = Path(os.getenv("APPDATA", str(Path.home()))) / "KeyPass"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    return user_data_dir


def get_salt_path() -> Path:
    """Retourne le chemin du fichier salt."""
    if hasattr(sys, "_MEIPASS"):
        return get_user_data_dir() / "salt.bin"
    base = get_app_base_path()
    salt_dir = base / "src" / "core"
    salt_dir.mkdir(parents=True, exist_ok=True)
    return salt_dir / "salt.bin"


def get_db_path() -> Path:
    """Retourne le chemin de la base de données SQLite."""
    if hasattr(sys, "_MEIPASS"):
        return get_user_data_dir() / "database.db"
    base = get_app_base_path()
    db_folder = base / "src" / "db"
    db_folder.mkdir(parents=True, exist_ok=True)
    return db_folder / "database.db"


# ---------------------------------------------------------------------------
# Cryptographie
# ---------------------------------------------------------------------------

_VERIFICATION_TOKEN = b"KEYPASS_MASTER_VERIFY"


def get_salt() -> bytes:
    """Lit ou génère le salt cryptographique."""
    salt_path = get_salt_path()
    if not salt_path.exists():
        salt_path.write_bytes(os.urandom(16))
    return salt_path.read_bytes()


def derive_key(password: str) -> bytes:
    """Dérive une clé Fernet à partir du mot de passe maître."""
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_password(password: str, key: bytes) -> str:
    """Chiffre un mot de passe avec la clé Fernet."""
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(token: str, key: bytes) -> str:
    """Déchiffre un mot de passe avec la clé Fernet."""
    fernet = Fernet(key)
    return fernet.decrypt(token.encode()).decode()


# ---------------------------------------------------------------------------
# Vérification du mot de passe maître
# ---------------------------------------------------------------------------

def _get_verify_path() -> Path:
    """Retourne le chemin du fichier de vérification du mot de passe maître."""
    if hasattr(sys, "_MEIPASS"):
        return get_user_data_dir() / "verify.bin"
    base = get_app_base_path()
    return base / "src" / "core" / "verify.bin"


def is_first_run() -> bool:
    """Vérifie si c'est le premier lancement (pas encore de mot de passe maître)."""
    return not _get_verify_path().exists()


def store_master_verification(key: bytes) -> None:
    """Stocke un token de vérification chiffré avec la clé dérivée.

    Appelé lors de la première connexion pour enregistrer le mot de passe maître.
    """
    fernet = Fernet(key)
    encrypted = fernet.encrypt(_VERIFICATION_TOKEN)
    _get_verify_path().write_bytes(encrypted)


def verify_master_password(key: bytes) -> bool:
    """Vérifie que la clé dérivée correspond au mot de passe maître enregistré.

    Retourne True si le déchiffrement du token de vérification réussit.
    """
    verify_path = _get_verify_path()
    if not verify_path.exists():
        return True  # Premier lancement, pas de vérification

    try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(verify_path.read_bytes())
        return decrypted == _VERIFICATION_TOKEN
    except InvalidToken:
        return False