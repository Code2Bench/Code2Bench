from typing import List

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