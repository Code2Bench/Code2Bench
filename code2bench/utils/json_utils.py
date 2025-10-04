import json
import os

from code2bench import logger


def save_json(file_path: str, data: dict):
    try:
        # 获取文件所在的目录路径
        dir_path = os.path.dirname(file_path)
        
        # 如果目录不存在，则创建目录
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.exception(f"Error saving json file: {e}")

def load_json(file_path: str):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.exception(f"Error loading json file: {e}")

def clean_response_content(raw_content: str) -> str:
    """
    Removes code block markers from the response content if present.
    """
    raw_content = raw_content.strip()
    if raw_content.startswith("```"):
        first_newline = raw_content.find('\n')
        last_backticks = raw_content.rfind('```')
        if first_newline != -1 and last_backticks != -1:
            return raw_content[first_newline + 1:last_backticks].strip()
    return raw_content.strip()

def get_python_response(raw_content: str) -> str:
    if "```python" in raw_content:
        return raw_content.split("```python")[1].split("```")[0].strip()
    raise ValueError("No Python code block found in the response.")