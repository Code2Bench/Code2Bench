from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_context_factors(user_query: str) -> List[str]:
    """
    从用户查询中提取上下文因子

    Args:
        user_query: 用户查询

    Returns:
        上下文因子列表
    """
    query_lower = user_query.lower()
    factors = []

    # 技术关键词
    tech_keywords = {
        'api': 'api_related',
        '数据库': 'database_related',
        '网络': 'network_related',
        '文件': 'file_related',
        '爬虫': 'scraping_related',
        '分析': 'analysis_related',
        '机器学习': 'ml_related',
        '实时': 'real_time',
        '高性能': 'high_performance',
        '安全': 'security_related'
    }

    for keyword, factor in tech_keywords.items():
        if keyword in query_lower:
            factors.append(factor)

    # 复杂度关键词
    complexity_keywords = {
        '复杂': 'high_complexity',
        '简单': 'low_complexity',
        '快速': 'speed_critical',
        '稳定': 'stability_critical',
        '优化': 'optimization_needed'
    }

    for keyword, factor in complexity_keywords.items():
        if keyword in query_lower:
            factors.append(factor)

    return factors

# Strategy for generating user queries
def user_query_strategy():
    tech_keywords = ['api', '数据库', '网络', '文件', '爬虫', '分析', '机器学习', '实时', '高性能', '安全']
    complexity_keywords = ['复杂', '简单', '快速', '稳定', '优化']
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=50
    ).map(lambda s: ' '.join([s] + st.lists(
        st.sampled_from(tech_keywords + complexity_keywords),
        min_size=0,
        max_size=5
    ).example()))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(user_query=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50))
@example(user_query="api 数据库")
@example(user_query="复杂 机器学习")
@example(user_query="简单 安全")
@example(user_query="快速 高性能")
@example(user_query="稳定 优化")
@example(user_query="网络 文件")
@example(user_query="爬虫 分析")
@example(user_query="实时 高性能")
@example(user_query="安全 复杂")
@example(user_query="优化 简单")
def test_extract_context_factors(user_query: str):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = extract_context_factors(user_query)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"user_query": user_query},
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