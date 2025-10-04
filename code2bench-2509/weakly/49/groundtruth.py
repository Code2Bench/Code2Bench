from typing import Optional, Tuple
from urllib.parse import urlparse

def normalize_run_path(target: str, entity: Optional[str], project: Optional[str]) -> Tuple[str, str, str]:
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 3:
            raise ValueError(f"Could not parse run information from URL: {target}")
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    parts = [p for p in target.split("/") if p]
    if len(parts) == 1:
        if not entity or not project:
            raise ValueError("Bare run ids require --entity and --project.")
        return entity, project, parts[0]

    if len(parts) >= 3:
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    raise ValueError(f"Unrecognized run target: {target}")