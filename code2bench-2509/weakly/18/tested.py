from xml.sax.saxutils import escape as xml_escape

def _convert_text_danmaku_to_xml(text_content: str) -> str:
    danmaku_data = []
    lines = text_content.strip().split('\n')
    for line in lines:
        if not line:
            continue
        try:
            time_str, mode, _, color, _, content = line.split(' | ')
            time = float(time_str)
            mode = mode.strip()
            color = color.strip()
            content = content.strip()
            # 假设字体大小为默认值，例如24
            font_size = 24
            danmaku_data.append({
                'time': time,
                'mode': mode,
                'font_size': font_size,
                'color': color,
                'content': content
            })
        except ValueError:
            continue
    xml_output = ['<danmaku_server>']
    xml_output.append(f'  <task_id>1</task_id>')
    xml_output.append(f'  <source>input_text</source>')
    for danmaku in danmaku_data:
        xml_output.append('  <danmaku>')
        xml_output.append(f'    <time>{danmaku["time"]}</time>')
        xml_output.append(f'    <mode>{xml_escape(danmaku["mode"])}</mode>')
        xml_output.append(f'    <font_size>{danmaku["font_size"]}</font_size>')
        xml_output.append(f'    <color>{xml_escape(danmaku["color"])}</color>')
        xml_output.append(f'    <content>{xml_escape(danmaku["content"])}</content>')
        xml_output.append('  </danmaku>')
    xml_output.append('</danmaku_server>')
    return '\n'.join(xml_output)