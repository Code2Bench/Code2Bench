from typing import List, Dict, Any

def format_transcript(transcript: List[Dict[str, Any]]) -> str:
    if not transcript:
        return "(empty)"
    
    result = []
    for turn in transcript:
        round_num = turn['round']
        agent_id = turn['agent_id']
        role = turn['role']
        argument = turn.get('argument')
        answer = turn.get('answer')
        
        if argument is not None and answer is not None:
            result.append(f"[Round {round_num}] Agent#{agent_id} ({role})\nArgument: {argument}\nAnswer: {answer}\n")
        elif argument is not None:
            result.append(f"[Round {round_num}] Agent#{agent_id} ({role})\nArgument: {argument}\n")
        elif answer is not None:
            result.append(f"[Round {round_num}] Agent#{agent_id} ({role})\nArgument: \nAnswer: {answer}\n")
    
    return ''.join(result)