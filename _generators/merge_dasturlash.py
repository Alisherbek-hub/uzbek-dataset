# -*- coding: utf-8 -*-
import json
import os

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash"
out_file = os.path.join(base_dir, "zamonaviy_dasturlash_1000.jsonl")

files = [
    os.path.join(base_dir, "docker_200.jsonl"),
    os.path.join(base_dir, "kubernetes_200.jsonl"),
    os.path.join(base_dir, "linux_shell_bash_200.jsonl"),
    os.path.join(base_dir, "devops_cicd_cloud_200.jsonl"),
    os.path.join(base_dir, "algoritmlar_tuzilmalar_200.jsonl")
]

total_count = 0
with open(out_file, "w", encoding="utf-8") as outfile:
    for fpath in files:
        file_count = 0
        with open(fpath, "r", encoding="utf-8") as infile:
            for line in infile:
                if line.strip():
                    outfile.write(line.strip() + "\n")
                    file_count += 1
                    total_count += 1
        print(f"Fayl qo'shildi: {os.path.basename(fpath)} ({file_count} ta qator)")

print(f"=== BARCHA DASTURLASH VAZIFALARI BIRLASHDI: {out_file} (Jami: {total_count} ta) ===")
