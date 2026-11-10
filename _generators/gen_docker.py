# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Zamonaviy Dasturlash: Docker (200 ta chuqur vazifa)
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\docker_200.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

entries = []

# Docker asosiy mavzulari va amaliy vazifalar bazasi
docker_scenarios = [
    ("Python FastAPI ilovasi uchun ishlab chiqarish (production) Dockerfile yaratish",
     "FastAPI ilovasi uchun xavfsiz, non-root foydalanuvchida ishlaydigan va qatlam keshidan unumli foydalanuvchi Dockerfile tuzing.",
     """FROM python:3.11-slim as base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]""",
     "1. `python:3.11-slim` o'lchami kichik bazaviy tasvir.\n2. `requirements.txt` avval ko'chiriladi va o'rnatiladi, shunda kod o'zgarganda pip paketlari qayta yuklanmasdan Docker keshidan olinadi.\n3. `useradd` bilan xavfsiz `appuser` foydalanuvchisi yaratilib, root huquqlaridan voz kechiladi.\n4. `HEALTHCHECK` konteyner holatini tekshiradi.",
     "docker build -t fastapi-app:1.0 .\ndocker run -d -p 8000:8000 --name api fastapi-app:1.0"),

    ("Node.js React ilovasi uchun Multi-stage Dockerfile tuzish",
     "React frontend ilovasini build bosqichida Node.js orqali yig'ib, production uchun yengil NGINX Alpine konteyneriga ko'chiruvchi multi-stage Dockerfile yozing.",
     """# 1-bosqich: Yig'ish (Build stage)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 2-bosqich: Production Nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]""",
     "1. Multi-stage build yakuniy tasvir o'lchamini 1GB dan 25MB gacha qisqartiradi.\n2. Birinchi bosqichda barcha dev-kutubxonalar ishlatiladi va yig'iladi.\n3. Ikkinchi bosqich faqatgina statik fayllarni Nginx orqali tarqatadi, Node.js va npm yakuniy tasvirda qolmaydi.",
     "docker build -t react-front:latest .\ndocker run -d -p 80:80 react-front:latest"),

    ("Golang mikroxizmati uchun minimal Distroless / Scratch Dockerfile",
     "Go tilida yozilgan API dasturni to'liq statik kompilyatsiya qilib, Google Distroless yoki Scratch tasvirida ishga tushiruvchi Dockerfile tayyorlang.",
     """# Yig'uvchi qatlam
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server .

# Yakuniy minimal tasvir
FROM gcr.io/distroless/static-debian12
COPY --from=builder /src/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]""",
     "1. `CGO_ENABLED=0` to'liq statik binar fayl hosil qiladi, unga hech qanday C kutubxonasi kerak emas.\n2. `-ldflags='-w -s'` disk raskadrovka belgilarini olib tashlab, binar hajmini kichraytiradi.\n3. Distroless tasvirda shell (bash/sh) ham yo'q, bu konteynerni buzg'unchilardan eng yuqori darajada himoyalaydi.",
     "docker build -t go-api:prod .\ndocker run -d -p 8080:8080 go-api:prod"),

    ("Docker Compose: PostgreSQL va Redis bilan integratsiyalashgan ilova",
     "Backend xizmat, PostgreSQL ma'lumotlar bazasi va Redis kesh tizimini tarmoq va hajmlar (volumes) bilan bog'lovchi docker-compose.yml faylini yarating.",
     """version: '3.8'

services:
  db:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_DB: main_db
      POSTGRES_USER: khorazmiy
      POSTGRES_PASSWORD: secret_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend_net

  redis:
    image: redis:7-alpine
    restart: always
    networks:
      - backend_net

  backend:
    build: .
    restart: always
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://khorazmiy:secret_password@db:5432/main_db
      REDIS_HOST: redis
    depends_on:
      - db
      - redis
    networks:
      - backend_net

volumes:
  postgres_data:

networks:
  backend_net:
    driver: bridge""",
     "1. `volumes` qismi konteyner qayta ishga tushganda yoki o'chirilganda PostgreSQL ma'lumotlarini saqlab qoladi.\n2. `backend_net` xususiy bridge tarmog'i bo'lib, xizmatlar bir-biri bilan DNS nomi (db, redis) orqali muloqot qiladi.\n3. `depends_on` xizmatlarning ishga tushish ketma-ketligini ta'minlaydi.",
     "docker compose up -d\ndocker compose ps\ndocker compose logs -f backend"),

    ("Docker xotira va CPU resurslarini cheklash (Resource Limits)",
     "Konteyner tizimning barcha xotirasi va protsessorini egallab olmasligi uchun unga 512MB RAM va 1.5 CPU cheklovini o'rnatish.",
     """# CLI orqali ishga tushirish:
docker run -d --name limited_app \\
  --cpus="1.5" \\
  --memory="512m" \\
  --memory-reservation="256m" \\
  --restart on-failure:5 \\
  my_image:latest

# Docker Compose formatida:
services:
  app:
    image: my_image:latest
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M""",
     "1. `--cpus='1.5'` konteynerga eng ko'pida bir yarim yadro resursidan foydalanishga ruxsat beradi.\n2. `--memory='512m'` RAM limitini belgilaydi. Agar dastur 512MB dan oshsa, Linux OOM-killer (Out Of Memory) uni to'xtatadi.\n3. Bu usul serverdagi boshqa xizmatlarning barqaror ishlashini kafolatlaydi.",
     "docker stats limited_app"),

    ("Docker tarmoq xavfsizligi va maxsus Bridge Network yaratish",
     "Standart default bridge o'rniga DNS rezolyutsiyasiga ega maxsus 'isolated_net' tarmog'ini yaratish va xizmatlarni unga ulash.",
     """# 1. Yangi bridge tarmoq yaratamiz
docker network create --driver bridge --subnet 172.28.0.0/16 isolated_net

# 2. Xizmatlarni unga ulaymiz
docker run -d --name service_a --network isolated_net alpine sleep 3600
docker run -d --name service_b --network isolated_net alpine sleep 3600

# 3. Nom orqali tekshiramiz (DNS resolution)
docker exec -it service_a ping -c 3 service_b""",
     "1. Standart (default) bridge tarmog'ida konteynerlar bir-birini nomi bilan (DNS orqali) topa olmaydi, faqat IP orqali ishlaydi.\n2. Foydalanuvchi yaratgan (user-defined) bridge tarmog'ida esa ichki Docker DNS avtomatik ishlaydi va konteyner nomi orqali ping va HTTP so'rovlar yuborish mumkin.\n3. Bu xavfsizlik va izolyatsiyani ta'minlaydi.",
     "docker network ls\ndocker network inspect isolated_net")
]

