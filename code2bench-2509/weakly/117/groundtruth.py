
from urllib.parse import urlparse

def parse_database_uri(uri):
    """Parse database URI and return connection parameters"""
    parsed = urlparse(uri)

    # Remove the driver part (postgresql+pg8000 -> postgresql)
    scheme = parsed.scheme.split('+')[0]

    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/'),
        'user': parsed.username,
        'password': parsed.password
    }