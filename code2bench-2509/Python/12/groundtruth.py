

def build_expected_version_hex(matches):
    patch_level_serial = matches["PATCH"]
    serial = None
    try:
        major = int(matches["MAJOR"])
        minor = int(matches["MINOR"])
        flds = patch_level_serial.split(".")
        if flds:
            patch = int(flds[0])
            level = None
            if len(flds) == 1:
                level = "0"
                serial = 0
            elif len(flds) == 2:
                level_serial = flds[1]
                for level in ("a", "b", "c", "dev"):
                    if level_serial.startswith(level):
                        serial = int(level_serial[len(level) :])
                        break
    except ValueError:
        pass
    if serial is None:
        msg = 'Invalid PYBIND11_VERSION_PATCH: "{}"'.format(patch_level_serial)
        raise RuntimeError(msg)
    return (
        "0x"
        + "{:02x}{:02x}{:02x}{}{:x}".format(
            major, minor, patch, level[:1], serial
        ).upper()
    )