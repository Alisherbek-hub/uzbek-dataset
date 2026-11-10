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
        if "## Yechim (Ruby kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Ruby kodi):' bo'limi yo'q"
        if "```ruby" not in task_block:
            return False, f"{task_num}-topshiriqda '```ruby' blok mavjud emas"
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
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby"
    files = [
        ("ruby_01_asoslar_tiplar_va_operatorlar.md", 1),
        ("ruby_02_satrlar_va_regulyar_ifodalar.md", 51),
        ("ruby_03_shart_va_takrorlanish_operatorlari.md", 101),
        ("ruby_04_massivlar_va_hashlar.md", 151),
        ("ruby_05_bloklar_procs_va_lambdalar.md", 201),
        ("ruby_06_enumerable_va_iteratorlar.md", 251),
        ("ruby_07_metodlar_va_argumentlar.md", 301),
        ("ruby_08_oop_asoslari_sinflar_va_obyektlar.md", 351),
        ("ruby_09_merosxorlik_va_modullar_mixins.md", 401),
        ("ruby_10_metaprogramming_va_dinamik_kod.md", 451),
        ("ruby_11_xatoliklarni_boshqarish_exceptions.md", 501),
        ("ruby_12_fayllar_io_va_serializatsiya.md", 551),
        ("ruby_13_gemlar_va_kutubxonalar_bundler.md", 601),
        ("ruby_14_rails_asoslari_marshrutlash_va_kontrollerlar.md", 651),
        ("ruby_15_rails_active_record_va_migratsiyalar.md", 701),
        ("ruby_16_rails_view_viewcomponent_va_hotwire.md", 751),
        ("ruby_17_rails_api_va_autentifikatsiya.md", 801),
        ("ruby_18_fon_vazifalari_va_realtaym_sidekiq_actioncable.md", 851),
        ("ruby_19_rspec_va_avtomatlashtirilgan_testlash.md", 901),
        ("ruby_20_zamonaviy_ruby3_va_ai_agent_startap.md", 951),
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
    enc_path = os.path.join(base_dir, "ruby_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"ruby_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
    else:
        print("ruby_mukammal_qollanma.md: Mavjud emas")
        all_ok = False
        
    print(f"\nJami to'g'ri topshiriqlar soni: {total_tasks}/1000")
    if all_ok and total_tasks == 1000:
        print("BARCHA TEKSHIRUVLAR MUVAFFAQIYATLI O'TDI! RUBY DATASET TAYYOR.")
    else:
        print("Kamchiliklar aniqlandi.")
        
    return all_ok

if __name__ == "__main__":
    run_validation()
