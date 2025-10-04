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
from code2bench.func_selector.groundtruth_filter import filter_groundtruth
from code2bench.instruction_generator.instruction_generator import assess_difficulty, generate_one_instruction
from code2bench.data_model import FuncToGenerate, FuncType
from code2bench.pipeline.reasoning.reasoning import generate_reasoning_testcases, generate_reasoning_testcases_outputs
from code2bench.program_analysis.source_parse.parse import run_python_source_parse
from code2bench.program_analysis.source_parse.python_metainfo_builder import run_python_metainfo_builder
from code2bench import logger, llm_client
from code2bench.runner_generator.runner_generator import generate_one_runner, generate_runner_with_llm, generate_runner_without_llm
from code2bench.test_runner.dry_run import add_settings_decorator, dry_run
from code2bench.utils.helper import (
    get_index_dicts, get_func_list, deduplicate_dict_values, get_existing_func_name_list
)
from code2bench.utils.json_utils import load_json, save_json
from code2bench.utils.python import detect_other_imports, extract_typing_imports
from code2bench.run_weakly_self_contained import batch_run_weakly


def run_once(idx: str, func: FuncToGenerate) -> Tuple[bool, str]:    
    func_name = func.name
    func_str = func.original_str
    
    benchmark_dir = Path(config.BENCHMARK_PATH) / str(idx)
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    
    type_hints = extract_all_type_hints(func_str=func_str)
    import_statement = extract_typing_imports(type_hints=type_hints)
    func_str = import_statement + "\n\n" + func_str
    groundtruth_path = Path(config.BENCHMARK_PATH) / str(idx) / "groundtruth.py"
    with open(groundtruth_path, "w") as f:
        f.write(func_str)
    logger.info(f"Generated groundtruth for function {idx}.")
    
    difficulty = assess_difficulty(func, llm_client)
    
    status, reason = run_once_testcase_generation(idx=idx, from_path="groundtruth.py", to_path="testcase_generator.py", )
    if status is False:
        return False, reason
    
    example_usages, reason = generate_reasoning_testcases(idx, llm_client)
    if not example_usages:
        return False, "Failed to generate example usages" + "###" + reason
    
    max_retries = 3
    retry_count = 0
    last_error = None
    last_res = None
    while retry_count < max_retries:
        generated_instruction, python_signature = generate_one_instruction(func, llm_client, last_res=last_res, last_error=last_error)
        if generated_instruction.error:
            logger.info(f"Failed to generate instruction for function {idx}: {func_name} Due to error: {generated_instruction.error}")
            last_error = generated_instruction.error
        last_res = generated_instruction.instruction
        if generated_instruction.instruction:
            break
        retry_count += 1
    
    instruction = generated_instruction.instruction
    # print(instruction)
    if not instruction:
        return False, "Failed to generate instruction" + "###" + generated_instruction.error
        
    # Write pure instruction first
    pure_instruction_path = Path(config.BENCHMARK_PATH) / idx / "pure_instruction.txt"
    with open(pure_instruction_path, "w") as f:
        f.write(instruction)

    # Write python instruction to file
    instruction_path = Path(config.BENCHMARK_PATH) / idx / "instruction.txt"
    python_instruction = (
        # f"### Instruction\n{instruction}\n\n"
        f"{instruction}\n"
        # f"### Example Usages\n{example_usages}\n\n"
        f"You should write code starting with:\n{python_signature}\n\n"
    )
    with open(instruction_path, "w") as f:
        f.write(python_instruction)

    logger.info(f"Generated instruction for function {idx}.")
    
    tested_path = Path(config.BENCHMARK_PATH) / idx / "tested.py"
    with open(tested_path, "w") as f:
        f.write(python_signature)

    # Add difficulty
    metainfo_path = Path(config.BENCHMARK_PATH) / idx / "metainfo.json"
    save_json(file_path=metainfo_path, data={
        "project": config.PROJECT_NAME,
        "project_url": config.PROJECT_URI,
        "uri": func.uri,
        "func_name": func_name,
        "difficulty": difficulty,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    status, reason = generate_runner_without_llm(idx, func_name=func_name, language="Python")
    if not status:
        return False, reason

    status, reason = generate_runner_with_llm(idx, language="TS", func_name=func_name)
    if not status:
        return False, reason
    logger.info(f"Generated TS runner for function {idx}.")

    status, reason = generate_runner_with_llm(idx, language="JS", func_name=func_name)
    if not status:
        return False, reason
    logger.info(f"Generated TS runner for function {idx}.")
    
    status, reason = generate_runner_with_llm(idx, language="Go", func_name=func_name)
    if not status:
        return False, reason
    logger.info(f"Generated Go runner for function {idx}.")

    status, reason = generate_runner_with_llm(idx, language="Java", func_name=func_name)
    if not status:
        return False, reason
    logger.info(f"Generated Java runner for function {idx}.")
    
    return True, ""

def batch_run(specific_func_name=None) -> int:
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
    if os.path.exists(config.CANDIDATE_POOL_INDEX_PATH):
        candidate_index_dict = load_json(config.CANDIDATE_POOL_INDEX_PATH)
        candidate_list = [int(idx) for idx in candidate_index_dict.keys()]
        candidate_max_num = max(candidate_list)

    if os.path.exists(config.EXCLUDED_POOL_INDEX_PATH):
        excluded_index_dict = load_json(config.EXCLUDED_POOL_INDEX_PATH)
        excluded_list = [int(idx) for idx in excluded_index_dict.keys()]
        excluded_max_num = max(excluded_list)
        
    if os.path.exists(config.GENERATION_ERROR_POOL_INDEX_PATH):
        error_index_dict = load_json(config.GENERATION_ERROR_POOL_INDEX_PATH)
        error_list = [int(idx) for idx in error_index_dict.keys()]
        error_max_num = max(error_list)

    benchmark_index_path, benchmark_skip_path = get_index_dicts()
    if os.path.exists(benchmark_index_path):
        index_dict = load_json(benchmark_index_path)
        index_list = [int(idx) for idx in index_dict.keys()]
        max_num = max(max_num, max(index_list))
        func_to_idx = {func: idx for idx, func in index_dict.items()}
    if os.path.exists(benchmark_skip_path):
        skip_dict = load_json(benchmark_skip_path)

    func_list = get_func_list()
    
    if config.PROJECT_NAME == "intelmq":
        pass

    cnt = 0
    for func in func_list:
        # if cnt >= 10:
        #     logger.info("Generated 10 benchmarks, stop.")
        #     break
        
        if func['cyclomatic_complexity'] < config.CYCLOMATIC_COMPLEXITY:
            continue
        
        if func['cyclomatic_complexity'] > config.MAX_CYCLOMATIC_COMPLEXITY:
            logger.info(f"Function {func['uris']} cyclomatic complexity is {func['cyclomatic_complexity']}, skip it.")
            continue
        
        uri = config.PROJECT_NAME + '.' + func['uris']
                
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
        func_name = func['uris'].split('.')[-2]
        if func_name in func_name_list:
            logger.info(f"Function {func_name} already exists, may be semantic similar, skip it.")
            continue
            
        if specific_func_name is not None and func_name != specific_func_name:
            logger.info(f"Function {func_name} is not the specific function {specific_func_name}, skip it.")
            continue

        # Write to candidate pool
        candidate_max_num += 1
        directory = Path(config.CANDIDATE_POOL_PATH) / str(candidate_max_num)
        directory.mkdir(parents=True, exist_ok=True)
        candidate_path = directory / "candidate.py"
        with open(candidate_path, "w") as f:
            f.write(func['code'])
        
        candidate_index_dict[str(candidate_max_num)] = uri
        save_json(config.CANDIDATE_POOL_INDEX_PATH, deduplicate_dict_values(candidate_index_dict))
        logger.info(f"Generated candidate for function {candidate_max_num}, {uri}")


        func_str = func['code']
        func_name = func_str.split("(")[0].split()[-1]
        if config.MODE == FuncType.SELF_CONTAINED:
            func = FuncToGenerate(original_str=func_str, func_type=FuncType.SELF_CONTAINED, name=func_name, uri=func['uris'])
        elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
            func = FuncToGenerate(
                original_str=func_str, func_type=FuncType.LEVEL_SELF_CONTAINED, 
                name=func_name, level=func['level'], contains=[
                    FuncToGenerate(original_str=func['func_call']['code'], func_type=FuncType.SELF_CONTAINED, 
                                   name=func['func_call']['uris'].split('.')[-2], uri=func['func_call']['uris'])
                ]
            )
        elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
            func = FuncToGenerate(
                original_str=func_str, func_type=FuncType.WEAKLY_SELF_CONTAINED, uri=func['uris'],
                name=func_name, call_libs=func['allowed_libraries']
            )
            
        if uri in excluded_index_dict.values():
            logger.info(f"Function {uri} is already in excluded pool.")
            continue
            
        status, reason = filter_groundtruth(func, llm_client)
        if not status:
            # write to excluded pool
            excluded_max_num += 1
            directory = Path(config.EXCLUDED_POOL_PATH) / str(excluded_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            excluded_path = directory / "excluded.py"
            with open(excluded_path, "w") as f:
                f.write(func.original_str)
                f.write("\n")
                f.write(f"# Reason: {reason}")
            excluded_index_dict[str(excluded_max_num)] = uri
            save_json(config.EXCLUDED_POOL_INDEX_PATH, deduplicate_dict_values(excluded_index_dict))
            logger.info(f"Function {idx}: {func_name} is not suitable for benchmark.")
            return 0
        
        max_num += 1
        idx = str(max_num)
        try:
            status, reason = run_once(idx, func)
        except Exception as e:
            logger.error(f"Failed to generate benchmark for function {idx}: {e}")
            import traceback
            traceback.print_exc()
            status = False
            reason = "Run once error:" + str(e)
            
        if status:
            # max_num += 1
            index_dict[idx] = uri
            func_to_idx[uri] = idx 
            save_json(benchmark_index_path, deduplicate_dict_values(index_dict))
            logger.info(f"Generated benchmark for function {idx}, {uri}")
            cnt += 1
        else:
            benchmark_dir = Path(config.BENCHMARK_PATH) / idx
            # write to error pool
            error_max_num += 1
            directory = Path(config.GENERATION_ERROR_POOL_PATH) / str(error_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            # Move benchmark_dir to error pool
            for item in benchmark_dir.iterdir():
                shutil.move(str(item), str(directory))
            logger.info(f"Moved {benchmark_dir} to {directory}")
            error_index_dict[str(error_max_num)] = uri
            save_json(config.GENERATION_ERROR_POOL_INDEX_PATH, deduplicate_dict_values(error_index_dict))

            if config.PROJECT_NAME not in skip_dict:
                skip_dict[config.PROJECT_NAME] = []
            skip_dict[config.PROJECT_NAME].append(uri)
            logger.info(f"Failed to generate benchmark for function {max_num}, {uri}")
            save_json(benchmark_skip_path, deduplicate_dict_values(skip_dict))
            
            if benchmark_dir.exists():
                shutil.rmtree(benchmark_dir)

    return cnt

def run_pipeline(start_time=None, end_time=None):
    run_python_source_parse(repo_path=config.REPO_PATH)
    
    run_python_metainfo_builder(metainfo_json_path=config.ALL_METAINFO_PATH)
    
    select_function(start_time=start_time, end_time=end_time)
    
def run_git_clone(project_name: str, uri: str, workspace_path: str, use_proxy: bool = False) -> bool:
    project_path = Path(workspace_path) / project_name

    if project_path.exists():
        logger.info(f"Project {project_name} already exists at {project_path}. Remove it.")
        shutil.rmtree(project_path)
    
    logger.info(f"Cloning {project_name} from {uri} to {project_path}...")

    command = ["git", "clone", uri, str(project_path)]

    env = os.environ.copy()
    if use_proxy:
        proxy = config.PROXY_URL
        logger.debug(f"Using proxy server: {proxy}")
        env["http_proxy"] = proxy
        env["https_proxy"] = proxy

    try:
        result = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=240
        )
        logger.info(f"Command output:\n{result.stdout}")
        logger.info(f"Successfully cloned {project_name} from {uri} to {project_path}.")
        return True
    except subprocess.CalledProcessError as e:
        logger.info(f"Failed to clone {project_name} from {uri}. Error: {e.stderr}")
        return False

def run_git_pull(project_name: str, project_path: str, branch: str = None, use_proxy: bool = False) -> bool:
    project_path = Path(project_path).resolve()  
    
    if not project_path.exists():
        return False

    logger.info(f"开始更新项目 {project_name} @ {project_path}...")

    command = ["git", "-C", str(project_path), "pull"]

    env = os.environ.copy()
    if use_proxy:
        if not config.PROXY_URL.startswith(("http://", "https://")):
            logger.error("代理地址格式错误，必须包含协议声明（http:// 或 https://）")
            return False
            
        logger.debug(f"使用代理服务器：{config.PROXY_URL}")
        
        proxy = config.PROXY_URL
        env.update({
            "http_proxy": proxy,
            "HTTP_PROXY": proxy,
            "https_proxy": proxy,
            "HTTPS_PROXY": proxy,
        })

    try:
        result = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=30 
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

def run_one_project(project_name: str, uri: str, branch: str=None, start_time=None, end_time=None,
                    skip_pipeline: bool = False, use_proxy: bool = False, mode: FuncType = FuncType.SELF_CONTAINED,
                    only_pipeline: bool = False):
    config.PROJECT_NAME = project_name
    config.PROJECT_URI = uri
    config.MODE = mode

    project_path = str(Path(config.WORKSPACE_PATH) / config.PROJECT_NAME)
    
    # if os.path.exists(project_path):
    #     logger.info(f"Project {project_name} already exists at {project_path}. Continue.")
    #     return

    # 暂时先注释了
    file_list = []
    if os.path.exists(project_path):
        file_list = os.listdir(project_path)
    file_list = [f for f in file_list if f != "playground"]
    if os.path.exists(project_path) and len([f for f in file_list if not f.startswith(".")]) > 0:
        # run git pull
        run_git_pull(project_name=config.PROJECT_NAME, project_path=project_path, branch=branch, use_proxy=use_proxy)
    else:
        run_git_clone(project_name=project_name, uri=uri, workspace_path=config.WORKSPACE_PATH, use_proxy=use_proxy)
    
    switch_branch(project_name, project_path, branch)
    
    #####################
    # # 新开一个，会先跳过当前目录下已经有的
    # exsiting_projects = os.listdir(config.WORKSPACE_PATH)
    # if project_name in exsiting_projects:
    #     logger.info(f"Project {project_name} already exists at {project_path}.")
    #     return
    # run_git_clone(project_name=project_name, uri=uri, workspace_path=config.WORKSPACE_PATH, use_proxy=use_proxy)
    ######################
    
    if skip_pipeline is False:
        run_pipeline(start_time=start_time, end_time=end_time)

    # run_once("002")
    if only_pipeline:
        return
    
    if config.MODE == FuncType.SELF_CONTAINED:
        success_num = batch_run()
    elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
        success_num = batch_run_weakly()
    elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
        raise NotImplementedError("LEVEL_SELF_CONTAINED mode is not implemented yet.")
    logger.info(f"Generated {success_num} benchmarks.")
    
def run_all_projects(start_time=None, end_time=None, skip_pipeline: bool = False, 
                     use_proxy: bool = False, mode: FuncType = FuncType.SELF_CONTAINED,
                     only_pipeline: bool = False):
    projects = load_yaml_config(config.PROJECTS_PATH)
    python_projects = projects.get("Python", [])
    branch = projects.get("branch")
    # 按 URL 去重
    python_projects = deduplicate_projects_by_url(python_projects)
    python_projects = sorted(python_projects, key=lambda x: x['name'])

    for project in python_projects:
        try:
            logger.info(f"Running project {project['name']}...")
            config.PROJECT_NAME = project["name"]
            
            # if project["name"][0] < 'o':
            #     continue

            run_one_project(project["name"], project["url"], 
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
    # config.BENCHMARK_NAME = "weakly"
    # config.MODE = FuncType.WEAKLY_SELF_CONTAINED
    # run_all_projects(start_time='2024-08-01', end_time='2025-05-30', 
    #                  skip_pipeline=True, use_proxy=True, mode=FuncType.WEAKLY_SELF_CONTAINED,
    #                  only_pipeline=False)
    
    # run_all_projects(start_time='2024-08-01', end_time='2025-03-30', 
    #                  skip_pipeline=False, use_proxy=True, mode=FuncType.SELF_CONTAINED,
    #                  only_pipeline=True)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmark_name', type=str, choices=['Python', 'JS', 'TS', 'Java', 'Go', 'weakly'], default='Python',
                        help='Benchmark name, e.g. Python, JS, TS, Java, Go, or weakly')
    parser.add_argument('--mode', type=str, choices=['weakly', 'self'], default='weakly',
                        help='Benchmark mode: weakly (weakly self-contained) or self (self-contained)')
    parser.add_argument('--start_time', type=str, default='2024-08-01',
                        help='Start time for function selection, e.g. 2024-08-01')
    parser.add_argument('--end_time', type=str, default='2025-05-30',
                        help='End time for function selection, e.g. 2025-05-30')
    parser.add_argument('--skip_pipeline', action='store_true',
                        help='Skip the pipeline stage if set')
    parser.add_argument('--use_proxy', action='store_true',
                        help='Use proxy for git clone/pull if set')
    parser.add_argument('--only_pipeline', action='store_true',
                        help='Only run the pipeline stage if set')
    args = parser.parse_args()

    config.BENCHMARK_NAME = args.benchmark_name
    if args.mode == 'weakly':
        config.MODE = FuncType.WEAKLY_SELF_CONTAINED
        mode = FuncType.WEAKLY_SELF_CONTAINED
        config.BENCHMARK_NAME = "weakly"
    else:
        config.MODE = FuncType.SELF_CONTAINED
        mode = FuncType.SELF_CONTAINED
        config.BENCHMARK_NAME = "Python"

    run_all_projects(
        start_time=args.start_time,
        end_time=args.end_time,
        skip_pipeline=args.skip_pipeline,
        use_proxy=args.use_proxy,
        mode=mode,
        only_pipeline=args.only_pipeline
    )
