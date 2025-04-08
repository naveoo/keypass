from secrets import choice
from string import ascii_letters, digits, punctuation
from dotenv import load_dotenv
from os import getenv

load_dotenv()
PASSWORD_MIN_SIZE = getenv("PASSWORD_MIN_SIZE")
PASSWORD_MAX_SIZE = getenv("PASSWORD_MAX_SIZE")

def build_readable_password(length:int):
    assert length >= PASSWORD_MIN_SIZE
    assert length <= PASSWORD_MAX_SIZE
    vowels = "aeiouyAEIOUY"
    consonants = ''.join([c for c in ascii_letters if c not in vowels])
    return ''.join(choice(vowels) if (i % 2 == 0) else choice(consonants)for i in range(length))

def build_random_password(length:int, character_flags:list):
    assert length >= PASSWORD_MIN_SIZE
    assert length <= PASSWORD_MAX_SIZE
    assert len(character_flags) == 3
    for i in range(len(character_flags)):
        assert type(character_flags[i]) == bool
    pool = ""
    if (character_flags[0]):
        pool += ascii_letters
    if (character_flags[1]):
        pool += digits
    if (character_flags[2]):
        pool += punctuation
    return ''.join(choice(pool) for _ in range(length))

def generate_password(length:int=PASSWORD_MIN_SIZE, character_flags:list=[True,True,True], readable:bool=False):
    assert length >= PASSWORD_MIN_SIZE
    assert length <= PASSWORD_MAX_SIZE
    assert len(character_flags) == 3
    for i in range(len(character_flags)):
        assert type(character_flags[i]) == bool
    return build_readable_password(length) if (readable) else build_random_password(length, character_flags)