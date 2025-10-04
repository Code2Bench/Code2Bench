from typing import List, Dict, Any

def collect_last_round_candidates(transcript: List[Dict[str, Any]], num_agents: int, last_round_index: int) -> List[Dict[str, Any]]:
    result = []
    for agent in range(num_agents):
        agent_id = f"agent_{agent}"
        # Find the last record for this agent in the last round
        last_record = None
        for record in transcript:
            if record['agent_id'] == agent_id and record['round'] == last_round_index:
                last_record = record
                break
        if last_record:
            text = last_record.get('answer', last_record.get('argument'))
            if text:
                result.append({'agent_id': agent_id, 'text': text})
    return result