from secrets import choice
from string import ascii_letters, digits, punctuation
from dotenv import load_dotenv
from os import getenv

load_dotenv()
try:
    PASSWORD_MIN_SIZE = int(getenv("PASSWORD_MIN_SIZE"))
    PASSWORD_MAX_SIZE = int(getenv("PASSWORD_MAX_SIZE"))
except (TypeError, ValueError) as e:
    raise RuntimeError(f"Error loading password size constraints from environment variables: {e}")

def build_readable_password(length: int):
    try:
        assert length >= PASSWORD_MIN_SIZE, f"Password length must be at least {PASSWORD_MIN_SIZE}."
        assert length <= PASSWORD_MAX_SIZE, f"Password length must not exceed {PASSWORD_MAX_SIZE}."
        vowels = "aeiouyAEIOUY"
        consonants = ''.join([c for c in ascii_letters if c not in vowels])
        return ''.join(choice(vowels) if (i % 2 == 0) else choice(consonants) for i in range(length))
    except AssertionError as e:
        raise RuntimeError("Invalid password length for readable password.")
    except Exception as e:
        raise RuntimeError("An error occurred while building a readable password.")

def build_random_password(length: int, character_flags: list):
    try:
        assert length >= PASSWORD_MIN_SIZE, f"Password length must be at least {PASSWORD_MIN_SIZE}."
        assert length <= PASSWORD_MAX_SIZE, f"Password length must not exceed {PASSWORD_MAX_SIZE}."
        assert len(character_flags) == 3, "Character flags must be a list of 3 booleans."
        for flag in character_flags:
            assert isinstance(flag, bool), "Each character flag must be a boolean."

        pool = ""
        if character_flags[0]:
            pool += ascii_letters
        if character_flags[1]:
            pool += digits
        if character_flags[2]:
            pool += punctuation

        if not pool:
            raise ValueError("Character pool is empty due to flags configuration.")
        
        return ''.join(choice(pool) for _ in range(length))
    except AssertionError as e:
        raise RuntimeError("Invalid input for random password generation.")
    except Exception as e:
        raise RuntimeError("An error occurred while building a random password.")

def generate_password(length: int = PASSWORD_MIN_SIZE, character_flags: list = [True, True, True], readable: bool = False):
    try:
        assert length >= PASSWORD_MIN_SIZE, f"Password length must be at least {PASSWORD_MIN_SIZE}."
        assert length <= PASSWORD_MAX_SIZE, f"Password length must not exceed {PASSWORD_MAX_SIZE}."
        assert len(character_flags) == 3, "Character flags must be a list of 3 booleans."
        for flag in character_flags:
            assert isinstance(flag, bool), "Each character flag must be a boolean."
        
        return build_readable_password(length) if readable else build_random_password(length, character_flags)
    except AssertionError as e:
        raise RuntimeError("Invalid input for password generation.")
    except Exception as e:
        raise RuntimeError("An error occurred while generating a password.")