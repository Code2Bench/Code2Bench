from code2bench.program_analysis.scope_graph.build_scopes import build_scope_graph

from code2bench.program_analysis.scope_graph.repo_resolution.repo_graph import RepoGraph
from pathlib import Path

from code2bench.program_analysis.scope_graph.scope_resolution.graph import ScopeGraph
from code2bench.program_analysis.scope_graph.scope_resolution.scope import LocalScope


## Failing tests
# Dotted assignment/ref
# test = """
# h.a = 1
# h.a = h.b

# def func1():
#     a = b
#     b = 2
# """

def test_unresolved_refs():
    test = """
def _create_span_id(self, block: CodeBlock, label: Optional[str] = None):
    if block.type.group == CodeBlockTypeGroup.STRUCTURE:
        structure_block = block
    else:
        structure_block = block.find_type_group_in_parents(
            CodeBlockTypeGroup.STRUCTURE
        )

    span_id = structure_block.path_string()
    if label and span_id:
        span_id += f":{label}"
    elif label and not span_id:
        span_id = label
    elif not span_id:
        span_id = "impl"

    if span_id in self._span_counter:
        self._span_counter[span_id] += 1
        span_id += f":{self._span_counter[span_id]}"
    else:
        self._span_counter[span_id] = 1

    return span_id

def _count_tokens(self, content: str):
    if not self.tokenizer:
        return 0
    return len(self.tokenizer(content))

def debug_log(self, message: str):
    if self.debug:
        logger.debug(message)

"""

    g = build_scope_graph(bytearray(test, encoding="utf-8"), language="python")

    print([g.get_node(r).name for r in g.references_by_origin(1)])
    

def test_insert_scope():
    scope_graph = ScopeGraph(range(start=1, end=6))

    # scope 1:
    #   -> scope2
    #       -> scope 3
    #   -> scope 4
    scope1 = LocalScope(range(1, 5))
    scope2 = LocalScope(range(2, 4))
    scope3 = LocalScope(range(3, 4))
    scope4 = LocalScope(range(1, 4))

    scope_graph.insert_local_scope(scope1)
    scope_graph.insert_local_scope(scope2)
    scope_graph.insert_local_scope(scope3)
    scope_graph.insert_local_scope(scope4)

    print(scope_graph.to_str())
    graph_state = """
1: --ScopeToScope-> 0:
2: --ScopeToScope-> 1:
3: --ScopeToScope-> 2:
4: --ScopeToScope-> 1:
"""

    assert scope_graph.to_str() == graph_state


test_method = """
def print_python_files_content(directory, exclude_patterns=None):
    if exclude_patterns is None:
        exclude_patterns = []

    out = out_func()
    out2 = out
    matched = 0
    files_content = ""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if any(
                    fnmatch.fnmatch(file_path, pattern) for pattern in exclude_patterns
                ):
                    continue
                matched += 1

                files_content += f"File: {file_path}"
                with open(file_path, "r", encoding="utf-8") as f:
                    files_content += f.read()

    return files_content
"""





def read_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# scope_graph = build_scope_graph(bytearray(test_class_java3, encoding="utf-8"), language="java")
# print(scope_graph.to_str())


test_python1 = """
def get_platform(self):
    # 获取平台类型（根据第一个候选商品判断）
    first_item = self.interaction_tool.get_item(self.task['candidate_list'][0])
    platform = first_item.get('source', 'yelp').lower()
    return platform
"""

test_python2 = """
def _process_item(self, item, platform):
    base_info = {
        'item_id': item['item_id'],
        'name': item.get('name') or item.get('title'),
        'rating': item.get('stars') or item.get('average_rating')
    }
    
    if platform == 'yelp':
        return {
            **base_info,
            'categories': item.get('categories', '').split(', ')[:3],
            'features': self._extract_yelp_features(item)
        }
    elif platform == 'amazon':
        return {
            **base_info,
            # 'item_id': item['item_id'],
            'main_category': item.get('main_category'),
            'title': item.get('title', ''),
            'categories': item.get('categories', []),
            'brand': item.get('details', {}).get('Brand'),
            'price': item.get('price'),
            'features': item.get('features', [])[:5]
        }
    elif platform == 'goodreads':
        return {
            **base_info,
            'author': item.get('authors', [{}])[0].get('author_id'),
            'popular_shelves': [shelf['name'] for shelf in item.get('popular_shelves', [])[:3]]
        }
    else:
        return base_info
"""

test_python3 = """
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    # Look at previous line's indentation first
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):  # Ignore continuation lines
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]

    # Look backward for containing blocks
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:  # Skip empty lines
            continue
        # Get the indentation of this line
        curr_indent = line[: len(line) - len(line.lstrip())]
        # If the line starts with 8+ spaces, it was probably properly nested
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        # If we find a class or function definition, use its base indentation
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "  # One level deeper than definition

        # If line ends with colon, use its indentation level
        if line.endswith(":"):
            return curr_indent + "  "  # One level deeper than block starter

    # Default to base level if we couldn't determine
    return ""
"""

test_java = """
public static String _get_correct_indent_level(List<String> lines, int lineIndex) {
    if (lineIndex < 0 || lineIndex >= lines.size()) {
        return "";
    }

    String currentLine = lines.get(lineIndex);
    if (lineIndex == 0) {
        return "";
    }

    String previousLine = lines.get(lineIndex - 1);
    if (!previousLine.isEmpty() && !previousLine.trim().endsWith(",")) {
        return getIndentation(previousLine);
    }

    if (previousLine.trim().startsWith("class ") || previousLine.trim().startsWith("def ") || previousLine.endsWith(":")) {
        return getIndentation(previousLine) + "  ";
    }

    for (String line : lines) {
        if (line.length() >= 8 && line.substring(0, 8).trim().isEmpty()) {
            return getIndentation(line);
        }
    }

    return "";
}
"""

scope_graph = build_scope_graph(bytearray(test_java, encoding="utf-8"), language="java")


print("unresolved refs: ")
# print(scope_graph.find_unresolved_refs())
unresolved_refs = set(scope_graph.unresolved_refs_name())
print(unresolved_refs)



# scope_graph = build_scope_graph(bytearray(test, encoding="utf-8"), language="python")
# print(scope_graph.to_str())

# test_unresolved_refs()

# # print(scope_graph.to_str())
# repo_graph = RepoGraph(Path("tests/repos/small_repo"))
# repo_graph.print_missing_imports()
# print("repo graph:")
# print(repo_graph.to_str())
