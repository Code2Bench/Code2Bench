from pathlib import Path
from typing import Set

from code2bench.data_model import FuncType

class _ProjectConfig:
    def __init__(self):
        # 基础路径（固定值）
        self._current_project_path = Path(__file__).resolve().parent.parent
        print(f"CURRENT_PROJECT_PATH: {self._current_project_path}")
        # 动态配置项（带默认值）
        self._project_name = "Python"  # 默认项目名称
        self._project_name_java = "Java"  # Java 项目名称
        self._benchmark_name = "default"
        self._level_benchmark_name = "level"
        self._weakly_benchmark_name = "weakly"
        self._reasoning_benchmark_name = "reasoning"
        self._proxy_url = "http://127.0.0.1:7890"
        self._mode = FuncType.SELF_CONTAINED
        self._cyclo_complexity = 4
        self._language = "python" # 默认为Python
        self.project_url = None  # 项目 URL，默认为 None
        self.workspace_name = "workspace"  # 默认工作空间名称

    # 核心属性
    @property
    def PROJECT_NAME(self) -> str:
        return self._project_name
    
    @PROJECT_NAME.setter
    def PROJECT_NAME(self, value: str):
        self._project_name = value

    @property
    def PROJECT_NAME_JAVA(self) -> str:
        return self._project_name_java
    @PROJECT_NAME_JAVA.setter
    def PROJECT_NAME_JAVA(self, value: str):
        self._project_name_java = value

    @property
    def PROJECT_URI(self) -> str:
        return self.project_url
    
    @PROJECT_URI.setter
    def PROJECT_URI(self, value: str):
        self.project_url = value

    @property
    def CURRENT_PROJECT_PATH(self) -> str:
        return str(self._current_project_path)

    # 动态计算的路径
    @property
    def WORKSPACE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / self.workspace_name)
    
    @WORKSPACE_PATH.setter
    def WORKSPACE_PATH(self, value: str):
        self.workspace_name = value
    
    @property
    def REPO_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "workspace" / self.PROJECT_NAME)

    @property
    def REPO_PATH_JAVA(self) -> str:
        return str(self._current_project_path / "autocodebench" / "workspace_java" / self.PROJECT_NAME_JAVA)

    @REPO_PATH_JAVA.setter
    def REPO_PATH_JAVA(self, value: str):
        self.PROJECT_NAME_JAVA = value
    
    @property
    def _playground(self) -> Path:
        """复用路径计算"""
        if self.MODE == "Java":
            return Path(self.REPO_PATH_JAVA) / "playground"
        return Path(self.REPO_PATH) / "playground"
    
    @property
    def _java_playground(self) -> Path:
        """复用路径计算"""
        return Path(self.REPO_PATH_JAVA) / "playground"

    # 自动计算的元信息路径
    @property
    def MODIFIED_METHODS_PATH(self) -> str:
        return str(self._playground / "modified_methods.json")
    
    @property
    def CLASS_METAINFO_PATH(self) -> str:
        return str(self._playground / "class_metainfo.json")
    
    @property
    def FILE_METAINFO_PATH(self) -> str:
        return str(self._playground / "file_metainfo.json")
    
    @property
    def METHOD_METAINFO_PATH(self) -> str:
        return str(self._playground / "method_metainfo.json")
    
    @property
    def TESTCASE_METAINFO_PATH(self) -> str:
        return str(self._playground / "testcase_metainfo.json")
    
    @property
    def TESTCLASS_METAINFO_PATH(self) -> str:
        return str(self._playground / "testclass_metainfo.json")
    
    @property
    def TESTFILE_METAINFO_PATH(self) -> str:
        return str(self._playground / "testfile_metainfo.json")
    
    @property
    def FILE_IMPORTS_PATH(self) -> str:
        return str(self._playground / "file_imports.json")
    
    @property
    def PACKAGES_METAINFO_PATH(self) -> str:
        return str(self._playground / "packages_metainfo.json")
    
    @property
    def RESOLVED_METAINFO_PATH(self) -> str:
        return str(self._playground / "resolved_metainfo.json")
    
    @property
    def ALL_METAINFO_PATH(self) -> str:
        return str(self._playground / "all_metainfo.json")
    
    @property
    def EXCEPTE_PATH(self) -> str:
        return ""

    @property
    def SELF_COTAINED_PATH(self) -> str:
        return str(self._playground / "self_contained.json")
    
    @property
    def FILTERED_SELF_COTAINED_PATH(self) -> str:
        return str(self._playground / "filtered_self_contained.json")

    @property
    def JAVA_SELF_COTAINED_PATH(self) -> str:
        return str(self._java_playground / "self_contained.json")
    
    @property
    def BENCHMARK_JAVA_STATISTICS_PATH(self) -> str:
        return str(self._java_playground / "statistics.json")

    @property
    def SELF_COTAINED_CLASS_METHOD_PATH(self) -> str:
        return str(self._playground / "self_contained_class_method.json")
    
    @property
    def WEAKLY_SELF_COTAINED_PATH(self) -> str:
        return str(self._playground / "weakly_self_contained.json")
    
    @property
    def WEAKLY_SELF_COTAINED_CLASS_METHOD_PATH(self) -> str:
        return str(self._playground / "weakly_self_contained_class_method.json")
    
    @property
    def ONE_LEVEL_SELF_CONTAINED_PATH(self) -> str:
        return str(self._playground / "one_level_self_contained.json")
    
    @property
    def ONE_LEVEL_SELF_CONTAINED_CLASS_METHOD_PATH(self) -> str:
        return str(self._playground / "one_level_self_contained_class_method.json")
    
    @property
    def ONE_LEVEL_WEAKLY_SELF_CONTAINED_PATH(self) -> str:
        return str(self._playground / "one_level_weakly_self_contained.json")
    
    @property
    def TWO_LEVEL_SELF_CONTAINED_PATH(self) -> str:
        return str(self._playground / "two_level_self_contained.json")
    
    @property
    def TWO_LEVEL_SELF_CONTAINED_CLASS_METHOD_PATH(self) -> str:
        return str(self._playground / "two_level_self_contained_class_method.json")
    
    @property
    def TWO_LEVEL_WEAKLY_SELF_CONTAINED_PATH(self) -> str:
        return str(self._playground / "two_level_weakly_self_contained.json")
    
    @property
    def KEYWORD_AND_BUILTIN_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "program_analysis" / "scope_graph" / "languages" / "python" / "keyword_and_builtin.json")
    
    @property
    def JAVA_KEYWORD_AND_BUILTIN_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "program_analysis" / "scope_graph" / "languages" / "java" / "keyword_and_builtin.json")
    
    ### For Java
    @property
    def RECORD_METAINFO_PATH(self) -> str:
        return str(self._playground / "record_metainfo.json")
    
    @property
    def INTERFACE_METAINFO_PATH(self) -> str:
        return str(self._playground / "interface_metainfo.json")

    @property
    def ABSTRACTCLASS_METAINFO_PATH(self) -> str:
        return str(self._playground / "abstractclass_metainfo.json")

    @property
    def BROTHER_RELATIONS_PATH(self) -> str:
        return str(self._playground / "brother_relations.json")
    
    @property
    def JUNIT_VERSION_PATH(self) -> str:
        return str(self._playground / "junit_version.json")

