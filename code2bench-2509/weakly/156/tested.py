import itertools

def undistribute(iterable) -> list:
    result = []
    for i in range(max(len(sub) for sub in iterable)):
        for sub in iterable:
            if i < len(sub):
                result.append(sub[i])
    return [x for x in result if x is not None]