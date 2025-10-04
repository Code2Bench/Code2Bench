import json
import re
import base64

def voe_decode(ct: str, luts: str) -> dict:
    # Escape special characters in the lookup table
    escaped_luts = re.escape(luts)
    # Compile the regex pattern for removing patterns
    pattern = re.compile(escaped_luts)
    # Remove patterns from the ciphertext
    cleaned_ct = pattern.sub('', ct)
    # Apply character shifts (example: shift each character by 1)
    shifted_ct = ''.join([chr(ord(c) + 1) for c in cleaned_ct])
    # Decode using base64
    decoded_bytes = base64.b64decode(shifted_ct)
    decoded_str = decoded_bytes.decode('utf-8')
    # Apply final character shift and decode again
    final_shifted = ''.join([chr(ord(c) + 1) for c in decoded_str])
    final_decoded_bytes = base64.b64decode(final_shifted)
    final_decoded_str = final_decoded_bytes.decode('utf-8')
    # Parse as JSON object
    return json.loads(final_decoded_str)