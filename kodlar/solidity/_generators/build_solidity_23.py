# -*- coding: utf-8 -*-
import sys
import os

# Add current dir to sys.path
curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from sol_tasks_1101_1125 import TASKS_1101_1125
from sol_tasks_1126_1150 import TASKS_1126_1150

def build():
    all_tasks = TASKS_1101_1125 + TASKS_1126_1150
    print(f"Jami yuklangan topshiriqlar soni: {len(all_tasks)}")
    assert len(all_tasks) == 50, f"Kutilgan 50, lekin {len(all_tasks)} ta topshiriq bor!"

    # ID larni tekshirish
    for idx, t in enumerate(all_tasks):
        expected_id = 1101 + idx
        assert t["id"] == expected_id, f"ID mos kelmadi: kutilgan {expected_id}, haqiqiy {t['id']}"

    output_lines = [
        "# Khorazmiy AI: Solidity - Modul 23",
        "## Mavzu: Cross-Chain xabarlar protokollari (Chainlink CCIP, LayerZero, Wormhole), Oracle tarmoqlari va EIP-4337 Account Abstraction\n"
    ]

    for t in all_tasks:
        block = f"""### Topshiriq #{t['id']}: {t['title']}
**Tavsif:** {t['desc']}
**Talablar:** {t['req']}
**Yechim (Solidity):**
```solidity
{t['code'].strip()}
```
**Tushuntirish:** {t['expl']}
"""
        output_lines.append(block)

    full_content = "\n---\n\n".join(output_lines[:2]) + "\n" + "\n---\n\n".join(output_lines[2:]) + "\n"
    
    out_path = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\solidity\solidity_23_cross_chain_va_oracles.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Muvaffaqiyatli yaratildi: {out_path} ({len(all_tasks)} ta topshiriq)")

if __name__ == "__main__":
    build()
