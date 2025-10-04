

def wrap_text_for_svg(text, max_width=80):
    """Simple text wrapping for SVG - split into lines that fit within max_width characters"""
    if len(text) <= max_width:
        return [text]

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines