"""
Khorazmiy AI: GitHub Actions Avtomatlashtirilgan Bulutli Dataset Kengaytirgich
Har bir ishga tushganda 20 ta dasturlash tili bo'yicha keyingi yangi modullarni generatsiya qiladi va fayllarga saqlaydi.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from continuous_100k_generator import run_continuous_expansion, load_keys, LANGUAGES, get_existing_modules

def main():
    keys, model = load_keys()
    print(f"[Khorazmiy Cloud Actions] Generator ishga tushdi. Kalitlar mavjud: {bool(keys)}, Model: {model}")
    if not keys:
        print("[Xato] API kaliti topilmadi. GEMINI_API_KEY sozlanmagan.")
        return

    # Qaysi modulda ekanligimizni aniqlash
    min_mod = 100
    for l in LANGUAGES:
        existing = get_existing_modules(l["dir"])
        next_m = max(existing) + 1 if existing else 1
        if next_m < min_mod:
            min_mod = next_m

    target = min(min_mod, 100)
    print(f"[Khorazmiy Cloud Actions] Modul {min_mod} (target: {target}) generatsiyasi boshlanmoqda...")
    run_continuous_expansion(start_module=min_mod, target_module=target)
    print("[Khorazmiy Cloud Actions] Ushbu bosqich muvaffaqiyatli yakunlandi!")

if __name__ == "__main__":
    main()
