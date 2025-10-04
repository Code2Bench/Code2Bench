
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    验证URL格式

    Args:
        url: URL字符串

    Returns:
        是否为有效URL
    """
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url)
        return all([
            result.scheme in ['http', 'https'],
            result.netloc,
            len(url) < 2048  # URL长度限制
        ])
    except Exception:
        return False