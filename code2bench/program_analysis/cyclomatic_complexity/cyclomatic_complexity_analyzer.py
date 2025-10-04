import textwrap
from python_graphs import control_flow
from python_graphs import cyclomatic_complexity

# from autocodebench.program_analysis.scope_graph.build_scopes import build_scope_graph
# from autocodebench.utils.json_utils import save_json

def analyze_cyclomatic_complexity(source_code):
    source_code = textwrap.dedent(source_code)
    graph = control_flow.get_control_flow_graph(source_code)
    value = cyclomatic_complexity.cyclomatic_complexity(graph)
    return value

    return 0