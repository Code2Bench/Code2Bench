

def functionParams(args, vars):
    """
    Build a dictionary of var/value from :param: args.
    Parameters can be either named or unnamed. In the latter case, their
    name is taken fron :param: vars.
    """
    params = {}
    index = 1
    for var in vars:
        value = args.get(var)
        if value is None:
            value = args.get(str(index))  # positional argument
            if value is None:
                value = ''
            else:
                index += 1
        params[var] = value
    return params