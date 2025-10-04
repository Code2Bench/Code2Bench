from urllib.parse import urlparse

def parse_database_uri(uri: str) -> dict:
    parsed = urlparse(uri)
    scheme = parsed.scheme.split('+')[0]
    netloc = parsed.netloc
    path = parsed.path.lstrip('/')
    
    host_port = netloc.split(':') if ':' in netloc else [netloc, None]
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 and host_port[1].isdigit() else 5432
    
    params = parsed.query
    if params:
        params_dict = dict(pair.split('=') for pair in params.split('&'))
        user = params_dict.get('user')
        password = params_dict.get('password')
        database = params_dict.get('database', path)
    else:
        user = None
        password = None
        database = path
    
    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }