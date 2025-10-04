from typing import List, Dict, Any, Union

def extract_content_string(content: Union[str, List[Union[str, Dict[str, Any]]], Any]) -> str:
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        result = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    result.append(item['text'])
                elif item.get('type') == 'tool_use':
                    result.append(f'[Tool: {item["name"]}]')
                else:
                    result.append(str(item))
            else:
                result.append(str(item))
        return ' '.join(result)
    else:
        return str(content)