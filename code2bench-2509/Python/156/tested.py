from typing import List

def build_summary_request_text(retain_count: int, evicted_messages: List[str], in_context_messages: List[str]) -> str:
    result = []
    
    # Primary instruction based on retain_count
    if retain_count == 0:
        result.append("The AI is about to forget all prior messages.")
    else:
        result.append(f"The AI should retain up to {retain_count} messages.")
    
    # Section for evicted messages
    if evicted_messages:
        result.append(f"Evicted messages: {evicted_messages}")
    
    # Section for in-context messages
    if retain_count > 0 and in_context_messages:
        result.append(f"In-context messages: {in_context_messages}")
    
    return "\n".join(result)