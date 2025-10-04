
import math

def total_byte_entropy_stats(python_code):
    # Count the occurrence of each byte (character for simplicity)
    byte_counts = {}
    for byte in python_code.encode('utf-8'):
        byte_counts[byte] = byte_counts.get(byte, 0) + 1

    total_bytes = sum(byte_counts.values())
    entropy = -sum(
        (count / total_bytes) * math.log2(count / total_bytes)
        for count in byte_counts.values()
    )

    return {'total_byte_entropy': entropy}