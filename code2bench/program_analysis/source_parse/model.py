from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List


class Method:
    """
    uri: 全局标识 = file + class + name + arguments （本来想直接使用file + class + signature，但是signature无法区分重载方法, Python里面没有类型，仅仅通过参数数量就可以区分重载方法）
    name: 方法名
    class: 属于哪个class
    signature: 方法签名
    original_string: 原始字符串
    default_arguments: 默认参数
    file: 属于哪个文件，相对于项目根目录
    """
    """
    "attributes": {
        "decorators": [
            "@pytest.mark.parametrize(\n    \"test_input,expected\",\n    [\n        (\n            [\n                [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n            ],\n            [\n                [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n            ],\n        ),\n        (\n            [\n                [\"XXX\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n                [\"a\", \"XXX\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n            ],\n            [\n                [\"XXX\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n            ],\n        ),\n        (\n            [\n                [\"XXX\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n                [\"a\", \"XXX\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"] * 100,\n            ],\n            [\n                [\"XXX\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"],\n                [\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\", \"i\"],\n            ],\n        ),\n    ],\n)"
        ]
    },
    """
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None, 
                 arg_nums: str = None,
                 params: str = None,
                 signature: str = None, 
                 original_string: str = None, 
                 default_arguments: Dict[str, str] = None, 
                 file: str = None, 
                 class_name: str = None, class_uri: str = None,
                 attributes: Dict[str, List[str]] = None, 
                 docstring: str = None,
                 return_type: str = None):
        self.uris = uris
        self.name = name
        self.arg_nums = arg_nums
        self.params = params
        self.signature = signature
        self.original_string = original_string
        self.default_arguments = default_arguments
        self.file = file
        self.class_name = class_name
        self.class_uri = class_uri
        self.attributes = attributes
        self.docstring = docstring
        self.return_type = return_type

    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "arg_nums": self.arg_nums,
            "params": self.params,
            "return_type": self.return_type,
            "signature": self.signature,
            "original_string": self.original_string,
            "default_arguments": self.default_arguments,
            "file": self.file,
            "class_name": self.class_name,
            "class_uri": self.class_uri,
            "attributes": self.attributes,
            "docstring": self.docstring,
        }

class Class:
    """
    uri: 相对路径名 + 类名
    name: 类名
    parnets: 父类
    methods: 方法列表 = 自定义的方法列表 + 父类的方法列表
    overrides: 重写的父类的方法 
    """
    def __init__(self, 
                 uris: List[str] = None, 
                 name: str = None, 
                 file_path: str = None,
                 superclasses: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 ):
        self.uris = uris
        self.name = name
        self.file_path = file_path
        self.superclasses = superclasses
        self.methods = methods
        self.method_uris = method_uris
        self.overrides = overrides
        self.attributes = attributes
        self.class_docstring = class_docstring
        self.original_string = original_string
    
    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "file_path": self.file_path,
            "superclasses": self.superclasses,
            "methods": self.methods,
            "method_uris": self.method_uris,
            "overrides": self.overrides,
            "attributes": self.attributes,
            "class_docstring": self.class_docstring,
            "original_string": self.original_string
        }
        
class PythonClass(Class):
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None, 
                 file_path: str = None,
                 superclasses: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 ):
        super().__init__(uris, name, file_path, superclasses, methods, method_uris, overrides, attributes, class_docstring, original_string)
        # TODO: support class fields      
        # self.fields = fields
    
    def to_json(self):
        return {
            **super().to_json(),
        }
    
class GoClass(Class):
    def __init__(self, 
                 uris: List[str] = None, # This is needed, since in Go, type MyAddress = Address is allowed
                 name: str = None,
                 superclasses: List[str] = None,
                 super_interfaces: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None, 
                 file_path: str = None,
                 overrides: List[str] = None, 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None, 
                 original_string: str = None,
                 fields: List[Dict] = None):
        super().__init__(uris, name, file_path, superclasses, methods, method_uris, overrides, attributes, class_docstring, original_string)
        self.super_interfaces = super_interfaces
        self.fields = fields

    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "super_interfaces": self.super_interfaces,
            "methods": self.methods,
            "method_uris": self.method_uris,
            "class_docstring": self.class_docstring,
            "original_string": self.original_string,
            "fields": self.fields
        }
    
