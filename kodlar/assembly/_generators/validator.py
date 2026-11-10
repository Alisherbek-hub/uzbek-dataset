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

    pattern = re.compile(r'^#\s+(\d+)-Topshiriq:\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    
    if len(matches) != expected_count:
        return False, f"Topshiriqlar soni noto'g'ri: kutilgan {expected_count}, topilgan {len(matches)}"
    
    expected_nums = list(range(expected_start, expected_start + expected_count))
    found_nums = [int(m.group(1)) for m in matches]
    
    if found_nums != expected_nums:
        return False, f"Topshiriq raqamlari mos kelmadi. Kutilgan: {expected_nums[:3]}...{expected_nums[-1]}, Topilgan: {found_nums[:3]}...{found_nums[-1]}"
    
    for i in range(len(matches)):
        start_idx = matches[i].start()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        task_block = content[start_idx:end_idx]
        task_num = found_nums[i]
        
        if "## Topshiriq sharti:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Topshiriq sharti:' bo'limi yo'q"
        if "## Yechim (Assembly kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Assembly kodi):' bo'limi yo'q"
        if "```assembly" not in task_block and "```asm" not in task_block:
            return False, f"{task_num}-topshiriqda '```assembly' yoki '```asm' blok mavjud emas"
        if "## Tushuntirish va Mantiq:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Tushuntirish va Mantiq:' bo'limi yo'q"
        if "## Ishlash natijasi:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Ishlash natijasi:' bo'limi yo'q"
        if "```text" not in task_block:
            return False, f"{task_num}-topshiriqda '```text' blok mavjud emas"
        
        for bad_word in [r'\bTODO\b', r'\bFIXME\b', r'\.\.\.qolgan qismi\.\.\.', r"o'zingiz yozing"]:
            if re.search(bad_word, task_block, re.IGNORECASE):
                return False, f"{task_num}-topshiriqda taqiqlangan so'z/placeholder topildi: {bad_word}"
                
    return True, f"OK! {len(matches)} ta topshiriq to'liq va to'g'ri ({expected_start}-{expected_start+expected_count-1})"

def run_validation():
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
    files = [
        ("assembly_01_asoslar_va_arxitektura.md", 1),
        ("assembly_02_x86_64_registrlari_va_harakatlar.md", 51),
        ("assembly_03_arm64_registrlari_va_harakatlar.md", 101),
        ("assembly_04_arifmetik_va_mantiqiy_amallar_x86.md", 151),
        ("assembly_05_arifmetik_va_mantiqiy_amallar_arm64.md", 201),
        ("assembly_06_boshqaruv_oqimi_va_tarmoqlanish_x86.md", 251),
        ("assembly_07_boshqaruv_oqimi_va_tarmoqlanish_arm64.md", 301),
        ("assembly_08_stek_xotirasi_va_funksiyalar_x86.md", 351),
        ("assembly_09_stek_va_funksiyalar_arm64.md", 401),
        ("assembly_10_calling_conventions_va_abi.md", 451),
        ("assembly_11_tizim_chaqiruvlari_syscalls.md", 501),
        ("assembly_12_xotira_xaritalash_va_segmentatsiya.md", 551),
        ("assembly_13_satrlar_va_massivlar_bilan_ishlash.md", 601),
        ("assembly_14_simd_va_vektorli_hisoblash_sse_avx_neon.md", 651),
        ("assembly_15_c_va_assembly_integratsiyasi.md", 701),
        ("assembly_16_makroslar_va_modulli_dasturlash.md", 751),
        ("assembly_17_reverse_engineering_asoslari.md", 801),
        ("assembly_18_kiberxavfsizlik_va_zaifliklar.md", 851),
        ("assembly_19_rop_va_xavfsizlik_aylanib_otish.md", 901),
        ("assembly_20_operatsion_tizim_va_bare_metal.md", 951),
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
            
    enc_path = os.path.join(base_dir, "assembly_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"assembly_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
        if size < 10000:
            print("OGOHLANTIRISH: Ensiklopediya hajmi juda kichik!")
            all_ok = False
    else:
        print("assembly_mukammal_qollanma.md: Mavjud emas")
        all_ok = False

    print(f"\nJami to'liq tekshirilgan topshiriqlar soni: {total_tasks} / 1000")
    if all_ok and total_tasks == 1000:
        print("BARCHA 21 TA FAYL (1000 TA TOPSHIRIQ + ENSIKLOPEDIYA) 100% MUKAMMAL VA TAYYOR!")
        return True
    else:
        print("BA'ZI FAYLLARDA XATOLIKLAR YOKI YETISHMOVCHILIKLAR MAVJUD!")
        return False

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
