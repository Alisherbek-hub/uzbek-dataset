# -*- coding: utf-8 -*-
import os
import re
import sys

def validate_task_file(file_path, expected_start, expected_count=50):
    if not os.path.exists(file_path):
        return False, f"Fayl topilmadi: {file_path}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip():
        return False, "Fayl bo'sh"

    # Find all task headers: # N-Topshiriq: Sarlavha
    pattern = re.compile(r'^#\s+(\d+)-Topshiriq:\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    
    if len(matches) != expected_count:
        return False, f"Topshiriqlar soni noto'g'ri: kutilgan {expected_count}, topilgan {len(matches)}"
    
    expected_nums = list(range(expected_start, expected_start + expected_count))
    found_nums = [int(m.group(1)) for m in matches]
    
    if found_nums != expected_nums:
        return False, f"Topshiriq raqamlari mos kelmadi. Kutilgan: {expected_nums[:3]}...{expected_nums[-1]}, Topilgan: {found_nums[:3]}...{found_nums[-1]}"
    
    # Check sections for each task
    for i in range(len(matches)):
        start_idx = matches[i].start()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        task_block = content[start_idx:end_idx]
        task_num = found_nums[i]
        
        if "## Topshiriq sharti:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Topshiriq sharti:' bo'limi yo'q"
        if "## Yechim (R kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (R kodi):' bo'limi yo'q"
        if "```r" not in task_block:
            return False, f"{task_num}-topshiriqda '```r' blok mavjud emas"
        if "## Tushuntirish va Mantiq:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Tushuntirish va Mantiq:' bo'limi yo'q"
        if "## Ishlash natijasi:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Ishlash natijasi:' bo'limi yo'q"
        if "```text" not in task_block:
            return False, f"{task_num}-topshiriqda '```text' blok mavjud emas"
        
        # Check for forbidden placeholder patterns
        for bad_word in [r'\bTODO\b', r'\bFIXME\b', r'\.\.\.qolgan qismi\.\.\.', r"o'zingiz yozing"]:
            if re.search(bad_word, task_block, re.IGNORECASE):
                return False, f"{task_num}-topshiriqda taqiqlangan so'z/placeholder topildi: {bad_word}"
                
    return True, f"OK! {len(matches)} ta topshiriq to'liq va to'g'ri ({expected_start}-{expected_start+expected_count-1})"

def run_validation():
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\r"
    files = [
        ("r_01_asoslar_vektorlar_va_tiplar.md", 1),
        ("r_02_matritsalar_va_massivlar.md", 51),
        ("r_03_faktorlar_va_ro_yxatlar_lists.md", 101),
        ("r_04_data_frame_asoslari_va_manipulyatsiya.md", 151),
        ("r_05_boshqaruv_oqimlari_va_maxsus_funksiyalar.md", 201),
        ("r_06_apply_oilasi_va_funksional_dasturlash.md", 251),
        ("r_07_dplyr_bilan_tezkor_manipulyatsiya.md", 301),
        ("r_08_tidyr_va_ma_lumotlarni_tozalash.md", 351),
        ("r_09_data_table_yuqori_unumdor_tahlil.md", 401),
        ("r_10_kiruvchi_va_chiquvchi_ma_lumotlar_io.md", 451),
        ("r_11_ggplot2_asoslari_va_geometriyalar.md", 501),
        ("r_12_ggplot2_ilg_or_vizualizatsiya_va_temalar.md", 551),
        ("r_13_ehtimollar_va_tasodifiy_taqsimotlar.md", 601),
        ("r_14_tavsifiy_va_xulosaviy_statistika.md", 651),
        ("r_15_regressiya_tahlili_chiziqli_va_logistik.md", 701),
        ("r_16_vaqt_qatorlari_va_ekonometrika.md", 751),
        ("r_17_mashinali_o_rganish_va_klasterlash.md", 801),
        ("r_18_bioinformatika_va_genomik_tahlillar.md", 851),
        ("r_19_shiny_veb_ilovalar_va_reaktivlik.md", 901),
        ("r_20_yuqori_unumdorlik_rcpp_parallel_va_ai.md", 951),
    ]
    
    all_ok = True
    total_tasks = 0
    for fname, start_idx in files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            ok, msg = validate_task_file(fpath, start_idx)
            print(f"{fname}: {msg}")
            if ok:
                total_tasks += 50
            else:
                all_ok = False
        else:
            print(f"{fname}: Mavjud emas")
            all_ok = False
            
    # Check encyclopedia
    enc_path = os.path.join(base_dir, "r_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"r_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
    else:
        print("r_mukammal_qollanma.md: Mavjud emas")
        all_ok = False
        
    print(f"\nJami to'g'ri topshiriqlar soni: {total_tasks}/1000")
    if all_ok and total_tasks == 1000:
        print("BARCHA TEKSHIRUVLAR MUVAFFAQIYATLI O'TDI! R DATASET TAYYOR.")
    else:
        print("Kamchiliklar aniqlandi.")
        
    return all_ok

if __name__ == "__main__":
    run_validation()
