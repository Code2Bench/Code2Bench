import base64

def base64_decode(url_content: str) -> str:
    # Replace URL-safe characters
    url_content = url_content.replace('-', '+').replace('_', '/')
    # Ensure the length is a multiple of 4
    padding = len(url_content) % 4
    if padding != 0:
        url_content += '=' * (4 - padding)
    # Decode the Base64 content
    try:
        decoded_bytes = base64.b64decode(url_content, validate=True)
        return decoded_bytes.decode('utf-8')
    except base64.binascii.Error:
        return decoded_bytes.hex()