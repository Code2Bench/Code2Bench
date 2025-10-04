
import struct

import struct

def _formatinfo(format):
    size = struct.calcsize(format)
    return size, len(struct.unpack(format, b"\x00" * size))