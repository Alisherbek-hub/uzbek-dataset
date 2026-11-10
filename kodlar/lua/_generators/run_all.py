# -*- coding: utf-8 -*-
"""
Run all generators and validation for Lua (19-til)
"""
import sys
import os
import subprocess

def main():
    generators_dir = os.path.dirname(__file__)
    scripts = [
        "generate_lua_part1.py",
        "generate_lua_part2.py",
        "generate_lua_part3_4_5.py",
        "generate_lua_part6_to_10.py",
        "generate_lua_part11_to_15.py",
        "generate_lua_part16_to_20.py",
        "gen_encyclopedia.py",
        "validator.py"
    ]
    for script in scripts:
        script_path = os.path.join(generators_dir, script)
        print(f"\n--- Bajarilmoqda: {script} ---")
        res = subprocess.run([sys.executable, script_path], check=True)
        if res.returncode != 0:
            print(f"Xatolik yuz berdi: {script}")
            sys.exit(1)
    print("\nLUA TILI BO'YICHA BARCHA FAYLLAR MUVAFFAQIYATLI YARATILDI VA TEKSHIRILDI!")

if __name__ == "__main__":
    main()
