from typing import List

def build_summary_request_text(retain_count: int, evicted_messages: List[str], in_context_messages: List[str]) -> str:
    parts: List[str] = []
    if retain_count == 0:
        parts.append(
            "You’re a memory-recall helper for an AI that is about to forget all prior messages. Scan the conversation history and write crisp notes that capture any important facts or insights about the conversation history."
        )
    else:
        parts.append(
            f"You’re a memory-recall helper for an AI that can only keep the last {retain_count} messages. Scan the conversation history, focusing on messages about to drop out of that window, and write crisp notes that capture any important facts or insights about the human so they aren’t lost."
        )

    if evicted_messages:
        parts.append("\n(Older) Evicted Messages:")
        for item in evicted_messages:
            parts.append(f"    {item}")

    if retain_count > 0 and in_context_messages:
        parts.append("\n(Newer) In-Context Messages:")
        for item in in_context_messages:
            parts.append(f"    {item}")

    return "\n".join(parts) + "\n"