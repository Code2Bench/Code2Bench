import logging

from code2bench.llm.deepseek_llm import DeepSeekLLM
from code2bench.llm.qwen_llm import QwenLLM
from code2bench.utils.json_utils import clean_response_content

# Configure logging to output to a file
logging.basicConfig(filename='llm_caller.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def call_llm(llm, system_message, user_message, clean=True):
    logging.info("Calling LLM with user message: " + user_message)
    
    if isinstance(llm, DeepSeekLLM):
        response_content = llm.chat(system_message, user_message)
    elif isinstance(llm, QwenLLM):
        response_content = llm.chat(system_message, user_message)
        
    if clean:
        response_content = clean_response_content(response_content)
    
    return response_content