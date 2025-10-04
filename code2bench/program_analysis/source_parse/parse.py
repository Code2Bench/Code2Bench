import os
from enum import Enum

from source_parser.parsers.language_parser import LanguageParser
from source_parser.parsers import CppParser
from source_parser.parsers import JavaParser
from source_parser.utils import static_hash
from code2bench.program_analysis.source_parse.python_parser import RefinedPythonParser
from code2bench.utils.json_utils import save_json
from code2bench.config import config
from code2bench import logger


class LanguageEnum(Enum):
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"

LANGUAGE_TO_SUFFIX = {
    LanguageEnum.PYTHON: "py",
    LanguageEnum.JAVA: "java",
    LanguageEnum.CPP: "cpp",
    LanguageEnum.GO: "go",
}


def process_cpp_files(directory):
    parser = CppParser()
    all_results = []

    for root, dirs, files in os.walk(directory):
        # 检查当前目录是否是 build 目录，如果是则从 dirs 列表中移除，跳过此目录
        if 'build' in root.split(os.sep):
            dirs.clear()  # 清空dirs列表，避免递归进入子目录
            continue
        
        for file in files:
            if not file.endswith(('.cpp', '.h', '.hpp')):
                continue  # 跳过非 C++ 文件

            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents = f.read()

            statistics = {}
            try:
                processed_contents = parser.preprocess_file(file_contents)
                parser.update(processed_contents)
                if not processed_contents:
                    continue

            except Exception as e_err:
                logger.exception(f"\n\tFile {file_path} raised {type(e_err)}: {e_err}\n")
                continue

            statistics["number_of_lines"] = processed_contents.count("\n")
            statistics["number_of_chars"] = len(processed_contents)

            schema = parser.schema

            if not any(schema.values()):
                continue  # 跳过没有特征的文件

            statistics["relevant_files_with_structures"] = 1
            statistics["number_of_methods"] = len(schema["methods"])
            statistics["number_of_classes"] = len(schema["classes"])
            file_results = {
                "relative_path": file_path,
                "original_string": processed_contents,
            }
            file_results.update(schema)
            all_results.append(file_results)

    return all_results


class Processer:
    def __init__(self, 
                 repo_dir: str, 
                 language: LanguageEnum,
                 parser: LanguageParser):
        self.repo_dir = repo_dir
        self.language = language
        self.parser = parser
        
    def process_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
        self.parser.update(file_contents)
        return self.parser.schema
    
    def batch_procoess(self, directory):
        # directory是绝对路径
        results = []
        parser = self.parser
        file_suffix = LANGUAGE_TO_SUFFIX[self.language]
        
        for root, dirs, files in os.walk(directory):
            root_abs = os.path.abspath(root)
            
            # 跳过.开头的目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            new_dirs = []
            for d in dirs:
                if os.path.join(root_abs, d) not in config.EXCEPTE_PATH:
                    new_dirs.append(d)
            dirs[:] = new_dirs

            for file in files:
                if not file.endswith(file_suffix):
                    continue  # 跳过

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)

                try:
                    with open(file_path, 'r', encoding="utf-8") as f:
                        file_contents = f.read()
                except UnicodeDecodeError:
                    continue

                try:
                    processed_contents = parser.preprocess_file(file_contents)
                    parser.update(processed_contents)
                    if not processed_contents:
                        continue

                except Exception as e_err:
                    logger.exception(f"\n\tFile {file_path} raised {type(e_err)}: {e_err}\n")
                    continue

                schema = parser.schema

                if not any(schema.values()):
                    continue  # 跳过没有特征的文件

                file_results = {
                    "relative_path": relative_path,
                    "original_string": processed_contents,
                    "file_hash": static_hash(file_contents),  # REQUIRED!
                }
                file_results.update(schema)
                results.append(file_results)
                
        logger.info(f"{len(results)} files processed")
        return results

def process_python_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_contents = f.read()
    parser = RefinedPythonParser()
    parser.update(file_contents)
    return parser.schema

def batch_procoess(directory):
    results = []
    parser = RefinedPythonParser()
    
    for root, dirs, files in os.walk(directory):
        # 跳过.开头的目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.py'):
                continue  # 跳过非python文件

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents = f.read()

            try:
                processed_contents = parser.preprocess_file(file_contents)
                parser.update(processed_contents)
                if not processed_contents:
                    continue

            except Exception as e_err:
                logger.exception(f"\n\tFile {file_path} raised {type(e_err)}: {e_err}\n")
                continue

            schema = parser.schema

            if not any(schema.values()):
                continue  # 跳过没有特征的文件

            file_results = {
                "relative_path": relative_path,
                "original_string": processed_contents,
                "file_hash": static_hash(file_contents),  # REQUIRED!
            }
            file_results.update(schema)
            results.append(file_results)

    return results

def run_source_parse(repo_path: str, language: LanguageEnum, parser: LanguageParser):
    logger.info("start repo parsing...")
    processer = Processer(repo_dir=repo_path, language=language, parser=parser)
    results = processer.batch_procoess(repo_path)
    
    save_json(config.ALL_METAINFO_PATH, results)
    logger.info("repo parsed successfully!")
    
def run_python_source_parse(repo_path: str = ""):
    logger.info("start python repo parsing...")    
    run_source_parse(repo_path, LanguageEnum.PYTHON, RefinedPythonParser())


if __name__ == "__main__":
    # schema = process_python_file(file_path)
    # print(schema)
    
    repo_path = config.REPO_PATH
    processer = Processer(repo_dir=repo_path, language=LanguageEnum.PYTHON, parser=RefinedPythonParser())
    results = processer.batch_procoess(repo_path)
    save_json(config.ALL_METAINFO_PATH, results)