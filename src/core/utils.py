import re

# Mots de passe courants à rejeter immédiatement
_COMMON_PASSWORDS = frozenset({
    "123456", "password", "123456789", "12345", "qwerty", "abc123",
    "password1", "111111", "1234567", "iloveyou", "admin", "letmein",
    "welcome", "monkey", "master", "dragon", "login", "princess",
    "football", "shadow", "sunshine", "trustno1", "azerty", "000000",
})


def evaluate_password_strength(password: str) -> int:
    """Évalue la force d'un mot de passe sur une échelle de 0 à 5.

    Critères :
    - Longueur >= 12 : +1 point (>= 8 et < 12 : +0 point bonus, mais pas pénalisé)
    - Longueur >= 16 : +1 point supplémentaire
    - Contient des majuscules : +1
    - Contient des minuscules : +1
    - Contient des chiffres : +1
    - Contient des caractères spéciaux : +1
    - Mot de passe courant : score forcé à 0

    Returns:
        Score entier entre 0 et 5.
    """
    if password in _COMMON_PASSWORDS:
        return 0

    score = 0

    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", password):
        score += 1

    return min(score, 5)


def get_strength_label(score: int) -> str:
    """Retourne un libellé lisible pour un score de force de mot de passe."""
    labels = {
        5: "Mot de passe très sécurisé !",
        4: "Mot de passe sécurisé.",
        3: "Mot de passe moyen.",
        2: "Mot de passe faible.",
    }
    return labels.get(score, "Mot de passe très faible.")