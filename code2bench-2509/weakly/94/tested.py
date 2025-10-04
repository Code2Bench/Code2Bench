import base64
import json

def decode_url_params(encoded_map: dict, apply_on_keys: list = None) -> dict:
    decoded_map = {}
    if apply_on_keys is None:
        apply_on_keys = []
    
    for key in encoded_map:
        if key in apply_on_keys:
            value = encoded_map[key]
            if value.startswith('b64_'):
                # Replace URL-safe characters and add padding if necessary
                b64_str = value[4:]
                b64_str = b64_str.replace('-', '+').replace('_', '/')
                # Ensure the length is a multiple of 4
                padding = (4 - (len(b64_str) % 4)) % 4
                b64_str += '=' * padding
                try:
                    decoded_bytes = base64.b64decode(b64_str)
                    decoded_value = json.loads(decoded_bytes.decode('utf-8'))
                    decoded_map[key] = decoded_value
                except (base64.binascii.Error, json.JSONDecodeError):
                    # Handle decoding errors if needed
                    pass
    return decoded_map