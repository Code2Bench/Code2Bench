def linear_warmup_schedule(
    step: int,
    warmup_steps: int,
    start_value: float,
    end_value: float,
) -> float:
    if warmup_steps < 0:
        raise ValueError("warmup_steps must be non-negative")
    if step < 0:
        raise ValueError("step must be non-negative")
    if start_value < 0:
        raise ValueError("start_value must be non-negative")
    if end_value <= 0 or start_value > end_value:
        raise ValueError("end_value must be positive and greater than or equal to start_value")
    
    if step > warmup_steps:
        return end_value
    
    return start_value + (end_value - start_value) * (step / warmup_steps)