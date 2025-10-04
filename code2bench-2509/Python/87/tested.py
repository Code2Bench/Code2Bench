from typing import Union

def enquote_executable(executable: str) -> str:
    if '/usr/bin/env' in executable:
        return f"/{executable.split('/usr/bin/env')[1]}"
    if ' ' in executable:
        return f'"{executable}"'
    return executable