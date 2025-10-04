from typing import Any, Dict, List
from collections import defaultdict
import re

def group_sse_events(sse_files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group SSE event files by trace ID and sort by sequence number."""
    trace_groups = defaultdict(list)

    for file_info in sse_files:
        trace_id = None
        sequence = None

        if file_info.get("is_local", True):
            # local pattern: {trace_id}_{timestamp}-sse_events_{sequence}.json
            filename = file_info["name"]
            match = re.match(r"([a-f0-9_]+)-sse_events_(\d+)\.json", filename)
            if match:
                trace_id, sequence = match.groups()
        else:
            # s3 pattern: app-{app_id}.req-{req_id}_{timestamp}/sse_events/{sequence}.json
            path = file_info["path"]
            match = re.match(r"(app-[a-f0-9-]+\.req-[a-f0-9-]+)_\d+/sse_events/(\d+)\.json", path)
            if match:
                trace_id, sequence = match.groups()
                # trace_id now has timestamp stripped (app-xxx.req-xxx)

        if trace_id and sequence is not None:
            file_info["trace_id"] = trace_id
            file_info["sequence"] = int(sequence)
            trace_groups[trace_id].append(file_info)

    # sort each group by sequence number (keep ALL events in sequence)
    for trace_id in trace_groups:
        trace_groups[trace_id].sort(key=lambda x: x["sequence"])

    return dict(trace_groups)