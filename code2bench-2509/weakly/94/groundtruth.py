
import base64
import json

def decode_url_params(encoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    decoded_map = {}
    for key, val in encoded_map.items():
        if val.startswith("b64_") and key in apply_on_keys:
            try:
                # This manual base64 decoding could be simplified with base64.urlsafe_b64decode.
                # It's kept here to match the javascript implementation.
                base64_str = val[4:].replace("-", "+").replace("_", "/")
                base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
                binary_data = base64.b64decode(base64_str)
                json_str = binary_data.decode("utf-8")
                decoded_map[key] = json.loads(json_str)
            except Exception as e:
                print(f"Failed to decode URL parameter: {key}, {val} - {e}")  # noqa
    return decoded_map