import math

def total_byte_entropy_stats(python_code: str) -> dict:
    byte_counts = {}
    for byte in python_code.encode('utf-8'):
        byte_counts[byte] = byte_counts.get(byte, 0) + 1
    total_bytes = len(python_code.encode('utf-8'))
    entropy = 0.0
    for count in byte_counts.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    return {'total_byte_entropy': entropy}