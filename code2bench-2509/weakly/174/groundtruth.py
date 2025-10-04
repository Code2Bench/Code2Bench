
import ast
import re

import re
import ast

def parse_nested_str_list(input_string):
    # Add quotation marks around the words in the string
    quoted_string = re.sub(r"(\w+)", r'"\1"', input_string)

    # Safely evaluate the string as a Python object
    try:
        python_object = ast.literal_eval(quoted_string)
        return python_object
    except (ValueError, SyntaxError) as e:
        print(f"Failed to convert string to Python object: {e}")
        return input_string