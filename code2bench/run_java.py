import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple

from code2bench.config import config
from code2bench.driver_generator.driver_generator import generate_one_driver
from code2bench.driver_generator.testcases_generator import run_once_testcase_generation
from code2bench.func_selector.func_selector import extract_all_type_hints, select_function
from code2bench.func_selector.groundtruth_filter import filter_groundtruth, filter_and_refactor_class_method
from code2bench.instruction_generator.instruction_generator import assess_difficulty, generate_one_instruction, judge_instruction, modify_instruction
from code2bench.data_model import FuncToGenerate, FuncType
from code2bench.llm.llm_caller import call_llm
from code2bench.pipeline.reasoning.reasoning import generate_reasoning_testcases, generate_reasoning_testcases_outputs
from code2bench.program_analysis.source_parse.java_metainfo_builder import run_java_metainfo_builder
from code2bench.program_analysis.source_parse.parse import run_java_source_parse, run_python_source_parse
from code2bench.program_analysis.source_parse.python_metainfo_builder import run_python_metainfo_builder
from code2bench import logger, llm_client
from code2bench.runner_generator.runner_generator import generate_one_runner, generate_runner_with_llm, generate_runner_without_llm
from code2bench.test_runner.dry_run import add_settings_decorator, dry_run
from code2bench.utils.helper import (
    get_index_dicts, get_func_list, deduplicate_dict_values, get_existing_func_name_list
)
from code2bench.utils.json_utils import get_java_response, load_json, save_json
from code2bench.utils.python import detect_other_imports, extract_typing_imports
from code2bench.run_weakly_self_contained import batch_run_weakly
from code2bench.func_selector.java_func_selector import select_function_for_java
from code2bench.driver_generator.testcases_generator import run_once_testcase_generation_java
from code2bench.runner_generator.runner_generator import generate_java_runner
from code2bench.program_analysis.cyclomatic_complexity.cyclomatic_complexity_analyzer import analyze_cyclomatic_complexity


