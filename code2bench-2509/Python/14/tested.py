def convert_url(url: str) -> str:
    # Check if the URL ends with /mcp or /mcp/
    if url.endswith('/mcp') or url.endswith('/mcp/'):
        return url
    # Check if the URL ends with /sse
    if url.endswith('/sse'):
        return url.replace('/sse', '/mcp/')
    # Append /mcp/ to the URL
    return url + '/mcp/'