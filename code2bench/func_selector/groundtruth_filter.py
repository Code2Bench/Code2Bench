import json

from code2bench import logger, config
from code2bench.data_model import FuncToGenerate, FuncType
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.groundtruth_filter import GROUNG_TRUTH_FILTER_PROMPT, WEAKLY_GROUNG_TRUTH_FILTER_PROMPT
from code2bench.utils.json_utils import clean_response_content


class GroundTruthFilter:
    def __init__(self, llm):
        self.llm = llm
        
    def llm_filter(self, func: FuncToGenerate, last_result=None, last_error=None):
        error_prompt = (
            f"Please check the last result: {last_result} and provide a suitable answer. "
            f"Error response: {last_error}."
        ) if last_result and last_error else ""
        
        if config.MODE == FuncType.SELF_CONTAINED:
            system_prompt = GROUNG_TRUTH_FILTER_PROMPT
            user_message = func.original_str + error_prompt
        elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
            system_prompt = WEAKLY_GROUNG_TRUTH_FILTER_PROMPT
            user_message = (
                f"Function: {func.original_str}\n"
                f"Function calls: {func.call_libs}\n"
            )
            user_message = user_message + error_prompt
        
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            return res.get("Suitable"), res.get("Reason")
        except Exception as e:
            logger.exception(f"Error generating instruction: {e}")
            return cleaned_response, str(e)

    def length_filter(self, func: FuncToGenerate):
        max_length = 100
        min_length = 5 
        func_length = len(func.original_str.splitlines())
      
        if func_length > max_length:
            return False, f"Function string exceeds maximum length of {max_length} characters."
        elif func_length < min_length:
            return False, f"Function string is shorter than minimum length of {min_length} characters."
        return True, ""
    

def filter_groundtruth(func: FuncToGenerate, llm):
    # Initialize the filter
    groundtruth_filter = GroundTruthFilter(llm)
    
    # length_filter
    is_valid, error_message = groundtruth_filter.length_filter(func)
    if not is_valid:
        return False, error_message
    
    # llm_filter
    
    cnt = 0
    max_retry = 3
    last_result = None
    last_error = None
    # Retry the LLM filter a few times in case of transient errors
    while cnt < max_retry:
        cnt += 1
        try:
            is_valid, reason = groundtruth_filter.llm_filter(func, last_result, last_error)
        
            if is_valid in [True, False]:
                return is_valid is True, reason
            
            last_result = is_valid
            last_error = reason
        except Exception as e:
            logger.exception(f"Error generating instruction: {e}")
            return False, str(e)
    
    return False, "Max retries exceeded."


if __name__ == "__main__":
    pass
