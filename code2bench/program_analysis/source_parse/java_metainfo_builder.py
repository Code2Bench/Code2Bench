from collections import defaultdict
from typing import Dict, List, Tuple

from code2bench.program_analysis.source_parse.metainfo_builder import MetaInfoBuilder
from code2bench.program_analysis.source_parse.model import JavaAbstractClass, JavaClass, JavaInterface, JavaMethodSignature, JavaRecord, Method, TestMethod
from code2bench.utils.json_utils import load_json, save_json
from code2bench.utils.java import get_java_standard_method_name
from code2bench import logger
from code2bench.config import config


class JavaMetaInfoBuilder(MetaInfoBuilder):
    def __init__(self, metainfo_json_path: str) -> None:
        super().__init__(metainfo_json_path)
        self.interfaces = []
        self.records = []
        self.abstract_classes = []
        self.brother_relations_path = config.BROTHER_RELATIONS_PATH
        
    def save(self):
        path_to_data = {
            config.CLASS_METAINFO_PATH: self.classes,
            config.METHOD_METAINFO_PATH: self.methods,
            config.RECORD_METAINFO_PATH: self.records,
            config.INTERFACE_METAINFO_PATH: self.interfaces,
            config.ABSTRACTCLASS_METAINFO_PATH: self.abstract_classes
        }
        self.save_metainfo(path_to_data)
        
    def resolve_brother_relation(self, save: bool = True):
        inherit_relations: List[Tuple[str, str]] = []
        childs: Dict[str, List[str]] = defaultdict(list)  # 父类 -> 子类
        self.class_metainfo = load_json(file_path=config.CLASS_METAINFO_PATH)
        
        for class_info in self.class_metainfo:
            class_name, parent_names = class_info['name'], class_info['superclasses']
            for parent_name in parent_names:
                inherit_relations.append((class_name, parent_name))
                childs[parent_name].append(class_name)
        
        brother_relations: Dict[str, List[str]] = {}
        for _, children in childs.items():
            if len(children) < 2:
                continue
            for child in children:
                # 构建兄弟关系
                if child not in brother_relations:
                    brother_relations[child] = []
                for sibling in children:
                    if sibling != child:
                        brother_relations[child].append(sibling)
        
        if save:
            save_json(file_path=self.brother_relations_path, data=brother_relations)

    def resolve_package_metainfo(self):
        self.file_imports = load_json(file_path=config.FILE_IMPORTS_PATH)
        package_to_file_path = defaultdict(list)
        for k, v in self.file_imports.items():
            if not v:
                continue
            package_to_file_path[v[0]].append(k)
        
        save_json(file_path=config.PACKAGES_METAINFO_PATH, data=package_to_file_path)
        logger.info(f"packages metainfo saved to {config.PACKAGES_METAINFO_PATH}")
        

    def resolve_interface_brother_relation(self):
        """
        {
            "uris": "",
            "name": "YourInterfaceName",
            "methods": [只要method的[Doctor]updateDoctor(DoctorUpdatedDataDTO)这一部分，还需要把继承的其他接口的方法也添加过来]，
            "implementations": [
                "class_uris1",
                "class_uris2",
            ]
        }
        """
        pass

    def resolve_file_imports(self, file_imports_path=config.FILE_IMPORTS_PATH):
        file_imports = {}
        junit_version = None

        for file in self.metainfo:
            if junit_version is None:
                if (
                    "import org.junit.jupiter.api.Test;" in file['contexts'] or
                    "import org.junit.jupiter.api.*;" in file['contexts']
                ):
                    junit_version = '5'
                    logger.info(f"Detected JUnit version: {junit_version}")
                elif "import org.junit.Test;" in file['contexts']:
                    junit_version = '4'
                    logger.info(f"Detected JUnit version: {junit_version}")
            file_imports[file['relative_path']] = file['contexts']
        
        if junit_version is None:
            logger.error("JUnit version not detected.")
            raise Exception("JUnit version not detected.")

        save_json(file_imports_path, file_imports)
        logger.info(f"Saved file imports to {file_imports_path}")
        
        save_json(config.JUNIT_VERSION_PATH, {"junit_version": junit_version})
        logger.info(f"Saved JUnit version to {config.JUNIT_VERSION_PATH}")

        return file_imports

    def get_standard_method_name(self, method: Method):
        return f'[{method.return_type}]' + method.name + \
            '(' + ','.join([param['type'] for param in method.params]) + ')'
            
    def is_non_marker_test_method(self, non_marker_annotations):
        for marker in non_marker_annotations:
            if 'ParameterizedTest' in marker or 'Test' in marker:
                return True
        return False

    def build_metainfo(self):
        testclass_set = set()
        for file in self.metainfo:
            file_path = file['relative_path']
            if file_path == "src/main/java/io/github/sashirestela/openai/BaseSimpleOpenAI.java":
                pass # For debug
            # # For java: method must be in class
            classes = file['classes']
            for cls in classes:
                is_test_class = False
                is_abstract_class = False
                inner_class = None
                method_list = []
                testcase_list = []
                methods = cls['methods']
                if 'abstract' in cls.get('attributes', {}).get('non_marker_annotations', []):
                    is_abstract_class = True
                
                inner_class = cls.get('attributes', {}).get('classes', [])
                if inner_class:
                    logger.info(f"Found inner class in {file_path} {cls['name']}")
                    
                    
                for method in methods:
                    marker_annotations = method['attributes'].get('marker_annotations', [])
                    non_marker_annotations = method['attributes'].get('non_marker_annotations', [])
                    return_type = method.get('attributes', {}).get('return_type', '')
                    uri = JavaMethodSignature(
                                file_path=file['relative_path'], 
                                class_name=cls['name'], 
                                method_name=method['name'], 
                                params=method['params'], 
                                return_type=return_type).unique_name()
                    if (
                        '@Test' in marker_annotations or
                        '@ParameterizedTest' in marker_annotations or
                        self.is_non_marker_test_method(non_marker_annotations)
                    ):
                        is_test_class = True
                        testcase = TestMethod(
                            uris=uri,
                            name=method['name'],
                            arg_nums=len(method['params']),
                            params=method['params'],
                            signature=method['signature'],
                            original_string=method['original_string'],
                            file=file['relative_path'],
                            attributes=method['attributes'],
                            docstring=method['docstring'],
                            class_name=cls['name'],
                            class_uri=file['relative_path'] + '.' + cls['name'],
                            return_type=return_type
                        )
                        self.testcases.append(testcase)
                        testcase_list.append(testcase)
                    else:
                        _method = Method(
                            uris=uri,
                            name=method['name'],
                            arg_nums=len(method['params']),
                            params=method['params'],
                            signature=method['signature'],
                            original_string=method['original_string'],
                            file=file['relative_path'],
                            attributes=method['attributes'],
                            docstring=method['docstring'],
                            class_name=cls['name'],
                            class_uri=file['relative_path'] + '.' + cls['name'],
                            return_type=return_type,
                        )
                        self.methods.append(_method)
                        method_list.append(_method)
                
                if is_abstract_class:
                    _class = JavaAbstractClass(
                        uris=file['relative_path'] + '.' + cls['name'],
                        name=cls['name'],
                        file_path=file_path,
                        superclasses=cls['superclasses'],
                        super_interfaces=cls['super_interfaces'],
                        methods=[self.get_standard_method_name(method) for method in method_list],
                        method_uris=[method.uris for method in method_list],
                        attributes=inner_class,
                        class_docstring=cls['class_docstring'],
                        original_string=cls['original_string'],
                        fields=cls.get('attributes', {}).get('fields', []),
                    )
                    self.abstract_classes.append(_class)
                elif not is_test_class:
                    _class = JavaClass(
                        uris=file['relative_path'] + '.' + cls['name'],
                        name=cls['name'],
                        file_path=file_path,
                        superclasses=cls['superclasses'],
                        super_interfaces=cls['super_interfaces'],
                        methods=[self.get_standard_method_name(method) for method in method_list],
                        method_uris=[method.uris for method in method_list],
                        attributes=inner_class,
                        class_docstring=cls['class_docstring'],
                        original_string=cls['original_string'],
                        fields=cls.get('attributes', {}).get('fields', []),
                    )
                    self.classes.append(_class)
                else:
                    if cls['name'] in testclass_set:
                        continue

                    name = cls['name']
                    _class = JavaClass(
                        uris=file['relative_path'] + '.' + cls['name'],
                        name=name,
                        file_path=file_path,
                        superclasses=cls['superclasses'],
                        super_interfaces=cls['super_interfaces'],
                        methods=[self.get_standard_method_name(testcase) for testcase in testcase_list],
                        method_uris=[method.uris for method in method_list],
                        attributes=inner_class,
                        class_docstring=cls['class_docstring'],
                        original_string=cls['original_string'],
                        fields=cls.get('attributes', {}).get('fields', []),
                    )
                    self.testclasses.append(_class)
                    testclass_set.add(name) # 我当时为啥要加这个set来着？
                    
            for record in file['records']: 
                r = JavaRecord(
                    uris=file['relative_path'] + '.' + record['name'],
                    name=record['name'],
                    methods=record['methods'],
                    attributes=record['attributes'],
                    class_docstring=record['class_docstring'],
                    original_string=record['original_string'],
                    fields=record['fields'],
                )
                self.records.append(r)
                
            for interface in file['interfaces']:
                method_list = []
                methods = interface['methods']
                for method in methods:
                    _method = Method(
                        uris=file['relative_path'] + '.' + interface['name'] + '.' + get_java_standard_method_name(
                            method_name=method['name'],
                            params=method['params'],
                            return_type=method.get('attributes', {}).get('return_type', '')
                        ),
                        name=method['name'],
                        arg_nums=len(method['params']),
                        params=method['params'],
                        signature=method['signature'],
                        original_string=method['original_string'],
                        file=file['relative_path'],
                        attributes=method['attributes'],
                        docstring=method['docstring'],
                        class_name=interface['name'],
                        class_uri=file['relative_path'] + '.' + interface['name'],
                        return_type=method.get('attributes', {}).get('return_type', ''),
                    )
                    self.methods.append(_method)
                    method_list.append(_method)
                        
                i = JavaInterface(
                    uris=file['relative_path'] + '.' + interface['name'],
                    name=interface['name'],
                    file_path=file_path,
                    superclasses=interface['extends_interfaces'],
                    methods=[self.get_standard_method_name(method) for method in method_list],
                    method_uris=[method.uris for method in method_list],
                    class_docstring=interface['interface_docstring'],
                    original_string=interface['original_string'],
                    fields=interface.get('attributes', {}).get('fields', []),
                )
                self.interfaces.append(i)
                

def run_java_metainfo_builder(metainfo_json_path):
    logger.info('run_java_metainfo_builder start.')
    builder = JavaMetaInfoBuilder(metainfo_json_path)
    builder.build_metainfo()
    builder.save()