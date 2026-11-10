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
        if "## Yechim (Lua kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Lua kodi):' bo'limi yo'q"
        if "```lua" not in task_block:
            return False, f"{task_num}-topshiriqda '```lua' blok mavjud emas"
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
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\lua"
    files = [
        ("lua_01_asoslar_tiplar_va_ozgaruvchilar.md", 1),
        ("lua_02_boshqaruv_oqimlari_shartlar_va_tsikllar.md", 51),
        ("lua_03_funksiyalar_va_birinchi_darajali_qiymatlar.md", 101),
        ("lua_04_closures_va_leksik_qamrov.md", 151),
        ("lua_05_jadvallar_tables_massiv_va_lugat_asoslari.md", 201),
        ("lua_06_metatablelar_va_metametodlar_chuqur_tahlil.md", 251),
        ("lua_07_obektga_yonaltirilgan_dasturlash_oop_prototiplar.md", 301),
        ("lua_08_satrlar_va_namuna_qidirish_pattern_matching.md", 351),
        ("lua_09_korutinalar_coroutines_va_kooperativ_multitasking.md", 401),
        ("lua_10_standart_kutubxonalar_va_io_tizimi.md", 451),
        ("lua_11_modullar_va_paketlar_require_tizimi.md", 501),
        ("lua_12_xatoliklarni_boshqarish_pcall_va_xpcall.md", 551),
        ("lua_13_luajit_va_ffi_foreign_function_interface.md", 601),
        ("lua_14_c_api_va_lua_c_integratsiyasi.md", 651),
        ("lua_15_roblox_luau_skriptlash_va_game_dev_asoslari.md", 701),
        ("lua_16_roblox_ilgari_amaliyotlar_remoteevents_va_datastore.md", 751),
        ("lua_17_love2d_va_oyin_dvijoklarida_lua.md", 801),
        ("lua_18_openresty_va_nginx_lua_arxitekturasi.md", 851),
        ("lua_19_redis_va_lua_atomar_skriptlar.md", 901),
        ("lua_20_unumdorlik_xotira_boshqaruvi_va_gc_tahlil.md", 951),
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
            
    enc_path = os.path.join(base_dir, "lua_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"lua_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
        if size < 10000:
            print("OGOHLANTIRISH: Ensiklopediya hajmi juda kichik!")
            all_ok = False
    else:
        print("lua_mukammal_qollanma.md: Mavjud emas")
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
