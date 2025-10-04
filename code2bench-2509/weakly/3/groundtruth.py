from typing import Tuple
from math import ceil
import math

def make_shifted_720Pwindows_bysize(size: Tuple[int, int, int], num_windows: Tuple[int, int, int]):
    t, h, w = size
    resized_nt, resized_nh, resized_nw = num_windows
    #cal windows under 720p
    scale = math.sqrt((45 * 80) / (h * w))
    resized_h, resized_w = round(h * scale), round(w * scale)
    wh, ww = ceil(resized_h / resized_nh), ceil(resized_w / resized_nw)  # window size.
    wt = ceil(min(t, 30) / resized_nt)  # window size.

    st, sh, sw = (  # shift size.
        0.5 if wt < t else 0,
        0.5 if wh < h else 0,
        0.5 if ww < w else 0,
    )
    nt, nh, nw = ceil((t - st) / wt), ceil((h - sh) / wh), ceil((w - sw) / ww)  # window size.
    nt, nh, nw = (  # number of window.
        nt + 1 if st > 0 else 1,
        nh + 1 if sh > 0 else 1,
        nw + 1 if sw > 0 else 1,
    )
    return [
        (
            slice(max(int((it - st) * wt), 0), min(int((it - st + 1) * wt), t)),
            slice(max(int((ih - sh) * wh), 0), min(int((ih - sh + 1) * wh), h)),
            slice(max(int((iw - sw) * ww), 0), min(int((iw - sw + 1) * ww), w)),
        )
        for iw in range(nw)
        if min(int((iw - sw + 1) * ww), w) > max(int((iw - sw) * ww), 0)
        for ih in range(nh)
        if min(int((ih - sh + 1) * wh), h) > max(int((ih - sh) * wh), 0)
        for it in range(nt)
        if min(int((it - st + 1) * wt), t) > max(int((it - st) * wt), 0)
    ]