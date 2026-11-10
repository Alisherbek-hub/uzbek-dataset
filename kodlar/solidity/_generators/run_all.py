# -*- coding: utf-8 -*-
"""
Run all generators and validation for Solidity (20-til)
"""
import sys
import os
import subprocess

def main():
    generators_dir = os.path.dirname(__file__)
    scripts = [
        "generate_solidity_part1_to_5.py",
        "generate_solidity_part6_to_10.py",
        "generate_solidity_part11_to_15.py",
        "generate_solidity_part16_to_20.py",
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
    print("\nSOLIDITY TILI BO'YICHA BARCHA FAYLLAR MUVAFFAQIYATLI YARATILDI VA TEKSHIRILDI!")

if __name__ == "__main__":
    main()
