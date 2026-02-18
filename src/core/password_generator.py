from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from dotenv import load_dotenv
from os import getenv

load_dotenv()

try:
    PASSWORD_MIN_SIZE = int(getenv("PASSWORD_MIN_SIZE", "12"))
    PASSWORD_MAX_SIZE = int(getenv("PASSWORD_MAX_SIZE", "50"))
except (TypeError, ValueError) as e:
    raise RuntimeError(
        f"Erreur lors du chargement des contraintes de taille de mot de passe : {e}"
    )


def generate_password(
    length: int = 12,
    include_letters: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> str:
    if length < PASSWORD_MIN_SIZE:
        raise ValueError(f"La longueur doit être d'au moins {PASSWORD_MIN_SIZE}.")
    if length > PASSWORD_MAX_SIZE:
        raise ValueError(f"La longueur ne doit pas dépasser {PASSWORD_MAX_SIZE}.")

    pool = ""
    required_chars: list[str] = []

    if include_letters:
        pool += ascii_lowercase + ascii_uppercase
        required_chars.append(choice(ascii_uppercase))
        required_chars.append(choice(ascii_lowercase))
    if include_digits:
        pool += digits
        required_chars.append(choice(digits))
    if include_symbols:
        pool += punctuation
        required_chars.append(choice(punctuation))

    if not pool:
        raise ValueError("Au moins un type de caractère doit être sélectionné.")

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [choice(pool) for _ in range(remaining_length)]
    from secrets import randbelow
    for i in range(len(password_chars) - 1, 0, -1):
        j = randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)