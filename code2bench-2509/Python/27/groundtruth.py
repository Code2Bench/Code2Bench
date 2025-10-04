

def analyze_content(markdown_content):
    """Analyze the content structure of the markdown."""
    analysis = {}

    # Count different elements
    analysis['lines'] = len(markdown_content.split('\n'))
    analysis['words'] = len(markdown_content.split())
    analysis['headers'] = markdown_content.count('#')
    analysis['lists'] = markdown_content.count('- ') + markdown_content.count('* ')
    analysis['tables'] = markdown_content.count('|')
    analysis['links'] = markdown_content.count('[')

    # Determine content type
    if analysis['tables'] > 10:
        analysis['type'] = 'structured_data'
    elif analysis['headers'] > 5:
        analysis['type'] = 'document'
    elif analysis['lists'] > 5:
        analysis['type'] = 'list_content'
    else:
        analysis['type'] = 'text'

    return analysis