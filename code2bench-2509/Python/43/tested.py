from typing import Union

def to_data_url(image_str: str) -> str:
    if image_str and isinstance(image_str, str):
        if image_str.startswith('data:') or image_str.startswith('http://') or image_str.startswith('https://'):
            return image_str
        if image_str.startswith('base64,'):
            # Convert base64 string to data URL with image/png MIME type
            import base64
            encoded_data = image_str.split(',', 1)[1]
            decoded_data = base64.b64decode(encoded_data)
            return f'data:image/png;base64,{decoded_data.decode("utf-8")}'
        return f'data:image/png;base64,{image_str}'
    return image_str