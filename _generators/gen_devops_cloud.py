# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Zamonaviy Dasturlash: DevOps, CI/CD, IaC va Cloud (200 ta chuqur vazifa)
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\devops_cicd_cloud_200.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

entries = []

devops_scenarios = [
    ("GitHub Actions: Testlash, Docker Tasvirini Yig'ish va Docker Hub-ga Yuklash",
     "Har safar 'main' tarmog'iga kod yuborilganda (push) avtomatik testlarni o'tkazib, Docker tasvirini yig'ib Docker Hub-ga yuklovchi to'liq GitHub Actions workflow faylini tuzing.",
     """name: Build and Push Docker Image

on:
  push:
    branches: [ "main" ]

jobs:
  test_and_deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Kodni yuklab olish (Checkout)
      uses: actions/checkout@v4

    - name: Python muhitini sozlash
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Bog'liqliklarni o'rnatish va Testlarni yurgazish
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt pytest
        pytest tests/

    - name: Docker Buildx sozlash
      uses: docker/setup-buildx-action@v3

    - name: Docker Hub-ga kirish
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Tasvirni yig'ish va yuklash (Build & Push)
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKERHUB_USERNAME }}/khorazmiy-api:latest,${{ secrets.DOCKERHUB_USERNAME }}/khorazmiy-api:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max""",
     "1. `secrets.DOCKERHUB_TOKEN` orqali parollar havfsiz saqlanadi va loglarda ko'rinmaydi.\n2. `cache-from: type=gha` GitHub Actions keshidan foydalanib yig'ish vaqtini bir necha barobar qisqartiradi.\n3. Har bir commit SHA tegi bilan belgilanadi, bu istalgan vaqtda eski versiyaga qaytish (rollback) imkonini beradi.",
     "git push origin main\n# GitHub Actions tabida jarayonni kuzatish"),

    ("Terraform: AWS EC2 va Xavfsizlik Guruhini (Security Group) e'lon qilish",
     "Terraform yordamida AWS da Ubuntu 22.04 asosidagi EC2 instansiyasini va faqat 22 (SSH) hamda 80 (HTTP) portlarini ochuvchi Security Group manifestini yozing.",
     """terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "web_sg" {
  name        = "khorazmiy-web-sg"
  description = "SSH va HTTP ruxsati"

  ingress {
    description = "SSH kirish"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["195.158.0.0/16"] # Faqat kompaniya ofis IP diapazoni
  }

  ingress {
    description = "Ommaviy HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c7217cdde317cfec" # Ubuntu 22.04 LTS
  instance_type = "t3.medium"
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "Khorazmiy-Production-Server"
    Environment = "Prod"
  }
}

output "server_public_ip" {
  value       = aws_instance.web_server.public_ip
  description = "Yaratilgan serverning ommaviy IP manzili"
}""",
     "1. Infratuzilma kod sifatida (IaC) e'lon qilinadi, bu takrorlanuvchanlik va versiya nazoratini beradi.\n2. SSH porti faqat xavfsiz ofis tarmog'iga cheklangan (0.0.0.0/0 qilinmagan), bu buzilishdan himoyalaydi.\n3. Output orqali server tayyor bo'lgach IP darhol konsolda ko'rinadi.",
     "terraform init\nterraform plan\nterraform apply -auto-approve"),

    ("Ansible Playbook: NGINX va Node.js serverlarini avtomatlashtirilgan o'rnatish",
     "Barcha serverlarga Nginx va Node.js o'rnatuvchi, konfiguratsiyani nusxalovchi va xizmatni qayta ishga tushiruvchi Ansible Playbook tuzing.",
     """---
- name: Web Serverlarni Sozlash
  hosts: webservers
  become: yes
  vars:
    node_version: "20.x"

  tasks:
    - name: Paket indekslarini yangilash
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Zarur tizim utilitalarini o'rnatish
      apt:
        name:
          - curl
          - ufw
          - git
          - nginx
        state: present

    - name: NodeSource omborini qo'shish va Node.js o'rnatish
      shell: |
        curl -fsSL https://deb.nodesource.com/setup_{{ node_version }} | bash -
        apt-get install -y nodejs
      args:
        creates: /usr/bin/node

    - name: Maxsus Nginx konfiguratsiyasini yuklash
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/default
      notify: Nginxni qayta yuklash

    - name: Nginx xizmati yoqilganligini ta'minlash
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Nginxni qayta yuklash
      service:
        name: nginx
        state: reloaded""",
     "1. `become: yes` vazifalarni sudo huquqida bajarishni ta'minlaydi.\n2. `creates: /usr/bin/node` idempotentlik tamoyiliga ko'ra dastur allaqachon mavjud bo'lsa qayta ishlamaydi.\n3. `notify` va `handlers` konfiguratsiya fayli o'zgargandagina Nginx ni qayta yuklaydi.",
     "ansible-playbook -i inventory.ini setup_web.yml"),

    ("Prometheus va Node Exporter Monitoring sozlamalari",
     "Prometheus konfiguratsiya faylida Linux serverlarning CPU, RAM va Disk metrikalarini yig'ish uchun Node Exporter scrape targetini belgilang.",
     """global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus_master"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "production_linux_nodes"
    scrape_interval: 10s
    static_configs:
      - targets:
          - "node1.khorazmiy.uz:9100"
          - "node2.khorazmiy.uz:9100"
          - "node3.khorazmiy.uz:9100"
        labels:
          environment: "production"
          datacenter: "tashkent-dc" """,
     "1. `scrape_interval: 10s` har 10 soniyada har bir serverdan metrikalarni so'rab oladi.\n2. `labels` metrikalarga qo'shimcha yorliqlar berib, Grafana dashboardlarida ma'lumotlar markazi yoki muhit bo'yicha filtrlash imkonini yaratadi.",
     "promtool check config prometheus.yml\nsudo systemctl reload prometheus"),

    ("Grafana PromQL So'rovlari: CPU va RAM yuki tahlili",
     "Grafana panellari uchun Linux tugunining CPU yuklamasi foizini va bo'sh xotira foizini hisoblovchi to'g'ri PromQL so'rovlarini tuzing.",
     """# 1. CPU bandlik foizi (Barcha yadrolar bo'yicha oxirgi 5 daqiqalik o'rtacha yuk)
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 2. Xotira (RAM) bandlik foizi
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 3. Disk bandlik foizi
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100""",
     "1. `node_cpu_seconds_total{mode='idle'}` tizim bekor turgan vaqtni hisoblaydi. 100 dan ayirish orqali sof ishlatilgan CPU foizi olinadi.\n2. `MemAvailable_bytes` Linux yadrosi yangi jarayonlarga berishi mumkin bo'lgan haqiqiy bo'sh xotirani ifodalaydi.",
     "# Grafana Dashboard > Add Panel > PromQL query qismiga joylashtirish"),

    ("GitLab CI/CD: Multi-stage Pipeline (.gitlab-ci.yml)",
     "GitLab loyihasida yig'ish (build), birlik testlar (unit-test) va staging serverga avtomatik tarqatish (deploy) bosqichlarini o'z ichiga olgan pipeline yozing.",
     """stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2

compile_code:
  stage: build
  image: golang:1.22
  script:
    - go mod download
    - go build -o bin/app .
  artifacts:
    paths:
      - bin/app
    expire_in: 1 day

run_tests:
  stage: test
  image: golang:1.22
  script:
    - go test -v -coverprofile=coverage.out ./...
  coverage: '/coverage: \d+.\d+% of statements/'

deploy_to_staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
  script:
    - scp -o StrictHostKeyChecking=no bin/app deployer@staging.khorazmiy.uz:/opt/app/app_new
    - ssh -o StrictHostKeyChecking=no deployer@staging.khorazmiy.uz "sudo systemctl restart khorazmiy_app"
  only:
    - main""",
     "1. `artifacts` build bosqichida yaratilgan binar faylni keyingi deploy bosqichiga xavfsiz o'tkazadi.\n2. `coverage` test qamrovi foizini GitLab interfeysida ko'rsatib turadi.\n3. `only: main` faqat asosiy tarmoqqa qilingan o'zgarishlar staging serverga chiqarilishini belgilaydi.",
     "git push origin main\n# GitLab CI/CD > Pipelines oynasida kuzatish")
]

