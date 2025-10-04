

def collect_round_candidates(
    transcript: list, num_agents: int, round_index: int
) -> list:
    """Collect candidates from specified round (prioritizes answer, falls back to argument)."""
    candidates = []
    for agent_id in range(num_agents):
        records = [
            t for t in transcript if t.get("agent_id") == agent_id and t.get("round") == round_index
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