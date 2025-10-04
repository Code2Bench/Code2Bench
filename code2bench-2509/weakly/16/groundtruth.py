
from collections import defaultdict
import re

def extract_error_files(output):
    """
    从输出中提取错误文件列表
    Extract error files list from output
    """
    error_files = defaultdict(list)

    # 匹配错误行的正则表达式
    error_pattern = r'❌\s+([^:]+):\s*(.+)'

    lines = output.split('\n')
    for line in lines:
        match = re.match(error_pattern, line.strip())
        if match:
            file_path = match.group(1).strip()
            error_msg = match.group(2).strip()
            error_files[file_path].append(error_msg)

    return error_files