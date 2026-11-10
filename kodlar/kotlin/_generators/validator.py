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
        if "## Yechim (Kotlin kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Kotlin kodi):' bo'limi yo'q"
        if "```kotlin" not in task_block:
            return False, f"{task_num}-topshiriqda '```kotlin' blok mavjud emas"
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

if __name__ == "__main__":
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin"
    files = [
        ("kotlin_01_asoslar_tiplar_va_ozgaruvchilar.md", 1),
        ("kotlin_02_null_safety_va_operatorlar.md", 51),
        ("kotlin_03_boshqaruv_oqimlari_va_shartlar.md", 101),
        ("kotlin_04_funksiyalar_va_standart_argumentlar.md", 151),
        ("kotlin_05_sinflar_konstruktorlar_va_xususiyatlar.md", 201),
        ("kotlin_06_merosxorlik_va_interfeyslar.md", 251),
        ("kotlin_07_maxsus_sinflar_data_va_sealed.md", 301),
        ("kotlin_08_obyektlar_va_delegatsiya.md", 351),
        ("kotlin_09_funksional_dasturlash_va_lambdalar.md", 401),
        ("kotlin_10_scope_funksiyalari.md", 451),
        ("kotlin_11_kengaytmalar_extension_functions.md", 501),
        ("kotlin_12_generiklar_generics.md", 551),
        ("kotlin_13_kolleksiyalar_va_operatsiyalar.md", 601),
        ("kotlin_14_xatoliklarni_boshqarish_exceptions.md", 651),
        ("kotlin_15_koroutinalar_asoslari_coroutines.md", 701),
        ("kotlin_16_koroutinalar_chuqur_va_bekor_qilish.md", 751),
        ("kotlin_17_oqimlar_va_reaktiv_flow.md", 801),
        ("kotlin_18_fayllar_va_serialization.md", 851),
        ("kotlin_19_android_jetpack_compose_asoslari.md", 901),
        ("kotlin_20_zamonaviy_android_va_ai_agent_mobile.md", 951),
    ]
    
    all_ok = True
    for fname, start_idx in files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            ok, msg = validate_task_file(fpath, start_idx)
            print(f"{fname}: {msg}")
            if not ok:
                all_ok = False
        else:
            print(f"{fname}: Mavjud emas")
            all_ok = False
            
    # Check encyclopedia
    enc_path = os.path.join(base_dir, "kotlin_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"kotlin_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
    else:
        print("kotlin_mukammal_qollanma.md: Mavjud emas")
        all_ok = False

    if all_ok:
        print("\nBARCHA 20 TA FAYL VA QO'LLANMA MUVAFFAQIYATLI TEKSHIRILDI! 100% SIFAT!")
    else:
        print("\nBA'ZI FAYLLARDA XATOLIKLAR MAVJUD!")
