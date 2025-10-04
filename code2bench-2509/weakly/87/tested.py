from urllib.parse import urlunsplit, urlsplit

def metadata_url_for_resource(resource_url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(resource_url)
    if path:
        new_path = f"{path}"
    else:
        new_path = ""
    new_netloc = f"{netloc}/.well-known/oauth-protected-resource"
    return urlunsplit((scheme, new_netloc, new_path, query, fragment))