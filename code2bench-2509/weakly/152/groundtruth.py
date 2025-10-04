
import struct
import codecs

import codecs
import struct

def pack_name(name, off, label_ptrs):
    name = codecs.encode(name, 'utf-8')
    if name:
        labels = name.split(b'.')
    else:
        labels = []
    labels.append(b'')
    buf = b''
    for i, label in enumerate(labels):
        key = b'.'.join(labels[i:]).upper()
        ptr = label_ptrs.get(key)
        if ptr is None:
            if len(key) > 1:
                ptr = off + len(buf)
                if ptr < 0xc000:
                    label_ptrs[key] = ptr
            i = len(label)
            buf += struct.pack("B", i) + label
        else:
            buf += struct.pack('>H', (0xc000 | ptr))
            break
    return buf