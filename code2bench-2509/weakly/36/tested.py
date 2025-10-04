from urllib.parse import urlparse
from typing import Dict

def parse_pg_uri(uri: str) -> Dict[str, str]:
    parsed = urlparse(uri)
    host = parsed.hostname or 'localhost'
    port = parsed.port or 5432
    user = parsed.username or 'mirix'
    database = parsed.path[1:] if parsed.path else 'mirix'
    return {
        'host': host,
        'port': str(port),
        'user': user,
        'database': database
    }