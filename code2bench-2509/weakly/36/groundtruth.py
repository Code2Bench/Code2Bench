from typing import Dict
from urllib.parse import urlparse

def parse_pg_uri(uri: str) -> Dict[str, str]:
    """Parse PostgreSQL URI and extract connection details."""
    parsed = urlparse(uri)
    return {
        'host': parsed.hostname or 'localhost',
        'port': str(parsed.port or 5432),
        'user': parsed.username or 'mirix',
        'database': parsed.path.lstrip('/') or 'mirix'
    }