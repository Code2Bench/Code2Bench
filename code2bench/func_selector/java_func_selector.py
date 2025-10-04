"""
仅仅实现对Self contained函数的筛选，暂时不考虑weakly self contained函数
"""

# In java_func_selector.py
import json
import os
from typing import Dict, List, Set, Union

from code2bench.config import config
from code2bench.program_analysis.cyclomatic_complexity.cyclomatic_complexity_analyzer import compute_java_cyclomatic_complexity
from code2bench.program_analysis.scope_graph import get_unresolved_refs
from code2bench.program_analysis.cfg.java_cfg_builder import check_java_non_null_non_constant_return
from code2bench.program_analysis.git.analyse_commit_time import analyze_commit_changes
from code2bench.utils.json_utils import load_json, save_json
from code2bench import logger

class JavaFunctionSelector:
    def __init__(self, method_metainfo: List[Dict], allowed_libraries: Set[str] = None):
        """
        Initialize JavaFunctionSelector.
        :param method_metainfo: Java method meta information list.
        :param allowed_libraries: Set of allowed external libraries.
        """
        self.method_metainfo = method_metainfo
        self.allowed_libraries = allowed_libraries or set()
        self.self_contained_functions = set()
        self.modified_methods = set()

    def check_function_containment(self, func_code: str) -> bool:
        """
        Check if a Java method is self-contained.
        :param func_code: Java method source code.
        :return: True if self-contained, False otherwise.
        """
        # For Java, a self-contained method has no unresolved references
        # except for Java built-ins and allowed libraries
        unresolved_refs = set(get_unresolved_refs(code=func_code, language="java"))
        
        # If no unresolved references, it's self-contained
        if not unresolved_refs:
            return True
            
        # If all unresolved references are in allowed libraries, it's weakly self-contained
        # For now, we only consider fully self-contained functions
        return False

    def get_modified_methods(self, start_time: str, end_time: str) -> List[str]:
        """
        Get methods modified within the specified time range.
        """
        modified_methods = analyze_commit_changes(
            config.REPO_PATH_JAVA, start_time, end_time, config.ALL_METAINFO_PATH, mode="java")
        self.modified_methods = set(modified_methods)
        save_json(config.MODIFIED_METHODS_PATH, {"modified_methods": modified_methods})
        logger.info("Modified methods saved.")
        return modified_methods

    def is_constructor_or_simple_method(self, method: Dict) -> bool:
        """
        Check if the method is a constructor or simple method (no complex dependencies).
        """
        # Java constructors have the same name as the class
        class_name = method.get("class_name", "")
        method_name = method.get("name", "")
        
        # This is a simplified check - you might want to enhance this based on your meta info structure
        return True

    def run(self, output_to_file: bool = True, 
            self_contained_file: str = None,
            txt_output: bool = False):
        """
        Select self-contained Java methods.
        """
        self_contained_output = []

        for method in self.method_metainfo:
            method_uri = method.get("uris", "")
            
            # Check if method was modified (if we have that info)
            if self.modified_methods and method_uri not in self.modified_methods:
                 continue

            original_string = method.get("original_string", "")

            # 过滤没有返回值或者返回值为常量的函数
            non_null_non_constant_return = check_java_non_null_non_constant_return(original_string)

            if not non_null_non_constant_return:
                continue
            
            # Check if method is self-contained
            if self.check_function_containment(original_string):
                # Check cyclomatic_complexity
                # complexity = compute_java_cyclomatic_complexity(original_string)
                # if complexity < 3:
                #     continue  # Skip methods with low complexity
                
                # Check if it's a simple method (constructor or regular method)
                if self.is_constructor_or_simple_method(method):
                    self_contained_output.append({
                        "type": "java_method",
                        "uri": method_uri,
                        "class_name": method.get("class_name", ""),
                        "method_name": method.get("name", ""),
                        "arg_nums": method.get("arg_nums", 0),
                        "code": original_string
                    })

        # Output results
        if output_to_file and self_contained_file:
            save_json(self_contained_file, self_contained_output)
            logger.info(f"Self-contained Java methods saved to {self_contained_file}")
            
            if txt_output:
                txt_file = self_contained_file.replace(".json", ".txt")
                with open(txt_file, "w") as f:
                    for func in self_contained_output:
                        f.write(f"{func['type']}: {func['uri']}\n")
                        f.write(func["code"] + "\n\n")
                logger.info(f"Self-contained Java methods saved to {txt_file}")
        else:
            print("Self-contained Java methods:")
            print(json.dumps(self_contained_output, indent=4))

def select_function_for_java(start_time: str = "", end_time: str = ""):
    """
    Main function to select self-contained Java functions.
    """
    # Load Java method meta information
    method_metainfo = load_json(config.METHOD_METAINFO_PATH)  # You'll need to define this
    # file_metainfo = load_json(config.FILE_METAINFO_PATH)

    # # Define allowed libraries for Java
    # allowed_libraries = config.ALLOWED_JAVA_LIBRARIES  # You'll need to define this
    allowed_libraries = config.ALLOWED_JAVA_LIBRARIES

    # Initialize selector
    selector = JavaFunctionSelector(method_metainfo, allowed_libraries)
    
    # selector.get_modified_methods(start_time, end_time)
    
    # Get modified methods if time range is specified
    if start_time and end_time:
        if not os.path.exists(config.MODIFIED_METHODS_PATH):
            modified_methods = selector.get_modified_methods(start_time, end_time)
        else:
            modified_methods = load_json(config.MODIFIED_METHODS_PATH).get("modified_methods", [])
            selector.modified_methods = set(modified_methods)

    # Run selection
    selector.run(
        output_to_file=True,
        self_contained_file=config.JAVA_SELF_COTAINED_PATH,  # You'll need to define this
        txt_output=True
    )


if __name__ == "__main__":
    select_function_for_java()