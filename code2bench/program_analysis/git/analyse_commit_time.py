import subprocess
import json
import os
from typing import List
from code2bench.config import config
from code2bench.utils.python import get_python_method_uris


def get_changed_files(start_date, end_date, repo_path):
    """
    获取在某段时间内改动的所有 Python 文件（.py）。
    """
    if not os.path.isdir(repo_path):
        raise ValueError(f"Invalid repository path: {repo_path}")

    # Git 命令：获取在指定时间范围内修改的文件
    command = [
        'git', 'log', '--since', start_date, '--until', end_date,
        '--name-only', '--pretty=format:', '--', '.'
    ]
    try:
        result = subprocess.check_output(command, cwd=repo_path, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error executing git command: {e}")
    
    changed_files = set(result.splitlines())
    python_files = [file for file in changed_files if file.endswith('.py')]
    return python_files


def get_changed_details(python_files, repo_path, start_date, end_date):
    """
    获取每个改动的文件的详细差异。
    """
    if not python_files:
        raise ValueError("No Python files to check diffs for.")
    
    file_diffs = {}
    for file in python_files:
        diff_command = [
            'git', 'log', '--since', start_date, '--until', end_date,
            '-p', '--', file
        ]
        
        try:
            diff_result = subprocess.check_output(diff_command, cwd=repo_path, text=True)
            file_diffs[file] = diff_result
        except subprocess.CalledProcessError as e:
            file_diffs[file] = None  # 如果获取 diff 失败，记录 None
            print(f"Warning: Failed to get diff for file {file}: {e}")
    
    return file_diffs


def extract_line_ranges(diff):
    """
    从 diff 内容中提取修改的行号范围。
    """
    line_ranges = []
    lines = diff.splitlines()

    for line in lines:
        if line.startswith('@@'):
            parts = line.split(' ')
            try:
                new_range = parts[2][1:].split(',')
                start_line = int(new_range[0])
                end_line = start_line + int(new_range[1]) - 1
                line_ranges.append((start_line, end_line))
            except (IndexError, ValueError) as e:
                print(f"Error parsing line range in diff: {e}")
                continue

    return line_ranges


def get_changed_funcs_uris(file_diffs, json_file_path):
    """
    根据文件差异，获取修改的函数（根据行号判断），并生成对应的 URI。
    """
    if not os.path.isfile(json_file_path):
        raise ValueError(f"Invalid JSON file path: {json_file_path}")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Error loading JSON file: {e}")

    changed_uris = []

    for file, diff in file_diffs.items():
        if not diff:
            continue
        
        line_ranges = extract_line_ranges(diff)
        if not line_ranges:
            continue

        # 找到该文件的 JSON 数据条目
        file_data = next((item for item in data if item['relative_path'] == file), None)
        if not file_data:
            # print(f"Warning: No data found for file {file} in JSON.")
            continue

        # 处理全局函数
        for method in file_data.get('methods', []):
            start_line = method.get('start_line')
            end_line = method.get('end_line')

            for start, end in line_ranges:
                if start_line >= start and end_line <= end:
                    num_arguments = method.get("args_nums", 0)
                    method_uri = get_python_method_uris(file.strip('.py').replace('/', '.'), method=method)
                    changed_uris.append(method_uri)

        # 处理类中的方法
        for class_info in file_data.get('classes', []):
            class_name = class_info.get('name')
            for method in class_info.get('methods', []):
                start_line = method.get('start_line')
                end_line = method.get('end_line')

                for start, end in line_ranges:
                    if start_line >= start and end_line <= end:
                        # num_arguments = method.get("args_nums", 0)
                        method_uri = get_python_method_uris(file.strip('.py').replace('/', '.'), method=method, class_name=class_name)
                        changed_uris.append(method_uri)

    return changed_uris

def analyze_commit_changes(repo_path, start_date, end_date, json_path) -> List[str]:
    """
    分析指定日期范围内的提交更改，获取更改的 Python 文件和函数 URI。

    :param repo_path: 仓库路径
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param json_path: JSON 文件路径
    """
    try:
        python_files = get_changed_files(start_date, end_date, repo_path)
        if not python_files:
            print("No Python files have been changed in the specified date range.")
            return []

        file_diffs = get_changed_details(python_files, repo_path, start_date, end_date)
        changed_uris = get_changed_funcs_uris(file_diffs, json_path)

        if changed_uris:
            # print("Changed function URIs:")
            for uri in changed_uris:
                # print(f"- {uri}")
                pass
        else:
            print("No functions were changed in the specified range.")

        for uri in changed_uris:
            # print(f"修改的函数 URI: {uri}")
            pass
        
        return changed_uris
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    try:
        repo_path = REPO_PATH
        start_date = '2024-9-30'
        end_date = '2024-12-02'
        json_path = ALL_METAINFO_PATH

        python_files = get_changed_files(start_date, end_date, repo_path)
        if not python_files:
            print("No Python files have been changed in the specified date range.")
        
        file_diffs = get_changed_details(python_files, repo_path, start_date, end_date)
        changed_uris = get_changed_funcs_uris(file_diffs, json_path)

        if changed_uris:
            # print("Changed function URIs:")
            for uri in changed_uris:
                # print(f"- {uri}")
                pass
        else:
            print("No functions were changed in the specified range.")

        for uri in changed_uris:
            # print(f"修改的函数 URI: {uri}")
            pass
            
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
