import base64
import binascii
import urllib.parse

def clean_pot(po_token: str) -> str:
    # Remove any URL parameters or invalid characters
    cleaned_token = urllib.parse.unquote(po_token).split('?')[0]
    
    # Decode from URL-safe base64
    try:
        decoded_bytes = base64.urlsafe_b64decode(cleaned_token)
    except (binascii.Error, ValueError) as e:
        raise ValueError("Invalid PO Token") from e
    
    # Re-encode to URL-safe base64 to ensure proper formatting
    encoded_token = base64.urlsafe_b64encode(decoded_bytes).decode('utf-8')
    
    return encoded_token