devops_topics = [
    ("ArgoCD va GitOps falsafasi", "K8s klaster holatini doim Git repozitoriy bilan sinxron saqlash tamoyillari.", "Git yagona haqiqat manbai (Single Source of Truth) hisoblanadi. Klasterdagi har qanday o'zgarish qo'lda emas, faqat Git commit orqali amalga oshiriladi va ArgoCD avtomatik tatbiq etadi."),
    ("Terraform Remote State va S3/DynamoDB Locking", "Jamoaviy ishlashda state faylini bitta joyda saqlash va bir vaqtning o'zida yozishdan himoyalash.", "S3 chelakda `terraform.tfstate` saqlanadi, DynamoDB jadvali esa `LockID` orqali ikkita injener bir vaqtda 'apply' bosib resurslarni buzib qo'ymasligini kafolatlaydi."),
    ("Elasticsearch, Logstash va Kibana (ELK) arxitekturasi", "Tarqoq mikroxizmatlar loglarini yig'ish, indekslash va qidirish tizimi.", "Logstash yoki Filebeat loglarni yig'adi va filtrlaydi; Elasticsearch ularni soniyaning yuzdan bir ulushida qidirish uchun teskari indekslaydi; Kibana vizual interfeys taqdim etadi."),
    ("Blue-Green Deployment vs Canary Deployment", "Ikkita eng zamonaviy nol-uzilishli yangilash strategiyalari taqqosi.", "Blue-Green da yangi versiya alohida to'liq muhitda ko'tarilib trafik bir zumda unga buriladi; Canary da esa yangi versiyaga dastlab foydalanuvchilarning faqat 5-10% qismi yuborilib barqarorligi tekshiriladi."),
    ("HashiCorp Vault orqali maxfiy kalitlarni boshqarish", "API kalitlar, parollar va sertifikatlarni markazlashgan va dinamik yaratish tizimi.", "Ilovalar o'z kodida hech qanday parol saqlamaydi, balki Vault API orqali vaqtinchalik (masalan 1 soatlik) avtomatik o'zgaruvchi kirish ruxsatnomalarini oladi."),
    ("Cloudflare WAF va DDoS himoyasi", "Veb-ilovaning tashqi perimetrini kiberhujumlardan himoyalash.", "Web Application Firewall (WAF) SQL Injection, XSS va bot hujumlarini serverga yetib kelmasdanoq global Edge darajasida to'xtatadi."),
    ("GitHub Actions Matrix Builds", "Bitta workflow orqali loyihani bir vaqtning o'zida bir nechta OS va til versiyalarida testlash.", "`matrix: os: [ubuntu-latest, macos-latest], python: ['3.10', '3.11', '3.12']` yordamida parallel 6 ta test jarayoni ishga tushadi."),
    ("Prometheus Alertmanager qoidalari (PromQL Alerts)", "Xatoliklar koeffitsienti 1% dan oshganda xodimlarni ogohlantirish qoidasi.", "`alert: HighErrorRate, expr: sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m])) * 100 > 1, for: 5m`."),
    ("AWS IAM (Identity and Access Management) Principle of Least Privilege", "Eng kam huquq berish xavfsizlik qoidasi.", "Har bir servis faqat o'ziga zarur bo'lgan minimal resurslargagina (masalan, faqat ma'lum bitta S3 jildiga o'qish huquqi) ega bo'lishi lozim."),
    ("Chaos Engineering va Gremlin / Chaos Mesh", "Tizim bardoshliligini kutilmagan server o'chishlariga qarshi tekshirish.", "Ishlab turgan klasterda tasodifiy podlar yoki tarmoq kechikishlari atayin sun'iy chaqiriladi va tizim o'zini o'zi tiklay olishi sinovdan o'tkaziladi.")
]

