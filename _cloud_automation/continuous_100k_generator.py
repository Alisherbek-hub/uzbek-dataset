"""
Khorazmiy AI: 100 000 talik Suveren Dasturlash Dataset Generatori (Continuous 100k Generator)
-----------------------------------------------------------------------------------------
20 ta dasturlash tili bo'yicha 21-moduldan 100-modulgacha (jami 100 000 ta topshiriq)
avtomatik tarzda yaratadi, tekshiradi va uzluksiz kengaytirib boradi.

Xususiyatlari:
1. Smart Resume: Mavjud fayllarni tekshiradi va to'xtagan joyidan davom etadi;
2. Multi-Key Rotation: API kalitlarini avtomatik almashtirib boradi;
3. Rate Limit & Error Handling: HTTP 429 yoki uzilishlarda o'z-o'zidan kutib qayta urinadi;
4. Real-time Progress: Umumiy 100 000 talik marraga nisbatan foiz va hisobot yuritadi.
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

LANGUAGES = [
    {"dir": "python", "name": "Python"},
    {"dir": "cpp", "name": "C++"},
    {"dir": "dart", "name": "Dart"},
    {"dir": "rust", "name": "Rust"},
    {"dir": "go", "name": "Go"},
    {"dir": "html_css", "name": "HTML & CSS"},
    {"dir": "c", "name": "C"},
    {"dir": "csharp", "name": "C#"},
    {"dir": "javascript_typescript", "name": "JavaScript & TypeScript"},
    {"dir": "sql", "name": "SQL"},
    {"dir": "java", "name": "Java"},
    {"dir": "kotlin", "name": "Kotlin"},
    {"dir": "swift", "name": "Swift"},
    {"dir": "php", "name": "PHP"},
    {"dir": "bash_shell", "name": "Bash & Shell"},
    {"dir": "assembly", "name": "Assembly"},
    {"dir": "ruby", "name": "Ruby"},
    {"dir": "r", "name": "R"},
    {"dir": "lua", "name": "Lua"},
    {"dir": "solidity", "name": "Solidity"}
]

# Modullar uchun ilg'or professional mavzular o'quv dasturi (22-moduldan 100-modulgacha)
MODULE_TOPICS = {
    22: ("Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari", "algoritmlar_va_daraxtlar"),
    23: ("Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets", "tarmoq_va_protokollar"),
    24: ("Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash", "kriptografiya_va_xavfsizlik"),
    25: ("Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash", "storage_engines_va_indekslar"),
    26: ("Yuqori yuklamali kesh tizimlari: Redis, Memcached va Cache Invalidation", "keshlash_va_invalidation"),
    27: ("Xabarlar navbati va oqimlar: Kafka, RabbitMQ va Event-Driven arxitektura", "event_driven_va_kafka"),
    28: ("Mikroservislar va Taqsimlangan Tranzaksiyalar: Saga, Outbox va 2PC", "saga_va_taqsimlangan_tizimlar"),
    29: ("Asinxron oqimlar va Reaktiv Dasturlash: Reactive Streams, Coroutines", "reaktiv_dasturlash"),
    30: ("Kompilyatorlar va Virtual Mashinalar: AST, Lexer, Parser va Bytecode", "kompilyator_va_ast"),
    31: ("Nol-Nusxa (Zero-Copy) I/O va Katta Hajmli Ma'lumotlarni Uzatish", "zero_copy_io"),
    32: ("Taqsimlangan Konsensus: Raft, Paxos va Vector Clocks algoritmlari", "raft_va_konsensus"),
    33: ("Kiber-hujumlardan himoya: Memory Corruption, Buffer Overflow va ASLR", "memory_corruption_himoya"),
    34: ("Konteynerizatsiya va Klasterlar: Dockerfile, K8s Operators va Service Mesh", "k8s_operators_va_mesh"),
    35: ("Kuzatuvchanlik (Observability): OpenTelemetry, Distributed Tracing va Prometheus", "opentelemetry_va_metrikalar"),
    36: ("Lock-Free va Wait-Free Ma'lumotlar Tuzilmalari (Atomic amallar)", "lock_free_tuzilmalar"),
    37: ("GPU hisoblashlari va Parallel Matritsalar Ko'paytirish (CUDA / Compute Shaders)", "gpu_parallel_hisoblash"),
    38: ("AI Model Injiniringi: KV-Cache, PagedAttention va Quantization (INT4/INT8)", "ai_inference_injiniringi"),
    39: ("Katta hajmli Time-Series ma'lumotlar bazalari (TSDB va Anomaliyalarni aniqlash)", "time_series_va_monitoring"),
    40: ("Taqsimlangan Fayl Tizimlari (HDFS, Ceph va S3-mos Storage tuzilishi)", "taqsimlangan_fayl_tizimlari"),
    41: ("Search Engine Injiniringi: Inverted Index, BM25 va Vektor Qidiruv (HNSW)", "vektor_qidiruv_va_hnsw"),
    42: ("Kriptografik Protokollar: Zero-Knowledge Proofs (zk-SNARKs) va Post-Quantum", "zk_proofs_va_postquantum"),
    43: ("Domain-Driven Design (DDD): Aggregates, Value Objects va Hexagonal Arxitektura", "ddd_va_hexagonal"),
    44: ("Serverless va Edge Computing (Wasm / Cloudflare Workers runtime)", "serverless_va_wasm_edge"),
    45: ("Tizimli Operatsion Dasturlash: Linux Syscalls, Signals va IPC mexanizmlari", "linux_syscalls_va_ipc"),
    46: ("Katta Masshtabli API Gateway: Rate Limiting (Token Bucket, Leaky Bucket)", "api_gateway_va_rate_limiting"),
    47: ("Reliability Engineering: Chaos Engineering, Fault Injection va Circuit Breakers", "chaos_va_circuit_breaker"),
    48: ("Graph Data Processing: PageRank, Breadth-First Search va Graflar Tahlili", "graph_processing_pagerank"),
    49: ("Advanced Metaprogramming: Makroslar, Reflection va Code Generation", "metaprogramming_va_makroslar"),
    50: ("Khorazmiy Oltin Standarti: 2500-topshiriq Yubiley Mukammal Arxitektura Loyihasi", "oltin_standart_arxitektura")
}

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    try:
        print(formatted)
    except Exception:
        try:
            print(formatted.encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def load_keys():
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return [env_key], os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    if os.path.exists(KEYS_PATH):
        with open(KEYS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("active_keys", []), data.get("default_model", "gemini-2.5-flash")
    return [], "gemini-2.5-flash"

class KeyRotator:
    def __init__(self, keys, model_name):
        self.keys = keys
        self.model_name = model_name
        self.current_idx = 0
        self.call_count = 0

    def get_current_key(self):
        return self.keys[self.current_idx]

    def rotate(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        log(f"-> Yangi API kalitiga o'tildi (Idx: {self.current_idx + 1}/{len(self.keys)})")

    def generate(self, prompt, max_retries=6):
        for attempt in range(max_retries):
            key = self.get_current_key()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.35,
                    "maxOutputTokens": 8192
                }
            }).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    self.call_count += 1
                    return text
            except urllib.error.HTTPError as e:
                log(f"[HTTP Xatolik {e.code}] Kalit: ...{key[-6:]} - {e.reason}")
                if e.code in (429, 403, 401, 503):
                    self.rotate()
                    time.sleep(4)
                else:
                    time.sleep(3)
            except Exception as e:
                log(f"[Tarmoq Xatolik] {e}")
                time.sleep(4)
        raise RuntimeError("Barcha API kalitlari bilan urinishlar tugadi.")

def get_existing_modules(lang_dir):
    """Mavjud modul raqamlarini aniqlaydi"""
    full_dir = os.path.join(KODLAR_DIR, lang_dir)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir, exist_ok=True)
        return set()
    
    existing = set()
    for fname in os.listdir(full_dir):
        if fname.endswith(".md") and "_" in fname:
            parts = fname.split("_")
            if len(parts) >= 2 and parts[1].isdigit():
                existing.add(int(parts[1]))
    return existing

def generate_subbatch(rotator, lang_name, topic, start_id, end_id):
    count = end_id - start_id + 1
    prompt = f"""Sen 'Khorazmiy AI' suveren sun'iy intellektining bosh dataset muhandisisan.
{lang_name} dasturlash tili bo'yicha 100 000 talik suveren milliy dataset uchun #{start_id} dan #{end_id} gacha bo'lgan ({count} ta) yangi topshiriq va yechimlarni yarat.

