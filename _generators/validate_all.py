# -*- coding: utf-8 -*-
"""
Khorazmiy AI Dataset Validator
"""
import json
import os

target_files = [
    # Kitoblar
    r"C:\Users\User\Desktop\uzbek_dataset\kitoblar\mumtoz_va_adabiy_asarlar_sft.jsonl",
    # Dasturlash
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\docker_200.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\kubernetes_200.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\linux_shell_bash_200.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\devops_cicd_cloud_200.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\algoritmlar_tuzilmalar_200.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\zamonaviy_dasturlash_1000.jsonl",
    # Dialoglar
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_01_salom_alik.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_02_oila_va_qadriyat.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_03_bozor_va_savdo.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_04_mehmondorchilik.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_05_mahalla_va_qoshni.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_06_milliy_taomlar.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_07_talim_va_ustoz.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_08_kasb_va_biznes.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_09_sayyohlik_shaharlar.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_10_sanat_va_madaniyat.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_11_salomatlik_va_sport.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\dialoglar_12_hayotiy_dalda.jsonl",
    r"C:\Users\User\Desktop\uzbek_dataset\dialoglar\jonli_ozbekcha_dialoglar_3000.jsonl"
]

print("=" * 80)
print(f"{'FAYL NOMI':<45} | {'QATORLAR':<10} | {'HAJMI (KB)':<12} | {'HOLAT'}")
print("=" * 80)

total_lines_all = 0
all_valid = True

for fpath in target_files:
    fname = os.path.basename(fpath)
    if not os.path.exists(fpath):
        print(f"{fname:<45} | YO'Q       | 0            | XATOLIK")
        all_valid = False
        continue

    line_count = 0
    errors = 0
    size_kb = os.path.getsize(fpath) / 1024.0

    with open(fpath, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not data.get("instruction") or not data.get("output"):
                    errors += 1
                line_count += 1
            except Exception as e:
                errors += 1

    status = "OK (TO'LIQ TOZA)" if errors == 0 else f"XATO ({errors} ta)"
    if errors > 0:
        all_valid = False

    print(f"{fname:<45} | {line_count:<10} | {size_kb:<12.1f} | {status}")
    total_lines_all += line_count

print("=" * 80)
print(f"JAMI TEKSHIRILGAN QATORLAR (Barcha fayllar yig'indisi): {total_lines_all}")
res_text = "BARCHA MA'LUMOTLAR 100% YAROQLI VA TOZA" if all_valid else "KAMCHILIK BOR"
print(f"YAKUNIY SIFAT NAZORATI: {res_text}")
print("=" * 80)
