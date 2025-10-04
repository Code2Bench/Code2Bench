import codecs
import struct

def pack_name(name: str, off: int, label_ptrs: dict) -> bytes:
    labels = name.split('.')
    result = b''
    i = 0
    while i < len(labels):
        label = labels[i]
        if label in label_ptrs:
            # Use pointer to existing label
            ptr = label_ptrs[label]
            result += struct.pack('!H', ptr)
            break
        else:
            # Encode current label
            label_bytes = codecs.encode(label, 'utf-8')
            if len(label_bytes) > 63:
                raise ValueError("Label length exceeds maximum allowed DNS label length (63 bytes)")
            result += struct.pack('!B', len(label_bytes))
            result += label_bytes
            # Store pointer for future reuse
            label_ptrs[label] = off + len(result)
        i += 1
    return result