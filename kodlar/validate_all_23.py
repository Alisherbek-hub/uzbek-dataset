# -*- coding: utf-8 -*-
import os
import re

modules = [
    (
        r"C:\Users\User\Desktop\uzbek_dataset\kodlar\solidity\solidity_23_cross_chain_va_oracles.md",
        "Solidity",
        "solidity"
    ),
    (
        r"C:\Users\User\Desktop\uzbek_dataset\kodlar\lua\lua_23_tarmoq_va_openresty_protocols.md",
        "Lua",
        "lua"
    ),
    (
        r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\ruby_23_tarmoq_va_falcon_async.md",
        "Ruby",
        "ruby"
    )
]

def validate():
    total_ok = True
    for path, lang_name, lang_tag in modules:
        print(f"\n==================================================")
        print(f"Tekshirilmoqda: {lang_name}")
        print(f"Fayl yo'li: {path}")
        if not os.path.exists(path):
            print(f"[XATO] Fayl mavjud emas: {path}")
            total_ok = False
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        file_size_kb = len(content.encode("utf-8")) / 1024
        print(f"Fayl hajmi: {file_size_kb:.1f} KB")

        # 1. Topshiriq sarlavhalari
        task_headers = re.findall(r"^### Topshiriq #(\d+):\s*(.+)$", content, re.MULTILINE)
        print(f"Topshiriqlar soni: {len(task_headers)} ta")
        if len(task_headers) != 50:
            print(f"[XATO] Kutilgan 50 ta, ammo {len(task_headers)} ta topildi!")
            total_ok = False
            continue

        # ID lar ketma-ketligi
        ids_valid = True
        for i, (tid, title) in enumerate(task_headers):
            expected_id = 1101 + i
            if int(tid) != expected_id:
                print(f"[XATO] Topshiriq indeksi xato: kutilgan #{expected_id}, lekin #{tid}")
                ids_valid = False
                total_ok = False
                break
        if ids_valid:
            print(f"[OK] Barcha ID lar tartibli (#1101 dan #1150 gacha)")

        # 2. Bloklar hisobi
        tavsif_count = len(re.findall(r"^\*\*Tavsif:\*\*", content, re.MULTILINE))
        talablar_count = len(re.findall(r"^\*\*Talablar:\*\*", content, re.MULTILINE))
        yechim_count = len(re.findall(rf"^\*\*Yechim \({lang_name}\):\*\*", content, re.MULTILINE))
        code_fence_start = len(re.findall(rf"^```{lang_tag}$", content, re.MULTILINE))
        code_fence_end = len(re.findall(r"^```$", content, re.MULTILINE))
        tushuntirish_count = len(re.findall(r"^\*\*Tushuntirish:\*\*", content, re.MULTILINE))

        print(f"Tavsif bloklari: {tavsif_count}/50")
        print(f"Talablar bloklari: {talablar_count}/50")
        print(f"Yechim bloklari: {yechim_count}/50")
        print(f"Kod ochilishi (```{lang_tag}): {code_fence_start}/50")
        print(f"Kod yopilishi (```): {code_fence_end}/50")
        print(f"Tushuntirish bloklari: {tushuntirish_count}/50")

        if (tavsif_count == 50 and talablar_count == 50 and yechim_count == 50 and
            code_fence_start == 50 and code_fence_end == 50 and tushuntirish_count == 50):
            print(f"[MUVAFFAQIN] {lang_name} 23-modul 100% to'liq va benuqson!")
        else:
            print(f"[XATO] Ba'zi bloklar 50 taga yetmadi!")
            total_ok = False

    print("\n==================================================")
    if total_ok:
        print("BARCHA 3 TA MODUL (Solidity, Lua, Ruby) TO'LIQ VA MUVAFFAQIYATLI TEKSHIRUVDAN O'TDI!")
    else:
        print("XATOLIKLAR MAVJUD!")

if __name__ == "__main__":
    validate()
