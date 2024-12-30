import base64
import zlib
import json
from typing import Dict
import keyword
import ast
from typing import List, Dict, Tuple
import builtins

from pydantic.v1.utils import is_valid_field


class ConfigEncoder:
    @staticmethod
    def encode_config(config: Dict[str, str]) -> str:
        """
        Encodes a configuration dictionary into a compressed base64 string.
        The process:
        1. Convert dict to JSON string
        2. Compress using zlib
        3. Encode to base64
        4. Make URL-safe
        """
        # Convert dict to JSON string
        json_str = json.dumps(config, sort_keys=True)

        # Compress the string
        compressed = zlib.compress(json_str.encode('utf-8'))

        # Encode to base64 and make URL-safe
        encoded = base64.urlsafe_b64encode(compressed)

        return encoded.decode('ascii')

    @staticmethod
    def decode_config(encoded_str: str) -> Dict[str, str]:
        """
        Decodes a compressed base64 string back into a configuration dictionary.
        The process:
        1. Decode base64
        2. Decompress
        3. Parse JSON
        """
        try:
            # Decode base64
            decoded = base64.urlsafe_b64decode(encoded_str.encode('ascii'))

            # Decompress
            decompressed = zlib.decompress(decoded)

            # Parse JSON
            config = json.loads(decompressed.decode('utf-8'))

            # Validate the structure
            if not isinstance(config, dict) or not all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in config.items()
            ):
                raise ValueError("Invalid configuration structure")

            return config

        except Exception as e:
            raise ValueError(f"Invalid configuration string: {str(e)}")

class KeywordValidator:
    def __init__(self):
        self.python_words = set(keyword.kwlist)

    def get_all_python_words(self) -> set[str]:
        return self.python_words

    @staticmethod
    def validate_custom_keyword(word: str) -> tuple[bool, str]:
        if not word.isidentifier():
            return False, f"{word} is not a valid Python identifier"
        return True, ""

    def validate_mapping(self, mapping: dict[str, str]) -> tuple[bool, list[str]]:
        errors = []
        used_custom_words = set()

        for original_word, custom_word in mapping.items():
            if original_word not in self.python_words:
                errors.append(f"{original_word} is not a Python keyword.")

            is_valid, error = self.validate_custom_keyword(custom_word)
            if not is_valid:
                errors.append(error)

            if custom_word in used_custom_words:
                errors.append(f"{custom_word} is used multiple times as a custom keyword")
            used_custom_words.add(custom_word)

        return len(errors) == 0, errors
