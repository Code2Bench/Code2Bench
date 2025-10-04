from code2bench import logger
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.benchmark_runner import JAVA_PROMPT
from code2bench.utils.json_utils import clean_response_content


class JavaTestedGenerator:
    def __init__(self, llm, ):
        self.llm = llm

    def generate_tested(self, instruction: str):
        # Logic to generate a test based on the test_file
        system_prompt = JAVA_PROMPT
        user_message = instruction
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            return cleaned_response
        except Exception as e:
            logger.exception(f"Error generating instruction: {e}")
            return str(e)
        