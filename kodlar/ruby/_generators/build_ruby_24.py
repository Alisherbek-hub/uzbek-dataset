# -*- coding: utf-8 -*-
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from ruby_tasks_1151_1175 import TASKS_1151_1175
from ruby_tasks_1176_1200 import TASKS_1176_1200

def build():
    all_tasks = TASKS_1151_1175 + TASKS_1176_1200
    print(f"Jami yuklangan topshiriqlar soni: {len(all_tasks)}")
    assert len(all_tasks) == 50, f"Kutilgan 50, lekin {len(all_tasks)} ta topshiriq bor!"

    for idx, t in enumerate(all_tasks):
        expected_id = 1151 + idx
        assert t["id"] == expected_id, f"ID mos kelmadi: kutilgan {expected_id}, haqiqiy {t['id']}"

    output_lines = [
        "# Khorazmiy AI: Ruby - Modul 24\n"
        "## Mavzu: Kriptografiya va Rails Xavfsizligi: OpenSSL, ActiveSupport::MessageEncryptor, Rails credentials (master.key), Devise/Argon2, CSRF himoyasi, Arel SQL injection audit va Rack::Attack rate limiting\n"
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

    full_content = "\n\n---\n\n".join(output_lines) + "\n"
    
    out_path = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\ruby_24_kriptografiya_va_xavfsizlik.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Muvaffaqiyatli yaratildi: {out_path} ({len(all_tasks)} ta topshiriq)")

if __name__ == "__main__":
    build()
