from secrets import choice
from string import ascii_letters, digits, punctuation

def build_readable_password(length:int):
    """Créé un mot de passe composé d'une alternance de voyelles et de consonnes.

    Args:
        length (int): La longueur du mot de passe.

    Returns:
        str: Le mot de passe généré.
    """
    vowels = "aeiouyAEIOUY"
    consonants = ''.join([c for c in ascii_letters if c not in vowels])
    return ''.join(choice(vowels) if (i % 2 == 0) else choice(consonants)for i in range(length))

def build_random_password(length:int, character_flags:list):
    """Créé un mot de passe composé de caractères spécifiés par la liste character_flag passée en argument.

    Args:
        length (int): La longueur du mot de passe.
        character_flags (list): Les charactères à ajouter ou non définis par un booléen([Lettres ASCII, Nombres, Caractères spéciaux]).

    Returns:
        str: Le mot de passe généré.
    """
    pool = ""
    if (character_flags[0]):
        pool += ascii_letters
    if (character_flags[1]):
        pool += digits
    if (character_flags[2]):
        pool += punctuation
    return ''.join(choice(pool) for _ in range(length))

def generate_password(length: int, characters: list, readable: bool):
    """Créé un mot de passe.

    Args:
        length (int): Longueur du mot de passe.
        characters (list): Les charactères à ajouter ou non définis par un booléen([Lettres ASCII, Nombres, Caractères spéciaux]).
        readable (bool): Lisibilité du mot de passe généré.

    Returns:
        str: Mot de passe généré.
    """
    return build_readable_password(length) if (readable) else build_random_password(length, characters)