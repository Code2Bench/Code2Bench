import re
from typing import Dict, List

def parse_grounding_worldmodeling(response: str, special_token_list: List[str] = None, action_sep: str = ',', max_actions: int = 3) -> Dict:
    format_correct = True
    response_dict = {
        "llm_raw_response": response,
        "llm_response": response,
        "observation_content": "",
        "reasoning_content": "",
        "prediction_content": "",
        "think_content": "",
        "action_content": "",
        "actions": [],
        "format_correct": format_correct
    }

    # Define regex patterns for the tags
    pattern_observation = r"<observation>(.*?)</observation>"
    pattern_reasoning = r"<reasoning>(.*?)</reasoning>"
    pattern_prediction = r"<prediction>(.*?)</prediction>"
    pattern_answer = r"<answer>(.*?)</answer>"
    pattern_think = r"</think>(.*?)"

    # Extract content from the tags
    observation_match = re.search(pattern_observation, response, re.DOTALL)
    reasoning_match = re.search(pattern_reasoning, response, re.DOTALL)
    prediction_match = re.search(pattern_prediction, response, re.DOTALL)
    answer_match = re.search(pattern_answer, response, re.DOTALL)
    think_match = re.search(pattern_think, response, re.DOTALL)

    if observation_match:
        response_dict["observation_content"] = observation_match.group(1)
    else:
        format_correct = False

    if reasoning_match:
        response_dict["reasoning_content"] = reasoning_match.group(1)
    else:
        format_correct = False

    if prediction_match:
        response_dict["prediction_content"] = prediction_match.group(1)
    else:
        format_correct = False

    if answer_match:
        response_dict["action_content"] = answer_match.group(1)
    else:
        format_correct = False

    if think_match:
        response_dict["think_content"] = think_match.group(1)
    else:
        format_correct = False

    # Clean the action content by removing special tokens
    if special_token_list:
        for token in special_token_list:
            response_dict["action_content"] = response_dict["action_content"].replace(token, "")

    # Split the action content into individual actions
    if response_dict["action_content"]:
        actions = response_dict["action_content"].split(action_sep)
        response_dict["actions"] = actions[:max_actions]

    response_dict["format_correct"] = format_correct
    return response_dict