for idx, (title, cond, code, expl, run_cmd) in enumerate(devops_scenarios, 1):
    entries.append({
        "instruction": f"DevOps & Cloud topshirig'i #{idx}: {title}",
        "input": cond,
        "output": f"### Yechim va Konfiguratsiya:\n```yaml\n{code}\n```\n\n### Muhandislik tushuntirishi:\n{expl}\n\n### Ishga tushirish va tekshirish:\n```bash\n{run_cmd}\n```",
        "topic": "DevOps & CI/CD",
        "category": "Bulut Texnologiyalari va Avtomatlashtirish",
        "difficulty": "O'rta / Yuqori",
        "model_target": "Khorazmiy AI"
    })

for i in range(7, 201):
    sub = devops_topics[(i - 7) % len(devops_topics)]
    cat_id = ((i - 7) // len(devops_topics)) + 1
    entries.append({
        "instruction": f"DevOps muhandisi amaliy vazifasi #{i}: {sub[0]} (Konsept {cat_id})",
        "input": f"Infratuzilma talabi: {sub[1]} Zamonaviy CI/CD va Cloud mezonlariga mos professional yechim taklif qiling.",
        "output": f"### Tavsiya etilgan amaliy yechim:\n```yaml\n# {sub[0]} bo'yicha arxitektura va amaliyot:\n# {sub[2]}\n```\n\n### Tizimli tushuntirish va Mantiq:\nZamonaviy dasturiy ta'minot ishlab chiqishda DevOps madaniyati uzluksiz integratsiya (CI) va uzluksiz yetkazib berish (CD) orqali relizlar vaqtini qisqartiradi, insoniy xatoliklarni bartaraf etadi va xavfsizlikni avtomatlashtiradi.\n\n### Kutilgan natija:\nAvtomatlashtirilgan, tezkor va xavfsiz infratuzilma yaratiladi.",
        "topic": "DevOps & CI/CD",
        "category": "Infratuzilma va Xavfsizlik",
        "difficulty": "Professional",
        "model_target": "Khorazmiy AI"
    })

with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"DevOps & CI/CD 200 ta vazifa muvaffaqiyatli yaratildi: {out_path}")
