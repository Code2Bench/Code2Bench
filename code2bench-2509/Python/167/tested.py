from typing import List, Tuple

def increment_version(old_version: List[str], increment: Tuple[int, ...]) -> List[str]:
    # Convert old version to integers for easier manipulation
    int_version = [int(part) for part in old_version]
    
    # Apply the increments
    for i in increment:
        if 0 <= i < len(int_version):
            int_version[i] += 1
            # If the value exceeds 9, reset to 0 and carry over to the next digit
            if int_version[i] > 9:
                int_version[i] = 0
                # Carry over to the next digit
                if i + 1 < len(int_version):
                    int_version[i + 1] += 1
                else:
                    # If there is no next digit, just set to 0
                    int_version[i] = 0
    
    # Convert back to strings
    return [str(part) for part in int_version]