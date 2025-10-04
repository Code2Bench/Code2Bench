from urllib.parse import urlparse
from typing import Optional, Tuple

def normalize_run_path(target: str, entity: Optional[str], project: Optional[str]) -> Tuple[str, str, str]:
    if target.startswith("http://") or target.startswith("https://"):
        parsed = urlparse(target)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 3:
            raise ValueError("Invalid URL format for run path.")
        return path_parts[0], path_parts[1], path_parts[2]
    else:
        parts = target.strip("/").split("/")
        if len(parts) < 3:
            if entity is None or project is None:
                raise ValueError("Bare run ID requires entity and project.")
            return entity, project, parts[0]
        return parts[0], parts[1], parts[2]