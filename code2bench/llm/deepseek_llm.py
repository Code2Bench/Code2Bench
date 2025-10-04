from openai import OpenAI
from dotenv import load_dotenv
import os

from code2bench.llm.llm import LLM

# Load environment variables from .env file
load_dotenv()
API_BASE = os.getenv("API_BASE")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("API_KEY")

class DeepSeekLLM(LLM):
    def __init__(self, api_key=API_KEY, api_base=API_BASE):
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        self.model_name = MODEL_NAME
        self.temperature = 0
    
    def __str__(self) -> str:
        return self.model_name

    def chat(self, system_prompt, user_input, max_tokens=4096, stream=True):
        history_openai_format = [{"role": "system", "content": system_prompt}]
        history_openai_format.append({"role": "user", "content": user_input})
        
        response_stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=history_openai_format,
            max_tokens=max_tokens,
            temperature=self.temperature,
            stream=stream,
        )
        
        if stream:
            return self._process_stream(response_stream)
        else:
            return response_stream.choices[0].message.content

    def _process_stream(self, stream):
        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_response += content
        print("\n")
        return full_response
    
if __name__ == "__main__":
    # Example usage
    deepseek_llm = DeepSeekLLM()
    response = deepseek_llm.chat(
        system_prompt="You are a helpful assistant",
        user_input="Hello",
        stream=False,
    )
    print("Final Response:", response)