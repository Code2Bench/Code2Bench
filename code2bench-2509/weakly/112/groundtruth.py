from typing import Any, Dict, List
from datetime import datetime

def generate_test_report(
    test_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate a test report in JSON format.

    Args:
        test_results: List of test results

    Returns:
        Dict containing the test report
    """
    total_tests = len(test_results)
    passed_tests = sum(
        1 for result in test_results if result["success"]
    )
    failed_tests = total_tests - passed_tests
    total_time = sum(
        result["execution_time"] for result in test_results
    )

    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "total_execution_time": total_time,
            "average_execution_time": (
                total_time / total_tests if total_tests > 0 else 0
            ),
        },
        "test_results": test_results,
    }

    return report