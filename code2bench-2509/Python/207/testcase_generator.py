from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Tuple
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
def parse_expression_response(response: str, chat_id: str) -> List[Tuple[str, str, str]]:
    expressions: List[Tuple[str, str, str]] = []
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        idx_when = line.find('当"')
        if idx_when == -1:
            continue
        idx_quote1 = idx_when + 1
        idx_quote2 = line.find('"', idx_quote1 + 1)
        if idx_quote2 == -1:
            continue
        situation = line[idx_quote1 + 1 : idx_quote2]
        idx_use = line.find('使用"', idx_quote2)
        if idx_use == -1:
            continue
        idx_quote3 = idx_use + 2
        idx_quote4 = line.find('"', idx_quote3 + 1)
        if idx_quote4 == -1:
            continue
        style = line[idx_quote3 + 1 : idx_quote4]
        expressions.append((chat_id, situation, style))
    return expressions

# Strategy for generating valid lines
def valid_line_strategy():
    return st.tuples(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    ).map(lambda x: f'当"{x[0]}" 使用"{x[1]}"')

# Strategy for generating invalid lines
def invalid_line_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: f'当"{x[0]}" 使用{x[1]}'),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: f'当"{x[0]}" 使用"{x[1]}')
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    response=st.lists(st.one_of([valid_line_strategy(), invalid_line_strategy()]), min_size=1, max_size=10).map(lambda x: "\n".join(x)),
    chat_id=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
)
@example(response='当"情况1" 使用"风格1"', chat_id="chat1")
@example(response='当"情况1" 使用"风格1"\n当"情况2" 使用"风格2"', chat_id="chat2")
@example(response='当"情况1" 使用"风格1"\n无效行', chat_id="chat3")
@example(response='', chat_id="chat4")
@example(response='当"情况1" 使用"风格1"\n\n当"情况2" 使用"风格2"', chat_id="chat5")
def test_parse_expression_response(response: str, chat_id: str):
    global stop_collecting
    if stop_collecting:
        return
    
    response_copy = copy.deepcopy(response)
    chat_id_copy = copy.deepcopy(chat_id)
    try:
        expected = parse_expression_response(response_copy, chat_id_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any('当"' in line and '使用"' in line for line in response.splitlines()):
        generated_cases.append({
            "Inputs": {"response": response, "chat_id": chat_id},
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