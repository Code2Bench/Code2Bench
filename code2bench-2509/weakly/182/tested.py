import struct

def tlv(buf: bytes) -> tuple[int, int, bytes, bytes]:
    t, l_ = struct.unpack('>HH', buf[:4])
    v = buf[4:4 + l_]
    padding = (4 - (4 + l_) % 4) % 4
    return t, l_, v, buf[4 + l_ + padding:]