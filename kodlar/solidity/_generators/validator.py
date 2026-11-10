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
        if "## Yechim (Solidity kodi):" not in task_block:
            return False, f"{task_num}-topshiriqda '## Yechim (Solidity kodi):' bo'limi yo'q"
        if "```solidity" not in task_block:
            return False, f"{task_num}-topshiriqda '```solidity' blok mavjud emas"
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
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\solidity"
    files = [
        ("solidity_01_asoslar_tiplar_va_ozgaruvchilar.md", 1),
        ("solidity_02_funksiyalar_korinish_va_holat_mutabilligi.md", 51),
        ("solidity_03_xotira_joylashuvi_storage_memory_calldata.md", 101),
        ("solidity_04_shartlar_tsikllar_va_xatoliklarni_boshqarish.md", 151),
        ("solidity_05_massivlar_va_mappinglar.md", 201),
        ("solidity_06_strukturalar_va_enumlar.md", 251),
        ("solidity_07_modifikatorlar_modifiers_va_kirish_nazorati.md", 301),
        ("solidity_08_hodisalar_events_va_indexed_parametrlari.md", 351),
        ("solidity_09_merosxorlik_polimorfizm_va_interfeyslar.md", 401),
        ("solidity_10_efir_yuborish_va_qabul_qilish.md", 451),
        ("solidity_11_past_darajali_chaqiruvlar_call_va_delegatecall.md", 501),
        ("solidity_12_erc20_token_standarti_va_amaliyoti.md", 551),
        ("solidity_13_erc721_va_nft_standartlari.md", 601),
        ("solidity_14_erc1155_kop_tokenli_standart.md", 651),
        ("solidity_15_yangilanuvchi_kontraktlar_upgradeable_va_proksilar.md", 701),
        ("solidity_16_defi_primitivlari_staking_dex_va_likvidlik.md", 751),
        ("solidity_17_xavfsizlik_va_zaifliklar_security_exploits.md", 801),
        ("solidity_18_gas_optimizatsiyasi_usullari_gas_golfing.md", 851),
        ("solidity_19_inline_assembly_yul_va_evm_opkodlari.md", 901),
        ("solidity_20_kriptografiya_imzolar_va_oracllar.md", 951),
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
            
    enc_path = os.path.join(base_dir, "solidity_mukammal_qollanma.md")
    if os.path.exists(enc_path):
        size = os.path.getsize(enc_path)
        print(f"solidity_mukammal_qollanma.md: Mavjud, hajmi {size} bayt")
        if size < 10000:
            print("OGOHLANTIRISH: Ensiklopediya hajmi juda kichik!")
            all_ok = False
    else:
        print("solidity_mukammal_qollanma.md: Mavjud emas")
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
