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
        if "## Yechim (Bash kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Bash kodi):' bo'limi yo'q"
        if "```bash" not in task_block:
            return False, f"{task_num}-topshiriqda '```bash' blok mavjud emas"
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
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
    files = [
        ("bash_01_asoslar_va_buyruqlar_satri.md", 1),
        ("bash_02_ozgaruvchilar_va_parametrlar.md", 51),
        ("bash_03_arifmetika_va_operatorlar.md", 101),
        ("bash_04_shartlar_va_tarmoqlanish.md", 151),
        ("bash_05_sikllar_va_iteratsiyalar.md", 201),
        ("bash_06_funksiyalar_va_modullik.md", 251),
        ("bash_07_massivlar_va_assotsiativ_lugatlar.md", 301),
        ("bash_08_kiritish_chiqarish_va_qayta_yonaltirish.md", 351),
        ("bash_09_quvurlar_va_oqimli_qayta_ishlash.md", 401),
        ("bash_10_matn_qayta_ishlash_grep_va_regex.md", 451),
        ("bash_11_oqimli_tahrirlash_sed.md", 501),
        ("bash_12_matn_dasturlash_tili_awk.md", 551),
        ("bash_13_fayllar_va_kataloglar_boshqaruvi.md", 601),
        ("bash_14_jarayonlar_va_signallar_boshqaruvi.md", 651),
        ("bash_15_tizim_monitoringi_va_resurslar.md", 701),
        ("bash_16_rejalashtirish_cron_va_systemd_timers.md", 751),
        ("bash_17_tarmoq_va_veb_avtomatlashtirish.md", 801),
        ("bash_18_devops_docker_va_konteynerlar.md", 851),
        ("bash_19_cicd_quvurlari_va_avtomatlashtirish.md", 901),
        ("bash_20_xavfsizlik_audit_va_robust_skriptlar.md", 951),
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
            
    enc_path = os.path.join(base_dir, "bash_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"bash_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
        if size < 10000:
            print("OGOHLANTIRISH: Ensiklopediya hajmi juda kichik!")
            all_ok = False
    else:
        print("bash_mukammal_qollanma.md: Mavjud emas")
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