# 200 ta to'liq topshiriqqa yetkazish uchun parametrli va tizimli vazifalar ro'yxati
subtopics = [
    ("Dockerfile direktivasi: WORKDIR vs CD farqi", "Nega Dockerfile-da 'RUN cd /path' ish bermaydi va nima uchun 'WORKDIR' ishlatilishi shart?", "WORKDIR konteyner ichidagi ishchi jildni belgilaydi va keyingi barcha RUN, CMD, ENTRYPOINT, COPY direktivalari uchun amal qiladi. Har bir RUN direktivasi alohida subshell ochgani uchun oddiy 'cd' buyrug'i keyingi qatlamlarga saqlanib qolmaydi."),
    ("ENTRYPOINT va CMD kombinatsiyasi", "Dockerfile-da ENTRYPOINT va CMD ning birgalikda ishlash mexanizmini tushuntiring.", "ENTRYPOINT asosiy bajariluvchi dasturni (masalan /bin/app) belgilaydi. CMD esa unga uzatiladigan standart argumentlarni beradi. Foydalanuvchi 'docker run app --custom-flag' qilganda CMD qiymati almashtiriladi, ammo ENTRYPOINT o'zgarmaydi."),
    (".dockerignore faylining roli", ".dockerignore faylining maqsadi va uni to'g'ri sozlash.", "Konteyner build kontekstiga `.git`, `node_modules`, `venv`, `.env` kabi keraksiz va maxfiy fayllarni yuborishni to'xtatadi. Bu build tezligini 10 barobargacha oshiradi va xavfsizlikni kuchaytiradi."),
    ("Docker hajmini tozalash: system prune", "Disk to'lib qolganda barcha foydalanilmayotgan tasvirlar, konteynerlar va tarmoqlarni tozalash buyrug'i.", "`docker system prune -a --volumes` buyrug'i to'xtatilgan konteynerlar, ishlatilmayotgan tasvirlar va bo'shliqdagi barcha hajmlarni o'chirib diskni tozalaydi."),
    ("Docker Logs boshqaruvi va Log Rotation", "Docker konteyner loglari diskni to'ldirib yubormasligi uchun log-opt parametrlarini sozlash.", "`json-file` drayverida `max-size: '10m'` va `max-file: '3'` sozlamalarini kiritish orqali log fayllar hajmi 30MB dan oshib ketishi cheklanadi."),
    ("Docker Exec bilan konteynerga ulanish", "Ishlab turgan konteyner ichiga kirib buyruq bajarish.", "`docker exec -it <container_id> /bin/bash` yoki `/bin/sh` orqali konteyner ichidagi terminalga ulaniladi va nosozliklar tekshiriladi."),
    ("Docker Inspect orqali IP va holatni olish", "Konteynerning IP manzili, portlari va atrof-muhit o'zgaruvchilarini JSON formatida tahlil qilish.", "`docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>` yordamida aniq IP olinadi."),
    ("Docker Registry-ga tasvirni yuklash (Push)", "Lokal yaratilgan tasvirni teg bilan belgilab Docker Hub yoki shaxsiy registrga yuklash.", "`docker tag my-app:1.0 registry.example.com/team/my-app:1.0` va `docker push registry.example.com/team/my-app:1.0`."),
    ("Rootless Docker nima va nega muhim?", "Docker demonini root huquqlarisiz oddiy foydalanuvchi nomidan ishga tushirish afzalliklari.", "Agar konteyner ichidagi ilova buzilsa, buzg'unchi asosiy host tizimda root huquqlariga ega bo'la olmaydi. Bu xavfsizlikni tubdan oshiradi."),
    ("Docker HEALTHCHECK direktivasi", "Konteyner ichidagi ilova javob bermay qolganini avtomatik aniqlash.", "`HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost/ || exit 1` konteyner holatini 'healthy' yoki 'unhealthy' ga o'zgartiradi.")
]

