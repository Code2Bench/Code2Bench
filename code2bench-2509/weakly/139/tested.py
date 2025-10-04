import struct

def _formatinfo(format: str) -> tuple[int, int]:
    size = struct.calcsize(format)
    num_elements = size // struct.calcsize('P')
    return (size, num_elements)