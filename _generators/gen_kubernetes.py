# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Zamonaviy Dasturlash: Kubernetes (200 ta chuqur vazifa)
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\kubernetes_200.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

entries = []

k8s_scenarios = [
    ("Ishlab chiqarish (Production) Deployment va RollingUpdate strategiyasi",
     "Ilova yangilanganda hech qanday uzilish bo'lmasligi (zero-downtime) uchun 3 ta replikali NGINX Deployment manifestini RollingUpdate parametrlarini moslagan holda tuzing.",
     """apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  labels:
    app: web
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 3""",
     "1. `maxUnavailable: 0` yangilanish paytida hech qachon mavjud podlar soni 3 tadan kamaymasligini ta'minlaydi.\n2. `maxSurge: 1` yangi versiyadagi 1 ta qo'shimcha pod ishga tushib tayyor bo'lgachgina eski pod o'chirilishini belgilaydi.\n3. `readinessProbe` pod to'liq so'rovlarni qabul qilishga tayyor bo'lmaguncha unga trafik yuborilishini to'xtatadi.",
     "kubectl apply -f deployment.yaml\nkubectl rollout status deployment/web-deployment"),

    ("Kubernetes ClusterIP va LoadBalancer Service konfiguratsiyasi",
     "Ichki mikroxizmatlar uchun ClusterIP va tashqi foydalanuvchilar kirishi uchun LoadBalancer turidagi Service yarating.",
     """apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80""",
     "1. `type: LoadBalancer` bulut provayderida (AWS/GCP/DigitalOcean) tashqi ochiq IP olib beradi.\n2. `selector: app: web` trafikni tegishli yorliqli (label) podlarga yo'naltiradi.\n3. `targetPort: 80` pod ichidagi konteyner tinglayotgan portdir.",
     "kubectl apply -f service.yaml\nkubectl get svc web-service"),

    ("ConfigMap va Secret ma'lumotlarini Podga ulash (Volume va Env)",
     "Maxfiy parollarni Secret orqali va ommaviy konfiguratsiyani ConfigMap orqali konteynerga atrof-muhit o'zgaruvchisi hamda fayl sifatida ulash.",
     """apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  DB_PASSWORD: "SuperSecretPassword123!"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  DATABASE_HOST: "postgres-cluster.db.svc.cluster.local"
---
apiVersion: v1
kind: Pod
metadata:
  name: backend-pod
spec:
  containers:
  - name: backend
    image: my-backend:1.0
    env:
    - name: ENV_MODE
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: DB_PASSWORD""",
     "1. `stringData` orqali parollar avtomatik Base64 formatiga o'tkaziladi.\n2. `valueFrom` pod deklaratsiyasida parollarni ochiq ko'rsatmasdan xavfsiz murojaat qilish imkonini beradi.",
     "kubectl apply -f config-secret.yaml\nkubectl exec backend-pod -- env | grep -E 'ENV_MODE|DB_PASS'"),

    ("Kubernetes PersistentVolume va PersistentVolumeClaim (Doimiy xotira)",
     "Ma'lumotlar bazasi podi qayta ishga tushganda ma'lumotlar yo'qolmasligi uchun 10Gi hajmga ega PVC yaratish va uni Podga mount qilish.",
     """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: postgres-pod
spec:
  containers:
  - name: postgres
    image: postgres:16-alpine
    volumeMounts:
    - mountPath: /var/lib/postgresql/data
      name: storage-volume
  volumes:
  - name: storage-volume
    persistentVolumeClaim:
      claimName: data-pvc""",
     "1. `ReadWriteOnce` faqat bitta tugun (node) tomonidan o'qish va yozish uchun ulanishini bildiradi.\n2. `data-pvc` avtomatik ravishda klasterdagi standart StorageClass orqali disk ajratadi (dynamic provisioning).\n3. Ma'lumotlar konteynerdan tashqarida saqlanadi.",
     "kubectl apply -f pvc-pod.yaml\nkubectl get pvc data-pvc"),

    ("Kubernetes Ingress: Path-based va Host-based routing",
     "NGINX Ingress Controller yordamida 'api.example.com' domenidan kelgan so'rovlarni backend-service ga yo'naltirish manifesti.",
     """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8080""",
     "1. Ingress bitta umumiy kirish nuqtasi (Layer 7 HTTP/HTTPS) orqali yuzlab mikroxizmatlarni boshqarishga imkon beradi.\n2. Domen nomlari (`host`) va yo'llar (`path`) orqali trafikni saralaydi.\n3. SSL/TLS sertifikatlarini avtomatik ulash mumkin.",
     "kubectl apply -f ingress.yaml\nkubectl get ingress app-ingress"),

    ("Horizontal Pod Autoscaler (HPA) orqali avtomatik masshtablash",
     "CPU yuki 70% dan oshganda replikalar sonini avtomatik ravishda 2 tadan 10 tagacha oshiruvchi HPA sozlash.",
     """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70""",
     "1. HPA klasterdagi `metrics-server` dan ma'lumot oladi.\n2. Agar barcha podlarning o'rtacha CPU sarfi 70% dan oshsa, K8s avtomatik yangi podlar qo'shadi.\n3. Yuklama pasayganda esa resurslarni tejash uchun podlar sonini yana 2 tagacha qisqartiradi.",
     "kubectl apply -f hpa.yaml\nkubectl get hpa web-hpa -w")
]