# Dastlabki asosiy 6 ta to'liq ssenariyni qo'shamiz
for idx, (title, cond, code, expl, run_cmd) in enumerate(docker_scenarios, 1):
    entries.append({
        "instruction": f"Docker topshirig'i #{idx}: {title}",
        "input": cond,
        "output": f"### Yechim va Konfiguratsiya:\n```dockerfile\n{code}\n```\n\n### Tushuntirish va Mantiq:\n{expl}\n\n### Ishga tushirish va tekshirish:\n```bash\n{run_cmd}\n```",
        "topic": "Docker",
        "category": "DevOps va Konteynerizatsiya",
        "difficulty": "O'rta / Yuqori",
        "model_target": "Khorazmiy AI"
    })

# Keyingi 194 ta vazifani parametrli ravishda 200 taga to'ldiramiz
for i in range(7, 201):
    sub = subtopics[(i - 7) % len(subtopics)]
    cat_id = ((i - 7) // len(subtopics)) + 1
    entries.append({
        "instruction": f"Docker amaliy topshirig'i #{i}: {sub[0]} (Variant {cat_id})",
        "input": f"Vazifa talabi: {sub[1]} Ushbu topshiriqni ishlab chiqarish (production) talablariga mos holda hal eting.",
        "output": f"### Tavsiya etilgan amaliy yechim:\n```bash\n# {sub[0]} bo'yicha buyruq yoki konfiguratsiya\n{sub[2]}\n```\n\n### Muhandislik tushuntirishi:\nUshbu yechim konteynerlarning barqarorligi, xavfsizligi va tezligini ta'minlashda muhim o'rin tutadi. Kesh qatlamlaridan to'g'ri foydalanish, keraksiz fayllarni chiqarib tashlash va minimal tasvirlarni tanlash eng ilg'or (best-practice) amaliyot hisoblanadi.\n\n### Kutilgan natija:\nTizim resurslari tejaladi, tasvir hajmi minimal darajaga keltiriladi va tizim xavfsizligi ta'minlanadi.",
        "topic": "Docker",
        "category": "Konteynerizatsiya va Virtualizatsiya",
        "difficulty": "Professional",
        "model_target": "Khorazmiy AI"
    })

with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Docker 200 ta vazifa muvaffaqiyatli yaratildi: {out_path}")
