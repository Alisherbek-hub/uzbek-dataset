"""
Khorazmiy AI: Kengaytirilgan Ommaviy Dataset Generatori (Batch Runner - Qism 2)
Qolgan 10 ta til: C, C#, HTML/CSS, Kotlin, PHP, Assembly, Ruby, R, Lua, Swift
bo'yicha #1001-#1050 topshiriqlarni avtomatik tarzda yaratadi va saqlaydi.
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
LOG_PATH = os.path.join(CURRENT_DIR, "generator_progress.log")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def load_keys():
    if not os.path.exists(KEYS_PATH):
        raise FileNotFoundError(f"keys.json topilmadi: {KEYS_PATH}")
    with open(KEYS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("active_keys", []), data.get("default_model", "gemini-3.1-flash-lite")

class KeyRotator:
    def __init__(self, keys, model_name):
        self.keys = keys
        self.current_idx = 0
        self.model_name = model_name

    def get_current_key(self):
        return self.keys[self.current_idx]

    def rotate(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        log(f"[Rotator] Yangi API kalitiga o'tildi (Kalit #{self.current_idx + 1})")

    def generate(self, prompt, retries=5):
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.25,
                "maxOutputTokens": 4096,
            }
        }).encode("utf-8")

        for attempt in range(retries):
            key = self.get_current_key()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={key}"
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return text
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                log(f"[API Xatosi {e.code}] Kalit #{self.current_idx + 1}: {err_body[:120]}")
                if e.code in (429, 401, 503):
                    self.rotate()
                    time.sleep(3)
                else:
                    time.sleep(2)
            except Exception as e:
                log(f"[Tarmoq xatosi] {e}. Qayta urinilmoqda...")
                self.rotate()
                time.sleep(3)

        return None

# Qolgan 10 ta til uchun 21-modullar
MODULE_21_SPECS_PART2 = [
    {
        "lang_dir": "c",
        "lang_name": "C",
        "file_name": "c_21_embedded_iot_va_drayverlar.md",
        "topic": "Embedded C, mikrokontrollerlar (STM32, ESP32), RTOS vazifalari va drayverlar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "csharp",
        "lang_name": "C#",
        "file_name": "csharp_21_cloud_native_dotnet_va_grpc.md",
        "topic": ".NET 8/9 cloud-native arxitekturasi, Span<T> xotira optimizatsiyasi va gRPC",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "html_css",
        "lang_name": "HTML & CSS",
        "file_name": "html_css_21_ilgori_animatsiyalar_va_canvas.md",
        "topic": "Canvas grafikasi, WebGL asoslari, CSS subgrid va murakkab responsive animatsiyalar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "kotlin",
        "lang_name": "Kotlin",
        "file_name": "kotlin_21_kmp_va_ilgori_korutinalar.md",
        "topic": "Kotlin Multiplatform (KMP), Compose Multiplatform va murakkab Coroutine Flows",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "php",
        "lang_name": "PHP",
        "file_name": "php_21_async_swoole_va_roadrunner.md",
        "topic": "Asinxron PHP (Swoole, RoadRunner), yuqori yuklamali e-commerce va WebSocketlar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "assembly",
        "lang_name": "Assembly",
        "file_name": "assembly_21_os_bootloader_va_bare_metal.md",
        "topic": "OS bootloader yozish (BIOS/UEFI), bare-metal x86/ARM64 va interrupt handling",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "ruby",
        "lang_name": "Ruby",
        "file_name": "ruby_21_yjit_va_katta_masshtabli_rails.md",
        "topic": "Ruby 3.3+ YJIT unumdorligi, Ractors parallelizm va enterprise Rails",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "r",
        "lang_name": "R",
        "file_name": "r_21_katta_hajmli_ekonometrika_va_biostatistika.md",
        "topic": "Katta hajmli ekonometrik modellashtirish, Bioconductor genomika va parallel R",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "lua",
        "lang_name": "Lua",
        "file_name": "lua_21_luajit_ffi_va_nginx_openresty.md",
        "topic": "LuaJIT FFI orqali C bilan aloqa, yuqori yuklamali Nginx OpenResty API shlyuzi",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "swift",
        "lang_name": "Swift",
        "file_name": "swift_21_actor_concurrency_va_visionos.md",
        "topic": "Swift 6 Data Isolation, Actors, Spatial Computing (visionOS) va Metal shaders",
        "start_id": 1001,
        "total_tasks": 50
    }
]

def generate_subbatch(rotator, lang_name, topic, start_id, end_id):
    count = end_id - start_id + 1
    prompt = f"""Sen 'Khorazmiy AI' loyihasining katta dataset muhandisisan.
{lang_name} dasturlash tili bo'yicha 100 000 talik datasetni boyitish uchun yangi ilg'or modullarni yarat.

