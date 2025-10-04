
import base64
import json

def encode_url_params(decoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    encoded_map = {}
    for key, value in decoded_map.items():
        if key in apply_on_keys:
            # This manual base64 encoding could be simplified with base64.urlsafe_b64encode.
            # It's kept here to match the javascript implementation.
            json_str = json.dumps(value, separators=(",", ":"))
            encoded_bytes = base64.b64encode(json_str.encode("utf-8"))
            encoded_str = encoded_bytes.decode("utf-8").replace("+", "-").replace("/", "_").rstrip("=")
            encoded_map[key] = "b64_" + encoded_str
    return encoded_map