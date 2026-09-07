"""
generator.py
------------
Turns a set of settings (length + which character types to use)
into a random password.

Why `secrets` instead of `random`?
Python's `random` module is *predictable* if you know its internal state —
it's designed for things like shuffling a deck of cards in a game, not
security. `secrets` is built on top of your operating system's
cryptographically secure random source, which is what passwords need.
"""

import secrets
import string

# A small, readable set of symbols. Kept intentionally simple —
# some sites reject exotic symbols, so this pool sticks to common ones.
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """
    Build a random password.

    length: how many characters long the password should be
    use_upper / use_lower / use_digits / use_symbols: booleans for which
        character types are allowed

    Raises ValueError with a human-readable message if the settings
    don't make sense (e.g. no character types selected).
    """
    if length < 1:
        raise ValueError("Password length must be at least 1.")

    character_pools = []
    if use_upper:
        character_pools.append(string.ascii_uppercase)
    if use_lower:
        character_pools.append(string.ascii_lowercase)
    if use_digits:
        character_pools.append(string.digits)
    if use_symbols:
        character_pools.append(SYMBOLS)

    if not character_pools:
        raise ValueError("Select at least one character type.")

    all_characters = "".join(character_pools)

    if length < len(character_pools):
        password_chars = [secrets.choice(all_characters) for _ in range(length)]
    else:
        password_chars = [secrets.choice(pool) for pool in character_pools]

        remaining = length - len(password_chars)
        password_chars += [secrets.choice(all_characters) for _ in range(remaining)]

        _secure_shuffle(password_chars)

    return "".join(password_chars)


def _secure_shuffle(items):
    """
    Shuffle a list in place using the Fisher-Yates algorithm, powered by
    secrets.randbelow() instead of the `random` module.
    """
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]
