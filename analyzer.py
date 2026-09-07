"""
analyzer.py
-----------
Looks at a password and returns:
  - a rating: "Weak", "Fair", "Good", or "Strong"
  - a list of plain-English reasons for that rating
"""

import string

COMMON_PATTERNS = [
    "password", "123456", "qwerty", "letmein", "admin",
    "welcome", "iloveyou", "monkey", "dragon", "111111", "abc123",
]

ALPHA_NUMERIC_SEQUENCE = "abcdefghijklmnopqrstuvwxyz0123456789"


def analyze_password(password):
    """
    Returns (rating, feedback_list).
    Raises ValueError if the password is empty.
    """
    if not password:
        raise ValueError("Enter a password to analyze.")

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    feedback = []
    score = 0

    if length < 8:
        feedback.append("Your password is short. Aim for 12+ characters.")
    elif length < 12:
        score += 1
        feedback.append("Consider a longer password (12+ characters) for better security.")
    elif length < 16:
        score += 2
    else:
        score += 3

    variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
    score += variety_count

    if not has_upper:
        feedback.append("Add uppercase letters.")
    if not has_lower:
        feedback.append("Add lowercase letters.")
    if not has_digit:
        feedback.append("Add numbers.")
    if not has_symbol:
        feedback.append("Add symbols.")
    if variety_count == 4:
        feedback.append("Good character variety.")

    if _has_repeated_characters(password):
        score -= 1
        feedback.append("Avoid repeating the same character multiple times in a row.")

    if _has_sequential_characters(password):
        score -= 1
        feedback.append("Avoid obvious sequences like 'abc' or '123'.")

    if _contains_common_pattern(password):
        score -= 2
        feedback.append("This contains a very common password pattern. Avoid dictionary words and well-known passwords.")

    score = max(score, 0)

    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Fair"
    elif score <= 6:
        rating = "Good"
    else:
        rating = "Strong"

    if not feedback:
        feedback.append("This password looks solid. No obvious weaknesses found.")

    return rating, feedback


def _has_repeated_characters(password):
    """True if any character repeats 3+ times in a row, e.g. 'aaa'."""
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True
    return False


def _has_sequential_characters(password):
    """True if the password contains a 3+ character run like 'abc',
    '123', or their reverse ('cba', '321')."""
    lowered = password.lower()
    reversed_sequence = ALPHA_NUMERIC_SEQUENCE[::-1]

    for i in range(len(lowered) - 2):
        chunk = lowered[i:i + 3]
        if chunk in ALPHA_NUMERIC_SEQUENCE or chunk in reversed_sequence:
            return True
    return False


def _contains_common_pattern(password):
    """True if the password contains one of a handful of very common,
    already-leaked password patterns."""
    lowered = password.lower()
    return any(pattern in lowered for pattern in COMMON_PATTERNS)
