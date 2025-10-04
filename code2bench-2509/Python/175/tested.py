from typing import List, Tuple

def grouplines(sdp: str) -> Tuple[List[str], List[List[str]]]:
    lines = sdp.split('\n')
    session_lines = []
    media_sections = []

    current_media = []
    for line in lines:
        if line.startswith('m='):
            if current_media:
                media_sections.append(current_media)
                current_media = []
            if line:
                current_media.append(line)
        elif line.startswith('s=') or line.startswith('t=') or line.startswith('c='):
            if current_media:
                media_sections.append(current_media)
                current_media = []
            session_lines.append(line)
        else:
            if current_media:
                media_sections.append(current_media)
                current_media = []
            session_lines.append(line)

    if current_media:
        media_sections.append(current_media)

    return session_lines, media_sections