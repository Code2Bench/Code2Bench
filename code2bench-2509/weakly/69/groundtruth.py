
import difflib

def format_diff_message(optim_text: str, incr_text: str) -> str:
    """Creates a detailed diff message between two texts."""
    diff: list[str] = list(difflib.ndiff(optim_text.splitlines(), incr_text.splitlines()))

    # Collect differences
    only_in_optim: list[str] = []
    only_in_incr: list[str] = []

    for line in diff:
        if line.startswith("- "):
            only_in_optim.append(line[2:])
        elif line.startswith("+ "):
            only_in_incr.append(line[2:])

    message: list[str] = []
    if only_in_optim:
        message.append("\nOnly in optimized prompt:")
        message.extend(f"  {line}" for line in only_in_optim)

    if only_in_incr:
        message.append("\nOnly in incremental prompt:")
        message.extend(f"  {line}" for line in only_in_incr)

    return "\n".join(message)