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
        if "## Yechim (SQL kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (SQL kodi):' bo'limi yo'q"
        if "```sql" not in task_block:
            return False, f"{task_num}-topshiriqda '```sql' blok mavjud emas"
        if "## Tushuntirish va Mantiq:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Tushuntirish va Mantiq:' bo'limi yo'q"
        if "## Ishlash natijasi:" not in task_block:
            return False, f"{task_num}-topshiriqda '## Ishlash natijasi:' bo'limi yo'q"
        if "```text" not in task_block:
            return False, f"{task_num}-topshiriqda '```text' blok mavjud emas"
        
        # Check for forbidden placeholder patterns
        for bad_word in ["TODO", "FIXME", "...qolgan qismi...", "o'zingiz yozing"]:
            if bad_word.lower() in task_block.lower():
                return False, f"{task_num}-topshiriqda taqiqlangan so'z/placeholder topildi: {bad_word}"
                
    return True, f"OK! {len(matches)} ta topshiriq to'liq va to'g'ri ({expected_start}-{expected_start+expected_count-1})"

if __name__ == "__main__":
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\sql"
    files = [
        ("sql_01_ddl_jadvallar_va_malumot_turlari.md", 1),
        ("sql_02_cheklovlar_constraints_va_yaxlitlik.md", 51),
        ("sql_03_dml_malumotlarni_boshqarish.md", 101),
        ("sql_04_dql_oddiy_tanlash_select_va_filtrlash.md", 151),
        ("sql_05_agregat_funksiyalar_va_guruhlash.md", 201),
        ("sql_06_jadvallarni_birlashtirish_joins.md", 251),
        ("sql_07_ichma_ich_sorovlar_subqueries.md", 301),
        ("sql_08_cte_va_rekursiv_sorovlar.md", 351),
        ("sql_09_oynador_funksiyalar_window_functions_1.md", 401),
        ("sql_10_oynador_funksiyalar_window_functions_2.md", 451),
        ("sql_11_toplam_amallari_set_operations.md", 501),
        ("sql_12_qator_va_sana_funksiyalari.md", 551),
        ("sql_13_shartli_mantiq_case_va_null_boshqaruvi.md", 601),
        ("sql_14_korinishlar_views_va_materialized_views.md", 651),
        ("sql_15_indekslar_va_sorovlarni_optimallashtirish.md", 701),
        ("sql_16_tranzaksiyalar_va_acid_xususiyatlari.md", 751),
        ("sql_17_protseduralar_va_maxsus_funksiyalar.md", 801),
        ("sql_18_triggerlar_va_hodisalarni_avtomatlashtirish.md", 851),
        ("sql_19_json_va_zamonaviy_malumotlar_bilan_ishlash.md", 901),
        ("sql_20_amaliy_korporativ_baza_va_ai_vector_db.md", 951),
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
    enc_path = os.path.join(base_dir, "sql_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"sql_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
    else:
        print("sql_mukammal_qollanma.md: Mavjud emas")
        all_ok = False

    sys.exit(0 if all_ok else 1)
