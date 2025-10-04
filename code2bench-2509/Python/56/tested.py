from typing import List, Tuple

def parse_lcov(outputs: List[str]) -> Tuple[float, List[str], List[str]]:
    covered_branches = []
    all_branches = []
    
    # Find the start and end of the record
    for line in outputs:
        if line.startswith('tmp_src'):
            start_index = outputs.index(line)
            break
    
    # Find the end of the record
    for line in outputs[start_index:]:
        if line.startswith('end_of_record'):
            end_index = outputs.index(line)
            break
    
    # Extract BRDA lines between start and end indices
    brda_lines = [line for line in outputs[start_index:end_index] if 'BRDA' in line]
    
    # Process BRDA lines to extract branch information
    for line in brda_lines:
        parts = line.split()
        if len(parts) < 5:
            continue
        
        # Extract branch information
        lineno = int(parts[1])
        blockno = int(parts[2])
        branchno = int(parts[3])
        
        branch_signature = f"BR:{lineno},{blockno},{branchno}"
        all_branches.append(branch_signature)
        
        # Check if the branch is covered
        if parts[4] not in ('0', '-'):
            covered_branches.append(branch_signature)
    
    # Calculate coverage percentage
    if len(all_branches) == 0:
        coverage_percentage = 1.0
    else:
        coverage_percentage = len(covered_branches) / len(all_branches)
    
    return coverage_percentage, all_branches, covered_branches