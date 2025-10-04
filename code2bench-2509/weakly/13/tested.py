from urllib.parse import quote
import re

def convert_goofish_link(url: str) -> str:
    match = re.search(r'product_id=(\d+)', url)
    if match:
        product_id = match.group(1)
        return f'https://m.goofish.com/product/{quote(product_id)}'
    return url