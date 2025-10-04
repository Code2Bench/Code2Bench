import json
import os
from typing import Dict

from code2bench import logger
from code2bench.test_runner.benchmark_runner import BaseBenchmarkRunner

class ReasoningRunner(BaseBenchmarkRunner):
    
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)
        self.benchmark_path = benchmark_path
        self.reasoning_testcases = self.load_reasoning_testcases()
    
    def load_reasoning_testcases(self):
        """加载推理基准测试用例"""
        test_case_path = os.path.join(self.benchmark_path, "test_cases", "reasoning_testcases.json")
        if not os.path.exists(test_case_path):
            raise FileNotFoundError(f"Test case file not found: {test_case_path}")
        with open(test_case_path, "r") as f:
            data = json.load(f)

        logger.info(f"Loaded {len(self.reasoning_testcases)} reasoning test cases.")
        return data
    
    def prepare_llm_input(self, groundtruth_and_case: tuple) -> Dict:
        """准备LLM输入"""
        groundtruth, case = groundtruth_and_case
        system_prompt = """You are an advanced AI assistant specialized in execution prediction and logical reasoning tasks. Your role is to analyze Python functions and predict their outputs based on given inputs through rigorous step-by-step reasoning.

## Task Instructions:
1. You will receive:
- A Python function implementation
- A test case with input parameters and description

2. Required Analysis:
- Predict the exact output through logical reasoning

## Example Input:
<Function>
def calculate_discount(price, is_member):
    if price > 100:
        if is_member:
            return price * 0.8
        return price * 0.9
    return price
</Function>

<Inputs>
- Description: Calculate final price after discount
- Inputs: {'price': 120, 'is_member': True}
</Inputs>

# Expected Output:
{
    "Answer": 80
}

# Note
"""
        user_message = f"""
<Function>
{groundtruth}
</Function>
<Inputs>
- Description: {case['Description']}
- Inputs: {case['Inputs']}
</Inputs>
"""
    
    def run_once(self, item_path: str):
        """运行一次"""
        groundtruth_path = os.path.join(item_path, "groundtruth.py")
        with open(groundtruth_path, "r") as f:
            groundtruth = f.read()
        
        for case in self.reasoning_testcases:
            self.run_item((groundtruth, case))
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证是否包含答案选项"""
        return any(opt in llm_output for opt in ["A", "B", "C", "D"])
    
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """对比标准答案"""
        with open(os.path.join(item_path, "answer.txt"), "r") as f:
            correct_answer = f.read().strip()
        
        # 提取LLM答案（简单实现）
        llm_answer = None
        for opt in ["A", "B", "C", "D"]:
            if opt in llm_output:
                llm_answer = opt
                break
                
        if not llm_answer:
            return False, "FormatError", "No valid answer found in response"
        
        is_correct = llm_answer == correct_answer
        if not is_correct:
            return False, "WrongAnswer", f"Expected {correct_answer}, got {llm_answer}"
        return True, None, None