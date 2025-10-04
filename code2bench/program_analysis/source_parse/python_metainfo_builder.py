import json
from typing import Dict, List

from code2bench.config import config
from code2bench.program_analysis.source_parse.metainfo_builder import MetaInfoBuilder
from code2bench.program_analysis.source_parse.model import Class, File, FileType, Method, PythonClass, PythonFile, TestClass, TestMethod
from code2bench.utils.json_utils import save_json
from code2bench.utils.python import get_class_uris, get_python_method_uris, resolve_relative_import
from code2bench import logger


class PythonMetaInfoBuilder(MetaInfoBuilder):
    def __init__(self, metainfo_json_path):
        super().__init__(metainfo_json_path)
        self.testfiles = []
        self.metainfo = self.load_metainfo()
        self.methods: List[Method] = []
        self.classes: List[Class] = []
        self.testcases: List[TestMethod] = []
        self.testclasses: List[TestClass] = []
        self.files: List[File] = []
        
    def save(self):
        path_to_data = {
            config.CLASS_METAINFO_PATH: self.classes,
            config.METHOD_METAINFO_PATH: self.methods,
            config.TESTCASE_METAINFO_PATH: self.testcases,
            config.TESTCLASS_METAINFO_PATH: self.testclasses,
            config.FILE_METAINFO_PATH: self.files,
            config.TESTFILE_METAINFO_PATH: self.testfiles
        }
        self.save_metainfo(path_to_data)

    def resolve_package_level_info(self, packages_metainfo_path):
        packages = {}
        for file in self.metainfo:
            relative_path = file['relative_path']
            if '/' not in relative_path:
                name = '$'  # 项目根目录的文件
            else:
                # name = '.'.join(relative_path.split('/')[:-1])  # 使用正确的路径分隔符
                name = relative_path.rstrip('.py').replace('/', '.')
            
            # 确保每个包层级都有对应的空字典
            if name not in packages:
                packages[name] = {
                    "global_variables": [],
                    "methods": [],
                    "classes": []
                }
            
            global_variables = file['global_variables']
            if global_variables:
                packages[name]["global_variables"].extend(global_variables)
                
            methods = file['methods']
            if methods:
                for method in methods:
                    packages[name]["methods"].extend(
                        get_python_method_uris(
                            relative_path=relative_path.strip('.py').replace('/', '.'), 
                            method=method, 
                            class_name=method['class_name'])
                        )
                
            classes = file['classes']
            if classes:
                for cls in classes:
                    packages[name]["classes"].extend(
                        get_class_uris(relative_path=relative_path, class_name=cls['name']))
        
        save_json(packages_metainfo_path, packages)
        
        return packages

    def resolve_file_imports(self, file_imports_path):
        file_imports = {}
        for file in self.metainfo:
            import_from = file["import_from"]
            file_imports[file['relative_path']] = []
            
            # TODO: add support for __init__.py's imports
            
            for import_from_node in import_from:
                # 假设每个import_from_node只有一个键值对
                for _, value in import_from_node.items():
                    import_info = value[0]
                    from_path = import_info['from']
                    if from_path.startswith('.'):
                        from_path = resolve_relative_import(
                            current_module=file['relative_path'], 
                            relative_import=from_path)
                    uri = ""
                    if "alias" in import_info:
                        alias = import_info['alias']
                        uri = f"{from_path}.{alias}"
                    else:
                        uri = f"{from_path}.{import_info['what']}"
                    
                    file_imports[file['relative_path']].append(uri)
            
            for _import_node in file['import']:
                # 假设每个import_from_node只有一个键值对
                for key, value in _import_node.items():
                    if len(value) == 0: continue
                    import_info = value[0]
                    from_path = import_info['from']
                    if from_path.startswith('.'):
                        from_path = resolve_relative_import(
                            current_module=file['relative_path'], 
                            relative_import=from_path)
                    uri = ""
                    if "alias" in import_info:
                        alias = import_info['alias']
                        uri = alias
                    else:
                        uri = from_path
                    
                    file_imports[file['relative_path']].append(uri)
            
        save_json(file_imports_path, file_imports)
        return file_imports
 
    def build_testcase_metainfo(self, file, cls, method):
        if method['attributes']:
            if 'decorators' in method['attributes'].keys():
                for decorator in method['attributes']['decorators']:
                    if decorator.strip().startswith('@pytest'):
                        testcase = TestMethod(
                            # uri="#".join([file['relative_path'], cls['name'], method['name']]),
                            uris=get_python_method_uris(
                                relative_path=file['relative_path'].strip('.py').replace('/', '.'),
                                method=method,
                                class_name=method.get('class_name')),
                            name=method['name'],
                            arg_nums=method['args_nums'],
                            params=method['params'],
                            signature=method['signature'],
                            original_string=method['original_string'],
                            default_arguments=method['default_arguments'],
                            file=file['relative_path'],
                            attributes=method['attributes'],
                            docstring=method['docstring']
                        )
                        self.testcases.append(testcase)
        elif method['name'].startswith('test_'):
            testcase = TestMethod(
                # uri="#".join([file['relative_path'], cls['name'], method['name']]),
                uris=get_python_method_uris(
                    relative_path=file['relative_path'].strip('.py').replace('/', '.'),
                    method=method,
                    class_name='test'),
                name=method['name'],
                arg_nums=method['args_nums'],
                params=method['params'],
                signature=method['signature'],
                original_string=method['original_string'],
                default_arguments=method['default_arguments'],
                file=file['relative_path'],
                attributes=method['attributes'],
                docstring=method['docstring']
            )
            self.testcases.append(testcase)

    def build_metainfo(self):
        for file in self.metainfo:
            file_path = file['relative_path']
            file_name = file_path.split('/')[-1]
            is_test_file = False
            if file_name.startswith('test_'):
                is_test_file = True
            method_uris = []
            class_uris = []

            for method in file['methods']:
                uris = get_python_method_uris(
                    relative_path=file['relative_path'].strip('.py').replace('/', '.'),
                    method=method)
                _method = Method(
                    # uri="#".join([file['relative_path'], '$', method['name'], method['signature'].replace(' ', '').replace('\n', '')]),
                    uris=uris,
                    name=method['name'],
                    arg_nums=method['args_nums'],
                    params=method['params'],
                    signature=method['signature'],
                    original_string=method['original_string'],
                    default_arguments=method['default_arguments'],
                    file=file['relative_path'],
                    attributes=method['attributes'],
                    docstring=method['docstring'],
                )
                self.build_testcase_metainfo(
                    file=file, cls={'name': '$'}, method=method # If there is no class, use $ as the class name
                )
                self.methods.append(_method)
                method_uris.append(uris)

            classes = file['classes']
            # if not classes:
            #     continue
            
            for cls in classes:
                method_list = []
                methods = cls['methods']
                for method in methods:
                    _method = Method(
                        # uri="#".join([file['relative_path'], cls['name'], method['name'], method['signature'].replace(' ', '').replace('\n', '')]),
                        uris=get_python_method_uris(
                            relative_path=file['relative_path'].strip('.py').replace('/', '.'),
                            method=method,
                            class_name=cls['name']), 
                        name=method['name'],
                        arg_nums=method['args_nums'],
                        params=method['params'],
                        signature=method['signature'],
                        original_string=method['original_string'],
                        default_arguments=method['default_arguments'],
                        file=file['relative_path'],
                        attributes=method['attributes'],
                        docstring=method['docstring'],
                        class_name=cls['name'],
                        class_uri=file['relative_path'] + cls['name']
                    )
                    # TODO: fix this, try to identify the unit test class.
                    self.build_testcase_metainfo(
                        file=file, cls=cls, method=method
                    )
                    self.methods.append(_method)
                    method_list.append(_method)
                
                name = cls['name']
                uris = get_class_uris(
                    relative_path=file['relative_path'],
                    class_name=cls['name']
                )
                _class = PythonClass(
                    # uri=file['relative_path'] + "#" + name,
                    uris=uris,
                    name=name,
                    file_path=file_path,
                    superclasses=cls['superclasses'],
                    methods=[method.name + "#" + str(method.arg_nums) for method in method_list],
                    method_uris=[method.uris for method in method_list],
                    class_docstring=cls['class_docstring'],
                    original_string=cls['original_string'],
                )
                superclasses: List[str] = cls['superclasses']
                if 'unittest.TestCase' in superclasses or 'TestCase' in superclasses:
                    self.testclasses.append(_class)
                # Fix this: class in testfile but not Testclass, we now also add it to normal class
                else:
                    self.classes.append(_class)
                class_uris.append(uris)

            _file = PythonFile(
                name=file_name,
                file_path=file_path, 
                original_string=file['original_string'],
                context=file['contexts'],
                _import=file['import'],
                _import_from=file['import_from'],
                global_variables=file['global_variables'],
                methods=method_uris,
                classes=class_uris,
                file_type=FileType.TEST if is_test_file else FileType.NORMAL
            )
            self.files.append(_file)
            if is_test_file:
                self.testfiles.append(_file)

    def resolve_inheritance(self):
        for cls in self.classes:
            for parent in cls.parents:
                for _class in self.classes:
                    if _class.name == parent:
                        cls.parents.append(_class.uri)
                        
                        for method in _class.methods:
                            if method.name not in cls.methods:
                                cls.methods.append(method)
                                
    # TODO: 建立uri -> class/method metainfo的索引，节省查找的时间

def run_python_metainfo_builder(metainfo_json_path):
    logger.info('run_build_metainfo start.')
    builder = PythonMetaInfoBuilder(metainfo_json_path)
    builder.build_metainfo()
    builder.save()


if __name__ == "__main__":
    pass