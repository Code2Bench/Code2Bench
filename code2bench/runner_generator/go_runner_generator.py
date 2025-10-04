
import json
from typing import Tuple

from code2bench import logger
from code2bench.data_model import GeneratedDriver
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.runner_generator import GO_RUNNER_GENERATOR_PROMPT
from code2bench.utils.json_utils import clean_response_content


class GoRunnerGenerator:
    def __init__(self, llm):
        self.llm = llm
    
    def generate_runner(self, python_runner: str, testcases_str: str, last_runner=None, error_msg=None) -> Tuple[GeneratedDriver, str]:
        system_prompt = GO_RUNNER_GENERATOR_PROMPT
        error_prompt = f"""
## Previous Error Information
The previously generated runner code:
{last_runner.driver}

The previously generated runner code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the runner code, and provide the updated runner code.
""" if last_runner else ""
        system_prompt = system_prompt.replace("{", "{{").replace("}", "}}")
        system_prompt = system_prompt.format(testcases_str=testcases_str)
        user_message = python_runner + error_prompt
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            code, signature = self.parse_llm_response(response)
            # res = json.loads(cleaned_response)
            # driver = res["JSONLoader"]
            return GeneratedDriver(driver=code), signature
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating driver failed: {e}")
            return GeneratedDriver(error=str(e)), ""
        
    def parse_llm_response(self, response: str):
        """
        Parses the LLM response to extract the code and signature parts.

        LLM response format:
        <code>
        ```go
        package main
        ...
        ```
        </code>
        <signature>
        ```go
        func main() {
            // Your code here
        }
        ```
        </signature>

        Returns:
        - code: The extracted code without the ```go markers.
        - signature: The extracted signature without the ```go markers.
        """
        def clean_code_block(block: str) -> str:
            """Removes ```go markers from the code block."""
            if block.startswith("```go"):
                block = block[len("```go"):].strip()
            if block.endswith("```"):
                block = block[:-len("```")].strip()
            return block

        # Extract code and signature parts
        code_start = response.find("<code>") + len("<code>")
        code_end = response.find("</code>")
        signature_start = response.find("<signature>") + len("<signature>")
        signature_end = response.find("</signature>")

        # Validate the response format
        if code_start == -1 or code_end == -1 or signature_start == -1 or signature_end == -1:
            raise ValueError("Invalid response format. Missing code or signature tags.")

        # Extract and clean the code and signature
        code = response[code_start:code_end].strip()
        signature = response[signature_start:signature_end].strip()

        # Remove ```go markers
        code = clean_code_block(code)
        signature = clean_code_block(signature)

        return code, signature