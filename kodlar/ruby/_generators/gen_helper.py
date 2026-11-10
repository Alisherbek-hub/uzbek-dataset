# -*- coding: utf-8 -*-
import os
import sys
import json

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file
from validator import validate_task_file

def register_topic(gen_script_name, md_filename, start_idx, tasks_data):
    if len(tasks_data) != 50:
        raise ValueError(f"{gen_script_name} topshiriqlar soni 50 ta emas: {len(tasks_data)}")
    
    # 1. Format and save .md file
    formatted = [format_task(*t) for t in tasks_data]
    save_file(md_filename, formatted)
    
    # 2. Write standalone gen_XX.py
    json_data = json.dumps(tasks_data, ensure_ascii=False)
    gen_code = f'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = json.loads({repr(json_data)})

if __name__ == '__main__':
    tasks = [format_task(*t) for t in tasks_data]
    save_file({repr(md_filename)}, tasks)
'''
    gen_file_path = os.path.join(gen_dir, gen_script_name)
    with open(gen_file_path, "w", encoding="utf-8") as f:
        f.write(gen_code)
        
    # 3. Validate
    md_file_path = os.path.join(base_dir, md_filename)
    ok, msg = validate_task_file(md_file_path, start_idx)
    print(f"[{'PASS' if ok else 'FAIL'}] {gen_script_name} -> {md_filename}: {msg}")
    if not ok:
        raise RuntimeError(f"Validatsiya xatosi: {msg}")
