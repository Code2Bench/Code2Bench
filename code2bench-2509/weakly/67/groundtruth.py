from typing import Dict
import re
from typing import Dict, List

def parse_grounding_worldmodeling(response: str, special_token_list=None, action_sep=',', max_actions=3) -> Dict:
    """
    Parse response in format: <think><observation>...</observation><reasoning>...</reasoning><prediction>...</prediction></think><answer>...</answer>

    Returns a dict with keys:
    - llm_raw_response: the original response
    - llm_response: the response with all tags
    - observation_content: the content inside <observation> tag
    - reasoning_content: the content inside <reasoning> tag
    - prediction_content: the content inside <prediction> tag
    - think_content: the entire content inside <think> tag
    - action_content: the content inside <answer> tag
    - actions: a list of actions extracted from action_content
    - format_correct: whether the response strictly follows the expected format
    """
    response = response.replace("<image>", "")
    # Pattern to check for content strictly in the expected format
    strict_pattern = r'^\s*<think>\s*<observation>(.*?)</observation>\s*<reasoning>(.*?)</reasoning>\s*<prediction>(.*?)</prediction>\s*</think>\s*<answer>(.*?)</answer>\s*$'
    strict_match = re.match(strict_pattern, response.strip(), re.DOTALL)
    format_correct = strict_match is not None

    # Pattern to extract content from tags
    extraction_pattern = r'<think>\s*<observation>(.*?)</observation>\s*<reasoning>(.*?)</reasoning>\s*<prediction>(.*?)</prediction>\s*</think>\s*<answer>(.*?)</answer>'
    match = re.search(extraction_pattern, response, re.DOTALL)

    if not match:
        observation_content, reasoning_content, prediction_content, action_content, actions = "", "", "", "", []
        think_content = ""
    else:
        observation_content = match.group(1)
        reasoning_content = match.group(2)
        prediction_content = match.group(3)
        action_content = match.group(4)
        think_content = "<observation>" + observation_content + "</observation><reasoning>" + reasoning_content + "</reasoning><prediction>" + prediction_content + "</prediction>"

        if special_token_list is not None:
            for special_token in special_token_list:
                observation_content = observation_content.replace(special_token, "").strip()
                reasoning_content = reasoning_content.replace(special_token, "").strip()
                prediction_content = prediction_content.replace(special_token, "").strip()
                action_content = action_content.replace(special_token, "").strip()
                think_content = think_content.replace(special_token, "").strip()

        actions = [action.strip() for action in action_content.split(action_sep) if action.strip()]
        if len(actions) > max_actions:
            actions = actions[:max_actions]
            action_content = (" " + action_sep + " ").join(actions)

    # Reconstruct the cleaned llm_response
    llm_response = "<think>" + think_content.strip() + "</think>" + "<answer>" + action_content.strip() + "</answer>"

    return {
        "llm_raw_response": response,
        "llm_response": llm_response,
        "observation_content": observation_content,
        "reasoning_content": reasoning_content,
        "prediction_content": prediction_content,
        "think_content": think_content,
        "action_content": action_content,
        "actions": actions,
        "format_correct": format_correct
    }