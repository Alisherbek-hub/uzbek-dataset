"""
Khorazmiy AI: Avtomatlashtirilgan Bulutli Dataset Kengaytirgich
20 ta dasturlash tili bo'yicha yangi ilg'or modullarni avtomatik generatsiya qiladi.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_PATH = os.path.join(CURRENT_DIR, "keys.json")
DATASET_ROOT = os.path.dirname(CURRENT_DIR)
KODLAR_DIR = os.path.join(DATASET_ROOT, "kodlar")

def load_keys():
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return [env_key], os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    if os.path.exists(KEYS_PATH):
        with open(KEYS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("active_keys", []), data.get("default_model", "gemini-2.5-flash")
    print("[Ogohlantirish] keys.json yoki GEMINI_API_KEY topilmadi.")
    return [], "gemini-2.5-flash"

class KeyRotator:
    def __init__(self, keys, model_name):
        self.keys = keys
        self.current_idx = 0
        self.model_name = model_name

    def get_current_key(self):
        return self.keys[self.current_idx]

    def rotate(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        print(f"[Rotator] Yangi kalitga o'tildi (Index: {self.current_idx})")

    def generate(self, prompt, retries=3):
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096,
            }
        }).encode("utf-8")

        for attempt in range(retries):
            key = self.get_current_key()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={key}"
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

            try:
                with urllib.request.urlopen(req, timeout=25) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return text
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                print(f"[Xatolik {e.code}] Kalit {self.current_idx} da xatolik yuz berdi: {err_body[:100]}")
                if e.code in (429, 401, 503):
                    self.rotate()
                    time.sleep(2)
                else:
                    time.sleep(1)
            except Exception as e:
                print(f"[Tarmoq xatosi] {e}. Qayta urinilmoqda...")
                time.sleep(2)

        return None

def generate_module(language, module_num, start_task_id, topic_title, count=10):
    """
    Belgilangan til va mavzu bo'yicha yangi topshiriqlar blokini generatsiya qiladi.
    """
    keys, model = load_keys()
    rotator = KeyRotator(keys, model)

    prompt = f"""Sen 'Khorazmiy AI' loyihasining professional dataset muhandisisan.
Biz {language} dasturlash tili bo'yicha datasetni 100 000 taga yetkazish uchun yangi ilg'or modullarni shakllantirmoqdamiz.

Mavzu: {topic_title}
Topshiriqlar raqami: #{start_task_id} dan #{start_task_id + count - 1} gacha ({count} ta topshiriq).

Har bir topshiriq QAT'IY quyidagi formatda bo'lishi shart:

# {{N}}-Topshiriq: {{Sarlavha}}

## Topshiriq sharti:
{{O'zbek tilida aniq va amaliy masala sharti}}

## Yechim ({language} kodi):
```{language.lower()}
{{To'liq ishlaydigan xatosiz kod}}
```

## Tushuntirish va Mantiq:
{{Koddagi har bir muhim qism va algoritmning o'zbekcha mantiqiy tahlili}}

## Ishlash natijasi:
```text
{{Terminal/konsolda chiqadigan aniq natija}}
```

Hech qanday qisqartirishsiz, to'liq va mukammal {count} ta topshiriqni o'zbek tilida yozib ber."""

    print(f"[{language.upper()}] '{topic_title}' mavzusi bo'yicha {count} ta topshiriq generatsiya qilinmoqda...")
    res = rotator.generate(prompt)
    return res

if __name__ == "__main__":
    keys, model = load_keys()
    print(f"Khorazmiy AI Generator tayyor. Faol kalitlar: {len(keys)} ta. Model: {model}")
    # Kichik sinov
    test_res = generate_module("Python", 21, 1001, "Kiberxavfsizlik va Xakerlikdan Himoya", count=3)
    if test_res:
        print("[Muvaffaqiyatli sinov!]")
        print(test_res[:400] + "...")
