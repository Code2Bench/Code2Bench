

def collect_last_round_candidates(
    transcript: list, num_agents: int, last_round_index: int
) -> list:
    """Collect candidates from the last round of debate.

    Returns list of [{"agent_id": int, "text": str}].
    Prioritizes answer field; falls back to argument if no valid answer.
    """
    candidates = []
    for agent_id in range(num_agents):
        # Find the agent's record in the last round (if multiple, take the last one)
        records = [
            t for t in transcript if t.get("agent_id") == agent_id and t.get("round") == last_round_index
        ]
        if not records:
            continue
        rec = records[-1]
        ans = (rec.get("answer") or "").strip()
        arg = (rec.get("argument") or "").strip()
        text = ans if ans else arg
        if text:
            candidates.append({"agent_id": agent_id, "text": text})
    return candidates