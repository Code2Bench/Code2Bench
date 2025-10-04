import os
import json
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from code2bench.llm.llm import LLM

# Load environment variables from .env file
load_dotenv()

# Qwen model configuration
# MODEL = "qwen-plus-2025-04-28"  # 更新为最新模型
# MODEL_NAME = "Qwen/qwen-plus"
# MODEL = "qwen3-235b-a22b"
# MODEL_NAME = "Qwen/qwen3-235b-a22b"
# MODEL = "qwen3-235b-a22b"
# MODEL_NAME = "Qwen/qwen3-235b-a22b-thinking"
# MODEL = "qwen3-32b"
# MODEL_NAME = "Qwen/qwen3-32b"
MODEL = "qwen3-8b"
MODEL_NAME = "Qwen/qwen3-8b"
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class QwenLLM(LLM):
    def __init__(self, api_key=None, api_base=API_BASE):
        if api_key is None:
            api_key = os.getenv("DASHSCOPE_API_KEY")
            # api_key = os.getenv("GEMINI_API_KEY")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        self.model_name = MODEL_NAME
        self.temperature = 0
        self.show_thinking = True  # 是否显示思考过程
        
        # 添加计时记录
        self.timing_log_file = f"qwen_timing_log_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(self.timing_log_file, "a") as f:
            f.write(f"=== 新会话开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"模型: {self.model_name}\n\n")
    
    def __str__(self) -> str:
        return self.model_name

    def chat(self, system_prompt, user_input, model=MODEL, max_tokens=4096, temperature=0.1, stream=True, enable_thinking=False):
        # 开始计时
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        
        # 为Qwen模型添加特殊参数配置
        extra_body = {"enable_thinking": enable_thinking}
        
        try:
            # 计算API调用时间开始
            api_start_time = time.time()
            
            response_stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=self.temperature,
                stream=stream,
                extra_body=extra_body,
            )
            
            # 计算API调用时间
            api_call_time = time.time() - api_start_time
            
            if stream:
                # 流式处理开始时间
                # stream_start_time = time.time()
                result = self._process_stream(response_stream)
                # stream_time = time.time() - stream_start_time
                # total_time = time.time() - start_time
                
                # # 记录时间
                # self._log_timing(user_input[:100], api_call_time, stream_time, total_time, len(result))
                
                return result
            else:
                # 非流式输出不支持思考过程
                result = response_stream.choices[0].message.content
                
                # 计算总时间
                total_time = time.time() - start_time
                
                # # 记录时间
                # self._log_timing(user_input[:100], api_call_time, 0, total_time, len(result))
                
                return result
                
        except Exception as e:
            # 计算错误发生时的总时间
            error_time = time.time() - start_time
            
            # 记录错误
            with open(self.timing_log_file, "a") as f:
                f.write(f"错误 ({datetime.now().strftime('%H:%M:%S')}): {str(e)}\n")
                f.write(f"用时: {error_time:.2f}s\n\n")
            
            print(f"Error during API call: {str(e)}")
            return f"Error: {str(e)}"

    def _process_stream(self, stream):
        """处理流式响应，分离思考过程和最终回答"""
        reasoning_content = ""  # 完整思考过程
        answer_content = ""  # 完整回复
        is_answering = False  # 是否进入回复阶段
        
        if self.show_thinking:
            print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
        
        for chunk in stream:
            if not chunk.choices:
                # 可能包含usage信息
                if hasattr(chunk, "usage") and self.show_thinking:
                    print("\nToken使用情况:")
                    print(chunk.usage)
                continue
            
            delta = chunk.choices[0].delta
            
            # 处理思考内容
            if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                if self.show_thinking and not is_answering:
                    print(delta.reasoning_content, end="", flush=True)
                reasoning_content += delta.reasoning_content
            
            # 处理回复内容
            if hasattr(delta, "content") and delta.content:
                if not is_answering:
                    if self.show_thinking:
                        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                
                print(delta.content, end="", flush=True)
                answer_content += delta.content
        
        print("\n")
        return answer_content
    
    def _log_timing(self, query, api_time, stream_time, total_time, response_length):
        """记录调用时间到文件"""
        with open(self.timing_log_file, "a") as f:
            f.write(f"时间 ({datetime.now().strftime('%H:%M:%S')})\n")
            f.write(f"查询: {query}...\n")
            f.write(f"API调用时间: {api_time:.2f}s\n")
            if stream_time > 0:
                f.write(f"流处理时间: {stream_time:.2f}s\n")
            f.write(f"总时间: {total_time:.2f}s\n")
            f.write(f"响应长度: {response_length} 字符\n\n")
    
    def set_show_thinking(self, value):
        """设置是否显示思考过程"""
        self.show_thinking = value


if __name__ == "__main__":
    # Example usage
    qwen_llm = QwenLLM()
    
    # 测试流式输出（带思考过程）
    print("===== 测试流式输出 =====")
    response1 = qwen_llm.chat(
        system_prompt="You are a helpful assistant.",
        user_input="用最简单的方式解释爱因斯坦的质能方程E=mc²",
        stream=True
    )
    
    print("\n\n===== 关闭思考过程 =====")
    qwen_llm.set_show_thinking(False)
    response3 = qwen_llm.chat(
        system_prompt="You are a helpful assistant.",
        user_input="你好，请介绍一下自己",
        stream=True
    )