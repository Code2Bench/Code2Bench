from typing import Any, Dict
import json
import re

def parse_llm_response(response: str) -> Dict[str, Any]:
    """Parse LLM response and extract trading decisions"""
    try:
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Raw response: {response}")
        return {"error": "Failed to parse response", "raw_response": response}