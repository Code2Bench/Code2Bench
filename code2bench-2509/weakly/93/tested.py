import base64
import json

def encode_url_params(decoded_map: dict, apply_on_keys: list = None) -> dict:
    if apply_on_keys is None:
        apply_on_keys = []
    
    encoded_map = decoded_map.copy()
    
    for key in apply_on_keys:
        if key in encoded_map:
            value = encoded_map[key]
            json_str = json.dumps(value)
            bytes_data = json_str.encode('utf-8')
            base64_bytes = base64.urlsafe_b64encode(bytes_data)
            url_safe_str = base64_bytes.decode('utf-8').rstrip('=')
            encoded_map[f"b64_{key}"] = url_safe_str
    
    return encoded_map