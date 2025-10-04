
import urllib

import urllib.parse

def egg_info_for_url(url):
    parts = urllib.parse.urlparse(url)
    scheme, server, path, parameters, query, fragment = parts
    base = urllib.parse.unquote(path.split('/')[-1])
    if server == 'sourceforge.net' and base == 'download':  # XXX Yuck
        base = urllib.parse.unquote(path.split('/')[-2])
    if '#' in base:
        base, fragment = base.split('#', 1)
    return base, fragment