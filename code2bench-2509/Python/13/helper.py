from unicodedata import normalize
import math

def deep_compare(a, b, tolerance=1e-6):
    """递归深度比较，自动处理Unicode规范化"""
    # 处理字符串类型（关键改动：添加Unicode规范化）
    if isinstance(a, str) and isinstance(b, str):
        return normalize('NFC', a) == normalize('NFC', b)
    
    # 处理浮点数类型（原逻辑保留）
    if isinstance(a, float) and isinstance(b, float):
        return math.isclose(a, b, abs_tol=tolerance)
    
    # 处理字典类型（原逻辑保留，但递归调用会应用Unicode规范化）
    if isinstance(a, dict) and isinstance(b, dict):
        return all(
            k in b and deep_compare(a[k], b[k], tolerance)
            for k in a
        ) and len(a) == len(b)
    
    # 处理列表类型（原逻辑保留，递归调用会应用Unicode规范化）
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(
            deep_compare(ai, bi, tolerance)
            for ai, bi in zip(a, b)
        )
    
    # 其他类型保持严格相等比较（包括DataFrame的列名和内容）
    return a == b