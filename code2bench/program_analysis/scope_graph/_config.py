
from pathlib import Path
current_dir = Path(__file__).parent

LANGUAGE = "python"
# LANGUAGE = "java"
JAVA_SCM = str(Path(__file__).parent / "languages" / "java" / "java.scm")

PYTHONTS_LIB = "repo_parse/scope_graph/languages/python/libs/my-python.so"
PYTHON_SCM = str(current_dir / "languages" / "python" / "python.scm")
PYTHON_REFS = "repo_parse/scope_graph/languages/python/python_refs.scm"

FILE_GLOB_ENDING = {"python": ".py"}

SUPPORTED_LANGS = {"python": "python"}

NAMESPACE_DELIMETERS = {"python": "."}

SYS_MODULES_LIST = "repo_parse/scope_graph/languages/{lang}/sys_modules.json".format(lang=LANGUAGE)

THIRD_PARTY_MODULES_LIST = (
    "repo_parse/scope_graph/languages/{lang}/third_party_modules.json".format(lang=LANGUAGE)
)
