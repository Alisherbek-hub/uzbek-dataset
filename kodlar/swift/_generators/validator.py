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
        if "## Yechim (Swift kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Swift kodi):' bo'limi yo'q"
        if "```swift" not in task_block:
            return False, f"{task_num}-topshiriqda '```swift' blok mavjud emas"
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
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\swift"
    files = [
        ("swift_01_asoslar_tiplar_va_ozgaruvchilar.md", 1),
        ("swift_02_optionals_va_unwrapping.md", 51),
        ("swift_03_operatorlar_va_boshqaruv_oqimlari.md", 101),
        ("swift_04_funksiyalar_va_inout_parametrlari.md", 151),
        ("swift_05_closures_va_funksional_usullar.md", 201),
        ("swift_06_strukturalar_va_sinflar_struct_vs_class.md", 251),
        ("swift_07_properties_va_property_wrappers.md", 301),
        ("swift_08_initialization_va_deinit.md", 351),
        ("swift_09_merosxorlik_va_polimorfizm.md", 401),
        ("swift_10_protokollar_va_delegatsiya.md", 451),
        ("swift_11_generiklar_generics_va_constraints.md", 501),
        ("swift_12_xatoliklarni_boshqarish_error_handling.md", 551),
        ("swift_13_kolleksiyalar_va_algoritmlar.md", 601),
        ("swift_14_extensions_va_protokol_kengaytmalari.md", 651),
        ("swift_15_async_await_va_structured_concurrency.md", 701),
        ("swift_16_actors_va_data_races_oldini_olish.md", 751),
        ("swift_17_xotira_boshqaruvi_arc_va_retain_cycles.md", 801),
        ("swift_18_swiftui_asoslari_va_reaktiv_state.md", 851),
        ("swift_19_swiftui_arxitekturasi_va_navigation.md", 901),
        ("swift_20_coreml_va_on_device_ai_agent.md", 951),
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
    enc_path = os.path.join(base_dir, "swift_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"swift_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
        if size < 10000:
            print("OGOHLANTIRISH: Ensiklopediya hajmi juda kichik!")
            all_ok = False
    else:
        print("swift_mukammal_qollanma.md: Mavjud emas")
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
