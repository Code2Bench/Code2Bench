from typing import List, Dict, Any
import datetime

def generate_test_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    timestamp = datetime.datetime.now().isoformat()
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result["success"])
    failed_tests = total_tests - passed_tests
    total_execution_time = sum(result["execution_time"] for result in test_results)
    average_execution_time = total_execution_time / total_tests if total_tests > 0 else 0
    
    summary = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "total_execution_time": total_execution_time,
        "average_execution_time": average_execution_time
    }
    
    return {
        "timestamp": timestamp,
        "summary": summary,
        "test_results": test_results
    }