import base64
import zlib
import json
from typing import Dict


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