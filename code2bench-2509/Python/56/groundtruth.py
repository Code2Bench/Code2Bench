from typing import List

def parse_lcov(outputs: List[str]):
    switch, extracted_outputs = False, []
    for line in outputs:
        if switch == False and "tmp_src" in line:
            switch = True
        if switch == True and "end_of_record" in line:
            switch = False
        if switch:
            extracted_outputs.append(line)

    branch, branch_covered = [], []
    for line in extracted_outputs:
        if line.startswith("BRDA"):
            # BRDA format: BR:<lineno>,<blockno>,<branchno>,<taken>
            lineno, blockno, branchno, taken = line[5:].split(",")
            branch_sig = f"BR:{lineno},{blockno},{branchno}"
            branch.append(branch_sig)
            if taken not in ["0", "-"]:
                branch_covered.append(branch_sig)
    per = 1.0 if len(branch) == 0 else len(branch_covered) / len(branch)
    return per, branch, branch_covered