def copy_template_to_package(package_name: str) -> bool:
    """
    从template目录复制文件到指定包目录
    
    :param package_name: 目标包名（如"p2"）
    :return: 复制成功返回True，失败返回False
    """
    # 基础路径定义
    base_dir = "/data/zhangzhe/code2bench/benchmark/Pure_Java"
    source_dir = os.path.join(base_dir, "template")
    dest_dir = os.path.join(base_dir, package_name)
    
    # 输入验证
    if not package_name or not isinstance(package_name, str):
        logger.error("无效的包名: 必须提供非空字符串")
        return False
    
    # 检查源目录是否存在
    if not os.path.isdir(source_dir):
        logger.error(f"源模板目录不存在: {source_dir}")
        return False
    
    try:
        # 如果目标目录已存在，先删除以确保干净复制
        if os.path.exists(dest_dir):
            logger.warning(f"目标目录已存在，将删除并重建: {dest_dir}")
            shutil.rmtree(dest_dir)
        
        # 复制整个目录树
        shutil.copytree(source_dir, dest_dir)
        
        # 把/data/zhangzhe/code2bench/benchmark/Pure_Java/template/src/main/java/template这个目录重命名为/data/zhangzhe/code2bench/benchmark/Pure_Java/package_name/src/main/java/package_name
        # 重命名 src/main/java/template 为 src/main/java/package_name
        java_src_dir = os.path.join(dest_dir, "src", "main", "java")
        old_package_dir = os.path.join(java_src_dir, "template")
        new_package_dir = os.path.join(java_src_dir, package_name)
        if os.path.exists(old_package_dir):
            os.rename(old_package_dir, new_package_dir)
        else:
            logger.warning(f"未找到目录: {old_package_dir}，无法重命名为 {new_package_dir}")
            raise FileNotFoundError(f"未找到目录: {old_package_dir}，无法重命名为 {new_package_dir}")
            
        # 还需要完成benchmark/Pure_Java/template/src/main/java/template/Helper.java的替换，把其中的package template改为package package_name
        helper_file = os.path.join(new_package_dir, "Helper.java")
        if os.path.exists(helper_file):
            with open(helper_file, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("package template;", f"package {package_name};")
            with open(helper_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            raise FileNotFoundError(f"未找到文件: {helper_file}，无法进行包名替换")
        
        logger.info(f"成功将模板复制到: {dest_dir}")
        return True
        
    except Exception as e:
        logger.error(f"复制目录失败: {str(e)}", exc_info=True)
        return False
    
def get_java_groundtruth(func_str: str, idx, llm_client):
    """
    调用LLM来把self contained的Java函数代码外层包成一层类的形式：
    输入：
    ```java
    public private int add(int x, int y) {
        return x + y;
    }
    ```
    输出：
    ```java
    package template;
    public class GroundTruth {
        public static int add(int x, int y) {
            return x + y;
        }
    }
    ```
    无论输入的被测函数是private还是public，输出的都是public且static的。
    """
    system_prompt = """
你是一名 Java 代码重构专家。请将下面输入的 Java 函数（可能是 private 或 public、带或不带 static 的成员方法）**包装成如下格式**：

- 外层包名为 `template`
- 类名为 `GroundTruth`
- 方法必须是 `public static`，方法名和参数保持不变
- 方法体和逻辑保持不变
- 移除原有的 `private` 或 `protected` 修饰符，仅保留 `public static`
- 如果原方法没有 static，请加上 static
- 保证方法可以被 `GroundTruth.funcName(...)` 直接静态调用

**输入示例：**
```java
private int add(int x, int y) {
    return x + y;
}
```

**输出示例：**
```java
package template;
public class GroundTruth {
    public static int add(int x, int y) {
        return x + y;
    }
}
```

**再如：**
```java
public String foo(String s) {
    return s.trim();
}
```
输出：
```java
package template;
public class GroundTruth {
    public static String foo(String s) {
        return s.trim();
    }
}
```

**要求：**
- 只输出完整的 Java 代码，不要解释
- 方法体和参数名保持原样
- 只输出一个类 GroundTruth，方法为 public static
"""
    response = call_llm(llm_client, system_message=system_prompt, user_message=func_str, clean=False)
    java_code = get_java_response(response)
    if not java_code:
        raise ValueError(f"Failed to get valid Java code from LLM for function {idx}. Response: {response}")
    # 完成package的替换
    java_code = java_code.replace("package template;", f"package {idx};")
    return java_code

def run_once_java(idx: str, func: FuncToGenerate) -> Tuple[bool, str]:
    func_name = func.name
    func_str = func.original_str
    
    # # 确保目标目录存在
    # benchmark_dir = Path(config.BENCHMARK_PATH) / str(idx)
    # benchmark_dir.mkdir(parents=True, exist_ok=True)
    
    # # 把groundtruth输出到对应的文件中
    # type_hints = extract_all_type_hints(func_str=func_str)
    # import_statement = extract_typing_imports(type_hints=type_hints)
    # func_str = import_statement + "\n\n" + func_str
    # groundtruth_path = Path(config.BENCHMARK_PATH) / str(idx) / "groundtruth.py"
    # with open(groundtruth_path, "w") as f:
    #     f.write(func_str)
    # logger.info(f"Generated groundtruth for function {idx}.")

    idx = "p" + idx

    copy_template_to_package(idx)

    java_code = get_java_groundtruth(func_str, idx, llm_client)

    # /data/zhangzhe/code2bench/benchmark/Pure_Java/p2/src/main/java/p1/Tested.java
    groundtruth_path = Path(config.BENCHMARK_PATH) / str(idx) / "src/main/java" / str(idx) / "GroundTruth.java"
    # 判断路径是否存在，如果路径不存在的话，就创建这个路径
    if not os.path.exists(os.path.dirname(groundtruth_path)):
        os.makedirs(os.path.dirname(groundtruth_path))

    with open(groundtruth_path, "w") as f:
        f.write(java_code)
    logger.info(f"Generated groundtruth for function {idx}.")
    
    # # # 1. 先进行难度判断
    # difficulty = assess_difficulty(func, llm_client)
    
    # # 2. 生成Testcase
    status, reason = run_once_testcase_generation_java(idx=idx, from_path=f"src/main/java/{idx}/GroundTruth.java", to_path="src/test/java/TestCaseGenerator.java", )
    if status is False:
        return False, reason
    
    # # 2. 生成Example Usage
    # example_usages, reason = generate_reasoning_testcases(idx, llm_client)
    # if not example_usages:
    #     return False, "Failed to generate example usages" + "###" + reason
    
    # 4. 生成Instruction
    max_retries = 3
    retry_count = 0
    last_error = None
    last_res = None
    while retry_count < max_retries:
        # 把instruction输出到对应的文件中
        generated_instruction = generate_one_instruction(func, llm_client, last_res=last_res, last_error=last_error, example_usages=None)
        if generated_instruction.error:
            logger.info(f"Failed to generate instruction for function {idx}: {func_name} Due to error: {generated_instruction.error}")
            last_error = generated_instruction.error
            last_res = generated_instruction.instruction
            retry_count += 1
            continue
        
        # # 找一个judger过来判断
        # judge_res = judge_instruction(generated_instruction.instruction, llm_client)
        # # for key, value in judge_res.items():
        # #     if value.get("status") == "ISSUE":
        # if judge_res.get("issues"):
        #     # logger.info(f"Instruction review failed for function {idx}: {func_name} Due to reason: {key}")
        #     modified_instruction = modify_instruction(func.original_str, generated_instruction.instruction, judge_res, llm_client)
        #     # 默认可以修改成功
        #     if modified_instruction:
        #         generated_instruction.instruction = modified_instruction
        #     break
        
        if generated_instruction.instruction:
            break
        retry_count += 1
    
    instruction = generated_instruction.instruction
    # print(instruction)
    if not instruction:
        return False, "Failed to generate instruction" + "###" + generated_instruction.error
        
    # Write pure instruction first
    # 添加package声明
    package_declaration = f"package {idx};\n\n"
    if package_declaration not in instruction:
        instruction = package_declaration + instruction
    instruction = instruction.replace("package template;", f"package {idx};")
    instruction_path = Path(config.BENCHMARK_PATH) / idx / "Instruction.java"
    with open(instruction_path, "w") as f:
        f.write(instruction)

    # # Write python instruction to file
    # instruction_path = Path(config.BENCHMARK_PATH) / idx / "instruction.txt"
    # python_instruction = (
    #     # f"### Instruction\n{instruction}\n\n"
    #     f"{instruction}\n"
    #     # f"### Example Usages\n{example_usages}\n\n"
    #     f"You should write code starting with:\n{python_signature}\n\n"
    # )
    # with open(instruction_path, "w") as f:
    #     f.write(python_instruction)

    # logger.info(f"Generated instruction for function {idx}.")
    
    # 在tested.py中添加函数, pass就可以了，防止import失败
    tested_path = Path(config.BENCHMARK_PATH) / idx / "src/main/java" / str(idx) / "Tested.java"
    # 添加package声明
    package_declaration = f"package {idx};\n\n"
    if package_declaration not in instruction:
        instruction = package_declaration + instruction
    # 把instruction写入到Tested.java中
    if not os.path.exists(os.path.dirname(tested_path)):
        os.makedirs(os.path.dirname(tested_path))
    # 这里的instruction是Java的，所以直接写入即可
    with open(tested_path, "w") as f:
        # f.write(f"def {func_name}(*args, **kwargs):\n    pass\n")
        f.write(instruction)

    # # Add difficulty
    # metainfo_path = Path(config.BENCHMARK_PATH) / idx / "metainfo.json"
    # save_json(file_path=metainfo_path, data={
    #     "project": config.PROJECT_NAME,
    #     "project_url": config.PROJECT_URI,
    #     "uri": func.uri,
    #     "func_name": func_name,
    #     "difficulty": difficulty,
    #     "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # })
    
    # # 5. 生成Python的Runner
    # status, reason = generate_runner_without_llm(idx, func_name=func_name, language="Python")
    # if not status:
    #     return False, reason

    # # 生成其他语言的Runner
    # # generate_runner_with_llm(idx, language="Go", func_name=func_name)
    # # logger.info(f"Generated Go runner for function {idx}.")

    # status, reason = generate_runner_with_llm(idx, language="TS", func_name=func_name)
    # if not status:
    #     return False, reason
    # logger.info(f"Generated TS runner for function {idx}.")

    # status, reason = generate_runner_with_llm(idx, language="JS", func_name=func_name)
    # if not status:
    #     return False, reason
    # logger.info(f"Generated TS runner for function {idx}.")
    
    # status, reason = generate_runner_with_llm(idx, language="Go", func_name=func_name)
    # if not status:
    #     return False, reason
    # logger.info(f"Generated Go runner for function {idx}.")

    # status, reason = generate_runner_with_llm(idx, language="Java", func_name=func_name)
    # if not status:
    #     return False, reason
    # logger.info(f"Generated Java runner for function {idx}.")
    
    status, reason = generate_java_runner(idx, llm=llm_client, func=func)
    if not status:
        return False, "generate_java_runner error:" + reason
    
    # 添加metainfo.json
    metainfo_path = Path(config.BENCHMARK_PATH) / idx / "metainfo.json"
    save_json(file_path=metainfo_path, data={
        "project": config.PROJECT_NAME,
        "project_url": config.PROJECT_URI,
        "uri": func.uri,
        "func_name": func_name,
        # "difficulty": difficulty,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return True, ""

def batch_run_java(specific_func_name=None) -> int:
    # max_num = get_benchmark_max_function_num(benchmark_path=BENCHMARK_PATH)
    max_num = 0
    candidate_max_num = 0
    excluded_max_num = 0
    error_max_num = 0
    index_dict: Dict[str, str] = {}
    func_to_idx: Dict[str, str] = {}
    skip_dict: Dict[str, List[str]] = {}
    candidate_index_dict: Dict[str, str] = {}
    excluded_index_dict: Dict[str, str] = {}
    error_index_dict: Dict[str, str] = {}
    if os.path.exists(config.JAVA_CANDIDATE_POOL_INDEX_PATH):
        candidate_index_dict = load_json(config.JAVA_CANDIDATE_POOL_INDEX_PATH)
        candidate_list = [int(idx) for idx in candidate_index_dict.keys()]
        candidate_max_num = max(candidate_list)

    if os.path.exists(config.JAVA_EXCLUDED_POOL_INDEX_PATH):
        excluded_index_dict = load_json(config.JAVA_EXCLUDED_POOL_INDEX_PATH)
        if not excluded_index_dict:
            raise ValueError(f"Failed to load excluded index dict from {config.JAVA_EXCLUDED_POOL_INDEX_PATH}")
        excluded_list = [int(idx) for idx in excluded_index_dict.keys()]
        excluded_max_num = max(excluded_list)
        
    if os.path.exists(config.JAVA_GENERATION_ERROR_POOL_INDEX_PATH):
        error_index_dict = load_json(config.JAVA_GENERATION_ERROR_POOL_INDEX_PATH)
        error_list = [int(idx) for idx in error_index_dict.keys()]
        error_max_num = max(error_list)

    benchmark_index_path, benchmark_skip_path = get_index_dicts()
    if os.path.exists(benchmark_index_path):
        index_dict = load_json(benchmark_index_path)
        index_list = [int(idx) for idx in index_dict.keys()]
        max_num = max(max_num, max(index_list)) + 1
        func_to_idx = {func: idx for idx, func in index_dict.items()}
    if os.path.exists(benchmark_skip_path):
        skip_dict = load_json(benchmark_skip_path)

    func_list = get_func_list()

    cnt = 0
    for func in func_list:
        if max_num > 500:
            logger.info("Generated 500 benchmarks, stop.")
            break

        # if cnt >= 10:
        #     logger.info("Generated 10 benchmarks, stop.")
        #     break
        
        # if func['cyclomatic_complexity'] < config.CYCLOMATIC_COMPLEXITY:
        #     continue
        
        # if func['cyclomatic_complexity'] > config.MAX_CYCLOMATIC_COMPLEXITY:
        #     logger.info(f"Function {func['uris']} cyclomatic complexity is {func['cyclomatic_complexity']}, skip it.")
        #     continue

        # 代码行数＜3直接去掉

        
        # uri = config.PROJECT_NAME + '.' + func['uris']
        uri = func['uri']
        
        # if uri != "spring-ai-alibaba-jmanus/src/main/java/com/alibaba/cloud/ai/manus/tool/uploadedFileLoader/UploadedFileLoaderTool.java.UploadedFileLoaderTool.[String]formatFileSize(long)":
        #     continue
                
        if uri in skip_dict.get(config.PROJECT_NAME, []):
            continue
        
        if uri in excluded_index_dict.values():
            logger.info(f"Function {uri} is already in excluded pool.")
            continue
        
        if func['arg_nums'] == 0:
            continue

        idx = func_to_idx.get(uri)
        if idx is not None:
            continue
        
        # Filter the function name that already exists
        func_name_list = get_existing_func_name_list(func_to_idx)
        func_name = func['uri'].split(']')[-1].split('(')[0]
        if func_name in func_name_list:
            logger.info(f"Function {func_name} already exists, may be semantic similar, skip it.")
            continue
            
        if specific_func_name is not None and func_name != specific_func_name:
            logger.info(f"Function {func_name} is not the specific function {specific_func_name}, skip it.")
            continue

        # Write to candidate pool
        candidate_max_num += 1
        directory = Path(config.JAVA_CANDIDATE_POOL_PATH) / str(candidate_max_num)
        directory.mkdir(parents=True, exist_ok=True)
        candidate_path = directory / "candidate.java"
        with open(candidate_path, "w") as f:
            f.write(func['code'])
        
        candidate_index_dict[str(candidate_max_num)] = uri
        save_json(config.JAVA_CANDIDATE_POOL_INDEX_PATH, deduplicate_dict_values(candidate_index_dict))
        logger.info(f"Generated candidate for function {candidate_max_num}, {uri}")

        func_str = func['code']
        func_name = func_str.split("(")[0].split()[-1]
        if config.MODE == FuncType.JAVA_SELF_CONTAINED:
            func = FuncToGenerate(original_str=func_str, func_type=FuncType.JAVA_SELF_CONTAINED, name=func_name, uri=uri)
        else:
            raise ValueError(f"Unsupported mode: {config.MODE}")
        
        if uri in excluded_index_dict.values():
            logger.info(f"Function {uri} is already in excluded pool.")
            continue
            
        status, reason = filter_groundtruth(func, llm_client)
        if not status:
            # write to excluded pool
            excluded_max_num += 1
            directory = Path(config.JAVA_EXCLUDED_POOL_PATH) / str(excluded_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            excluded_path = directory / "excluded.java"
            with open(excluded_path, "w") as f:
                f.write(func.original_str)
                f.write("\n")
                f.write(f"# Reason: {reason}")
            excluded_index_dict[str(excluded_max_num)] = uri
            save_json(config.JAVA_EXCLUDED_POOL_INDEX_PATH, deduplicate_dict_values(excluded_index_dict))
            logger.info(f"Function {idx}: {func_name} is not suitable for benchmark.")
            continue
        
        
        idx = str(max_num)
        try:
            status, reason = run_once_java(idx, func)
        except Exception as e:
            logger.error(f"Failed to generate benchmark for function {idx}: {e}")
            import traceback
            traceback.print_exc()
            status = False
            reason = "Run once error:" + str(e)
            
        if status:
            max_num += 1
            index_dict[idx] = uri
            func_to_idx[uri] = idx 
            save_json(benchmark_index_path, deduplicate_dict_values(index_dict))
            logger.info(f"Generated benchmark for function {idx}, {uri}")
            cnt += 1
        else:
            idx = 'p' + idx
            benchmark_dir = Path(config.BENCHMARK_PATH) / idx
            # 如果生成失败了，存到错误池中
            # write to error pool
            error_max_num += 1
            directory = Path(config.JAVA_GENERATION_ERROR_POOL_PATH) / str(error_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            # Move benchmark_dir to error pool
            # 移动 benchmark_dir 的内容到 directory
            # for item in benchmark_dir.iterdir():
            #     shutil.move(str(item), str(directory))
            logger.info(f"Moved {benchmark_dir} to {directory}")
            error_index_dict[str(error_max_num)] = uri
            save_json(config.JAVA_GENERATION_ERROR_POOL_INDEX_PATH, deduplicate_dict_values(error_index_dict))

            # 如果生成失败了，生成过程中创建的文件可以不手动删除，因为下次生成时会覆盖
            if config.PROJECT_NAME not in skip_dict:
                skip_dict[config.PROJECT_NAME] = []
            skip_dict[config.PROJECT_NAME].append(uri)
            logger.info(f"Failed to generate benchmark for function {max_num}, {uri}")
            save_json(benchmark_skip_path, deduplicate_dict_values(skip_dict))
            
            # 算了，需要手动删除的！
            if benchmark_dir.exists():
                shutil.rmtree(benchmark_dir)

    return cnt

def run_pipeline_java(project_path, start_time=None, end_time=None):
    run_java_source_parse(repo_path=project_path)

    run_java_metainfo_builder(metainfo_json_path=config.ALL_METAINFO_PATH)

    select_function_for_java(start_time=start_time, end_time=end_time)
     
def run_git_clone(project_name: str, uri: str, workspace_path: str, use_proxy: bool = False) -> bool:
    """
    克隆指定的 Git 仓库到工作区路径。

    :param project_name: 项目名称。
    :param uri: Git 仓库的 URI。
    :param workspace_path: 工作区路径。
    :param use_proxy: 是否使用代理，默认为 False。
    """
    project_path = Path(workspace_path) / project_name

    # 如果项目路径已经存在，则跳过克隆
    if project_path.exists():
        logger.info(f"Project {project_name} already exists at {project_path}. Remove it.")
        # return True
        shutil.rmtree(project_path)
    
    logger.info(f"Cloning {project_name} from {uri} to {project_path}...")

    # 构建 git clone 命令
    command = ["git", "clone", uri, str(project_path)]

    # 如果使用代理，则设置环境变量
    env = os.environ.copy()
    if use_proxy:
        proxy = config.PROXY_URL
        logger.debug(f"Using proxy server: {proxy}")
        env["http_proxy"] = proxy
        env["https_proxy"] = proxy

    # 执行 git clone 命令
    try:
        result = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=240  # 5分钟超时
        )
        logger.info(f"Command output:\n{result.stdout}")
        logger.info(f"Successfully cloned {project_name} from {uri} to {project_path}.")
        return True
    except subprocess.CalledProcessError as e:
        logger.info(f"Failed to clone {project_name} from {uri}. Error: {e.stderr}")
        return False

def run_git_pull(project_name: str, project_path: str, branch: str = None, use_proxy: bool = False) -> bool:
    """
    拉取指定 Git 仓库的最新更改（增强代理支持版）

    :param project_name: 项目名称
    :param project_path: 项目路径（建议使用绝对路径）
    :param use_proxy: 是否使用代理，默认为 False
    :return: 操作是否成功
    """
    # 转换为 Path 对象统一处理路径
    project_path = Path(project_path).resolve()  # 确保获取绝对路径
    
    if not project_path.exists():
        logger.error(f"项目路径不存在：{project_path}")
        return False

    logger.info(f"开始更新项目 {project_name} @ {project_path}...")

    # if branch:
    #     logger.info(f"切换到分支 {branch}...")
    #     # switch_branch(project_name, project_path, branch)
    #     # 构建基础命令
    #     command = ["git", "-C", str(project_path), "pull", f"origin/{branch}"]
    # else:
    # 构建基础命令
    command = ["git", "-C", str(project_path), "pull"]

    # 代理配置增强
    env = os.environ.copy()
    if use_proxy:
        # 验证代理地址格式
        if not config.PROXY_URL.startswith(("http://", "https://")):
            logger.error("代理地址格式错误，必须包含协议声明（http:// 或 https://）")
            return False
            
        logger.debug(f"使用代理服务器：{config.PROXY_URL}")
        
        # 同时设置大小写敏感的环境变量
        proxy = config.PROXY_URL
        env.update({
            "http_proxy": proxy,
            "HTTP_PROXY": proxy,
            "https_proxy": proxy,
            "HTTPS_PROXY": proxy,
        })

        # # 添加 Git 特定配置
        # command.extend([
        #     "-c", f"http.proxy={proxy}",
        #     "-c", f"https.proxy={proxy}"
        # ])

    # 执行命令（增强错误处理）
    try:
        result = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=30  # 5分钟超时
        )
        logger.info(f"命令输出：\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"拉取失败（退出码 {e.returncode}）：\n{e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("操作超时（超过5分钟）")
        return False
    
def switch_branch(project_name: str, project_path: str, branch: str) -> bool:
    """
    切换到指定的 Git 分支。

    :param project_name: 项目名称。
    :param project_path: 项目路径。
    :param branch: 要切换到的分支名称。
    :return: 如果切换成功，返回 True；否则返回 False。
    """
    if branch:
        # 构建 git checkout 命令
        command = ["git", "-C", project_path, "checkout", branch]
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )
            logger.info(f"Command output:\n{result.stdout}")
            logger.info(f"Switched to branch {branch} for project {project_name}.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to switch to branch {branch} for project {project_name}. Error: {e}")
            return False

def run_one_project_java(project_name: str, uri: str, branch: str=None, start_time=None, end_time=None,
                        skip_pipeline: bool = False, use_proxy: bool = False, mode: FuncType = FuncType.SELF_CONTAINED,
                        only_pipeline: bool = False):
    config.PROJECT_NAME = project_name
    config.PROJECT_URI = uri
    config.MODE = mode
    config.REPO_PATH_JAVA = project_name

    project_path = str(Path(config.WORKSPACE_PATH) / config.PROJECT_NAME)
    
    # if os.path.exists(project_path):
    #     logger.info(f"Project {project_name} already exists at {project_path}. Continue.")
    #     return

    # if only_pipeline:
    #     # 暂时先注释了
    #     file_list = []
    #     if os.path.exists(project_path):
    #         file_list = os.listdir(project_path)
    #     file_list = [f for f in file_list if f != "playground"]
    #     if os.path.exists(project_path) and len([f for f in file_list if not f.startswith(".")]) > 0:
    #         # run git pull
    #         run_git_pull(project_name=config.PROJECT_NAME, project_path=project_path, branch=branch, use_proxy=use_proxy)
    #     else:
    #         run_git_clone(project_name=project_name, uri=uri, workspace_path=config.WORKSPACE_PATH, use_proxy=use_proxy)
        
    #     switch_branch(project_name, project_path, branch)
    
    #####################
    if not skip_pipeline:
        # 新开一个，会先跳过当前目录下已经有的
        exsiting_projects = os.listdir(config.WORKSPACE_PATH)
        if project_name in exsiting_projects:
            logger.info(f"Project {project_name} already exists at {project_path}.")
            return
        run_git_clone(project_name=project_name, uri=uri, workspace_path=config.WORKSPACE_PATH, use_proxy=use_proxy)
    ######################
    
    if skip_pipeline is False:
        run_pipeline_java(project_path, start_time=start_time, end_time=end_time)
        # pass

    # run_once("002")
    if only_pipeline:
        return
    
    if config.MODE == FuncType.JAVA_SELF_CONTAINED:
        success_num = batch_run_java()
    # elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
    #     raise NotImplementedError("WEAKLY_SELF_CONTAINED mode is not implemented for Java yet.")
    # elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
    #     raise NotImplementedError("LEVEL_SELF_CONTAINED mode is not implemented for Java yet.")
    logger.info(f"Generated {success_num} benchmarks.")

def run_all_projects_java(start_time=None, end_time=None, skip_pipeline: bool = False, 
                     use_proxy: bool = False, mode: FuncType = FuncType.SELF_CONTAINED,
                     only_pipeline: bool = False):
    projects = load_yaml_config(config.JAVA_PROJECTS_PATH)
    java_projects = projects.get("Java", [])
    branch = projects.get("branch")
    # 按 URL 去重
    java_projects = deduplicate_projects_by_url(java_projects)
    java_projects = sorted(java_projects, key=lambda x: x['name'])

    for project in java_projects:
        try:
            logger.info(f"Running project {project['name']}...")
            config.PROJECT_NAME = project["name"]
            
            # if project["name"][0] < 'o':
            #     continue

            run_one_project_java(project["name"], project["url"], 
                            branch=branch, start_time=start_time, 
                            end_time=end_time, skip_pipeline=skip_pipeline, 
                            use_proxy=use_proxy, mode=mode, only_pipeline=only_pipeline)
        except Exception as e:
            logger.error(f"Failed to run project {project['name']}. Error: {e}")
            import traceback
            traceback.print_exc()
            continue


import yaml

def deduplicate_projects_by_url(projects_list):
    """
    对项目列表按 URL 进行去重，保留第一个出现的项目。

    Parameters:
    - projects_list (list): 项目列表，每个项目是包含 'name' 和 'url' 的字典。

    Returns:
    - list: 去重后的项目列表。
    """
    seen_urls = set()
    unique_projects = []

    for project in projects_list:
        url = project.get('url')
        if url and url not in seen_urls:
            unique_projects.append(project)
            seen_urls.add(url)

    return unique_projects

def load_yaml_config(file_path: str):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == '__main__':    
    config.MODE = FuncType.JAVA_SELF_CONTAINED
    config.BENCHMARK_NAME = "Pure_Java"
    config.WORKSPACE_PATH = "workspace_java"
    
    run_all_projects_java(start_time='2025-05-01', end_time='2025-09-30', 
                     skip_pipeline=False, use_proxy=True, mode=FuncType.JAVA_SELF_CONTAINED,
                     only_pipeline=True)
