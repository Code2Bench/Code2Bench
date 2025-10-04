#!/usr/bin/env python3
import os
import shutil

# 源目录（Python）
src_root = "/l2/zhangzhe/code2bench/code2bench-2505/Python"
# 目标语言目录
langs = ["Go", "JS", "TS"]
dst_roots = [f"/l2/zhangzhe/code2bench/code2bench-2505/{lang}" for lang in langs]

for folder in os.listdir(src_root):
    if folder.isdigit():
        src_json = os.path.join(src_root, folder, "test_cases", "test_cases.json")
        if not os.path.exists(src_json):
            print(f"Source not found: {src_json}")
            continue
        for dst_root in dst_roots:
            dst_dir = os.path.join(dst_root, folder, "test_cases")
            dst_json = os.path.join(dst_dir, "test_cases.json")
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_json, dst_json)
            print(f"Copied {src_json} -> {dst_json}")