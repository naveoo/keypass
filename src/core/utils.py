import re

_COMMON_PASSWORDS = frozenset({
    "123456", "password", "123456789", "12345", "qwerty", "abc123",
    "password1", "111111", "1234567", "iloveyou", "admin", "letmein",
    "welcome", "monkey", "master", "dragon", "login", "princess",
    "football", "shadow", "sunshine", "trustno1", "azerty", "000000",
})


def evaluate_password_strength(password: str) -> int:
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
    labels = {
        5: "Mot de passe très sécurisé !",
        4: "Mot de passe sécurisé.",
        3: "Mot de passe moyen.",
        2: "Mot de passe faible.",
    }
    return labels.get(score, "Mot de passe très faible.")