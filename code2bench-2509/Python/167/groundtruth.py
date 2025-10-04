

def increment_version(old_version, increment):
    """Compute the new version based on the previous value.
    :param old_version: Parts of the version string for the last
                        release.
    :type old_version: list(str)
    :param increment: Which positions to increment.
    :type increment: tuple(int)
    """
    new_version_parts = []
    clear = False
    for cur, inc in zip(old_version, increment):
        if clear:
            new_version_parts.append("0")
        else:
            new_version_parts.append(str(int(cur) + inc))
            if inc:
                clear = True
    return new_version_parts