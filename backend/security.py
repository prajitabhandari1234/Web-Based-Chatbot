"""
Basic input-sanitisation utilities for the AI Study Assistant.

This module provides lightweight protection against common prompt-injection
and system-instruction disclosure attempts before user input is forwarded
to the language model.
"""

import re


# Common phrases that may indicate an attempt to override system behaviour
# or reveal protected system instructions.
SUSPICIOUS_PATTERNS = [
    # Attempts to ignore or replace previous instructions.
    r"ignore\s+(all\s+)?(previous|prior|earlier)\s+instructions?",
    r"ignore\s+(all\s+)?(previous|prior|earlier)\s+messages?",
    r"forget\s+(all\s+)?(previous|prior|earlier)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior|earlier)\s+instructions?",
    r"override\s+(the\s+)?system\s+instructions?",
    r"bypass\s+(the\s+)?system\s+instructions?",

    # Attempts to reveal the system prompt.
    r"reveal\s+(the\s+|your\s+)?system\s+prompt",
    r"show\s+(me\s+)?(the\s+|your\s+)?system\s+prompt",
    r"display\s+(the\s+|your\s+)?system\s+prompt",
    r"provide\s+(me\s+)?(with\s+)?(the\s+|your\s+)?system\s+prompt",
    r"share\s+(the\s+|your\s+)?system\s+prompt",
    r"tell\s+me\s+(the\s+|your\s+)?system\s+prompt",
    r"what\s+is\s+(the\s+|your\s+)?system\s+prompt",
    r"repeat\s+(the\s+|your\s+)?system\s+prompt",
    r"print\s+(the\s+|your\s+)?system\s+prompt",

    # Attempts to reveal hidden or internal instructions.
    r"reveal\s+(the\s+|your\s+)?(hidden|internal)\s+instructions?",
    r"show\s+(me\s+)?(the\s+|your\s+)?(hidden|internal)\s+instructions?",
    r"provide\s+(me\s+)?(with\s+)?(the\s+|your\s+)?(hidden|internal)\s+instructions?",
    r"share\s+(the\s+|your\s+)?(hidden|internal)\s+instructions?",
]


def contains_prompt_injection(message: str) -> bool:
    """
    Check whether a user message contains common prompt-injection
    or system-instruction disclosure patterns.

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
    Clean basic unnecessary whitespace and control characters from user input.

    Args:
        message (str): The raw user message.

    Returns:
        str: The sanitised user message.
    """

    # Remove non-printable control characters.
    message = re.sub(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
        "",
        message,
    )

    # Normalise repeated whitespace.
    return " ".join(message.split())