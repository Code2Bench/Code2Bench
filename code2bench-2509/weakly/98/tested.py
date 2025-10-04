from datetime import datetime
from typing import Any

def _prepare_node_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if "created_at" not in metadata:
        metadata["created_at"] = datetime.utcnow().isoformat()
    if "updated_at" not in metadata:
        metadata["updated_at"] = datetime.utcnow().isoformat()
    if "embedding" in metadata and isinstance(metadata["embedding"], list):
        metadata["embedding"] = [float(x) for x in metadata["embedding"]]
    return metadata