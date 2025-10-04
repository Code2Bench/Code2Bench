
import ast

def scrape_python_blocks(source_code, file_path_for_logging):
    """
    Parses Python source code from a string and extracts top-level classes,
    functions, and try/if blocks. It ignores methods inside classes and
    any blocks nested within functions.

    Args:
        source_code (str): The Python source code as a string.
        file_path_for_logging (str): The path of the file being scraped, for logging purposes.

    Returns:
        list: A list of strings, where each string is a source code block.
    """
    blocks = []
    try:
        # Parse the source code into an Abstract Syntax Tree (AST)
        tree = ast.parse(source_code, filename=file_path_for_logging)
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing {file_path_for_logging}: {e}")
        return []

    # Iterate over only the top-level nodes in the module's body
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Extracts top-level functions and full classes
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.Try):
            # Extracts top-level try...except...finally blocks
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.If):
            # Extracts top-level if blocks, as requested
            blocks.append(ast.get_source_segment(source_code, node))

    return blocks