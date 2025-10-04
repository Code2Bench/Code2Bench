

def build_csp_header(csp_config):
    """
    Build the Content Security Policy header value from the configuration.
    """
    if not csp_config:
        return None

    directives = []
    for directive, value in csp_config.items():
        if value:
            directives.append(f"{directive} {value}")
        else:
            directives.append(directive)

    return "; ".join(directives)