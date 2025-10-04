from collections import defaultdict
import re
from typing import List, Dict, Any

def group_sse_events(sse_files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    trace_groups = defaultdict(list)
    
    for file in sse_files:
        if file.get('is_local'):
            filename = file['name']
            match = re.match(r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})_(\d+)_\d+\.json', filename)
            if match:
                trace_id, seq_num = match.groups()
                seq_num = int(seq_num)
        else:
            path = file['path']
            # Normalize trace ID by stripping timestamp
            trace_id_part = path.split('_')[0]
            # Extract sequence number from the path
            seq_num_part = path.split('_')[1]
            match = re.match(r'(\d+)', seq_num_part)
            if match:
                seq_num = int(match.group(1))
        
        trace_groups[trace_id].append(file)
    
    for trace_id, files in trace_groups.items():
        files.sort(key=lambda x: x['sequence_number'] if 'sequence_number' in x else 0)
    
    return trace_groups