
from urllib.parse import quote
import re

def convert_goofish_link(url: str) -> str:
    """
    将Goofish商品链接转换为只包含商品ID的手机端格式。
    """
    match_first_link = re.search(r'item\?id=(\d+)', url)
    if match_first_link:
        item_id = match_first_link.group(1)
        bfp_json = f'{{"id":{item_id}}}'
        return f"https://pages.goofish.com/sharexy?loadingVisible=false&bft=item&bfs=idlepc.item&spm=a21ybx.item.0.0&bfp={quote(bfp_json)}"
    return url