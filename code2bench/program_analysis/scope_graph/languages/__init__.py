from .python import PythonParse
from .java import JavaParse

# TODO: when we have to implement a third one of these things,
# build a factory class to do it properly
LANG_PARSER = {"python": PythonParse}
