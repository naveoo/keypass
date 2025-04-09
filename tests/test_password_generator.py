from rich import print
import pytest
from src.core.password_generator import (
    build_readable_password,
    build_random_password,
    generate_password,
    PASSWORD_MIN_SIZE,
    PASSWORD_MAX_SIZE
)

@pytest.mark.parametrize("length", [PASSWORD_MIN_SIZE, (PASSWORD_MIN_SIZE + PASSWORD_MAX_SIZE) // 2, PASSWORD_MAX_SIZE])
def test_readable_password_length(length):
    password = build_readable_password(length)
    print(f"[bold green]Mot de passe lisible généré (longueur {length}):[/] {password}")
    assert len(password) == length
    vowels = "aeiouyAEIOUY"
    consonants = ''.join([c for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in vowels])
    for i, char in enumerate(password):
        if i % 2 == 0:
            assert char in vowels
        else:
            assert char in consonants

@pytest.mark.parametrize("length", [PASSWORD_MIN_SIZE, PASSWORD_MAX_SIZE])
@pytest.mark.parametrize("flags", [
    [True, False, False],
    [False, True, False],
    [False, False, True],
    [True, True, True],
])
def test_random_password_content(length, flags):
    password = build_random_password(length, flags)
    print(f"[bold cyan]Mot de passe généré avec les flags {flags}: {password}[/]")
    assert len(password) == length
    pool = ""
    if flags[0]:
        pool += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if flags[1]:
        pool += "0123456789"
    if flags[2]:
        pool += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    assert all(c in pool for c in password)

def test_generate_password_readable():
    pw = generate_password(readable=True)
    print(f"[bold yellow]Mot de passe lisible généré :[/] {pw}")
    assert len(pw) >= PASSWORD_MIN_SIZE
    assert pw[0] in "aeiouyAEIOUY"

def test_generate_password_random():
    pw = generate_password(readable=False, character_flags=[True, True, False])
    print(f"[bold magenta]Mot de passe généré aléatoirement :[/] {pw}")
    assert any(c.isdigit() for c in pw)
    assert any(c.isalpha() for c in pw)

def test_invalid_lengths():
    with pytest.raises(AssertionError, match=f"Password length must be at least {PASSWORD_MIN_SIZE}."):
        build_random_password(PASSWORD_MIN_SIZE - 1, [True, True, True])
    with pytest.raises(AssertionError, match=f"Password length must not exceed {PASSWORD_MAX_SIZE}."):
        build_random_password(PASSWORD_MAX_SIZE + 1, [True, True, True])

def test_invalid_flags():
    with pytest.raises(AssertionError, match="Each character flag must be a boolean."):
        build_random_password(PASSWORD_MIN_SIZE, [1, 0, 0])
    with pytest.raises(AssertionError, match="Character flags must be a list of 3 booleans."):
        build_random_password(PASSWORD_MIN_SIZE, [True, True])