import re

def evaluate_password_strength(password: str) -> int:
    score = 0
    if len(password) >= 12:
        score += 1
    elif len(password) >= 8:
        score += 0.5
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    common_passwords = ["123456", "password", "123456789", "12345", "qwerty", "abc123"]
    if password in common_passwords:
        return 1
    return min(score, 5)