import urllib.parse

def egg_info_for_url(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.split('/')
    base_name = ''
    fragment = parsed.fragment
    
    if parsed.netloc == 'sourceforge.net' and path_parts[-1] == 'download':
        base_name = path_parts[-2]
    else:
        base_name = path_parts[-1]
    
    return base_name, fragment