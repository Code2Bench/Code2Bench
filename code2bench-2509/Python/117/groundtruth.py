

def shquote(arg):
    """Quote an argument for later parsing by shlex.split()"""
    for c in '"', "'", "\\", "#":
        if c in arg:
            return repr(arg)
    if arg.split() != [arg]:
        return repr(arg)
    return arg