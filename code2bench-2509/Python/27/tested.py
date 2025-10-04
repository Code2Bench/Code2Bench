from typing import Dict

def analyze_content(markdown_content: str) -> Dict[str, Any]:
    # Split the markdown content into lines
    lines = markdown_content.splitlines()
    
    # Count the number of lines
    lines_count = len(lines)
    
    # Count the number of words
    words = len(markdown_content.split())
    
    # Count the number of headers
    headers = 0
    for line in lines:
        if line.startswith('#'):
            headers += 1
    
    # Count the number of lists
    lists = 0
    for line in lines:
        if line.startswith('-') or line.startswith('*'):
            lists += 1
    
    # Count the number of tables
    tables = 0
    for line in lines:
        if line.startswith('|'):
            tables += 1
    
    # Count the number of links
    links = 0
    for line in lines:
        if '[' in line and ']' in line:
            links += 1
    
    # Determine the type of content
    if tables > 10:
        content_type = 'structured_data'
    elif headers > 5:
        content_type = 'document'
    elif lists > 5:
        content_type = 'list_content'
    else:
        content_type = 'text'
    
    return {
        'lines': lines_count,
        'words': words,
        'headers': headers,
        'lists': lists,
        'tables': tables,
        'links': links,
        'type': content_type
    }