Mavzu: {topic}
Topshiriqlar raqami: #{start_id} dan #{end_id} gacha (Jami {count} ta topshiriq).

Har bir topshiriq QAT'IY quyidagi standart formatda bo'lishi shart:

# {{N}}-Topshiriq: {{Sarlavha}}

## Topshiriq sharti:
{{O'zbek tilida aniq va amaliy masala sharti}}

## Yechim ({lang_name} kodi):
```{lang_name.lower()}
{{To'liq ishlaydigan xatosiz kod}}
```

## Tushuntirish va Mantiq:
{{Koddagi har bir muhim qism va algoritmning o'zbekcha mantiqiy tahlili}}

## Ishlash natijasi:
```text
{{Terminal/konsolda chiqadigan aniq natija}}
```

Hech qanday TODO, FIXME yoki qisqartirishsiz, aynan {count} ta topshiriqni to'liq o'zbek tilida yozib ber."""

    return rotator.generate(prompt)

def process_module(rotator, spec):
    lang_dir = spec["lang_dir"]
    lang_name = spec["lang_name"]
    file_name = spec["file_name"]
    topic = spec["topic"]
    start_id = spec["start_id"]
    total = spec["total_tasks"]

    target_dir = os.path.join(KODLAR_DIR, lang_dir)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, file_name)

    if os.path.exists(target_path):
        log(f"[O'tkazildi] {file_name} allaqachon mavjud.")
        return

    log(f"==================================================")
    log(f"Boshlandi: {lang_name} - {file_name}")
    log(f"Mavzu: {topic} (Jami {total} ta topshiriq)")

    batch_size = 10
    collected_content = []

    for sub_start in range(start_id, start_id + total, batch_size):
        sub_end = min(sub_start + batch_size - 1, start_id + total - 1)
        log(f"-> [{lang_name}] #{sub_start}-#{sub_end} topshiriqlar olinmoqda...")

        chunk = generate_subbatch(rotator, lang_name, topic, sub_start, sub_end)
        if chunk:
            collected_content.append(chunk.strip())
            log(f"   [OK] #{sub_start}-#{sub_end} muvaffaqiyatli qabul qilindi.")
        else:
            log(f"   [OGOHLANTIRISH] #{sub_start}-#{sub_end} qabul qilinmadi!")

        time.sleep(2)

    if collected_content:
        full_text = "\n\n---\n\n".join(collected_content)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        log(f"[YAKUNLANDI] {file_name} saqlandi! ({os.path.getsize(target_path)} bayt)")
    else:
        log(f"[XATO] {file_name} uchun hech qanday ma'lumot yig'ilmadi.")

def run_part2():
    keys, model = load_keys()
    log(f"Khorazmiy AI Batch Generator Part 2 ishga tushdi.")
    log(f"Faol API kalitlar: {len(keys)} ta. Model: {model}")
    rotator = KeyRotator(keys, model)

    for spec in MODULE_21_SPECS_PART2:
        try:
            process_module(rotator, spec)
        except Exception as e:
            log(f"[Xatolik yuz berdi] {spec['lang_name']} da: {e}")
            time.sleep(3)

    log("Barcha 2-qism modullar generatsiyasi muvaffaqiyatli yakunlandi!")

if __name__ == "__main__":
    run_part2()
