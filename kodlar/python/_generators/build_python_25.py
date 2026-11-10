# -*- coding: utf-8 -*-
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from py_tasks_1201_1225 import TASKS_1201_1225
from py_tasks_1226_1250 import TASKS_1226_1250

def build():
    all_tasks = TASKS_1201_1225 + TASKS_1226_1250
    print(f"Jami yuklangan topshiriqlar soni: {len(all_tasks)}")
    assert len(all_tasks) == 50, f"Kutilgan 50, lekin {len(all_tasks)} ta topshiriq bor!"

    for idx, t in enumerate(all_tasks):
        expected_id = 1201 + idx
        assert t["id"] == expected_id, f"ID mos kelmadi: kutilgan {expected_id}, haqiqiy {t['id']}"

    output_lines = [
        "# Khorazmiy AI: Python - Modul 25\n"
        "## Mavzu: Ma'lumotlar Bazasi Ichki Dvigatellari (Storage Engines): LSM-Trees (MemTable, WAL, SSTable, Leveled Compaction), B+Tree noldan qurish, Bitcask Log-Structured Storage, Bloom Filters va Buffer Pool Manager\n"
    ]

    for t in all_tasks:
        block = f"""### Topshiriq #{t['id']}: {t['title']}
**Tavsif:** {t['desc']}
**Talablar:** {t['req']}
**Yechim (Python):**
```python
{t['code'].strip()}
```
**Tushuntirish:** {t['expl']}
"""
        output_lines.append(block)

    full_content = "\n\n---\n\n".join(output_lines) + "\n"
    
    out_path = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\python\python_25_storage_engines_va_indekslar.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Muvaffaqiyatli yaratildi: {out_path} ({len(all_tasks)} ta topshiriq)")

if __name__ == "__main__":
    build()
