# -*- coding: utf-8 -*-
import os
import sys

# Ensure directory
base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)
from task_builder import format_task, save_file

print("Starting generation for Bash Modules 01 to 05...")