class GoInterface:
    def __init__(self,
                 uris: List[str] | str = None, 
                 name: str = None, 
                 methods: List[str] = None, 
                 methods_uris: List[List[str]] = None,
                 super_interfaces: List[str] = None,
                 original_string: str = None,
                 file_path: str = None,
                 class_docstring: str = None
                 ) -> None:
        self.uris = uris
        self.name = name
        self.methods = methods
        self.method_uris = methods_uris
        self.super_interfaces = super_interfaces
        self.original_string = original_string
        self.file_path = file_path
        self.self.class_docstring = class_docstring

    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "methods": self.methods,
            "method_uris": self.method_uris,
            "super_interfaces": self.super_interfaces,
            "original_string": self.original_string,
            "file_path": self.file_path,
            "class_docstring": self.class_docstring
        }


class JavaClass(Class):
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None, 
                 file_path: str = None,
                 superclasses: List[str] = None,
                 super_interfaces: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 fields: List[Dict] = None,
                 ):
        super().__init__(uris, name, file_path, superclasses, methods, method_uris, overrides, attributes, class_docstring, original_string)
        self.super_interfaces = super_interfaces
        self.fields = fields
    
    def to_json(self):
        return {
            **super().to_json(),
            "super_interfaces": self.super_interfaces,
            "fields": self.fields,
        }
        

class JavaAbstractClass(JavaClass):
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None, 
                 file_path: str = None,
                 superclasses: List[str] = None,
                 super_interfaces: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 fields: List[Dict] = None,
                 ):
        super().__init__(uris, name, file_path, superclasses, super_interfaces,
                         methods, method_uris, overrides, attributes, 
                         class_docstring, original_string, fields)

class JavaRecord(JavaClass):
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None, 
                 superclasses: List[str] = None,
                 super_interfaces: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 fields: List[Dict] = None,
                 ):
        super().__init__(uris, name, superclasses, methods, method_uris, overrides, attributes, class_docstring, original_string)
        self.fields = fields
    
    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "methods": self.methods,
            "attributes": self.attributes,
            "class_docstring": self.class_docstring,
            "original_string": self.original_string,
            "fields": self.fields
        }
        
class JavaInterface(JavaClass):
    def __init__(self, 
                 uris: List[str] | str = None, 
                 name: str = None,
                 file_path: str = None,
                 superclasses: List[str] = None,
                 super_interfaces: List[str] = None,
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 fields: List[Dict] = None,
                 ):
        super().__init__(
            uris=uris, 
            name=name, 
            file_path=file_path,
            superclasses=superclasses,
            super_interfaces=None,
            methods=methods, 
            method_uris=method_uris,
            overrides=overrides, #重写的父类的方法 
            attributes=attributes, 
            class_docstring=class_docstring,
            original_string=original_string,
            fields=None)
    
    def to_json(self):
        return {
            "uris": self.uris,
            "name": self.name,
            "file_path": self.file_path,
            "superclasses": self.superclasses,
            "methods": self.methods,
            "method_uris": self.method_uris,
            "overrides": self.overrides,
            "attributes": self.attributes,
            "class_docstring": self.class_docstring,
            "original_string": self.original_string
        }


class FileType(Enum):
    NORMAL = 1
    TEST = 2
    CONFIG = 3
    

class File:
    def __init__(self, 
                 name: str = None,
                 file_path: str = None, 
                 original_string: str = None, 
                 context: List[str] = None,
                 global_variables: List[Dict[str, str]] = None,
                 methods: List[Dict[Any, Any]] = None,
                 classes: List[Dict[Any, Any]] = None,
                 file_type: FileType = None
                 ) -> None:
        self.name = name
        self.file_path = file_path
        self.original_string = original_string
        self.context = context
        self.global_variables = global_variables
        self.methods = methods
        self.classes = classes
        self.file_type = file_type

    def to_json(self) -> str:
        # 将FileType枚举转换为字符串表示
        file_type_str = self.file_type.name if self.file_type else None
        return {
            'name': self.name,
            'file_path': self.file_path,
            'original_string': self.original_string,
            'context': self.context,
            'global_variables': self.global_variables,
            'methods': self.methods,
            'classes': self.classes,
            'file_type': file_type_str
        }


class PythonFile(File):
    def __init__(self, 
                 name: str = None,
                 file_path: str = None, 
                 original_string: str = None, 
                 context: List[str] = None,
                 _import: List[Dict[str, List[Dict]]] = None,
                 _import_from: List[Dict[str, List[Dict]]] = None,
                 global_variables: List[Dict[str, str]] = None,
                 methods: List[Dict[Any, Any]] = None,
                 classes: List[Dict[Any, Any]] = None,
                 file_type: FileType = None
                 ) -> None:
        File.__init__(self,
                      name=name, 
                      file_path=file_path, 
                      original_string=original_string, 
                      context=context,
                      global_variables=global_variables,
                      methods=methods,
                      classes=classes,
                      file_type=file_type)
        self._import = _import
        self._import_from = _import_from

    def to_json(self) -> str:
        return {
            **File.to_json(self),
            '_import': self._import,
            '_import_from': self._import_from
        }


