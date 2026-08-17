"""
Basic input-sanitisation utilities for the AI Study Assistant.

This module provides lightweight protection against common prompt-injection
patterns before user input is forwarded to the language model.
"""

import re


# Common phrases that may indicate an attempt to override system behaviour.
SUSPICIOUS_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+system\s+prompt",
    r"display\s+(your\s+)?system\s+prompt",
    r"what\s+is\s+your\s+system\s+prompt",
    r"override\s+(the\s+)?system\s+instructions",
    r"bypass\s+(the\s+)?system\s+instructions",
]


def contains_prompt_injection(message: str) -> bool:
    """
    Check whether a user message contains common prompt-injection patterns.

    Args:
        message (str): The message submitted by the user.

    Returns:
        bool: True if a suspicious pattern is detected; otherwise False.
    """

    normalised_message = message.strip().lower()

    return any(
        re.search(pattern, normalised_message)
        for pattern in SUSPICIOUS_PATTERNS
    )


def sanitise_message(message: str) -> str:
    """
    Clean basic unnecessary whitespace from user input.

    Args:
        message (str): The raw user message.

    Returns:
        str: The sanitised user message.
    """

    return " ".join(message.split())