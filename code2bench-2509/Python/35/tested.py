from typing import Optional

def compare_numerical_ans(ans_p: Optional[str], ans_l: str) -> bool:
    if ans_p is None:
        return False
    
    # Normalize the answers
    ans_p = ans_p.replace(',', '').replace('$', '').strip()
    ans_l = ans_l.replace(',', '').replace('$', '').strip()
    
    # Convert to float if possible
    try:
        val_p = float(ans_p)
        val_l = float(ans_l)
    except ValueError:
        return False
    
    # Compare the values with a small tolerance
    return abs(val_p - val_l) < 1e-3