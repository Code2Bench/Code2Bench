from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional

class Function:
    def __init__(self, name: str, uri: str):
        self.name = name  # 函数名
        self.uri = uri  # 函数的URI, 全局标识 = file + class + name + arguments
        self.callees: List['Function'] = []  # 调用了谁
        self.callers: List['Function'] = []  # 被谁调用
        self.level: Optional[int] = None  # 层级

    def get_callers(self) -> List['Function']:
        return self.callers

    def get_callees(self) -> List['Function']:
        return self.callees

class Repository:
    def __init__(self):
        self.functions: Dict[str, Function] = {}  # 存储所有函数，键是函数的URI

    def add_function(self, function: Function):
        self.functions[function.uri] = function

    def get_function(self, uri: str) -> Function:
        return self.functions.get(uri)

    def get_all_functions(self) -> List[Function]:
        return list(self.functions.values())

    def add_call_relationship(self, caller_uri: str, callee_uri: str):
        caller = self.get_function(caller_uri)
        callee = self.get_function(callee_uri)
        if caller and callee:
            caller.callees.append(callee)
            callee.callers.append(caller)

    def assign_levels(self):
        # Initialize levels
        for func in self.functions.values():
            func.level = None

        # Identify leaf nodes
        leaf_functions = [f for f in self.functions.values() if not f.callees]
        for func in leaf_functions:
            func.level = 0

        changed = True
        while changed:
            changed = False
            for func in self.functions.values():
                if func.level is None:
                    callee_levels = [callee.level for callee in func.callees if callee.level is not None]
                    if len(callee_levels) == len(func.callees):
                        func.level = max(callee_levels) + 1
                        changed = True

        # Handle functions involved in cycles
        for func in self.functions.values():
            if func.level is None:
                func.level = -1  # Indicate a cycle or undefined level

    def get_functions_by_level(self) -> Dict[int, List[Function]]:
        level_dict: Dict[int, List[Function]] = {}
        for func in self.functions.values():
            level = func.level
            if level not in level_dict:
                level_dict[level] = []
            level_dict[level].append(func)
        return level_dict


class Mode(Enum):
    pass

class FuncType(Enum):
    """
    函数类型枚举。
    """
    SELF_CONTAINED = 1
    WEAKLY_SELF_CONTAINED = 2
    LEVEL_SELF_CONTAINED = 3

@dataclass
class FuncToGenerate:
    original_str: str
    func_type: FuncType
    name: str = field(default="")
    uri: str = field(default="")
    level: int = field(default=0)
    contains: List['FuncToGenerate'] = field(default_factory=list)
    call_libs: List[str] = field(default_factory=list)
    
@dataclass
class GeneratedInstruction:
    instruction: str = field(default="")
    reason: str = field(default="")
    difficulty: str = field(default="")
    error: str = field(default="")

@dataclass
class GeneratedDriver:
    driver: str = field(default="")
    error: str = field(default="")
    language: str = field(default="Python")
    