Mavzu: {topic}

Har bir topshiriq formati aynan quyidagicha bo'lsin:
### Topshiriq #{start_id}: [Aniq va professional nom]
**Tavsif:** Muammo va real ishlab chiqarishdagi zarurati.
**Talablar:** Algoritmik murakkablik va xavfsizlik shartlari.
**Yechim ({lang_name}):**
```{lang_name.lower()}
// To'liq, ishlab turgan, o'zbekcha izohlar bilan yozilgan professional kod
```
**Tushuntirish:** Nima uchun ushbu yondashuv tanlangani, optimizatsiya siri.

Faqat #{start_id} dan #{end_id} gacha bo'lgan topshiriqlarni sifatli va to'liq yoz. Boshqa kirish yoki xulosa so'zlar yozma."""

    return rotator.generate(prompt)

def get_topic_for_module(module_num):
    if module_num in MODULE_TOPICS:
        return MODULE_TOPICS[module_num]
    # 51-moduldan 100-modulgacha bo'lgan chuqurlashtirilgan mavzular
    cat_idx = module_num % 10
    categories = [
        "Ilg'or Kiberxavfsizlik va Kriptografik Himoya",
        "High-Performance Tarmoq Dasturlash va Protobuf",
        "Taqsimlangan Ma'lumotlar Bazalari va Sharding",
        "Enterprise Mikroservislar va Domain Events",
        "Low-Latency Algoritmlar va Kesh Optimizatsiyasi",
        "Katta Hajmli Vektorli Qidiruv va AI Pipeline",
        "Operatsion Tizimlar va Bare-Metal Interfeyslar",
        "Reaktiv Oqimlar va Event-Driven Arxitektura",
        "Asinxron Konkurentlik va Xotira Boshqaruvi",
        "Khorazmiy Grand Master Muhandislik Loyihasi"
    ]
    name = categories[cat_idx]
    slug = f"ilgori_mavzu_{module_num}"
    return (f"{name} (Modul {module_num})", slug)

