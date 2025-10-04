from typing import List, Dict, Any

def collect_round_candidates(transcript: List[Dict[str, Any]], num_agents: int, round_index: int) -> List[Dict[str, str]]:
    result = []
    for agent in transcript:
        if agent['round'] == str(round_index):
            text = agent.get('answer', agent.get('argument', ""))
            if text:
                result.append({'agent_id': agent['agent_id'], 'text': text})
                if len(result) == num_agents:
                    break
    return result