from __future__ import annotations

import random
import string
from pathlib import Path
from typing import Any


class SimpleSubCipher:
    """Simple substitution cipher"""

    def __init__(self, chars_from: str, chars_to: str):
        if chars_from.lower() != chars_from or chars_to.lower() != chars_to:
            raise ValueError("only lowercase characters allowed in cipher")
        if '\n' in chars_from or '\n' in chars_to:
            raise ValueError("newlines not allowed in cipher")
        if not set(chars_from) == set(chars_to):
            raise ValueError("mismatch char sets")
        if not len(chars_from) == len(set(chars_from)):
            raise ValueError("chars_from has repeats")
        if not len(chars_to) == len(set(chars_to)):
            raise ValueError("chars_to has repeats")
        self._chars_from = chars_from
        self._chars_to = chars_to

    def encode(self, char: str) -> str:
        """Encode a singe character"""
        if len(char) != 1:
            raise ValueError("encode precisely one char")
        try:
            idx = self._chars_from.index(char.lower())
        except ValueError:
            return char
        encoded_char_lower = self._chars_to[idx]
        if char == char.lower():
            return encoded_char_lower
        return encoded_char_lower.upper()

    def decode(self, char: str) -> str:
        """Decode a single character"""
        if len(char) != 1:
            raise ValueError("decode precisely one char")
        try:
            idx = self._chars_to.index(char.lower())
        except ValueError:
            return char
        decoded_char_lower = self._chars_from[idx]
        if char == char.lower():
            return decoded_char_lower
        return decoded_char_lower.upper()

    def serialize(self) -> str:
        """Serialize the cipher itself"""
        return self._chars_from + '\n' + self._chars_to

    def __eq__(self, __value: SimpleSubCipher) -> bool:
        return self._chars_from == __value._chars_from and self._chars_to == __value._chars_to


def generate_simple_sub_cipher(
        chars: str = string.ascii_lowercase
) -> SimpleSubCipher:
    """Create a new cipher"""
    chars_list = list(chars)
    random.shuffle(chars_list)
    return SimpleSubCipher(chars, ''.join(chars_list))


def generate_seeded_sub_cipher(
        seed: Any,
        chars: str = string.ascii_lowercase
) -> SimpleSubCipher:
    """Create a new cipher generated with the given seed."""
    random.seed(seed)
    shufled_chars = list(chars)
    random.shuffle(shufled_chars)
    return SimpleSubCipher(chars, ''.join(shufled_chars))


def encode_simple_sub_cipher(cipher: SimpleSubCipher, input: str) -> str:
    """Encode a string using a simple substitution cipher"""
    out = ''
    for c in input:
        out += cipher.encode(c)
    return out


def decode_simple_sub_cipher(cipher: SimpleSubCipher, input: str) -> str:
    """Decode a string using a simple substitution cipher"""
    out = ''
    for c in input:
        out += cipher.decode(c)
    return out


def save_simple_sub_cipher(cipher: SimpleSubCipher, path: Path):
    """Persist a simple substitution cipher to disk"""
    if path.exists():
        raise ValueError(f"path {path} already exists")
    with path.open('w') as f:
        f.write(cipher.serialize())


def load_simple_sub_cipher(path: Path) -> SimpleSubCipher:
    """Read a simple substitution cipher from disk"""
    with path.open() as f:
        lines = f.readlines()
        if len(lines) != 2:
            raise ValueError("invalid serialization")
    chars_from = lines[0].strip()
    chars_to = lines[1].strip()
    return SimpleSubCipher(chars_from, chars_to)
