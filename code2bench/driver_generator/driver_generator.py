import json

from code2bench import logger
from code2bench.llm.llm_caller import call_llm
from code2bench.data_model import FuncToGenerate, FuncType, GeneratedDriver
from code2bench.prompt.driver_generator import LEVEL_1_SELF_CONTAINED_DRIVER_GENERATION_PROMPT, SELF_CONTAINED_DRIVER_GENERATION_PROMPT, WEAKLY_SELF_CONTAINED_DRIVER_GENERATION_PROMPT
from code2bench.utils.json_utils import clean_response_content


class DriverGenerator:

    def __init__(self, llm=None):
        self.llm = llm

    def generate_driver(self, func: FuncToGenerate, last_driver=None, error_msg=None) -> GeneratedDriver:
        level0_base_prompt = SELF_CONTAINED_DRIVER_GENERATION_PROMPT
        level1_base_prompt = LEVEL_1_SELF_CONTAINED_DRIVER_GENERATION_PROMPT
        weakly_self_contained_base_prompt = WEAKLY_SELF_CONTAINED_DRIVER_GENERATION_PROMPT

        error_prompt = f"""
## Previous Error Information
The previously generated driver code:
{last_driver}

The previously generated driver code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the driver code accordingly, and ensure that the new driver:
1. Fixes the specific error mentioned above
2. Maintains all original differential testing requirements
3. Includes proper error handling if applicable

Remember regenerating the driver in json format shown before.
"""
        if func.func_type == FuncType.SELF_CONTAINED:
            full_prompt = level0_base_prompt + (error_prompt if error_msg else "")
            user_message = func.original_str
        elif func.func_type == FuncType.LEVEL_SELF_CONTAINED:
            full_prompt = level1_base_prompt + (error_prompt if error_msg else "")
            user_message = f"""
<func0>
{func.original_str}
</func0>
<func_self_contained>
{func.contains[0].original_str}
</func_self_contained>
"""
        elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
            full_prompt = weakly_self_contained_base_prompt + (error_prompt if error_msg else "")
            user_message = f"""
<func0>
{func.original_str}
</func0>
<lib_func>
{",".join(func.call_libs)}
</lib_func>
"""
        try:
            response = call_llm(self.llm, system_message=full_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            driver = res["Driver"]
            return GeneratedDriver(driver=driver)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating driver failed: {e}")
            return GeneratedDriver(error=str(e))


def generate_one_driver(func: FuncToGenerate, llm, last_driver=None, error_msg=None) -> GeneratedDriver:
    driver_generator = DriverGenerator(llm)
    return driver_generator.generate_driver(func, last_driver, error_msg)

def regenereate_driver(func: FuncToGenerate, llm):
    driver_generator = DriverGenerator(llm)
    return driver_generator.generate_driver(func)

if __name__ == "__main__":
    from code2bench import gpt_llm
    llm = gpt_llm
    driver_generator = DriverGenerator(llm)
    func = FuncToGenerate("def add(a: int, b: int) -> int:\n    return a + b", FuncType.SELF_CONTAINED)
    driver = driver_generator.generate_driver(func=func)
    print(driver)