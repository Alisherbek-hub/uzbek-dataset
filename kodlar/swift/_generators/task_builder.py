# -*- coding: utf-8 -*-
import os

def format_task(n: int, title: str, condition: str, solution_code: str, explanation: str, result_text: str) -> str:
    return f"""# {n}-Topshiriq: {title}
## Topshiriq sharti:
{condition.strip()}

## Yechim (Swift kodi):
```swift
{solution_code.strip()}
```

## Tushuntirish va Mantiq:
{explanation.strip()}

## Ishlash natijasi:
```text
{result_text.strip()}
```
"""

def save_file(filename: str, tasks: list) -> None:
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\swift"
    out_path = os.path.join(base_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(tasks) + "\n")
    print(f"Muvaffaqiyatli saqlandi: {out_path} ({len(tasks)} ta topshiriq)")
