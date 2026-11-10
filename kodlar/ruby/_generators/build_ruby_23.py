# -*- coding: utf-8 -*-
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from ruby_tasks_1101_1125 import TASKS_1101_1125
from ruby_tasks_1126_1150 import TASKS_1126_1150

def build():
    all_tasks = TASKS_1101_1125 + TASKS_1126_1150
    print(f"Jami yuklangan topshiriqlar soni: {len(all_tasks)}")
    assert len(all_tasks) == 50, f"Kutilgan 50, lekin {len(all_tasks)} ta topshiriq bor!"

    for idx, t in enumerate(all_tasks):
        expected_id = 1101 + idx
        assert t["id"] == expected_id, f"ID mos kelmadi: kutilgan {expected_id}, haqiqiy {t['id']}"

    output_lines = [
        "# Khorazmiy AI: Ruby - Modul 23",
        "## Mavzu: Asinxron tarmoq: Async gem, Falcon HTTP/2 server, Socket va ActionCable WebSockets\n"
    ]

    for t in all_tasks:
        block = f"""### Topshiriq #{t['id']}: {t['title']}
**Tavsif:** {t['desc']}
**Talablar:** {t['req']}
**Yechim (Ruby):**
```ruby
{t['code'].strip()}
```
**Tushuntirish:** {t['expl']}
"""
        output_lines.append(block)

    full_content = "\n---\n\n".join(output_lines[:2]) + "\n" + "\n---\n\n".join(output_lines[2:]) + "\n"
    
    out_path = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\ruby_23_tarmoq_va_falcon_async.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Muvaffaqiyatli yaratildi: {out_path} ({len(all_tasks)} ta topshiriq)")

if __name__ == "__main__":
    build()
