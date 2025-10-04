from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
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

# Strategy for generating code-like lines
def line_strategy():
    return st.one_of([
        # Import statements
        st.tuples(
            st.one_of([st.just("import "), st.just("from "), st.just("sys.path."), st.just("load_dotenv(")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: "".join(x)),
        # Docstrings
        st.tuples(
            st.one_of([st.just('"""'), st.just("'''")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.one_of([st.just('"""'), st.just("'''")])
        ).map(lambda x: "".join(x)),
        # Comments
        st.tuples(
            st.just("#"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: "".join(x)),
        # Empty lines
        st.just(""),
        # Non-import statements
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(lines=st.lists(line_strategy(), min_size=1, max_size=20, unique=True))
@example(lines=["import os"])
@example(lines=["from sys import path"])
@example(lines=["sys.path.append('/path')"])
@example(lines=["load_dotenv()"])
@example(lines=['"""Docstring"""', "import os"])
@example(lines=["# Comment", "import os"])
@example(lines=["", "import os"])
@example(lines=["import os", "def func(): pass"])
def test_find_import_section_end(lines: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    lines_copy = copy.deepcopy(lines)
    try:
        expected = find_import_section_end(lines_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(
        line.strip().startswith('import ') or 
        line.strip().startswith('from ') or
        line.strip().startswith('sys.path.') or
        line.strip().startswith('load_dotenv(')
        for line in lines
    ):
        generated_cases.append({
            "Inputs": {"lines": lines},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)