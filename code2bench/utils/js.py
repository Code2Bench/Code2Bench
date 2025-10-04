import re

from code2bench.llm.llm_caller import call_llm
from code2bench import llm_client

def convert_python_docstring_to_js_doc(docstring):
    prompt = """
请严格按照以下规则将Python docstring转换为JSDoc格式，保持原始内容不变：

# 转换规则
1. 整体结构：
   - 输入内容直接包裹在/** 和 */之间
   - 每行前缀添加" * "
   - 保留原始空行（转换为" *"）

2. 标签转换：
   | Python标签 | JSDoc标签    | 转换规则                                                                 |
   |-----------|-------------|--------------------------------------------------------------------------|
   | Args:     | @param      | 保持参数描述原样，每行独立转换（例：`base: 描述...` → `@param {any} base - 描述...`）|
   | Returns:  | @returns    | 保持返回值描述原样，强制添加{any}类型                                    |
   | Raises:   | @throws     | 保持异常描述原样（例：`ValueError: 描述` → `@throws {ValueError} 描述`）|

3. 特别处理：
   - 保留所有原始换行和缩进
   - 不修改任何描述内容（包括标点符号、换行符、特殊字符）
   - 非标准段落（如"Special rules:"）直接保留为注释
   - 参数强制添加默认类型：{any}

# 输入示例
\"\"\"Recursively merge two JSON-like objects.

Args:
    base: A JSON-like object (can be dict/list)
    update: Update structure

Returns:
    New merged object

Raises:
    ValueError: If types incompatible

Special rules:
    - Dictionary merge
    - List concat
\"\"\"

# 期望输出
/**
 * Recursively merge two JSON-like objects.
 * 
 * @param {any} base - A JSON-like object (can be dict/list)
 * @param {any} update - Update structure
 * @returns {any} New merged object
 * @throws {ValueError} If types incompatible
 * 
 * Special rules:
 * - Dictionary merge
 * - List concat
 */    
"""
    res = call_llm(llm=llm_client, system_message=prompt, user_message=docstring)
    return res