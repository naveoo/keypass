import base64
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

SALT = b'secure_salt_1234'

def encrypt_password(password: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted.decode()

def decrypt_password(token: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted = fernet.decrypt(token.encode())
    return decrypted.decode()

SALT_PATH = Path(__file__).resolve().parent.parent / "db" / "salt.bin"

def get_salt():
    if not SALT_PATH.exists():
        SALT_PATH.write_bytes(os.urandom(16))
    return SALT_PATH.read_bytes()

def derive_key(password: str) -> bytes:
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))