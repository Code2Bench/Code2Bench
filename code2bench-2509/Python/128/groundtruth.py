

def format_transcript(transcript: list) -> str:
    """Format debate transcript for display."""
    if not transcript:
        return "(empty)"
    lines = []
    for turn in transcript:
        agent = turn.get("agent_id")
        rd = turn.get("round")
        role = turn.get("role")
        arg = (turn.get("argument") or "").strip()
        ans = (turn.get("answer") or "").strip()
        if ans:
            lines.append(f"[Round {rd}] Agent#{agent} ({role})\nArgument: {arg}\nAnswer: {ans}\n")
        else:
            lines.append(f"[Round {rd}] Agent#{agent} ({role})\nArgument: {arg}\n")
    return "\n".join(lines)