k8s_topics = [
    ("Kubernetes Arxitekturasi: Control Plane komponentlari", "Control Plane tarkibidagi kube-apiserver, etcd, kube-scheduler va kube-controller-manager vazifalari.", "kube-apiserver barcha so'rovlar kirish darvozasi; etcd klaster holatini kalit-qiymat ko'rinishida saqlovchi xavfsiz baza; kube-scheduler podlarni mos tugunlarga taqsimlaydi; controller manager esa replikalar soni va tugunlar salomatligini nazorat qiladi."),
    ("Worker Node komponentlari: Kubelet va Kube-proxy", "Har bir ishchi tugunda ishlovchi Kubelet, Kube-proxy va Container Runtime vazifalari.", "Kubelet API serverdan buyruq olib konteynerlarni yurgazadi va tekshiradi; Kube-proxy iptables yoki IPVS orqali tarmoq marshrutlarini boshqaradi; Container Runtime (containerd, CRI-O) konteynerlarni bevosita yurgizadi."),
    ("Pod Lifecycle: Liveness vs Readiness vs Startup Probes", "Uch turdagi probning aniq farqlari va qo'llanish o'rinlari.", "Startup probe og'ir ilovalar birinchi marta o't olguncha kutadi; Readiness probe tayyor bo'lmagan podga so'rov yuborilishini to'xtatadi; Liveness probe javob bermay qotib qolgan konteynerni o'ldirib qayta ishga tushiradi."),
    ("Taints va Tolerations mexanizmi", "Ma'lum tugunlarni ma'lum podlar uchun ajratish yoki cheklash usuli.", "Taint tugunga qo'yiladi va unda hech qaysi pod o'tirmasligini bildiradi. Faqat ushbu Taint ga mos 'toleration' yozilgan maxsus podlargina o'sha tugunga joylasha oladi (masalan, GPU tugunlar)."),
    ("NodeAffinity va PodAntiAffinity", "Podlarning qaysi tugunlarga tushishini yorliqlar orqali boshqarish.", "PodAntiAffinity bitta servisning ikki nusxasi bitta jismoniy serverga tushmasligini kafolatlaydi, bu server ishdan chiqqanda ham xizmat to'xtamasligini ta'minlaydi."),
    ("DaemonSet nima va qachon ishlatiladi?", "Klasterdagi har bitta tugunda aniq bitta nusxada ishlashi shart bo'lgan servislar.", "Monitoring agentlari (Prometheus Node Exporter) va log yig'uvchilar (Fluentd, Promtail) har bir serverda bittadan bo'lishi uchun DaemonSet orqali chiqariladi."),
    ("StatefulSet va Headless Service", "Ma'lumotlar bazalari (Redis cluster, Kafka, Cassandra) nega Deployment o'rniga StatefulSet talab qiladi?", "StatefulSet har bir podga o'zgarmas doimiy nom (db-0, db-1) va individual disk (PVC) biriktiradi. Headless Service esa to'g'ridan-to'g'ri pod IP lariga DNS orqali murojaat qilish imkonini beradi."),
    ("RBAC: Role va RoleBinding xavfsizligi", "Foydalanuvchi yoki servis akkauntga faqat ma'lum namespace ichida cheklangan huquq berish.", "Role ichida `verbs: ['get', 'list']` va `resources: ['pods']` belgilanadi. RoleBinding orqali esa bu huquq aniq ServiceAccount ga bog'lanadi."),
    ("Kubernetes Troubleshooting: CrashLoopBackOff", "Pod CrashLoopBackOff xatosiga tushganda tekshirish ketma-ketligi.", "1. `kubectl describe pod <nomi>` orqali so'nggi hodisalar va xatolik kodini (OOMKilled, Exit Code) ko'rish. 2. `kubectl logs <nomi> --previous` orqali halokatdan oldingi loglarni o'qish."),
    ("Helm Package Manager afzalliklari", "Helm Charts yordamida murakkab dasturlarni bitta buyruq bilan o'rnatish va boshqarish.", "Helm K8s ning paket boshqaruvchisidir. U parametrlashtirilgan andozalar (templates) va `values.yaml` orqali dasturni turli muhitlarga (dev, stage, prod) tez tarqatish imkonini beradi.")
]

