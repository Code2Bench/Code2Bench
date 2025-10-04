

def extract_block_content(text, start_idx):
    try:
        block_start = text.index("{", start_idx)

        brace_count = 1
        pos = block_start + 1

        while brace_count > 0 and pos < len(text):
            if text[pos] == '{':
                brace_count += 1
            elif text[pos] == '}':
                brace_count -= 1
            pos += 1

        if brace_count == 0:
            return text[block_start:pos]
    except ValueError as e:
        pass

    return ""