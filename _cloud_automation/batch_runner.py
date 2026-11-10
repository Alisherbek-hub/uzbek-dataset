"""
Khorazmiy AI: Kengaytirilgan Ommaviy Dataset Generatori (Batch Runner)
API kalitlar rotatsiyasi orqali 20 ta til bo'yicha #1001 dan yuqori vazifalarni
avtomatik tarzda yaratadi va tegishli papkalarga saqlaydi.
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

# 20 ta til uchun 21-modullar (Ilg'or mavzular)
MODULE_21_SPECS = [
    {
        "lang_dir": "python",
        "lang_name": "Python",
        "file_name": "python_21_kiberxavfsizlik_va_tarmoq_himoyasi.md",
        "topic": "Kiberxavfsizlik, xakerlikdan himoya, kriptografiya va tarmoq auditi",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "cpp",
        "lang_name": "C++",
        "file_name": "cpp_21_yuqori_unumdorlik_simd_va_parallelizm.md",
        "topic": "SIMD vektorlash, multi-threading, xotira optimizatsiyasi va GPU hisob-kitoblar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "rust",
        "lang_name": "Rust",
        "file_name": "rust_21_tizimli_drayverlar_va_unsafe_xavfsizlik.md",
        "topic": "Unsafe Rust nazorati, OS drayverlari, nol xarajatli abstraktsiya va FFI",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "go",
        "lang_name": "Go",
        "file_name": "go_21_katta_yuklamali_mikroservislar_va_grpc.md",
        "topic": "High-load mikroservislar, gRPC oqimlari, Redis kesh klasteri va taqsimlangan tranzaksiyalar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "javascript_typescript",
        "lang_name": "TypeScript",
        "file_name": "ts_21_enterprise_arxitektura_va_ddd.md",
        "topic": "Domain-Driven Design (DDD), Clean Architecture, micro-frontends va AST transformatsiyalar",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "solidity",
        "lang_name": "Solidity",
        "file_name": "solidity_21_ilgori_defi_va_mev_himoyasi.md",
        "topic": "MEV botlaridan himoya, Flash Loans, Oracle manipulyatsiyasiga qarshi shartnomalar va ZK-proofs",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "dart",
        "lang_name": "Dart",
        "file_name": "dart_21_offline_first_va_murakkab_izolyatsiyalar.md",
        "topic": "Offline-first sinxronizatsiya, Isolate orqali fon hisoblash va mahalliy SQLite shifrlash",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "sql",
        "lang_name": "SQL",
        "file_name": "sql_21_katta_hajmli_partitsiyalash_va_sharding.md",
        "topic": "Milliardlik jadvallarni partitsiyalash, sharding, WAL sozlamalari va deadlock tahlili",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "java",
        "lang_name": "Java",
        "file_name": "java_21_bank_xavfsizligi_va_yuqori_tranzaksiyalar.md",
        "topic": "Bank to'lov shlyuzlari, ikki bosqichli tasdiq (2PC), Spring Security OAuth2 va HSM integratsiyasi",
        "start_id": 1001,
        "total_tasks": 50
    },
    {
        "lang_dir": "bash_shell",
        "lang_name": "Bash",
        "file_name": "bash_21_kiber_xavfsizlik_va_server_hardening.md",
        "topic": "Linux server hardening, CIS benchmark tekshiruvi, iptables/nftables va avtomatik IDS/IPS",
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

    # 50 ta topshiriqni 5 ta sub-batchda (10 tadan) generatsiya qilamiz
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

        # Kichik orom (API rate limit uchun)
        time.sleep(2)

    if collected_content:
        full_text = "\n\n---\n\n".join(collected_content)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        log(f"[YAKUNLANDI] {file_name} saqlandi! ({os.path.getsize(target_path)} bayt)")
    else:
        log(f"[XATO] {file_name} uchun hech qanday ma'lumot yig'ilmadi.")

def run_all():
    keys, model = load_keys()
    log(f"Khorazmiy AI Batch Generator ishga tushdi.")
    log(f"Faol API kalitlar: {len(keys)} ta. Model: {model}")
    rotator = KeyRotator(keys, model)

    for spec in MODULE_21_SPECS:
        try:
            process_module(rotator, spec)
        except Exception as e:
            log(f"[Xatolik yuz berdi] {spec['lang_name']} da: {e}")
            time.sleep(3)

    log("Barcha rejalashtirilgan modullar generatsiyasi yakunlandi!")

if __name__ == "__main__":
    run_all()
