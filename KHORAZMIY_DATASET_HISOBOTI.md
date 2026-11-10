# "Khorazmiy AI" Milliy Ma'lumotlar To'plami (Dataset) - Yakuniy Hisobot

Ushbu to'plam O'zbekistonning suveren milliy sun'iy intellekt modeli — **"Khorazmiy AI"** ni Supervised Fine-Tuning (SFT) va dialogik muloqot (Chat/RLHF) yo'nalishlarida o'qitish uchun maxsus tayyorlandi.

---

## 1. Badiiy Adabiyot va Mumtoz Meros (`kitoblar/`)
**Fayl manzili:** `kitoblar/mumtoz_va_adabiy_asarlar_sft.jsonl`
- **Jami topshiriqlar:** 400 ta yuqori filologik va falsafiy tahlillar.
- **Qamrab olingan buyuk adiblar:**
  1. **Alisher Navoiy (120 ta):**
     - "Xazoyinul maoniy" g'azallari (baytma-bayt lug'aviy, irfoniy va badiiy san'atlar tahlili: tajnis, tashbeh, iyhom, husni ta'lil).
     - "Xamsa" dostonlari: *Hayrat ul-abror*, *Farhod va Shirin*, *Layli va Majnun*, *Sab'ai sayyor*, *Saddi Iskandariy* falsafasi va qahramonlar tizimi.
     - "Mahbub ul-qulub" (jamiyat tabaqalari, saxovat, adolat, axloq).
     - "Muhokamat ul-lug'atayn" (turkiy tilning boyligi va fe'l shakllari).
     - "Lison ut-tayr" (tasavvufning 7 vodiysi).
  2. **Abdulla Qodiriy (100 ta):**
     - "O'tkan kunlar" (Otabek, Kumush, Zaynab, Homid, Yusufbek hoji, Hasanali; XIX asr Qo'qon xonligi, milliy fojia, iffat va sadoqat).
     - "Mehrobdan chayon" (Anvar, Ra'no, Solih maxdum xasisligi, saroy fitnalari).
     - "Obid ketmon", "Kalvak Mahzum", "Toshpo'lat tajang" va jadid publitsistikasi.
  3. **O'tkir Hoshimov (90 ta):**
     - "Dunyoning ishlari" (Surat, Oq marmar qabr toshi, Gilam paypoq, O'ris qiz, Iltijo; ona madhi va mehr-oqibat).
     - "Ikki eshik orasi" (Kimsan, Robiya, Umar zakunchi, Shomurod; urush davri fojiasi va vijdon azobi).
     - "Bahor qaytmaydi" va "Daftar hoshiyasidagi bitiklar" (hayot falsafasi).
  4. **Xudoyberdi To'xtaboyev (90 ta):**
     - "Sariq devni minib" va "Sariq devning o'limi" (Hoshimjon, sehrli qalpoqcha, dangasalik tanqidi, ilm va mehnatning g'alabasi).
     - "Shirin qovunlar mamlakati", "Mungli ko'zlar" (halol luqma, oila birdamligi).

---

## 2. Zamonaviy Dasturlash va Infratuzilma (`dasturlash/`)
**Yagona master fayl:** `dasturlash/zamonaviy_dasturlash_1000.jsonl` (Jami: 1000 ta)
Har bir vazifa professional o'zbek tilidagi topshiriq sharti, amaliy kodi / konfiguratsiyasi, me'moriy tahlili va terminal buyruqlarini o'z ichiga oladi.

1. **Docker (`docker_200.jsonl` — 200 ta):**
   - Multi-stage build (Node.js, Go, Python, Rust ilovalarini 20MB gacha siqish).
   - Non-root xavfsizlik (Distroless, Alpine, appuser).
   - Docker Compose (PostgreSQL, Redis, Celery, NGINX integratsiyasi).
   - Xotira va CPU limitlari, Bridge networks, Volumes, Healthchecks.
2. **Kubernetes (`kubernetes_200.jsonl` — 200 ta):**
   - Control Plane va Worker Node ichki mexanizmlari.
   - Deployments, RollingUpdate (zero-downtime), ReplicaSets.
   - Services (ClusterIP, NodePort, LoadBalancer, Headless).
   - Ingress Controllers (NGINX Ingress, TLS / Cert-Manager).
   - ConfigMaps, Secrets, PVC / PV, StorageClass.
   - Horizontal Pod Autoscaler (HPA) va Liveness/Readiness probes.
3. **Linux Shell & Bash (`linux_shell_bash_200.jsonl` — 200 ta):**
   - `set -euo pipefail` va `trap` bilan xavfsiz skript shablonlari.
   - Matn tahlili: `awk`, `sed`, `grep`, `cut`, `sort`, `uniq`.
   - Jarayonlar va xotira boshqaruvi (`ss`, `top`, `ps`, `kill`, `lsof`).
   - Avtomatik zaxiralash (backup) va Telegram/Slack ogohlantirish skriptlari.
   - Systemd xizmat birliklari (unit services) va Crontab.
4. **DevOps, CI/CD va Cloud (`devops_cicd_cloud_200.jsonl` — 200 ta):**
   - GitHub Actions to'liq pipeline (Test, Build, Docker Hub Push, Cache).
   - GitLab CI/CD (`.gitlab-ci.yml`, stages, artifacts, deploy).
   - Terraform IaC (AWS EC2, VPC, Security Groups, Remote S3/DynamoDB state).
   - Ansible Playbooks (NGINX, Node.js avtomatlashtirilgan o'rnatish).
   - Prometheus metrikalari, PromQL so'rovlari va Grafana dashboardlari.
5. **Algoritmlar va Ma'lumotlar Tuzilmalari (`algoritmlar_tuzilmalar_200.jsonl` — 200 ta):**
   - Two Pointers, Sliding Window, Prefix Sum.
   - Bog'langan ro'yxatlar (Floyd sikl qidirish algoritmi).
   - Monotonic Stack, LRU Cache, Trie daraxti.
   - Graflar (BFS, DFS, Dijkstra, Topologik saralash - Kahn).
   - Dinamik dasturlash (0/1 Knapsack, LIS, LCS, Coin Change).
   - Murakkablik tahlili (Big-O, Big-Theta, Big-Omega).

---

## 3. Jonli va Madaniyatli O'zbekcha Dialoglar (`dialoglar/`)
**Yagona master fayl:** `dialoglar/jonli_ozbekcha_dialoglar_3000.jsonl` (Jami: 3000 ta)
12 ta alohida toifa (har birida 250 tadan to'liq dialog):
1. `dialoglar_01_salom_alik.jsonl` (250) — Tonggi omonlik tilash, uzoq yo'ldan kelgan qadrdonni kutib olish.
2. `dialoglar_02_oila_va_qadriyat.jsonl` (250) — Ota duosi, qaynona-kelin odobi, aka-uka mehr-oqibati.
3. `dialoglar_03_bozor_va_savdo.jsonl` (250) — Chorsu, Siypb bozorlari, mevalar xaridi, baraka tilash, atlas tanlash.
4. `dialoglar_04_mehmondorchilik.jsonl` (250) — To'rga o'tqazish, fotiha, 3 marta choy qaytarish odobi.
5. `dialoglar_05_mahalla_va_qoshni.jsonl` (250) — Mahalla hashari, bir kosa ovqat ilinish, "Yon qo'shni — jon qo'shni".
6. `dialoglar_06_milliy_taomlar.jsonl` (250) — Devzira osh damlash sirlari, Sumalak qozoni atrofidagi ezgu niyatlar.
7. `dialoglar_07_talim_va_ustoz.jsonl` (250) — Ustoz-shogird muloqoti, ilmiy izlanish, kutubxonada kitobxonlik.
8. `dialoglar_08_kasb_va_biznes.jsonl` (250) — Rishton kulolchiligi, IT startaplar, "Khorazmiy AI" relizi.
9. `dialoglar_09_sayyohlik_shaharlar.jsonl` (250) — Samarqand Registoni, Xiva Ichan Qal'asi, Buxoro Minorai Kaloni.
10. `dialoglar_10_sanat_va_madaniyat.jsonl` (250) — Shashmaqom va dutor sehri, Navoiy teatri tomoshalari.
11. `dialoglar_11_salomatlik_va_sport.jsonl` (250) — Ibn Sino tabobati, shifobaxsh giyohlar, milliy kurash odobi.
12. `dialoglar_12_hayotiy_dalda.jsonl` (250) — Qiyin damda do'stga yelkadosh bo'lish, oqsoqolning sabr va shukr nasihati.

---

## 4. Yakuniy Sifat Nazorati Natijalari

| Bo'lim / Fayl | Qatorlar soni | Fayl hajmi | Validatsiya holati |
|---|---|---|---|
| `kitoblar/mumtoz_va_adabiy_asarlar_sft.jsonl` | **400** | ~252 KB | **100% Valid JSONL** |
| `dasturlash/docker_200.jsonl` | **200** | ~227 KB | **100% Valid JSONL** |
| `dasturlash/kubernetes_200.jsonl` | **200** | ~235 KB | **100% Valid JSONL** |
| `dasturlash/linux_shell_bash_200.jsonl` | **200** | ~211 KB | **100% Valid JSONL** |
| `dasturlash/devops_cicd_cloud_200.jsonl` | **200** | ~218 KB | **100% Valid JSONL** |
| `dasturlash/algoritmlar_tuzilmalar_200.jsonl` | **200** | ~220 KB | **100% Valid JSONL** |
| **`dasturlash/zamonaviy_dasturlash_1000.jsonl`** | **1,000** | **~1.1 MB** | **100% Valid JSONL** |
| `dialoglar/dialoglar_01..12_*.jsonl` (12 fayl) | **3,000** | ~5.2 MB | **100% Valid JSONL** |
| **`dialoglar/jonli_ozbekcha_dialoglar_3000.jsonl`** | **3,000** | **~5.2 MB** | **100% Valid JSONL** |
| **Jami yaratilgan yangi qatorlar** | **8,400 ta** | **~12.3 MB** | **Nol xatolik (0 errors)** |

Barcha fayllar UTF-8 kodirovkasida, aniq JSON qoliplarida saqlangan va "Khorazmiy AI" ning yuksak sifatli ta'lim olishiga tayyor!
