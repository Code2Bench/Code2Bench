# import tree_sitter_python as tspython
from tree_sitter_languages import get_language, get_parser  # noqa: E402
from code2bench.program_analysis.scope_graph._config import JAVA_SCM


class JavaParse:

    @classmethod
    def _build_query(cls, file_content: bytearray, query_file: str):
        language = get_language("java")
        parser = get_parser("java")
        query_file = open(JAVA_SCM, "rb").read()
        
        root = parser.parse(file_content).root_node
        query = language.query(query_file)
        
        return query, root