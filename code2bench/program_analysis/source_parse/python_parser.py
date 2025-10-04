# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# pylint: disable=duplicate-code
"""
python_parser.py

This is the class which uses tree_sitter to parse python files
into structural components defined by the source_parser schema

#NOTE: Currently this parser ignores `if __name__ == "__main__":` blocks

"""

from collections import defaultdict
from textwrap import dedent
from typing import Dict, List, Tuple, Union

from source_parser.parsers.language_parser import (
    LanguageParser,
    has_correct_syntax,
)
from source_parser.langtools.python import check_python3_attempt_fix, fix_indentation
from source_parser.utils import static_hash
import tree_sitter


class RefinedPythonParser(LanguageParser):
    """
    Parser for python source code structural feature extraction
    into the source_parser schema.
    """

    _method_types = ("function_definition", "decorated_definition")
    _class_types = ("class_definition", "decorated_definition")
    _import_types = ("import_statement", "import_from_statement")
    _docstring_types = ("string", "comment")
    _include_patterns = "*?.py"  # this parser reads .py files!

    def __init__(self, file_contents=None, parser=None, remove_comments=True):
        """
        Initialize LanguageParser

        Parameters
        ----------
        file_contents : str
            string containing a source code file contents
        parser : tree_sitter.parser (optional)
            optional pre-initialized parser
        remove_comments: True/False
            whether to strip comments from the source file before structural
            parsing. Default is True as docstrings are separate from comments
        """
        super().__init__(file_contents, parser, remove_comments)

    @classmethod
    def get_lang(cls):
        return "python"

    @property
    def method_types(self):
        """Return method node types"""
        return self._method_types

    @property
    def class_types(self):
        """Return class node types string"""
        return self._class_types

    @property
    def import_types(self):
        """Return class node types string"""
        return self._import_types

    @property
    def include_patterns(self):
        return self._include_patterns

    @staticmethod
    def _distinguish_decorated(defn):
        def distinguish_decorated(node):
            if node.type == defn:
                return node
            if node.type == "decorated_definition":
                if node.children[-1].type == defn:
                    return node
            return None

        return distinguish_decorated

    def _get_decorated_defn(self, nodes, defn_type):
        return list(filter(None, map(self._distinguish_decorated(defn_type), nodes),))

    
    @property
    def global_variables(self):
        return self._get_decorated_defn(
            self.tree.root_node.children, "expression_statement"
        )
        
    @property
    def file_import(self):
        return self._get_decorated_defn(
            self.tree.root_node.children, "import_statement"
        )
    
    @property
    def file_import_from(self):
        return self._get_decorated_defn(
            self.tree.root_node.children, "import_from_statement"
        )

    @property
    def class_nodes(self):
        return self._get_decorated_defn(
            self.tree.root_node.children, "class_definition"
        )

    @property
    def method_nodes(self):
        return self._get_decorated_defn(
            self.tree.root_node.children, "function_definition"
        )

    @staticmethod
    def _clean_docstring_comments(comment):
        comment = comment.strip().strip(""" "' """)
        comment = "\n".join(map(lambda s: s.lstrip("#"), comment.splitlines()))
        return dedent(comment)

    def preprocess_file(self, file_contents):
        """
        Run any pre-processing on file_contents

        Raises
        ------
        source_parser.langtools.python.TimeoutException
        """
        return fix_indentation(check_python3_attempt_fix(file_contents))

    @property
    def file_docstring(self):
        """The first single or multi-line comment in the file"""
        file_docstring = ""
        if not self.tree.root_node.children:
            return file_docstring
        first = self.tree.root_node.children[0]
        if first.children and first.children[0].type == "string":
            file_docstring = self.span_select(first.children[0])
        elif first.type == "comment":
            file_docstring = self.span_select(first)
        return self._clean_docstring_comments(file_docstring)

    @property
    def file_context(self):
        """List of global import and assignment statements"""
        context = self.file_imports
        for child in self.tree.root_node.children:
            if (
                child.type == "expression_statement"
                and child.children[0].type == "assignment"
            ):
                context.append(self.span_select(child))
        return context

    def _parse_method_node(self, method_node):
        """See LanguageParser.parse_method_node for documentation"""

        results = {
            "attributes": defaultdict(list),
            "args_nums": None,
            "params": [],
            "syntax_pass": has_correct_syntax(method_node),
            "default_arguments": {},
            "original_string": self.span_select(method_node),
            # "byte_span": (method_node.start_byte, method_node.end_byte),
            # "start_point": (self.starting_point + method_node.start_point[0], method_node.start_point[1]),
            # "end_point": (self.starting_point + method_node.end_point[0], method_node.end_point[1]),
        }

        # handle decorators
        signature = []
        if method_node.type == "decorated_definition":
            for child in method_node.children:
                if child.type == "decorator":
                    decorator = self.span_select(child)
                    results["attributes"]["decorators"].append(decorator)
                    signature.append(decorator)
                elif child.type == "function_definition":
                    method_node = child

        # extract signature features and default arguments
        for def_child in method_node.children[:-1]:

            if def_child.type == "identifier":
                results["name"] = self.span_select(def_child, indent=False).strip()

            # store default arguments
            if def_child.type == "parameters":
                for arg_child in def_child.children:
                    if "default" in arg_child.type:
                        default_idx = list(
                            map(lambda n: n.type, arg_child.children)
                        ).index("=")
                        arg = self.span_select(
                            *arg_child.children[:default_idx], indent=False
                        )
                        results["default_arguments"][arg] = self.span_select(
                            *arg_child.children[default_idx + 1:], indent=False
                        )
                        
                number_of_params, params = self._parse_param_node(def_child)
                results["args_nums"] = number_of_params
                results["params"] = params

        signature.append(self.span_select(*method_node.children[:-1]))
        results["signature"] = "\n".join(signature)

        # Get start and end lines for the method
        start_point = method_node.start_point  # (line, column)
        end_point = method_node.end_point      # (line, column)
        
        results["start_line"] = start_point[0] + 1  # Lines in TreeSitter are 0-indexed, add 1
        results["end_line"] = end_point[0] + 1      # Lines in TreeSitter are 0-indexed, add 1

        results["body"] = ""
        results["docstring"] = ""
        body_node = method_node.children[-1]
        if body_node.children and body_node.children[0].children:
            if body_node.children[0].children[0].type in self._docstring_types:
                results["docstring"] = self._clean_docstring_comments(
                    self.span_select(body_node.children[0].children[0]),
                )
                results["body"] = self.span_select(*body_node.children[1:])
            else:
                results["body"] = self.span_select(body_node)

        return results
    
    def _parse_param_node(self, param_node) -> Tuple[int, List[str]]:
        number_of_params = 0
        params = []
        for arg_child in param_node.children:
            if arg_child.type in ("identifier", "default_parameter", "typed_parameter", "typed_default_parameter"):
                params.append(self.span_select(arg_child, indent=False))
                number_of_params += 1
        
        return number_of_params, params
            # else:
            #     if arg_child.type == "default_parameter":
            #         number_of_params += 1
            #         params.append(self.span_select(arg_child))
            #     elif arg_child.type == "typed_parameter":
            #         number_of_params += 1
            #         params.append(self.span_select(arg_child))
            #     elif arg_child.type == "typed_default_parameter":
            #         params.append(self.span_select(arg_child))
                
    def parse_global_variables_node(self, global_variables_node):  
        if not global_variables_node.children:
            return {}

        result = {}
        if global_variables_node.child_count == 1 and global_variables_node.children[0].type == 'assignment':
            if global_variables_node.children[0].children[0].type != "pattern_list": # For case: `logging.Logger.report = report`, `logging.Logger.report`'s type is attribute 
                result[self.span_select(global_variables_node.children[0].children[0], indent=False)] = \
                    self.span_select(global_variables_node.children[0].children[2], indent=False)
            elif global_variables_node.children[0].children[0].type == "pattern_list":
                left_list = []
                right_list = []
                # Handle the case for: ct, x, y, z = symbols("ct x y z")
                if isinstance(global_variables_node.children[0], tree_sitter.Node):
                    for c in global_variables_node.children[0].children:
                        if c.type == "pattern_list":
                            left_list.append(self.span_select(c, indent=False))
                        if c.type == "call":
                            right_list.append(self.span_select(c, indent=False))
                # Handle the case for: a, b = 1, 2   
                else:   
                    for c in global_variables_node.children[0]:
                        if c.type == "pattern_list":
                            for child in global_variables_node.children[0].children[0].children:
                                left_list.append(result[self.span_select(child, indent=False)])
                        if c.type == "expression_list":
                            for child in global_variables_node.children[0].children[2].children:
                                right_list.append(result[self.span_select(child, indent=False)])
                    
                    if len(left_list) != len(right_list):
                        raise ValueError("left and right list length not equal")
                
                for l, r in zip(left_list, right_list):
                    result[l] = r        
        return result
    
    def parse_import(self, import_node):
        """
        Input: import os, sys
        return: {"import os, sys": [{"from": os, "what": os}, {"from": sys, "what": sys}]}
        
        Input: import sys as E
        return: {"import sys as E": [{"from": sys, "what": os, "alias": E}]
        
        Input: import os, sys as E
        return: {"import os, sys as E": [{"from": os, "what": os}, {"from": sys, "what": sys, "alias": E}]}
        
        Input: import os
        return: {"import os": [{"from": os, "what": os}]}
        """
        origin_to_resloved = {}
        if import_node.child_count < 1:
            return origin_to_resloved
        
        origin_import = self.span_select(import_node, indent=False)
        origin_to_resloved[origin_import] = []
        for child in import_node.children:
            # For case: import os, sys
            if child.type == "dotted_name":
                text = self.span_select(child, indent=False)
                origin_to_resloved[origin_import].append({
                    "from": text, 
                    "what": text
                })
            # For case: import os as E
            if child.type == "aliased_import":
                if child.child_count != 2:
                    continue
                old = self.span_select(child.children[0], indent=False)
                new = self.span_select(child.children[1], indent=False)
                origin_to_resloved[origin_import].append({
                    "from": old, 
                    "what": old,
                    "alias": new,
                })
                
        return origin_to_resloved
    def parse_import_from(self, import_from_node):
        """
        Input: from typing import List
        return {"from typing import List": [{"from": typing, "what": List]}
        
        Input: from json import *
        return {"from json import *": [{"from": json, "what": *}]}
        
        Input: from DDDDD import EEEEE as FFFFF
        return {"from DDDDD import EEEEE as FFFFF": [{"from": DDDDD, "what": EEEEE, "alias": FFFFF}]}
        
        Input: from typing import List, Tuple
        return {"from typing import List, Tuple": [{"from": typing, "what": List}, {"from": typing, "what": Tuple}]}
        """
        origin_to_resloved = {}
        if import_from_node.child_count < 1:
            return origin_to_resloved
        
        origin_import = self.span_select(import_from_node, indent=False)
        origin_to_resloved[origin_import] = []

        # import_from_node.children[0] is `from` and import_from_node.children[1] is `package_prefix`
        # import_from_node.children[2] is `import` 
        package_prefix = self.span_select(import_from_node.children[1], indent=False)
        for child in import_from_node.children[2:]:
            if child.type == "dotted_name":
                text = self.span_select(child, indent=False)
                origin_to_resloved[origin_import].append({
                    "from": package_prefix, 
                    "what": text
                })
            elif child.type == "wildcard_import":
                origin_to_resloved[origin_import].append({
                    "from": package_prefix, 
                    "what": "*"
                })
            elif child.type == "aliased_import":
                old = self.span_select(child.children[0], indent=False)
                new = self.span_select(child.children[2], indent=False)
                origin_to_resloved[origin_import].append({
                    "from": package_prefix, 
                    "what": old,
                    "alias": new,
                })

        return origin_to_resloved
        
    def _parse_class_node(self, class_node):
        results = {
            "attributes": defaultdict(list),
            "class_docstring": "",
            "methods": [],
            # "byte_span": (class_node.start_byte, class_node.end_byte),
            # "start_point": (self.starting_point + class_node.start_point[0], class_node.start_point[1]),
            # "end_point": (self.starting_point + class_node.end_point[0], class_node.end_point[1]),
            "superclasses": [],
        }
        results["original_string"] = self.span_select(class_node)

        definition = []
        if class_node.type == "decorated_definition":
            for child in class_node.children:
                if child.type == "decorator":
                    decorator = self.span_select(child).strip()
                    results["attributes"]["decorators"].append(decorator)
                    definition.append(decorator)
                elif child.type == "class_definition":
                    class_node = child

        for child in class_node.children:
            if child.type == "argument_list":
                for c in child.children:
                    if c.type == "identifier":
                        results["superclasses"].append(self.span_select(c).strip())
                    if c.type == 'attribute':
                        results["superclasses"].append(self.span_select(c).strip())

        defn_index = list(map(lambda n: n.type, class_node.children)).index(":") + 1
        definition.append(self.span_select(*class_node.children[:defn_index]))
        results["definition"] = "\n".join(definition)

        results["name"] = self.span_select(class_node.children[1], indent=False)

        is_class = self._distinguish_decorated("class_definition")
        is_method = self._distinguish_decorated("function_definition")
        for i, child in enumerate(class_node.children[-1].children):
            if i == 0 and child.children and child.children[0].type == "string":
                results["class_docstring"] = self._clean_docstring_comments(
                    self.span_select(child.children[0])
                )
            if child.children and child.children[0].type == "assignment":
                results["attributes"]["attribute_expressions"].append(
                    self.span_select(child, indent=False)
                )
            if is_method(child):
                results["methods"].append(self.parse_method_node(child))
            if is_class(child):
                results["attributes"]["classes"].append(self.parse_class_node(child))
        return results
    
    def parse_method_node(self, method_node) -> Dict[str, Union[str, List, Dict]]:
        """
        Parse a method node into the correct schema

        Parameters
        ----------
        method_node : TreeSitter.Node
            tree_sitter node corresponding to a method


        Returns
        -------
        results : dict[str] = str, list, or dict
            parsed representation of the method corresponding to the following
            schema. See individual language implementations of `_parse_method_node`
            for guidance on language-specific entries.

            results = {
                'original_string': 'verbatim code of whole method',
                'signature':
                    'string corresponding to definition, name, arguments of method',
                'name': 'name of method',
                'args_nums': 'number of arguments',
                'docstring': 'verbatim docstring corresponding to this method',
                'body': 'verbatim code body',
                'byte_span': (start_byte, end_byte),
                'start_point': (start_line_number, start_column),
                'end_point': (end_line_number, end_column),
                'original_string_normed':
                    'code of whole method with string-literal, numeral normalization',
                'signature_normed': 'string-literals/numerals normalized signature',
                'body_normed': 'body with string-literals/numerals normalized',
                'default_arguments': ['arg1': 'default value 1', ...],
                'syntax_pass': 'whether the method is syntactically correct',
                'attributes': [
                        'language_specific_keys': 'language_specific_values',
                    ],
            }
        """
        msg = f"method_node is type {method_node.type}, requires types {self.method_types}"
        assert method_node.type in self.method_types, msg
        return self._parse_method_node(method_node)        
    
    @property
    def schema(self):
        """
        The file-level components of the schema

        See the top-level README.md file for a detailed description
        of the schema contents
        """
        return {
            "file_hash": static_hash(self.file_bytes),
            "file_docstring": self.file_docstring,
            "contexts": self.file_context,
            "import": [self.parse_import(c) for c in self.file_import],
            "import_from": [self.parse_import_from(c) for c in self.file_import_from],
            "global_variables": [self.parse_global_variables_node(c) for c in self.global_variables if c.children[0].type == "assignment"],
            "methods": [self.parse_method_node(c) for c in self.method_nodes],
            "classes": [self.parse_class_node(c) for c in self.class_nodes],
        }