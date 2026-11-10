# -*- coding: utf-8 -*-
"""
Builder for Ruby Generator files 02, 03, 04, 05 (Tasks 51 to 250)
"""
import os
import sys

base_gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"

def write_and_run_gen(gen_filename, code):
    gen_path = os.path.join(base_gen_dir, gen_filename)
    with open(gen_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Generator yozildi: {gen_path}")
    # Run the generator
    cmd = f'python "{gen_path}"'
    ret = os.system(cmd)
    if ret != 0:
        raise RuntimeError(f"{gen_filename} bajarilishida xatolik yuz berdi! Kod: {ret}")
    print(f"{gen_filename} muvaffaqiyatli bajarildi!")

print("Batch 1 yuklanmoqda...")
