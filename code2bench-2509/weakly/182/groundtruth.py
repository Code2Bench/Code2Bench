
import struct

import struct

def tlv(buf):
    n = 4
    t, l_ = struct.unpack('>HH', buf[:n])
    v = buf[n:n + l_]
    pad = (n - l_ % n) % n
    buf = buf[n + l_ + pad:]
    return t, l_, v, buf