# METHOD_METAINFO_PATH = RESOLVED_METAINFO_PATH + "method_metainfo.json"
# TESTCASE_METAINFO_PATH = RESOLVED_METAINFO_PATH + "testcase_metainfo.json"
# TESTCLASS_METAINFO_PATH = RESOLVED_METAINFO_PATH + "testclass_metainfo.json"
# FILE_IMPORTS_PATH = RESOLVED_METAINFO_PATH + "file_imports.json"
# PACKAGES_METAINFO_PATH = RESOLVED_METAINFO_PATH + "packages_metainfo.json"
# FILE_METAINFO_PATH = RESOLVED_METAINFO_PATH + "file_metainfo.json"
# TESTFILE_METAINFO_PATH = RESOLVED_METAINFO_PATH + "testfile_metainfo.json"
# ABSTRACTCLASS_METAINFO_PATH = RESOLVED_METAINFO_PATH + "abstractclass_metainfo.json"
# JUNIT_VERSION_PATH = RESOLVED_METAINFO_PATH + "junit_version.json"



    ####
    
    # Benchmark 相关路径
    @property
    def BENCHMARK_NAME(self) -> str:
        return self._benchmark_name
    
    @BENCHMARK_NAME.setter
    def BENCHMARK_NAME(self, value: str):
        self._benchmark_name = value
        
    @property
    def DEFAULT_BENCHMARK_NAME(self) -> str:
        return "default"
        
    @property
    def LEVEL_BENCHMARK_NAME(self) -> str:
        return self._level_benchmark_name
    
    @LEVEL_BENCHMARK_NAME.setter
    def LEVEL_BENCHMARK_NAME(self, value: str):
        self._level_benchmark_name = value
        
    @property
    def WEAKLY_BENCHMARK_NAME(self) -> str:
        return self._weakly_benchmark_name

    @WEAKLY_BENCHMARK_NAME.setter
    def WEAKLY_BENCHMARK_NAME(self, value: str):
        self._weakly_benchmark_name = value
    
    @property
    def REASONING_BENCHMARK_NAME(self) -> str:
        return self._reasoning_benchmark_name
    
    @REASONING_BENCHMARK_NAME.setter
    def REASONING_BENCHMARK_NAME(self, value: str):
        self._reasoning_benchmark_name = value
    
    @property
    def BENCHMARK_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / self.BENCHMARK_NAME)
    
    @BENCHMARK_PATH.setter
    def BENCHMARK_PATH(self, value: str):
        self._benchmark_name = value
    
    @property
    def BENCHMARK_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "index.json")
    
    @property
    def BENCHMARK_LEVEL_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "level_index.json")
    
    @property
    def BENCHMARK_WEAKLY_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "weakly_index.json")
    
    @property
    def BENCHMARK_JAVA_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "java_index.json")
    
    @property
    def BENCHMARK_SKIP_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "skip.json")
    
    @property
    def BENCHMARK_LEVEL_SKIP_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "level_skip.json")
    
    @property
    def BENCHMARK_WEAKLY_SKIP_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "weakly_skip.json")
    
    @property
    def BENCHMARK_JAVA_SKIP_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "java_skip.json")
    
    @property
    def BENCHMARK_STATISTICS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "statistics.json")
    
    @property
    def BENCHMARK_LEVEL_STATISTICS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "level_statistics.json")
    
    @property
    def BENCHMARK_WEAKLY_STATISTICS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "weakly_statistics.json")
    
    @property
    def BENCHMARK_RUNNING_STATUS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "running_status.json")
    
    @property
    def BENCHMARK_LEVEL_RUNNING_STATUS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "level_running_status.json")

    @property
    def BENCHMARK_WEAKLY_RUNNING_STATUS_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "weakly_running_status.json")
    
    @property
    def BENCHMARK_TESTCASES_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "testcases_index.json")
    
    @property
    def BENCHMARK_RUNNERS_INDEX_PATH(self) -> str:
        return str(Path(self.BENCHMARK_PATH) / "runners_index.json")
    
    @property
    def BENCMARK_REASONING_INDEX_PATH(self) -> str:
        return str(Path(self._current_project_path / "benchmark" / "reasoning" / "reasoning_index.json"))

    # 其他固定配置
    @property
    def LANGUAGE(self) -> str:
        return self._language
    
    @LANGUAGE.setter
    def LANGUAGE(self, value: str):
        self._language = value
    
    @property
    def LOG_DIR(self) -> str:
        return str(self._current_project_path / "logs")
    
    @property
    def PROXY_URL(self) -> str:
        return self._proxy_url
    
    @PROXY_URL.setter
    def PROXY_URL(self, value: str):
        self._proxy_url = value
        
    @property
    def MODE(self) -> str:
        return self._mode
    
    @MODE.setter
    def MODE(self, value: str):
        self._mode = value
        
    def WEAKLY_CYCLOMATIC_COMPLEXITY(self) -> int:
        return 2

    @property
    def CYCLOMATIC_COMPLEXITY(self) -> int:
        return self._cyclo_complexity
    
    @CYCLOMATIC_COMPLEXITY.setter
    def CYCLOMATIC_COMPLEXITY(self, value: int):
        self._cyclo_complexity = value
        
    @property
    def WEAKLY_MAX_CYCLOMATIC_COMPLEXITY(self) -> int:
        return 8
        
    @property
    def MAX_CYCLOMATIC_COMPLEXITY(self) -> int:
        return 10
        
    @property
    def JAVA_TESTED_TEMPLATE_PATH(self) -> str:
        # autocodebench/test_runner/java_tested_template.java
        return str(self._current_project_path / "autocodebench" / "test_runner" / "Tested.java")
        
    @property
    def GO_TESTED_TEMPLATE_PATH(self) -> str:
        # autocodebench/test_runner/go_tested_template.go
        return str(self._current_project_path / "autocodebench" / "test_runner" / "go_tested_template.go")
        
    @property
    def JAVA_POM_TEMPLATE_PATH(self) -> str:
        # autocodebench/runner_generator/pom.xml
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "pom.xml")
    
    @property
    def JAVA_RUNNER_HELPER_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "Helper.java")
    
    @property
    def TS_TESTED_TEMPLATE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "test_runner" / "ts_tested_template.ts")

    @property
    def JS_TESTED_TEMPLATE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "test_runner" / "js_tested_template.js")

    @property
    def PYTHON_RUNNER_HELPER_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "helper.py")
    
    @property
    def GO_RUNNER_HELPER_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "helper.go")
        
    @property
    def TESTCASE_RUNNER_TEMPLATE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "python_runnner_template.py")
    
    @property
    def JAVA_RUNNER_TEMPLATE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "runner_generator" / "Tester.java")
    
    @property
    def REASONING_RUNNER_TEMPLATE_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "pipeline" / "reasoning" / "reasoning_runner_template.py")
    
    @property
    def PROJECTS_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "projects.yaml")

    @property
    def JAVA_PROJECTS_PATH(self) -> str:
        return str(self._current_project_path / "autocodebench" / "projects_java.yaml")
    
    @property
    def WEAKLY_CANDIDATE_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "candidate_pool")

    @property
    def CANDIDATE_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "candidate_pool")
    
    @property
    def JAVA_CANDIDATE_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_candidate_pool")
    
    @property
    def WEAKLY_CANDIDATE_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "candidate_pool" / "weakly_candidate_pool_index.json")
    
    @property
    def CANDIDATE_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "candidate_pool" / "candidate_pool_index.json")
    
    @property
    def JAVA_CANDIDATE_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_candidate_pool" / "java_candidate_pool_index.json")
    
    @property
    def WEAKLY_EXCLUDED_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "excluded_pool")
    
    @property
    def EXCLUDED_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "excluded_pool")
    
    @property
    def JAVA_EXCLUDED_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_excluded_pool")
    
    @property
    def WEAKLY_EXCLUDED_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "excluded_pool" / "weakly_excluded_pool_index.json")
    
    @property
    def EXCLUDED_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "excluded_pool" / "excluded_pool_index.json")
    
    @property
    def JAVA_EXCLUDED_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_excluded_pool" / "java_excluded_pool_index.json")
    
    @property
    def WEAKLY_GENERATION_ERROR_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "generation_error_pool")
    
    @property
    def GENERATION_ERROR_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "generation_error_pool")
    
    @property
    def JAVA_GENERATION_ERROR_POOL_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_generation_error_pool")

    @property
    def WEAKLY_GENERATION_ERROR_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "weakly" / "generation_error_pool" / "weakly_generation_error_pool_index.json")
    
    @property
    def GENERATION_ERROR_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "generation_error_pool" / "generation_error_pool_index.json")

    @property
    def JAVA_GENERATION_ERROR_POOL_INDEX_PATH(self) -> str:
        return str(self._current_project_path / "benchmark" / "java_generation_error_pool" / "java_generation_error_pool_index.json")

    # @property
    # def ALLOWED_LIBRARIES(self) -> Set[str]:
    #     return {
    #         "math", "numpy", "pandas", "pd", "scipy", "decimal", "cmath", "fractions", "statistics",
    #         "time", "datetime", "dateutil", "calendar", "holidays", "pytz",
    #         "string", "re", "regex",
    #         "itertools", "sortedcontainers",
    #         "ast", 
    #         "typing", "functools", "operator", "pickle", "copy", "json",
    #         "xml", "html", 
    #         "pathlib", "struct", "tmpfile", 
    #         "sympy", "sklearn", "matplotlib", "seaborn", "plotly", "statsmodels",
    #         "inspect", "ctypes",
    #         "hashlib", "secrets", "codecs",
    #         "concurrent", "threading", "multiprocessing", "asyncio",
    #         # from collections import Counter，这种情况是不是忽略了？
    #         "heapq", "bisect", "queue", "deque", "array", "collections", 
    #         "argparse", "json", "base64", "binascii", "yaml", "cryptography",
    #         "rsa", "unicodedata"
    #     }
    
    @property
    def ALLOWED_LIBRARIES(self) -> Set[str]:
        return {
            # ========== 基础、类型与验证 ==========
            "typing", "typing_extensions", "types", "dataclasses", "enum", "abc",
            "pydantic", "attrs", "cerberus",
            
            # ========== 数值计算 ==========
            "math", "cmath", "decimal", "fractions", "statistics", "random",
            "numpy", "scipy", "sympy", "mpmath", "gmpy2", "uncertainties",
            
            # ========== 图像处理 ==========
            "skimage",
            
            # ========== 单位 & 量纲 ==========
            "pint",
            
            # ========== 数据结构 & 工具 ==========
            "collections", "itertools", "functools", "operator", "copy",
            "heapq", "bisect", "array", "weakref", "graphlib",
            "toolz", "more_itertools", "sortedcontainers", "portion",
            "boltons", "networkx",
            
            # ========== 函数式编程 ==========
            "fn",
            
            # ========== 文本、解析与生成 ==========
            "re", "regex", "string", "textwrap", "unicodedata", "difflib", "glom",
            "jinja2", "pyparsing", "nltk",  # 新增 nltk
            
            # ========== 时间处理 ==========
            "datetime", "time", "calendar", "dateutil", "pytz", "zoneinfo",
            "pandas.tseries.offsets",
            
            # ========== 标准格式与 Web 原语 ==========
            "json", "yaml", "toml", "csv", "pickle", "marshal", "configparser", "tomli",
            "base64", "binascii", "struct", "codecs",
            "xml", "urllib",
            
            # ========== 数据框 & 多维 ==========
            "pandas", "polars", "xarray",
            
            # ========== 假数据生成 ==========
            "faker",
            
            # ========== 自省 & AST ==========
            "ast", "inspect", "pprint",
            
            # ========== 新增：专业领域 ==========
            "rdkit",           # 化学信息学
            "geopandas",       # 地理空间（依赖 shapely）
            "empyrical",       # 金融统计
            # "hyperopt",        # 超参数搜索空间
            "constraint",      # 约束求解
            "music21",         # 音乐信息检索
            "ete3",            # 系统发育树
        }
        
    @property
    def ALLOWED_MODULES(self) -> Dict[str, str]:
        return {
            # ========== 基础 & 类型 ==========
            "dataclass": "from dataclasses import dataclass",
            "field": "from dataclasses import field",
            "asdict": "from dataclasses import asdict",
            "astuple": "from dataclasses import astuple",
            "is_dataclass": "from dataclasses import is_dataclass",
            "TypedDict": "from typing import TypedDict",
            "Literal": "from typing import Literal",
            "Optional": "from typing import Optional",
            "Union": "from typing import Union",
            "List": "from typing import List",
            "Dict": "from typing import Dict",
            "Tuple": "from typing import Tuple",
            "Any": "from typing import Any",
            "Enum": "from enum import Enum",
            "IntEnum": "from enum import IntEnum",
            "StrEnum": "from enum import StrEnum",  # Python 3.11+
            "NamedTuple": "from typing import NamedTuple",
            
            # ========== 数值计算 ==========
            "np": "import numpy as np",
            "array": "from numpy import array",
            "zeros": "from numpy import zeros",
            "ones": "from numpy import ones",
            "arange": "from numpy import arange",
            "linspace": "from numpy import linspace",
            "int32": "from numpy import int32",
            "float32": "from numpy import float32",
            "float64": "from numpy import float64",
            "bool_": "from numpy import bool_",
            "ufloat": "from uncertainties import ufloat",  # 新增
            "Fraction": "from fractions import Fraction",  # 显式
            "Decimal": "from decimal import Decimal",      # 显式
            "mpf": "from mpmath import mpf",               # 高精度浮点
            "mpz": "from gmpy2 import mpz",                # 大整数
            "mpq": "from gmpy2 import mpq",                # 有理数
            
            # ========== 科学计算 ==========
            "sparse": "from scipy import sparse",
            "csr_matrix": "from scipy.sparse import csr_matrix",
            "csc_matrix": "from scipy.sparse import csc_matrix",
            "coo_matrix": "from scipy.sparse import coo_matrix",
            "special": "from scipy import special",        # gamma, erf, etc.
            "linalg": "from scipy import linalg",          # solve, inv, det
            
            # ========== 符号计算 ==========
            "Symbol": "from sympy import Symbol",
            "symbols": "from sympy import symbols",
            "sin": "from sympy import sin",
            "cos": "from sympy import cos",
            "exp": "from sympy import exp",
            "latex": "from sympy import latex",            # 序列化为 LaTeX
            
            # ========== 数据框 ==========
            "DataFrame": "from pandas import DataFrame",
            "Series": "from pandas import Series",
            "read_csv": "from pandas import read_csv",     # 仅用于构造
            "pl": "import polars as pl",                   # Polars DataFrame
            "xr": "import xarray as xr",                   # Xarray DataArray
            "DataArray": "from xarray import DataArray",
            
            # ========== 单位量纲 ==========
            "ureg": "from pint import UnitRegistry",       # ureg = UnitRegistry()
            "Quantity": "from pint import Quantity",       # Q_ = ureg.Quantity
            
            # ========== 区间代数 ==========
            "P": "import portion as P",                    # P.closed(1, 3)
            
            # ========== 图 & 网络 ==========
            "nx": "import networkx as nx",                 # G = nx.Graph()
            "Graph": "from networkx import Graph",
            "DiGraph": "from networkx import DiGraph",
            "TopologicalSorter": "from graphlib import TopologicalSorter",
            
            # ========== 函数式编程 ==========
            "Option": "from fn.monad import Option",       # Some(x), Nothing
            "Some": "from fn.monad import Some",
            "Nothing": "from fn.monad import Nothing",
            "identity": "from toolz import identity",
            "compose": "from toolz import compose",
            "pipe": "from toolz import pipe",
            "partial": "from functools import partial",
            "reduce": "from functools import reduce",
            "lru_cache": "from functools import lru_cache",
            
            # ========== 文本处理 ==========
            "match": "from re import match",
            "search": "from re import search",
            "sub": "from re import sub",
            "findall": "from re import findall",
            "compile": "from re import compile",
            "ParserElement": "from pyparsing import ParserElement",  # 新增
            "Word": "from pyparsing import Word",
            "alphas": "from pyparsing import alphas",
            "Template": "from jinja2 import Template",     # 新增
            "word_tokenize": "from nltk import word_tokenize",  # 新增
            "pos_tag": "from nltk import pos_tag",
            
            # ========== 时间处理 ==========
            "datetime": "from datetime import datetime",
            "timedelta": "from datetime import timedelta",
            "timezone": "from datetime import timezone",
            "date": "from datetime import date",
            "time": "from datetime import time",
            "BDay": "from pandas.tseries.offsets import BDay",  # 金融日历
            "MonthEnd": "from pandas.tseries.offsets import MonthEnd",
            
            # ========== 标准格式 ==========
            "loads": "from json import loads",
            "dumps": "from json import dumps",
            "load": "from yaml import load",
            "dump": "from yaml import dump",
            "safe_load": "from yaml import safe_load",
            "safe_dump": "from yaml import safe_dump",
            "loads": "from toml import loads as toml_loads",  # toml
            "dumps": "from toml import dumps as toml_dumps",
            "ET": "import xml.etree.ElementTree as ET",    # 新增
            "urlparse": "from urllib.parse import urlparse",  # 新增
            "urlunparse": "from urllib.parse import urlunparse",
            "parse_qs": "from urllib.parse import parse_qs",
            
            # ========== 数据验证 ==========
            "BaseModel": "from pydantic import BaseModel",
            "validator": "from pydantic import validator",
            "Field": "from pydantic import Field",
            "Validator": "from cerberus import Validator",  # 新增
            
            # ========== 假数据生成 ==========
            "Faker": "from faker import Faker",            # fake = Faker()
            
            # ========== 专业领域 ==========
            # 化学
            "MolFromSmiles": "from rdkit.Chem import MolFromSmiles",  # 新增
            "Descriptors": "from rdkit.Chem import Descriptors",       # Descriptors.MolWt(mol)
            # 地理
            "Point": "from shapely.geometry import Point",             # 新增
            "Polygon": "from shapely.geometry import Polygon",
            "GeoSeries": "from geopandas import GeoSeries",
            # 金融
            "sharpe_ratio": "from empyrical import sharpe_ratio",      # 新增
            "max_drawdown": "from empyrical import max_drawdown",
            # 超参数
            "hp": "import hyperopt.hp as hp",                          # 新增
            "space_eval": "from hyperopt import space_eval",
            "rand": "from hyperopt import rand",
            # 约束求解
            "Problem": "from constraint import Problem",               # 新增
            "BacktrackingSolver": "from constraint import BacktrackingSolver",
            # 音乐
            "Note": "from music21.note import Note",                   # 新增
            "Chord": "from music21.chord import Chord",
            "Pitch": "from music21.pitch import Pitch",
            # 系统发育树
            "Tree": "from ete3 import Tree",                           # 新增
            
            # ========== Hypothesis 核心 ==========
            "given": "from hypothesis import given",
            "settings": "from hypothesis import settings",
            "Verbosity": "from hypothesis import Verbosity",
            "example": "from hypothesis import example",
            "note": "from hypothesis import note",
            "st": "from hypothesis import strategies as st",
            "arrays": "from hypothesis.extra.numpy import arrays",
            "from_dtype": "from hypothesis.extra.numpy import from_dtype",
            "datetime_ranges": "from hypothesis.extra.dateutil import datetime_ranges",
            
            # ========== 工具函数 ==========
            "glom": "from glom import glom",               # 嵌套数据访问
            "Coalesce": "from glom import Coalesce",
            "flatten": "from more_itertools import flatten",
            "chunked": "from more_itertools import chunked",
            "collapse": "from more_itertools import collapse",
        }
        
    # @property
    # def ALLOWED_MODULES(self) -> Set[str]:
    #     return {
    #         "np": "import numpy as np",
    #         "pd": "import pandas as pd",
    #         "Counter": "from collections import Counter",
    #         "defaultdict": "from collections import defaultdict",
    #         "OrderedDict": "from collections import OrderedDict",
    #         "namedtuple": "from collections import namedtuple",
    #         "deque": "from collections import deque",
    #         "ChainMap": "from collections import ChainMap",
    #         "UserDict": "from collections import UserDict",
    #         "UserList": "from collections import UserList",
    #         "UserString": "from collections import UserString",
    #         "loads": "from json import loads",
    #         "dumps": "from json import dumps",
    #         "b64encode": "from base64 import b64encode",
    #         "b64decode": "from base64 import b64decode",
    #         "hexlify": "from binascii import hexlify",
    #         "unhexlify": "from binascii import unhexlify",
    #         "load": "from yaml import load",
    #         "dump": "from yaml import dump",
    #         "mean": "from statistics import mean",
    #         "median": "from statistics import median",
    #         "mode": "from statistics import mode",
    #         "stdev": "from statistics import stdev",
    #         "pstdev": "from statistics import pstdev",
    #         "pvariance": "from statistics import pvariance",
    #         "variance": "from statistics import variance",
    #         "datetime": "from datetime import datetime",
    #         "timedelta": "from datetime import timedelta",
    #         "ascii_letters": "from string import ascii_letters",
    #         "digits": "from string import digits",
    #         "chain": "from itertools import chain",
    #         "cycle": "from itertools import cycle",
    #         "islice": "from itertools import islice",
    #         "parse": "from ast import parse",
    #         "NodeVisitor": "from ast import NodeVisitor",
    #         "sqrt": "from math import sqrt",
    #         "sin": "from math import sin",
    #         "cos": "from math import cos",
    #         "tan": "from math import tan",
    #         "array": "from numpy import array",
    #         "arange": "from numpy import arange",
    #         "linspace": "from numpy import linspace",
    #         "mean": "from numpy import mean",
    #         "std": "from numpy import std",
    #         "dot": "from numpy import dot",
    #         "DataFrame": "from pandas import DataFrame",
    #         "Series": "from pandas import Series",
    #         "match": "from re import match",
    #         "search": "from re import search",
    #         "sub": "from re import sub",
    #         "lru_cache": "from functools import lru_cache",
    #         "partial": "from functools import partial",
    #         "reduce": "from functools import reduce",
    #         "itemgetter": "from operator import itemgetter",
    #         "attrgetter": "from operator import attrgetter",
    #         "methodcaller": "from operator import methodcaller",
    #         "deepcopy": "from copy import deepcopy",
    #         "copy": "from copy import copy",
    #     }

    @property
    def ALLOWED_JAVA_LIBRARIES(self) -> Set[str]:
        return {
            "java.util", "java.lang", "java.io", "java.nio", "java.net",
            "java.math", "java.time", "java.util.concurrent",
            "org.junit", "org.junit.jupiter.api", "org.junit.jupiter.params",
            "org.mockito", "org.hamcrest"
        }


# 单例配置实例
config = _ProjectConfig()
config.PROJECT_NAME = "Python"