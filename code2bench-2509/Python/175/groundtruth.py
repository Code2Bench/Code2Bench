

def grouplines(sdp: str) -> tuple[list[str], list[list[str]]]:
    session = []
    media = []
    for line in sdp.splitlines():
        if line.startswith("m="):
            media.append([line])
        elif len(media):
            media[-1].append(line)
        else:
            session.append(line)
    return session, media