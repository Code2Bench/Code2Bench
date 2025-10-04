from datetime import datetime
import os
from pathlib import Path
import shutil
from typing import Dict, List, Tuple

from code2bench import config
from code2bench.data_model import FuncToGenerate, FuncType
from code2bench.driver_generator.testcases_generator import run_once_testcase_generation
from code2bench.func_selector.func_selector import extract_all_type_hints
from code2bench.func_selector.groundtruth_filter import filter_groundtruth
from code2bench.instruction_generator.instruction_generator import assess_difficulty, generate_one_instruction
from code2bench.pipeline.reasoning.reasoning import generate_reasoning_testcases, generate_weakly_example_usage
from code2bench.runner_generator.runner_generator import generate_runner_for_weakly
from code2bench.utils.helper import deduplicate_dict_values, get_existing_func_name_list, get_func_list, get_index_dicts
from code2bench.utils.json_utils import load_json, save_json
from code2bench import logger
from code2bench import llm_client
from code2bench.utils.python import extract_typing_imports


def run_once(idx: str, func: FuncToGenerate) -> Tuple[bool, str]:    
    func_name = func.name
    func_str = func.original_str
    call_libs = func.call_libs
    
    # 确保目标目录存在
    benchmark_dir = Path(config.BENCHMARK_PATH) / str(idx)
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    
    # 把groundtruth输出到对应的文件中
    type_hints = extract_all_type_hints(func_str=func_str)
    type_import_statement = extract_typing_imports(type_hints=type_hints)
    
    import_statements = []
    for lib in call_libs:
        import_statement = config.ALLOWED_MODULES.get(lib)
        if import_statement:
            import_statements.append(import_statement)
        else:
            if "import" in lib:
                import_statement = lib
            else:
                import_statement = f"import {lib}"
            import_statements.append(import_statement)
    import_statement = "\n".join(import_statements)
    
    func_str = type_import_statement + "\n" + import_statement + "\n\n" + func_str
    groundtruth_path = Path(config.BENCHMARK_PATH) / str(idx) / "groundtruth.py"
    with open(groundtruth_path, "w") as f:
        f.write(func_str)
    logger.info(f"Generated groundtruth for function {idx}.")
    
    # # 1. 先进行难度判断
    difficulty = assess_difficulty(func, llm_client)
    
    # # 2. 生成Testcase
    status, reason = run_once_testcase_generation(idx=idx, from_path="groundtruth.py", to_path="testcase_generator.py", )
    if status is False:
        return False, reason
    logger.info(f"Generated testcases for function {idx}.")
    
    # 2. 生成Example Usage
    example_usages, reason = generate_weakly_example_usage(idx, llm_client)
    if example_usages is False:
        return False, "Failed to generate example usages" + "###" + reason
    logger.info(f"Generated example usages for function {idx}.")
    
    # 4. 生成Instruction
    max_retries = 3
    retry_count = 0
    last_error = None
    last_res = None
    while retry_count < max_retries:
        # 把instruction输出到对应的文件中
        generated_instruction, python_signature = generate_one_instruction(func, llm_client, last_res=last_res, last_error=last_error)
        if generated_instruction.error:
            logger.info(f"Failed to generate instruction for function {idx}: {func_name} Due to error: {generated_instruction.error}")
            last_error = generated_instruction.error
        last_res = generated_instruction.instruction
        if generated_instruction.instruction:
            break
        retry_count += 1
    logger.info(f"Retry {retry_count} times to generate instruction for function {idx}: {func_name}")
    
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
    
    # 在tested.py中添加函数, pass就可以了，防止import失败
    tested_path = Path(config.BENCHMARK_PATH) / idx / "tested.py"
    with open(tested_path, "w") as f:
        # f.write(f"def {func_name}(*args, **kwargs):\n    pass\n")
        f.write(python_signature)

    # Add difficulty
    metainfo_path = Path(config.BENCHMARK_PATH) / idx / "metainfo.json"
    save_json(file_path=metainfo_path, data={
        "project": config.PROJECT_NAME,
        "project_url": config.PROJECT_URI,
        "uri": func.uri,
        "func_name": func_name,
        "difficulty": difficulty,
        "call_libs": func.call_libs,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 5. 生成Python的Runner
    status, reason = generate_runner_for_weakly(idx, func_name=func_name)
    if not status:
        return False, reason

    logger.info(f"Pipeline success for {idx}.")
    return True, ""

def batch_run_weakly(specific_func_name=None) -> int:
    assert config.BENCHMARK_NAME == config.WEAKLY_BENCHMARK_NAME, f"Please set the benchmark name to {config.WEAKLY_BENCHMARK_NAME}."

    config.MODE = FuncType.WEAKLY_SELF_CONTAINED
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
    if os.path.exists(config.WEAKLY_CANDIDATE_POOL_INDEX_PATH):
        candidate_index_dict = load_json(config.WEAKLY_CANDIDATE_POOL_INDEX_PATH)
        candidate_list = [int(idx) for idx in candidate_index_dict.keys()]
        candidate_max_num = max(candidate_list)

    if os.path.exists(config.WEAKLY_EXCLUDED_POOL_INDEX_PATH):
        excluded_index_dict = load_json(config.WEAKLY_EXCLUDED_POOL_INDEX_PATH)
        excluded_list = [int(idx) for idx in excluded_index_dict.keys()]
        excluded_max_num = max(excluded_list)
        
    if os.path.exists(config.WEAKLY_GENERATION_ERROR_POOL_INDEX_PATH):
        error_index_dict = load_json(config.WEAKLY_GENERATION_ERROR_POOL_INDEX_PATH)
        error_list = [int(idx) for idx in error_index_dict.keys()]
        error_max_num = max(error_list)

    assert config.MODE == FuncType.WEAKLY_SELF_CONTAINED, f"You must run this in weakly self-contained mode."
    benchmark_index_path, benchmark_skip_path = get_index_dicts()
    if os.path.exists(benchmark_index_path):
        index_dict = load_json(benchmark_index_path)
        index_list = [int(idx) for idx in index_dict.keys()]
        max_num = max(max_num, max(index_list))
        func_to_idx = {func: idx for idx, func in index_dict.items()}
    if os.path.exists(benchmark_skip_path):
        skip_dict = load_json(benchmark_skip_path)

    func_list = get_func_list()

    cnt = 0
    for func in func_list:
        # if cnt >= 10:
        #     logger.info("Generated 10 benchmarks, stop.")
        #     break
        
        # if func['cyclomatic_complexity'] < config.WEAKLY_CYCLOMATIC_COMPLEXITY:
        #     continue
        
        
        if func['cyclomatic_complexity'] > config.WEAKLY_MAX_CYCLOMATIC_COMPLEXITY:
            logger.info(f"Function {func['uris']} cyclomatic complexity is {func['cyclomatic_complexity']}, skip it.")
            continue
        
        uri = config.PROJECT_NAME + '.' + func['uris']
        
        if func['uris'] == "intelmq.intelmq.lib.upgrades.global.v340_deprecations.3":
            pass
                
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
        directory = Path(config.WEAKLY_CANDIDATE_POOL_PATH) / str(candidate_max_num)
        directory.mkdir(parents=True, exist_ok=True)
        candidate_path = directory / "candidate.py"
        with open(candidate_path, "w") as f:
            f.write(func['code'])
        
        candidate_index_dict[str(candidate_max_num)] = uri
        save_json(config.WEAKLY_CANDIDATE_POOL_INDEX_PATH, deduplicate_dict_values(candidate_index_dict))
        logger.info(f"Generated candidate for function {candidate_max_num}, {uri}")


        func_str = func['code']
        func_name = func_str.split("(")[0].split()[-1]

        func = FuncToGenerate(
            original_str=func_str, func_type=FuncType.WEAKLY_SELF_CONTAINED, 
            name=func_name, call_libs=func['allowed_libraries']
        )
            
        if uri in excluded_index_dict.values():
            logger.info(f"Function {uri} is already in excluded pool.")
            continue
            
        status, reason = filter_groundtruth(func, llm_client)
        if not status:
            # write to excluded pool
            excluded_max_num += 1
            directory = Path(config.WEAKLY_EXCLUDED_POOL_PATH) / str(excluded_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            excluded_path = directory / "excluded.py"
            with open(excluded_path, "w") as f:
                f.write(func.original_str)
                f.write("\n")
                f.write(f"# Reason: {reason}")
            excluded_index_dict[str(excluded_max_num)] = uri
            save_json(config.WEAKLY_EXCLUDED_POOL_INDEX_PATH, deduplicate_dict_values(excluded_index_dict))
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
            # 如果生成失败了，存到错误池中
            # write to error pool
            error_max_num += 1
            directory = Path(config.WEAKLY_GENERATION_ERROR_POOL_PATH) / str(error_max_num)
            directory.mkdir(parents=True, exist_ok=True)
            # Move benchmark_dir to error pool
            # 移动 benchmark_dir 的内容到 directory
            for item in benchmark_dir.iterdir():
                dest_path = directory / item.name
                if dest_path.exists():
                    if dest_path.is_dir():
                        shutil.rmtree(dest_path)
                    else:
                        dest_path.unlink()
                shutil.move(str(item), str(directory))
            logger.info(f"Moved {benchmark_dir} to {directory}")
            error_index_dict[str(error_max_num)] = uri
            save_json(config.WEAKLY_GENERATION_ERROR_POOL_INDEX_PATH, deduplicate_dict_values(error_index_dict))

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