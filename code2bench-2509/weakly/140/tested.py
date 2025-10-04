from base64 import urlsafe_b64decode

def str_from_base64url(base64url: str) -> str:
    # Ensure the string has proper padding
    padding = len(base64url) % 4
    if padding != 0:
        base64url += '=' * (4 - padding)
    return urlsafe_b64decode(base64url).decode('utf-8')