def run_continuous_expansion(target_module=100):
    keys, model_name = load_keys()
    rotator = KeyRotator(keys, model_name)
    log(f"==================================================")
    log(f"Khorazmiy AI: 100 000 talik Avtomatik Kengaytirish Dvigateli Ishga Tushdi!")
    log(f"Model: {model_name} | Faol kalitlar soni: {len(keys)}")
    log(f"==================================================")

    for module_num in range(22, target_module + 1):
        topic_title, topic_slug = get_topic_for_module(module_num)
        start_id = (module_num - 1) * 50 + 1
        end_id = module_num * 50

        log(f"\n>>> [MODUL {module_num}/{target_module}] Boshlandi: {topic_title} (#{start_id}-#{end_id})")

        for lang in LANGUAGES:
            lang_dir = lang["dir"]
            lang_name = lang["name"]
            existing = get_existing_modules(lang_dir)

            if module_num in existing:
                continue

            file_name = f"{lang_dir}_{module_num:02d}_{topic_slug}.md"
            target_path = os.path.join(KODLAR_DIR, lang_dir, file_name)

            log(f"--- Generatsiya qilinmoqda: {lang_name} ({file_name}) ---")
            collected = []
            
            # 50 ta topshiriqni 5 ta 10 talik sub-batch qilib olish
            for sub_start in range(start_id, end_id + 1, 10):
                sub_end = sub_start + 9
                log(f" -> [{lang_name}] #{sub_start}-#{sub_end} yuklanmoqda...")
                part_text = generate_subbatch(rotator, lang_name, topic_title, sub_start, sub_end)
                collected.append(part_text)
                time.sleep(1.5)

            full_content = f"# Khorazmiy AI: {lang_name} - Modul {module_num:02d}\n"
            full_content += f"## Mavzu: {topic_title}\n\n"
            full_content += "\n\n---\n\n".join(collected)

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(full_content)

            file_size = os.path.getsize(target_path)
            log(f" [OK] {file_name} saqlandi! ({file_size} bayt)")

            # Jami progressni hisoblash
            total_tasks_now = 0
            for l in LANGUAGES:
                mods = get_existing_modules(l["dir"])
                total_tasks_now += len(mods) * 50
            
            pct = (total_tasks_now / 100000) * 100
            log(f"[PROGRESS] [PROGRESS] Jami topshiriqlar: {total_tasks_now:,} / 100,000 ({pct:.2f}%)")

    log("[G'ALABA] TABRIKLAYMIZ! Barcha 20 ta til bo'yicha 100 000 talik dataset to'liq zabt etildi!")

if __name__ == "__main__":
    run_continuous_expansion(target_module=100)
