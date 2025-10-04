import urllib.parse
import base64

def _encode_auth(auth: str) -> str:
    decoded = urllib.parse.unquote(auth)
    bytes_data = decoded.encode('utf-8')
    base64_data = base64.b64encode(bytes_data)
    return base64_data.decode('utf-8').rstrip('\n')