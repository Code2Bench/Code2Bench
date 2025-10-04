from typing import List

def find_import_section_end(lines: List[str]) -> int:
    """找到import语句结束的位置"""
    import_end = 0
    in_docstring = False
    docstring_char = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 处理文档字符串
        if not in_docstring:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                docstring_char = stripped[:3]
                if stripped.count(docstring_char) == 1:  # 开始文档字符串
                    in_docstring = True
                # 如果同一行包含开始和结束，则不进入文档字符串状态
        else:
            if docstring_char in stripped:
                in_docstring = False
                continue

        if in_docstring:
            continue

        # 跳过注释和空行
        if not stripped or stripped.startswith('#'):
            continue

        # 检查是否是import语句
        if (stripped.startswith('import ') or 
            stripped.startswith('from ') or
            stripped.startswith('sys.path.') or
            stripped.startswith('load_dotenv(')):
            import_end = i + 1
        elif stripped and not stripped.startswith('#'):
            # 遇到非import语句，停止
            break

    return import_end