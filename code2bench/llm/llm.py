from abc import ABC, abstractmethod

class LLM(ABC):
    
    @abstractmethod
    def chat(self, system_prompt, user_input, max_tokens, stream=False):
        raise NotImplementedError
