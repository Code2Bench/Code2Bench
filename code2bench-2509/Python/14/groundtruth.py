

def convert_url(url: str) -> str:
    """Normalize an MCP server URL.

    - If it ends with `/sse`, replace with `/mcp`.
    - If it ends with `/mcp` already, leave it.
    - Otherwise, append `/mcp`.

    Args:
        url: The input server URL.

    Returns:
        str: Normalized MCP URL.

    Examples:
        >>> convert_url("http://localhost:4444/servers/uuid")
        'http://localhost:4444/servers/uuid/mcp/'
        >>> convert_url("http://localhost:4444/servers/uuid/sse")
        'http://localhost:4444/servers/uuid/mcp/'
        >>> convert_url("http://localhost:4444/servers/uuid/mcp")
        'http://localhost:4444/servers/uuid/mcp/'
    """
    if url.endswith("/mcp") or url.endswith("/mcp/"):
        if url.endswith("/mcp"):
            return url + "/"
        return url
    if url.endswith("/sse"):
        return url.replace("/sse", "/mcp/")
    return url + "/mcp/"