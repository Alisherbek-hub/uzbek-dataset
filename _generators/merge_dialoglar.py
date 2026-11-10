# -*- coding: utf-8 -*-
import json
import os

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\dialoglar"
out_file = os.path.join(base_dir, "jonli_ozbekcha_dialoglar_3000.jsonl")

files = [
    "dialoglar_01_salom_alik.jsonl",
    "dialoglar_02_oila_va_qadriyat.jsonl",
    "dialoglar_03_bozor_va_savdo.jsonl",
    "dialoglar_04_mehmondorchilik.jsonl",
    "dialoglar_05_mahalla_va_qoshni.jsonl",
    "dialoglar_06_milliy_taomlar.jsonl",
    "dialoglar_07_talim_va_ustoz.jsonl",
    "dialoglar_08_kasb_va_biznes.jsonl",
    "dialoglar_09_sayyohlik_shaharlar.jsonl",
    "dialoglar_10_sanat_va_madaniyat.jsonl",
    "dialoglar_11_salomatlik_va_sport.jsonl",
    "dialoglar_12_hayotiy_dalda.jsonl"
]

total_count = 0
with open(out_file, "w", encoding="utf-8") as outfile:
    for fname in files:
        fpath = os.path.join(base_dir, fname)
        file_count = 0
        with open(fpath, "r", encoding="utf-8") as infile:
            for line in infile:
                if line.strip():
                    outfile.write(line.strip() + "\n")
                    file_count += 1
                    total_count += 1
        print(f"Fayl qo'shildi: {fname} ({file_count} ta dialog)")

print(f"=== BARCHA DIALOGLAR BIRLASHDI: {out_file} (Jami: {total_count} ta) ===")