class MethodSignature(ABC):
    
    def __init__(self, file_path: str = None,
                 class_name: str = None,
                 method_name: str = None) -> None:
        self.file_path = file_path
        self.class_name = class_name
        self.method_name = method_name
    
    @abstractmethod
    def unique_name(self) -> str:
        pass


class PythonMethodSignature(MethodSignature):
    def __init__(self, file_path: str = None,
                 class_name: str = None,
                 method_name: str = None,) -> None:
        MethodSignature.__init__(self, file_path, class_name, method_name)
    
    def unique_name(self):
        pass


class JavaMethodSignature(MethodSignature):
    def __init__(self, 
                 file_path: str = None,
                 class_name: str = None,
                 method_name: str = None,
                 params: List[Dict[str, str]] = None,
                 return_type: str = None) -> None:
        MethodSignature.__init__(self, file_path, class_name, method_name)
        self.params = params
        self.return_type = return_type

    def unique_name(self):
        return self.file_path + '.' + self.class_name + '.' + f'[{self.return_type}]' + self.method_name + \
            '(' + ','.join([param['type'] for param in self.params]) +  ')'
    

class GoMethodSignature(MethodSignature):
    def __init__(self,
                 file_path: str = None,
                 receiver: str = None,
                 method_name: str = None,
                 params: List[Dict[str, str]] = None,
                 return_type: List[str] = None
                 ):
        self.file_path = file_path
        self.receiver = receiver
        self.method_name = method_name
        self.params = params or []
        self.return_type = return_type or []
        
    def unique_name(self) -> str:
        return self.file_path + '.' + self.receiver + '.' + self.method_name + \
            '.' + '(' + ','.join([param['type'] for param in self.params]) + ')' + '.' + '(' + ','.join(self.return_type) + ')'


# TODO: fix this, testcase maybe a Class or Method
class TestCase:
    pass
    
class TestMethod(Method, TestCase):
    def __init__(self, 
                 uris: List[str] = None, 
                 name: str = None, 
                 arg_nums: str = None, 
                 params: str = None,
                 signature: str = None,
                 original_string: str = None, 
                 default_arguments: Dict[str, str] = None, 
                 file: str = None, 
                 class_name: str = None, class_uri: str = None,
                 attributes: Dict[str, List[str]] = None, 
                 docstring: str = None,
                 return_type: str = None
                 ):
        super().__init__(
            uris, name, arg_nums, params, signature, original_string, default_arguments, file, class_name, class_uri, attributes, docstring, return_type)
        
    def to_json(self):
        return super().to_json()


class TestClass(Class, TestCase):
    def __init__(self, 
                 uris: List[str] = None, 
                 name: str = None, 
                 superclasses: List[str] = None, 
                 methods: List[str] = None, 
                 method_uris: List[List[str]] = None,
                 overrides: List[str] = None, #重写的父类的方法 
                 attributes: Dict[str, List[str]] = None, 
                 class_docstring: str = None,
                 original_string: str = None,
                 ):
        super().__init__(uris, name, superclasses, methods, method_uris, overrides, attributes, class_docstring, original_string)

    def to_json(self):
        super().to_json()


class Inheritance:
    def __init__(self, parent_class_uri: str, child_class_uri: str):
        self.parent_class_uri = parent_class_uri
        self.child_class_uri = child_class_uri

class Override:
    def __init__(self, parent_method_uri: str, child_method_uri: str):
        self.parent_method_uri = parent_method_uri
        self.child_method_uri = child_method_uri
        
class Implement:
    def __init__(self, interface_method_uri: str, class_method_uri: str):
        self.interface_method_uri = interface_method_uri
        self.class_method_uri = class_method_uri

# 还有什么关系？
# 得看看单测里面？也不是，得分析

class Dependency:
    def __init__(self, from_uri: str, to_uri: str):
        self.from_uri = from_uri
        self.to_uri = to_uri
        
class Package:
    
    name: str # 
    path: str # 
    uri: str
    classes: List[Class]
    methods: List[Method]
    testcases: List[TestCase]
    global_variables: List[str]
    imports: List[str]
    
    def __init__(self, name: str = None,
                 path: str = None,
                 uri: str = None,
                 classes: List[Class] = None,
                 methods: List[Method] = None,
                 testcases: List[TestCase] = None,
                 global_variables: List[str] = None,
                 imports: List[str] = None
                 ):
        self.name = name
        self.path = path
        self.uri = uri
        self.classes = classes
        self.methods = methods
        self.testcases = testcases
        self.global_variables= global_variables
        self.imports = imports
    
        