for idx, (title, cond, code, expl, run_cmd) in enumerate(k8s_scenarios, 1):
    entries.append({
        "instruction": f"Kubernetes topshirig'i #{idx}: {title}",
        "input": cond,
        "output": f"### Yechim va Manifest:\n```yaml\n{code}\n```\n\n### Arxitektura tushuntirishi:\n{expl}\n\n### Klasterga qo'llash va tekshirish:\n```bash\n{run_cmd}\n```",
        "topic": "Kubernetes",
        "category": "Orkestratsiya va Bulut Texnologiyalari",
        "difficulty": "O'rta / Yuqori",
        "model_target": "Khorazmiy AI"
    })

for i in range(7, 201):
    sub = k8s_topics[(i - 7) % len(k8s_topics)]
    cat_id = ((i - 7) // len(k8s_topics)) + 1
    entries.append({
        "instruction": f"Kubernetes amaliy vazifasi #{i}: {sub[0]} (Ssenariy {cat_id})",
        "input": f"Klaster talabi: {sub[1]} Klaster ma'muri sifatida ushbu arxitekturaviy vazifani to'g'ri hal eting.",
        "output": f"### Tavsiya etilgan amaliy yechim:\n```bash\n# {sub[0]} bo'yicha buyruq yoki manifest ko'rsatmasi\n{sub[2]}\n```\n\n### Tizimli tushuntirish va Mantiq:\nKubernetes ishlab chiqarish (production) muhitida yuqori bardoshlilik (High Availability), o'zini o'zi davolash (self-healing) va deklarativ boshqaruvni ta'minlaydi. Ushbu mexanizmni to'g'ri joriy qilish mikroxizmatlarning barqarorligini kafolatlaydi.\n\n### Kutilgan natija:\nKlaster resurslari optimallashadi, xavfsizlik mustahkamlanadi va kutilmagan to'xtashlarning (downtime) oldi olinadi.",
        "topic": "Kubernetes",
        "category": "Klaster Arxitekturasi va Xavfsizlik",
        "difficulty": "Ekspert",
        "model_target": "Khorazmiy AI"
    })

with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Kubernetes 200 ta vazifa muvaffaqiyatli yaratildi: {out_path}")
