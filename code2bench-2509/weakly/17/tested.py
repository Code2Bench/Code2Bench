from typing import List
from xml.sax.saxutils import escape as xml_escape

def _generate_dandan_xml(comments: List[dict]) -> str:
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<i>']
    xml_lines.append(f'<chatserver>chat.bilibili.com</chatserver>')
    xml_lines.append(f'<chatid>0</chatid>')
    xml_lines.append(f'<mission>0</mission>')
    xml_lines.append(f'<maxlimit>{len(comments)}</maxlimit>')
    xml_lines.append(f'<state>0</state>')
    xml_lines.append(f'<real_name>0</real_name>')
    xml_lines.append(f'<source>k-v</source>')
    
    for comment in comments:
        content = xml_escape(comment.get('m', ''))
        p_attr = comment.get('p', '')
        
        # Parse p attribute to ensure font size is valid
        p_parts = str(p_attr).split(',')
        if len(p_parts) >= 3:
            # Check if font size (3rd element) is valid, default to 25 if not
            try:
                font_size = float(p_parts[2])
                if font_size <= 0:
                    p_parts[2] = '25'
            except (ValueError, IndexError):
                p_parts[2] = '25'
            p_attr = ','.join(p_parts)
        else:
            # If p attribute is malformed, create a basic one
            p_attr = '0,1,25,16777215,0,0,0,0'
        
        xml_lines.append(f'<d p="{p_attr}">{content}</d>')
    
    xml_lines.append('</i>')
    return '\n'.join(xml_lines)