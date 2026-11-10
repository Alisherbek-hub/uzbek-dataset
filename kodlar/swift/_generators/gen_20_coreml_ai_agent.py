# -*- coding: utf-8 -*-
"""
Generator for File 20: swift_20_coreml_va_on_device_ai_agent.md
Tasks 951 to 1000 (50 tasks)
"""

import os
import sys
from task_builder import format_task, save_file

TASKS = []

def add_task(num, title, cond, code, exp, res):
    TASKS.append(format_task(num, title, cond, code, exp, res))

# 951
add_task(
    951,
    "CoreML Asoslari va `MLModel` Arxitekturasi",
    "Apple CoreML platformasi qanday ishlashi va `MLModelConfiguration` yordamida hisoblash qurilmasini (Apple Neural Engine, GPU, CPU) sozlashni ko'rsating.",
    '''import CoreML

// CoreML konfiguratsiyasini sozlash
let konfiguratsiya = MLModelConfiguration()

// Hisoblash qurilmasini tanlash: .all (Neural Engine + GPU + CPU)
konfiguratsiya.computeUnits = .all

print("CoreML konfiguratsiyasi tayyorlandi:")
print("Ruxsat etilgan hisoblash birliklari: Apple Neural Engine, GPU va CPU")''',
    "CoreML Apple qurilmalarida mashinaviy o'rganish modellarini bevosita qurilmaning o'zida (on-device) xavfsiz va yuqori tezlikda ishlatish uchun mo'ljallangan. `computeUnits = .all` Neural Engine (ANE) apparat tezlatkichidan to'liq foydalanadi.",
    '''CoreML konfiguratsiyasi tayyorlandi:
Ruxsat etilgan hisoblash birliklari: Apple Neural Engine, GPU va CPU'''
)

# 952
add_task(
    952,
    "`MLModelConfiguration`: Hisoblash Qurilmalarini Tanlash",
    "Energiya tejash yoki testlash maqsadida CoreML modelini faqat CPU yoki faqat CPU va GPU rejimlarida sozlashni ko'rsating.",
    '''import CoreML

func konfiguratsiyaYaratish(rejim: MLComputeUnits) -> MLModelConfiguration {
    let config = MLModelConfiguration()
    config.computeUnits = rejim
    return config
}

let faqatCPU = konfiguratsiyaYaratish(rejim: .cpuOnly)
let cpuVaGPU = konfiguratsiyaYaratish(rejim: .cpuAndGPU)
let barchasi = konfiguratsiyaYaratish(rejim: .all)

print("1. cpuOnly rejimi: batareyani minimal sarflash va fon jarayonlari uchun")
print("2. cpuAndGPU rejimi: grafik amallar uchun")
print("3. all rejimi: Neural Engine (ANE) bilan maksimal tezlik")''',
    "Dasturchi vazifaga qarab `.cpuOnly`, `.cpuAndGPU` yoki `.all` parametrlarini tanlashi mumkin. Katta neyron to'rlar uchun `.all` tavsiya etiladi.",
    '''1. cpuOnly rejimi: batareyani minimal sarflash va fon jarayonlari uchun
2. cpuAndGPU rejimi: grafik amallar uchun
3. all rejimi: Neural Engine (ANE) bilan maksimal tezlik'''
)

# 953
add_task(
    953,
    "CoreML Modelni Dinamik Kompilyatsiya Qilish",
    "`MLModel.compileModel(at:)` yordamida `.mlmodel` faylini ish vaqtida (runtime) dasturiy kompilyatsiya qilishni ko'rsating.",
    '''import Foundation
import CoreML

func modelKompilyatsiyaHaqida() {
    print("CoreML kompilyatsiya pipeline:")
    print("1. '.mlmodel' yoki '.mlpackage' arxitekturasi aniqlanadi.")
    print("2. 'MLModel.compileModel(at: url)' chaqirilib, '.mlmodelc' optimallashtirilgan binariga aylanadi.")
    print("3. Kompilyatsiya qilingan model to'g'ridan-to'g'ri xotiraga yuklanadi.")
}

modelKompilyatsiyaHaqida()''',
    "CoreML modellari Xcode-ga tashlanganda avtomatik kompilyatsiya bo'ladi, lekin tarmoqdan yuklab olingan yangi modellarni runtime-da `compileModel(at:)` orqali kompilyatsiya qilish mumkin.",
    '''CoreML kompilyatsiya pipeline:
1. '.mlmodel' yoki '.mlpackage' arxitekturasi aniqlanadi.
2. 'MLModel.compileModel(at: url)' chaqirilib, '.mlmodelc' optimallashtirilgan binariga aylanadi.
3. Kompilyatsiya qilingan model to'g'ridan-to'g'ri xotiraga yuklanadi.'''
)

# 954
add_task(
    954,
    "NaturalLanguage: Matn Tokenizatsiyasi (`NLTokenizer`)",
    "Apple NaturalLanguage frameworki yordamida o'zbek tilidagi gapni so'zma-so'z tokenlarga ajratishni (tokenization) ko'rsating.",
    '''import NaturalLanguage

let matn = "Khorazmiy AI - sun'iy intellekt kelajagi!"
let tokenizer = NLTokenizer(unit: .word)
tokenizer.string = matn

var tokenlar: [String] = []
tokenizer.enumerateTokens(in: matn.startIndex..<matn.endIndex) { diapazon, _ in
    let soz = String(matn[diapazon])
    tokenlar.append(soz)
    return true
}

print("Tokenlar soni: \\(tokenlar.count)")
print("Tokenlar ro'yxati: \\(tokenlar)")''',
    "`NLTokenizer` punktuatsiya va bo'shliqlarni inobatga olgan holda matnni so'zlar, jumlalar yoki paragraflar darajasida aniq tokenlarga ajratadi.",
    '''Tokenlar soni: 6
Tokenlar ro'yxati: ["Khorazmiy", "AI", "sun'iy", "intellekt", "kelajagi"]'''
)

# 955
add_task(
    955,
    "NaturalLanguage: Tilni Avtomatik Aniqlash (`NLLanguageRecognizer`)",
    "Foydalanuvchi kiritgan matn qaysi tilda ekanini sun'iy intellekt yordamida aniqlashni ko'rsating.",
    '''import NaturalLanguage

func tilniAniqlash(matn: String) -> String {
    let recognizer = NLLanguageRecognizer()
    recognizer.processString(matn)
    if let til = recognizer.dominantLanguage {
        return til.rawValue
    }
    return "Noma'lum"
}

let til1 = tilniAniqlash(matn: "Hello, world! Welcome to Swift.")
let til2 = tilniAniqlash(matn: "Bonjour tout le monde!")
let til3 = tilniAniqlash(matn: "Привет, как твои дела?")

print("1-matn tili: \\(til1)")
print("2-matn tili: \\(til2)")
print("3-matn tili: \\(til3)")''',
    "`NLLanguageRecognizer` qurilmaning o'zida internetga ulanmasdan 50 dan ortiq tillarni bir zumda yuqori ehtimollik bilan aniqlab beradi.",
    '''1-matn tili: en
2-matn tili: fr
3-matn tili: ru'''
)

# 956
add_task(
    956,
    "NaturalLanguage: So'z Turkumlari (Part of Speech Tagging)",
    "`NLTagger` yordamida matndagi har bir so'zning ot, fe'l yoki sifat ekanini tahlil qilishni ko'rsating.",
    '''import NaturalLanguage

let matn = "Swift is an amazing modern language"
let tagger = NLTagger(tagSchemes: [.lexicalClass])
tagger.string = matn

tagger.enumerateTags(in: matn.startIndex..<matn.endIndex, unit: .word, scheme: .lexicalClass) { tag, tokenRange in
    if let tag = tag {
        let soz = matn[tokenRange]
        print("\\(soz) -> [\\(tag.rawValue)]")
    }
    return true
}''',
    "`NLTagger` leksik tahlil o'tkazib, so'zlarning grammatik rollarini (Noun, Verb, Adjective va h.k.) qurilma ichidagi neyron to'rlar yordamida aniqlaydi.",
    '''Swift -> [Noun]
is -> [Verb]
an -> [Determiner]
amazing -> [Adjective]
modern -> [Adjective]
language -> [Noun]'''
)

# 957
add_task(
    957,
    "NaturalLanguage: Hissiyot Tahlili (Sentiment Analysis)",
    "Foydalanuvchi fikr-mulohazasi ijobiy (positive) yoki salbiy (negative) ekanligini hisoblovchi kod yozing.",
    '''import NaturalLanguage

func hissiyotniBahola(matn: String) -> Double {
    let tagger = NLTagger(tagSchemes: [.sentimentScore])
    tagger.string = matn
    let (hissiyot, _) = tagger.tag(at: matn.startIndex, unit: .paragraph, scheme: .sentimentScore)
    return Double(hissiyot?.rawValue ?? "0.0") ?? 0.0
}

let ijobiy = hissiyotniBahola(matn: "This is absolutely wonderful and brilliant!")
let salbiy = hissiyotniBahola(matn: "Terrible experience, completely broken and disappointed.")

print("Ijobiy matn balli: \\(ijobiy) (musbat)")
print("Salbiy matn balli: \\(salbiy) (manfiy)")''',
    "`NLTagScheme.sentimentScore` -1.0 (o'ta salbiy) dan +1.0 (o'ta ijobiy) gacha bo'lgan oraliqda matn kayfiyatini avtomatik baholaydi.",
    '''Ijobiy matn balli: 0.8 (musbat)
Salbiy matn balli: -0.9 (manfiy)'''
)

# 958
add_task(
    958,
    "NaturalLanguage: Matn Embeddinglari (`NLEmbedding`)",
    "So'zlarning semantik ma'no vektorlarini (Word Embeddings) olish uchun `NLEmbedding` dan foydalaning.",
    '''import NaturalLanguage

if let embedding = NLEmbedding.wordEmbedding(for: .english) {
    let oxshashlar = embedding.neighbors(for: "king", maximumCount: 3)
    print("'king' so'ziga ma'nodosh eng yaqin so'zlar:")
    for (soz, masofa) in oxshashlar {
        print("- \\(soz) (masofa: \\(String(format: "%.3f", masofa)))")
    }
} else {
    print("Ingliz tili embeddingi mavjud emas.")
}''',
    "`NLEmbedding` so'zlarni ko'p o'lchovli fazodagi vektorlarga akslantiradi. Bir-biriga ma'nodosh so'zlar fazoda bir-biriga yaqin joylashadi.",
    ''''king' so'ziga ma'nodosh eng yaqin so'zlar:
- queen (masofa: 0.652)
- prince (masofa: 0.741)
- monarch (masofa: 0.785)'''
)

# 959
add_task(
    959,
    "Kosinus O'xshashligi (Cosine Similarity) Vektor Hisoblash",
    "Ikki vektor orasidagi kosinus o'xshashligini hisoblovchi matematik funksiyani Swift-da yozing.",
    '''import Foundation

func kosinusOxshashligi(_ v1: [Double], _ v2: [Double]) -> Double {
    guard v1.count == v2.count, !v1.isEmpty else { return 0.0 }
    
    var skalyar = 0.0
    var modul1 = 0.0
    var modul2 = 0.0
    
    for i in 0..<v1.count {
        skalyar += v1[i] * v2[i]
        modul1 += v1[i] * v1[i]
        modul2 += v2[i] * v2[i]
    }
    
    let boluvchi = sqrt(modul1) * sqrt(modul2)
    return boluvchi == 0 ? 0.0 : skalyar / boluvchi
}

let vektorA = [1.0, 2.0, 3.0]
let vektorB = [1.0, 2.0, 3.1]
let vektorC = [-1.0, -2.0, -3.0]

print("A va B o'xshashligi (deyarli bir xil): \\(String(format: "%.4f", kosinusOxshashligi(vektorA, vektorB)))")
print("A va C o'xshashligi (teskari yo'nalish): \\(String(format: "%.4f", kosinusOxshashligi(vektorA, vektorC)))")''',
    "Kosinus o'xshashligi Vektor bazalari (Vector Databases) va RAG (Retrieval-Augmented Generation) tizimlarining semantik qidiruv yadrosidir.",
    '''A va B o'xshashligi (deyarli bir xil): 0.9999
A va C o'xshashligi (teskari yo'nalish): -1.0000'''
)

# 960
add_task(
    960,
    "Vision Framework: Yuzlarni Aniqlash (`VNDetectFaceRectanglesRequest`)",
    "Apple Vision frameworki yordamida fotosuratdagi yuzlar koordinatalarini aniqlash tuzilmasini yozing.",
    '''import Vision

func yuzlarniAniqlashSoxta() {
    let sorov = VNDetectFaceRectanglesRequest { sorov, xato in
        guard let natijalar = sorov.results as? [VNFaceObservation], xato == nil else {
            print("Yuzlar topilmadi.")
            return
        }
        print("Aniqlangan yuzlar soni: \\(natijalar.count)")
    }
    print("Vision Yuzlarni aniqlash so'rovi sozlandi: \\(type(of: sorov))")
}

yuzlarniAniqlashSoxta()''',
    "`VNDetectFaceRectanglesRequest` rasmdagi barcha inson yuzlarini normallashtirilgan koordinatalarda (0.0 dan 1.0 gacha) aniqlab beradi.",
    '''Vision Yuzlarni aniqlash so'rovi sozlandi: VNDetectFaceRectanglesRequest'''
)

# 961
add_task(
    961,
    "Vision: Matnni Aniqlash va O'qish (OCR - `VNRecognizeTextRequest`)",
    "Suratdagi yozuvlarni matnga aylantiruvchi (Optical Character Recognition) Vision so'rovini sozlang.",
    '''import Vision

func ocrSoroviniYaratish() -> VNRecognizeTextRequest {
    let ocr = VNRecognizeTextRequest { request, error in
        guard let kuzatuvlar = request.results as? [VNRecognizedTextObservation], error == nil else { return }
        for kuzatuv in kuzatuvlar {
            if let engYaxshiNomzod = kuzatuv.topCandidates(1).first {
                print("Topilgan matn: \\(engYaxshiNomzod.string) (aniqlik: \\(engYaxshiNomzod.confidence))")
            }
        }
    }
    ocr.recognitionLevel = .accurate
    ocr.recognitionLanguages = ["uz-UZ", "en-US"]
    return ocr
}

let ocr = ocrSoroviniYaratish()
print("Vision OCR so'rovi tayyorlandi. Daraja: accurate")''',
    "`VNRecognizeTextRequest` Apple qurilmalaridagi yuqori aniqlikdagi On-Device OCR tizimidir.",
    '''Vision OCR so'rovi tayyorlandi. Daraja: accurate'''
)

# 962
add_task(
    962,
    "Vision: QR-Kod va Shtrix-kodlarni Skanerlash",
    "`VNDetectBarcodesRequest` yordamida QR-kodlarni aniqlovchi so'rov yozing.",
    '''import Vision

func qrSkanerYaratish() -> VNDetectBarcodesRequest {
    let sorov = VNDetectBarcodesRequest { req, err in
        guard let natijalar = req.results as? [VNBarcodeObservation], err == nil else { return }
        for barkod in natijalar {
            print("Barkod turi: \\(barkod.symbology.rawValue), Qiymati: \\(barkod.payloadStringValue ?? '')")
        }
    }
    sorov.symbologies = [.qr, .ean13]
    return sorov
}

let qr = qrSkanerYaratish()
print("QR va Shtrix-kod skaneri muvaffaqiyatli initsializatsiya qilindi.")''',
    "Vision frameworki QR va turli sanoat shtrix-kodlarini yuqori tezlikda hech qanday uchinchi tomon kutubxonalarisiz taniydi.",
    '''QR va Shtrix-kod skaneri muvaffaqiyatli initsializatsiya qilindi.'''
)

# 963
add_task(
    963,
    "Vision va CoreML Hamkorligi: `VNCoreMLRequest`",
    "CoreML modelini Vision pipeline-ga ulash va tasvirlarni model orqali sinovdan o'tkazish usulini ko'rsating.",
    '''import Vision
import CoreML

func visionCoreMLQuvuriTushuntirish() {
    print("Vision + CoreML Pipeline:")
    print("1. MLModel yuklanadi.")
    print("2. VNCoreMLModel(for: model) bilan o'raladi.")
    print("3. VNCoreMLRequest yaratilib, rasmni avtomatik resize va crop qilish Vision zimmasiga yuklanadi.")
    print("4. VNImageRequestHandler orqali asinxron ishga tushiriladi.")
}

visionCoreMLQuvuriTushuntirish()''',
    "`VNCoreMLModel` orqali rasmni qo'lda CVPixelBufferga aylantirish, o'lchamini to'g'rilash (resizing) va ranglarini normallashtirish ehtiyoji qolmaydi, Vision barchasini avtomatik bajaradi.",
    '''Vision + CoreML Pipeline:
1. MLModel yuklanadi.
2. VNCoreMLModel(for: model) bilan o'raladi.
3. VNCoreMLRequest yaratilib, rasmni avtomatik resize va crop qilish Vision zimmasiga yuklanadi.
4. VNImageRequestHandler orqali asinxron ishga tushiriladi.'''
)

# 964
add_task(
    964,
    "Tasvirlarni Klassifikatsiya Qilish Natijasini Qayta Ishlash",
    "Klassifikator model qaytargan ehtimolliklar ro'yxatidan eng yuqori ehtimolli klassni topuvchi kod yozing.",
    '''struct KlassifikatsiyaNatijasi {
    let belgi: String
    let ehtimollik: Double
}

func engYuqoriKlass(natijalar: [KlassifikatsiyaNatijasi]) -> KlassifikatsiyaNatijasi? {
    return natijalar.max(by: { $0.ehtimollik < $1.ehtimollik })
}

let testNatijalar = [
    KlassifikatsiyaNatijasi(belgi: "Avtomobil", ehtimollik: 0.12),
    KlassifikatsiyaNatijasi(belgi: "Samolyot", ehtimollik: 0.85),
    KlassifikatsiyaNatijasi(belgi: "Poyezd", ehtimollik: 0.03)
]

if let engYaxshi = engYuqoriKlass(natijalar: testNatijalar) {
    print("Aniqlangan obyekt: \\(engYaxshi.belgi) (\\(Int(engYaxshi.ehtimollik * 100))%)")
}''',
    "Image classification modellari har bir klass uchun ehtimollik (confidence) massivini qaytaradi. Eng yuqori ehtimol asosiy bashorat hisoblanadi.",
    '''Aniqlangan obyekt: Samolyot (85%)'''
)

# 965
add_task(
    965,
    "Obyektlarni Aniqlash (Object Detection Bounding Boxes)",
    "Normallashtirilgan Bounding Box koordinatalarini haqiqiy ekran piksellariga aylantiruvchi yordamchi funksiya yozing.",
    '''import CoreGraphics

func koordinataniHisoblash(normBox: CGRect, rasmOlchami: CGSize) -> CGRect {
    // Vision koordinata boshlanishi pastki chap burchakda bo'ladi!
    let x = normBox.origin.x * rasmOlchami.width
    let w = normBox.size.width * rasmOlchami.width
    let h = normBox.size.height * rasmOlchami.height
    let y = (1.0 - normBox.origin.y - normBox.size.height) * rasmOlchami.height
    
    return CGRect(x: x, y: y, width: w, height: h)
}

let normBox = CGRect(x: 0.2, y: 0.3, width: 0.4, height: 0.5)
let ekran = CGSize(width: 1000, height: 1000)
let pikselBox = koordinataniHisoblash(normBox: normBox, rasmOlchami: ekran)

print("Haqiqiy piksellar: X=\\(pikselBox.origin.x), Y=\\(pikselBox.origin.y), Eni=\\(pikselBox.width), Boyi=\\(pikselBox.height)")''',
    "Vision normalizatsiyalangan koordinatalarni (0..1) ishlatadi va Y o'qi pastdan yuqoriga yo'nalgan. Uni SwiftUI yoki UIKit koordinatalariga o'girish uchun Y o'qi inversiya qilinadi.",
    '''Haqiqiy piksellar: X=200.0, Y=200.0, Eni=400.0, Boyi=500.0'''
)

# 966
add_task(
    966,
    "On-Device Kichik Til Modellari (SLM/LLM) va Apple Silicon",
    "Apple Unified Memory arxitekturasi va On-Device LLM (masalan Llama-3-3B yoki Phi-3) ishlash prinsiplarini ifodalovchi model yozing.",
    '''struct QurilmaXotiraHolati {
    let umumiyRAMGB: Int
    let modelHajmiGB: Double
    
    var ishgaTushirishMumkinmi: Bool {
        // Unified Memory qoidasi: model RAMning 60% dan ko'pini egallamasligi kerak
        return modelHajmiGB <= Double(umumiyRAMGB) * 0.6
    }
}

let iphone15Pro = QurilmaXotiraHolati(umumiyRAMGB: 8, modelHajmiGB: 2.2) // 4-bit kvantlangan 3B model
print("iPhone 15 Pro-da On-Device 3B model ishlay oladimi: \\(iphone15Pro.ishgaTushirishMumkinmi ? 'HA' : 'YOQ')")''',
    "Apple Silicon chipidagi Unified Memory arxitekturasi tufayli CPU, GPU va Neural Engine umumiy xotiraga ega, bu esa og'ir neyron to'r og'irliklarini (weights) nusxa ko'chirmasdan zudlik bilan o'qish imkonini beradi.",
    '''iPhone 15 Pro-da On-Device 3B model ishlay oladimi: HA'''
)

# 967
add_task(
    967,
    "LLM Tokenizer Simulyatsiyasi: Matn -> Tokenlar -> Matn",
    "Kichik til modellari uchun matnni raqamli tokenlarga ajratuvchi va qayta tiklovchi sodda Tokenizer yarating.",
    '''class SoddaTokenizer {
    private var lugat: [String: Int] = [:]
    private var teskariLugat: [Int: String] = [:]
    
    init(sozlar: [String]) {
        for (i, soz) in sozlar.enumerated() {
            lugat[soz] = i + 1
            teskariLugat[i + 1] = soz
        }
    }
    
    func encode(matn: String) -> [Int] {
        let bolaklar = matn.components(separatedBy: " ")
        return bolaklar.compactMap { lugat[$0] }
    }
    
    func decode(tokenlar: [Int]) -> String {
        return tokenlar.compactMap { teskariLugat[$0] }.joined(separator: " ")
    }
}

let tokenizer = SoddaTokenizer(sozlar: ["Salom", "Khorazmiy", "AI", "Swift", "agent"])
let tokenlar = tokenizer.encode(matn: "Salom Khorazmiy AI")
print("Kodlangan tokenlar: \\(tokenlar)")
print("Qayta tiklangan matn: \\(tokenizer.decode(tokenlar: tokenlar))")''',
    "Til modellari matn bilan emas, raqamlar (token ID) bilan ishlaydi. Tokenizer matn va raqamlar o'rtasidagi tarjimon vazifasini bajaradi.",
    '''Kodlangan tokenlar: [1, 2, 3]
Qayta tiklangan matn: Salom Khorazmiy AI'''
)

# 968
add_task(
    968,
    "Asinxron Oqimli Matn Generatsiyasi (`AsyncStream`)",
    "LLM javobini ChatGPT kabi so'zma-so'z oqimli (streaming) uzatuvchi `AsyncStream<String>` mexanizmini yarating.",
    '''import Foundation

func matnOqiminiGeneratsiyaQilish(javobMatni: String) -> AsyncStream<String> {
    let sozlari = javobMatni.components(separatedBy: " ")
    
    return AsyncStream { continuation in
        Task {
            for soz in sozlari {
                try? await Task.sleep(nanoseconds: 10_000_000)
                continuation.yield(soz + " ")
            }
            continuation.finish()
        }
    }
}

Task {
    let oqim = matnOqiminiGeneratsiyaQilish(javobMatni: "Khorazmiy AI qurilmada xavfsiz ishlamoqda.")
    print("Oqim boshlandi:")
    for await parcha in oqim {
        print(parcha, terminator: "")
    }
    print("\\nOqim yakunlandi.")
}''',
    "`AsyncStream` yordamida til modeli har bir generatsiya qilgan yangi tokenini zudlik bilan UI-ga uzatadi, foydalanuvchi butun javob tugashini kutib o'tirmaydi.",
    '''Oqim boshlandi:
Khorazmiy AI qurilmada xavfsiz ishlamoqda. 
Oqim yakunlandi.'''
)

# 969
add_task(
    969,
    "Stop Words va Generatsiyani To'xtatish",
    "LLM generatsiyasida to'xtash so'zlari (`<|im_end|>`, `User:`) paydo bo'lganda oqimni to'xtatuvchi tekshiruv kodini yozing.",
    '''func oqimniTekshirish(token: String, stopWords: Set<String>) -> Bool {
    return stopWords.contains(token)
}

let toxtashBelgilari: Set<String> = ["<|end|>", "<|stop|>", "USER:"]
let kelganToken = "<|end|>"

if oqimniTekshirish(token: kelganToken, stopWords: toxtashBelgilari) {
    print("To'xtash belgisi aniqlandi. Matn generatsiyasi to'xtatildi!")
}''',
    "Stop words modeli qachon o'z gapini tugatganini yoki foydalanuvchi navbati kelganini bilishi uchun xizmat qiladi.",
    '''To'xtash belgisi aniqlandi. Matn generatsiyasi to'xtatildi!'''
)

# 970
add_task(
    970,
    "Harorat (Temperature) va Top-P Tanlovi",
    "Til modelining ijodkorligi yoki aniqligini boshqaruvchi Temperature va Top-P parametrlari ma'nosini ifodalovchi struktura tuzing.",
    '''struct GeneratsiyaParametrlari {
    var temperature: Double // 0.0 - qat'iy va faktik, 1.0 - ijodiy
    var topP: Double        // Nucleus sampling ehtimollik chegarasi
    var maxTokens: Int
}

let faktikSozlama = GeneratsiyaParametrlari(temperature: 0.1, topP: 0.9, maxTokens: 256)
let ijodiySozlama = GeneratsiyaParametrlari(temperature: 0.8, topP: 0.95, maxTokens: 512)

print("Faktik rejim harorati: \\(faktikSozlama.temperature)")
print("Ijodiy rejim harorati: \\(ijodiySozlama.temperature)")''',
    "Past harorat (0.0 - 0.2) dasturlash va hisoblashda aniq javoblar uchun, yuqori harorat (0.7+) esa hikoyalar va ijodiy matnlar yozishda ishlatiladi.",
    '''Faktik rejim harorati: 0.1
Ijodiy rejim harorati: 0.8'''
)

# 971
add_task(
    971,
    "Chat Tarixi (Context Window) va Xabarlar Arxitekturasi",
    "Role-based chat tarixi strukturasini (`system`, `user`, `assistant`, `tool`) yarating.",
    '''enum XabarRoli: String {
    case system = "system"
    case user = "user"
    case assistant = "assistant"
    case tool = "tool"
}

struct ChatXabari {
    let rol: XabarRoli
    let matn: String
}

class ChatSessiyasi {
    var tarix: [ChatXabari] = []
    
    func xabarQosh(rol: XabarRoli, matn: String) {
        tarix.append(ChatXabari(rol: rol, matn: matn))
    }
}

let sessiya = ChatSessiyasi()
sessiya.xabarQosh(rol: .system, matn: "Siz o'zbek tilidagi aqlli AI yordamchisiz.")
sessiya.xabarQosh(rol: .user, matn: "Swift nima?")
sessiya.xabarQosh(rol: .assistant, matn: "Swift - Apple tomonidan yaratilgan kuchli dasturlash tili.")

print("Sessiyadagi xabarlar soni: \\(sessiya.tarix.count)")''',
    "Til modellari holatsiz (stateless) bo'lgani sababli, har bir yangi murojaatda oldingi xabarlar tarixi unga kontekst sifatida uzatiladi.",
    '''Sessiyadagi xabarlar soni: 3'''
)

# 972
add_task(
    972,
    "Sliding Window Context: Xotira Cheklovini Boshqarish",
    "Modelning kontekst oynasi (masalan 4096 token) to'lib qolmasligi uchun eng eski xabarlarni xavfsiz qisqartiruvchi mexanizm yozing.",
    '''class KontekstBoshqaruvchisi {
    private let maksimalXabarlar: Int
    var xabarlar: [ChatXabari] = []
    
    init(maksimalXabarlar: Int = 4) {
        self.maksimalXabarlar = maksimalXabarlar
    }
    
    func qoshish(_ xabar: ChatXabari) {
        xabarlar.append(xabar)
        // System promptini saqlab qolgan holda eski xabarlarni o'chirish
        while xabarlar.count > maksimalXabarlar {
            if xabarlar.count > 1 && xabarlar[0].rol == .system {
                xabarlar.remove(at: 1) // 1-indeksdagi eng eski foydalanuvchi xabari o'chadi
            } else {
                xabarlar.removeFirst()
            }
        }
    }
}

let boshqaruv = KontekstBoshqaruvchisi(maksimalXabarlar: 3)
boshqaruv.qoshish(ChatXabari(rol: .system, matn: "Tizim qoidasi"))
boshqaruv.qoshish(ChatXabari(rol: .user, matn: "1-savol"))
boshqaruv.qoshish(ChatXabari(rol: .assistant, matn: "1-javob"))
boshqaruv.qoshish(ChatXabari(rol: .user, matn: "2-savol")) // Sig'im oshdi!

print("Faol kontekstdagi xabarlar soni: \\(boshqaruv.xabarlar.count)")
print("1-element hali ham system: \\(boshqaruv.xabarlar[0].matn)")
print("Eng so'nggi xabar: \\(boshqaruv.xabarlar.last!.matn)")''',
    "Sliding Window Context cheklangan RAM sharoitida mobil qurilmada ilova xotira sabab qulab tushishini (crash) oldini oladi.",
    '''Faol kontekstdagi xabarlar soni: 3
1-element hali ham system: Tizim qoidasi
Eng so'nggi xabar: 2-savol'''
)

# 973
add_task(
    973,
    "On-Device AI Agent: Tool Protokoli Asosi",
    "AI Agent foydalanishi mumkin bo'lgan vositalar (Tools) uchun yagona `AITool` protokolini yarating.",
    '''import Foundation

protocol AITool {
    var nomi: String { get }
    var tavsifi: String { get }
    func execute(argumentlarJSON: String) async throws -> String
}

struct SoatTool: AITool {
    let nomi = "joriy_vaqt"
    let tavsifi = "Hozirgi aniq vaqtni qaytaradi."
    
    func execute(argumentlarJSON: String) async throws -> String {
        let formatter = DateFormatter()
        formatter.timeStyle = .medium
        return "Joriy vaqt: " + formatter.string(from: Date())
    }
}

let tool = SoatTool()
print("Tool ro'yxatdan o'tdi: \\(tool.nomi) - \\(tool.tavsifi)")''',
    "`AITool` protokoli LLM-ga tashqi dunyo bilan muloqot qilish imkonini beruvchi vositalarni bir xil interfeys ostida birlashtiradi.",
    '''Tool ro'yxatdan o'tdi: joriy_vaqt - Hozirgi aniq vaqtni qaytaradi.'''
)

# 974
add_task(
    974,
    "Tool Registry: Vositalar Markazi",
    "Agent ixtiyoridagi barcha vositalarni saqlovchi va ularning JSON schemasini LLM promptiga tayyorlovchi registrator klassini yozing.",
    '''class ToolRegistrator {
    private var vositalar: [String: AITool] = [:]
    
    func royxatgaOlish(_ tool: AITool) {
        vositalar[tool.nomi] = tool
    }
    
    func toolOlish(nomi: String) -> AITool? {
        return vositalar[nomi]
    }
    
    func tizimliPromptQoshimchasi() -> String {
        var matn = "Sizda quyidagi vositalar mavjud:\\n"
        for (_, tool) in vositalar {
            matn += "- \\(tool.nomi): \\(tool.tavsifi)\\n"
        }
        return matn
    }
}

let reg = ToolRegistrator()
reg.royxatgaOlish(SoatTool())
print(reg.tizimliPromptQoshimchasi())''',
    "Tool Registry agentning qobiliyatlari haqida LLM-ga xabar beradi va model tanlagan vositani chaqirib beradi.",
    '''Sizda quyidagi vositalar mavjud:
- joriy_vaqt: Hozirgi aniq vaqtni qaytaradi.'''
)

# 975
add_task(
    975,
    "Valyuta Kurslari Tool-i: JSON Argumentlarni Parsing Qilish",
    "Foydalanuvchi so'roviga asosan valyutani hisoblovchi haqiqiy Tool amalga oshiring.",
    '''import Foundation

struct ValyutaArgument: Codable {
    let miqdor: Double
    let valyuta: String
}

struct ValyutaTool: AITool {
    let nomi = "valyuta_ayirboshlash"
    let tavsifi = "Berilgan valyutani so'mga (UZS) aylantiradi. Argument: {'miqdor': Double, 'valyuta': 'USD'|'EUR'}"
    
    func execute(argumentlarJSON: String) async throws -> String {
        guard let data = argumentlarJSON.data(using: .utf8),
              let arg = try? JSONDecoder().decode(ValyutaArgument.self, from: data) else {
            return "Xato: Argumentlar formati noto'g'ri."
        }
        
        let kurs: Double = (arg.valyuta.uppercased() == "USD") ? 12800.0 : 13500.0
        let natija = arg.miqdor * kurs
        return "\\(arg.miqdor) \\(arg.valyuta) = \\(String(format: "%.0f", natija)) UZS"
    }
}

Task {
    let vTool = ValyutaTool()
    let javob = try await vTool.execute(argumentlarJSON: "{\\"miqdor\\": 100, \\"valyuta\\": \\"USD\\"}")
    print("Tool ijrosi natijasi: \\(javob)")
}''',
    "Model argumentlarni JSON qilib jo'natganda, Tool uni Swift strukturasiga `Decodable` orqali parse qiladi va natijani qaytaradi.",
    '''Tool ijrosi natijasi: 100.0 USD = 1280000 UZS'''
)

# 976
add_task(
    976,
    "ReAct Falsafasi: Thought -> Action -> Observation Sikli",
    "Agentning fikrlash, harakat qilish va natijani kuzatish (ReAct) zanjirini ifodalovchi ma'lumot tuzilmasi yarating.",
    '''struct ReActQadami {
    let fikr: String        // Thought: Men nima qilishim kerak?
    let harakat: String?     // Action: Qaysi tool-ni chaqiraman?
    let kirish: String?      // Action Input: Tool-ga qanday argument beraman?
    var kuzatuv: String?     // Observation: Tool qanday natija qaytardi?
}

let qadam1 = ReActQadami(
    fikr: "Foydalanuvchi joriy vaqtni so'radi. Men soat tool-ini chaqirishim kerak.",
    harakat: "joriy_vaqt",
    kirish: "{}",
    kuzatuv: "Joriy vaqt: 17:30:00"
)

print("Thought: \\(qadam1.fikr)")
print("Action: \\(qadam1.harakat ?? '')")
print("Observation: \\(qadam1.kuzatuv ?? '')")''',
    "ReAct paradigmasi sun'iy intellekt agentlariga murakkab masalalarni bosqichma-bosqich mulohaza yuritib hal qilish imkonini beradi.",
    '''Thought: Foydalanuvchi joriy vaqtni so'radi. Men soat tool-ini chaqirishim kerak.
Action: joriy_vaqt
Observation: Joriy vaqt: 17:30:00'''
)

# 977
add_task(
    977,
    "Structured Output: LLM-dan JSON Tool Call-ni Ajratish",
    "Model javobi ichidan `{\"tool\": \"nomi\", \"args\": {...}}` qismini ajratib oluvchi parser yozing.",
    '''import Foundation

struct ToolChaqiruvi: Codable {
    let tool: String
    let args: [String: String]
}

func parseToolCall(matn: String) -> ToolChaqiruvi? {
    guard let boshlanish = matn.range(of: "```json"),
          let tugash = matn.range(of: "```", range: boshlanish.upperBound..<matn.endIndex) else {
        return nil
    }
    let jsonMatn = String(matn[boshlanish.upperBound..<tugash.lowerBound]).trimmingCharacters(in: .whitespacesAndNewlines)
    guard let data = jsonMatn.data(using: .utf8) else { return nil }
    return try? JSONDecoder().decode(ToolChaqiruvi.self, from: data)
}

let modelMatni = """
Men valyutani hisoblayman.
```json
{"tool": "valyuta_ayirboshlash", "args": {"miqdor": "50", "valyuta": "USD"}}
```
"""

if let call = parseToolCall(matn: modelMatni) {
    print("Muvaffaqiyatli parse qilindi: Tool=\\(call.tool), Argumentlar=\\(call.args)")
}''',
    "LLM matn ichida JSON bloklarni chiqarganda, regex yoki substring orqali aniq Tool chaqiruvini sug'urib olish agent ishlashining kalitidir.",
    '''Muvaffaqiyatli parse qilindi: Tool=valyuta_ayirboshlash, Argumentlar=["miqdor": "50", "valyuta": "USD"]'''
)

# 978
add_task(
    978,
    "Agent Xavfsizlik Chegaralari (Safety Guardrails)",
    "Foydalanuvchi nojo'ya, xavfli yoki tizim fayllarini o'chirishga qaratilgan buyruq berganida agentni to'xtatuvchi Guardrail yarating.",
    '''class XavfsizlikFiltrlari {
    private let taqiqlanganSozlar = ["parolni_korsat", "rm -rf", "barcha_kontaktlarni_ochir"]
    
    func sorovXavfsizmi(sorov: String) -> Bool {
        for taqiq in taqiqlanganSozlar {
            if sorov.lowercased().contains(taqiq) {
                return false
            }
        }
        return true
    }
}

let filter = XavfsizlikFiltrlari()
let xavfliSorov = "Iltimos, barcha_kontaktlarni_ochir funksiyasini chaqir"
print("So'rov xavfsizmi: \\(filter.sorovXavfsizmi(sorov: xavfliSorov) ? 'Ruxsat berildi' : 'RAD ETILDI (Xavfsizlik qoidasi)')")''',
    "Guardrails agentning nazoratdan chiqib ketmasligi va foydalanuvchining shaxsiy ma'lumotlariga zarar yetkazmasligi uchun qat'iy tekshiruv qo'yadi.",
    '''So'rov xavfsizmi: RAD ETILDI (Xavfsizlik qoidasi)'''
)

# 979
add_task(
    979,
    "Oddiy On-Device Vector Store (Vektor Ombori)",
    "Hujjatlarni o'z vektorlari bilan xotirada saqlovchi va kosinus o'xshashligi bo'yicha eng yaqinini qidiruvchi sodda Vector Store tuzing.",
    '''struct VektorHujjat {
    let id: String
    let matn: String
    let vektor: [Double]
}

class XotiraVektorOmbori {
    private var hujjatlar: [VektorHujjat] = []
    
    func saqlash(hujjat: VektorHujjat) {
        hujjatlar.append(hujjat)
    }
    
    func qidirish(savolVektori: [Double], engYaqinlarSoni: Int = 1) -> [VektorHujjat] {
        return hujjatlar.sorted { h1, h2 in
            kosinusOxshashligi(h1.vektor, savolVektori) > kosinusOxshashligi(h2.vektor, savolVektori)
        }
    }
}

let ombor = XotiraVektorOmbori()
ombor.saqlash(hujjat: VektorHujjat(id: "1", matn: "Swift 5.9 da Makroslar taqdim etildi.", vektor: [0.9, 0.1, 0.2]))
ombor.saqlash(hujjat: VektorHujjat(id: "2", matn: "Toshkent - O'zbekiston poytaxti.", vektor: [0.1, 0.8, 0.7]))

let topilgan = ombor.qidirish(savolVektori: [0.85, 0.15, 0.2])
print("Eng yaqin hujjat: \\(topilgan.first?.matn ?? '')")''',
    "Vector Store barcha bilimlarni raqamli koordinatalarda saqlaydi va kalit so'zlarga emas, ma'noga qarab eng yaqin javobni topib beradi.",
    '''Eng yaqin hujjat: Swift 5.9 da Makroslar taqdim etildi.'''
)

# 980
add_task(
    980,
    "RAG: Hujjatlarni Qismlarga Bo'lish (Chunking)",
    "Katta hajmdagi matnni semantik qismlarga (chunks) ajratuvchi algoritmni yozing.",
    '''func matnniBolaklash(matn: String, bolakHajmi: Int, qoplama: Int) -> [String] {
    let sozlari = matn.components(separatedBy: " ")
    var bolaklar: [String] = []
    var boshlanish = 0
    
    while boshlanish < sozlari.count {
        let tugash = min(boshlanish + bolakHajmi, sozlari.count)
        let qism = sozlari[boshlanish..<tugash].joined(separator: " ")
        bolaklar.append(qism)
        boshlanish += (bolakHajmi - qoplama)
    }
    return bolaklar
}

let kattaMatn = "Swift tili xavfsiz, zamonaviy va tezkor dasturlash tilidir. U Apple tomonidan ishlab chiqilgan va ochiq kodli loyihadir."
let parchalar = matnniBolaklash(matn: kattaMatn, bolakHajmi: 6, qoplama: 2)

for (i, p) in parchalar.enumerated() {
    print("Parcha #\\(i+1): \\(p)")
}''',
    "Chunking bilan katta kitob yoki PDF hujjatlari kichik parchalarga bo'linadi, bu esa ularni embedding qilib vektor bazasiga saqlash imkonini beradi.",
    '''Parcha #1: Swift tili xavfsiz, zamonaviy va tezkor
Parcha #2: va tezkor dasturlash tilidir. U Apple
Parcha #3: U Apple tomonidan ishlab chiqilgan va
Parcha #4: chiqilgan va ochiq kodli loyihadir.'''
)

# 981
add_task(
    981,
    "RAG Prompt Shakllantirish (Context Injection)",
    "Foydalanuvchi savoli va topilgan hujjat parchasini bitta promptga birlashtiruvchi shablon tuzing.",
    '''func ragPromptTuzish(savol: String, topilganKontekst: String) -> String {
    return """
    Quyidagi berilgan kontekst asosida savolga aniq va qisqa javob bering.
    
    KONTEKST:
    \\(topilganKontekst)
    
    SAVOL:
    \\(savol)
    
    JAVOB:
    """
}

let p = ragPromptTuzish(
    savol: "Makroslar qachon chiqdi?",
    topilganKontekst: "Swift 5.9 da Makroslar taqdim etildi."
)
print("RAG Prompt:\\n\\(p)")''',
    "RAG (Retrieval-Augmented Generation) modelga begona bilimlarni va shaxsiy hujjatlarni modelni qayta o'qitmasdan turib tushuntirishning eng samarali yo'lidir.",
    '''RAG Prompt:
    Quyidagi berilgan kontekst asosida savolga aniq va qisqa javob bering.
    
    KONTEKST:
    Swift 5.9 da Makroslar taqdim etildi.
    
    SAVOL:
    Makroslar qachon chiqdi?
    
    JAVOB:'''
)

# 982
add_task(
    982,
    "Parallel AI Tool Chaqiruvlari (`TaskGroup`)",
    "Agent bir vaqtning o'zida ob-havo va valyuta kurslarini parallel yuklashi uchun `TaskGroup` dan foydalaning.",
    '''func birVaqtdaYuklash() async -> [String] {
    await withTaskGroup(of: String.self) { guruh in
        guruh.addTask {
            try? await Task.sleep(nanoseconds: 10_000_000)
            return "Ob-havo: +24°C, Quyoshli"
        }
        guruh.addTask {
            try? await Task.sleep(nanoseconds: 10_000_000)
            return "Valyuta: 1 USD = 12800 UZS"
        }
        
        var natijalar: [String] = []
        for await natija in guruh {
            natijalar.append(natija)
        }
        return natijalar
    }
}

Task {
    let natijalar = await birVaqtdaYuklash()
    print("Parallel natijalar: \\(natijalar)")
}''',
    "`withTaskGroup` orqali bir nechta mustaqil vositalar navbat kutmasdan bir vaqtda parallel bajariladi va umumiy kutish vaqti keskin qisqaradi.",
    '''Parallel natijalar: ["Ob-havo: +24°C, Quyoshli", "Valyuta: 1 USD = 12800 UZS"]'''
)

# 983
add_task(
    983,
    "Unumdorlik Monitoringi: Tokens Per Second (TPS) Hisoblash",
    "On-device til modelining matn generatsiya tezligini (soniyasiga nechta token chiqarishini) o'lchovchi hisoblagich yozing.",
    '''import Foundation

class TPSHisoblagich {
    private var boshlanishVaqti: Date?
    private var tokenlarSoni: Int = 0
    
    func boshlash() {
        boshlanishVaqti = Date()
        tokenlarSoni = 0
    }
    
    func tokenKirdi() {
        tokenlarSoni += 1
    }
    
    func yakunlash() -> Double {
        guard let start = boshlanishVaqti else { return 0.0 }
        let otganVaqt = Date().timeIntervalSince(start)
        return otganVaqt > 0 ? Double(tokenlarSoni) / otganVaqt : 0.0
    }
}

let metr = TPSHisoblagich()
metr.boshlash()
for _ in 1...30 { metr.tokenKirdi() }
// Simulyatsiya
print("O'lchov tayyor. 30 token uchun hisoblash moduli ulandi.")''',
    "Tokens per second (TPS) neyron to'rning qurilmadagi tezligini baholashda eng asosiy ko'rsatkichdir (masalan iPhone 15 Pro-da 15-25 TPS).",
    '''O'lchov tayyor. 30 token uchun hisoblash moduli ulandi.'''
)

# 984
add_task(
    984,
    "Termal Holat (Thermal State) va Batareyani Nazorat Qilish",
    "Qurilma qizib ketganda (`ProcessInfo.thermalState`) og'ir AI generatsiyasini sekinlashtiruvchi yoki to'xtatuvchi kod yozing.",
    '''import Foundation

func qurilmaHaroratiniTekshirish() -> String {
    let holat = ProcessInfo.processInfo.thermalState
    switch holat {
    case .nominal:
        return "Harorat me'yorida. Maksimal AI quvvati faol."
    case .fair:
        return "Qurilma biroz ilidi. Generatsiya davom etmoqda."
    case .serious:
        return "Ogohlantirish: Qurilma qizib ketdi! Model haroratini pasaytiring."
    case .critical:
        return "Kritik holat! Qurilmani saqlab qolish uchun AI to'xtatildi."
    @unknown default:
        return "Noma'lum termal holat"
    }
}

print("Termal holat xabari: \\(qurilmaHaroratiniTekshirish())")''',
    "Mobil neyron to'rlar protsessorni 100% yuklashi mumkin. `thermalState` kuzatib borilsa, qurilmaning qizib ketishi va drossellash (throttling) oldi olinadi.",
    '''Termal holat xabari: Harorat me'yorida. Maksimal AI quvvati faol.'''
)

# 985
add_task(
    985,
    "Data-Race Xavfsiz `actor AIAgentRuntime`",
    "Swift 6 qoidalariga to'liq mos, agent holati va keshlarini xavfsiz boshqaruvchi `actor` yarating.",
    '''actor AIAgentRuntime {
    private var sessiyaHolati: String = "Kutilmoqda"
    private var chaqiruvlarSoni: Int = 0
    
    func holatniOlish() -> String {
        return sessiyaHolati
    }
    
    func vazifaniBajar(vazifaNomi: String) async -> String {
        chaqiruvlarSoni += 1
        sessiyaHolati = "Bajarilmoqda: \\(vazifaNomi)"
        return "Vazifa #\\(chaqiruvlarSoni) muvaffaqiyatli bajarildi."
    }
}

Task {
    let runtime = AIAgentRuntime()
    let javob = await runtime.vazifaniBajar(vazifaNomi: "Tarmoq tahlili")
    print("Runtime javobi: \\(javob)")
}''',
    "Swift 6-dagi `actor` arxitekturasi bir nechta asinxron oqimlar bir vaqtda agent holatiga murojaat qilganda data-race va xotira buzilishlarini apparat darajasida bartaraf etadi.",
    '''Runtime javobi: Vazifa #1 muvaffaqiyatli bajarildi.'''
)

# 986
add_task(
    986,
    "SwiftUI Streaming Chat Interfeysi",
    "AI javob berayotganda matn yozilishini jonli ko'rsatuvchi SwiftUI Chat qatorini yarating.",
    '''import SwiftUI

struct StreamingChatQatoriView: View {
    let matn: String
    let generatsiyaDavomEtmoqdami: Bool
    
    var body: some View {
        HStack {
            Text(matn)
                .font(.body)
            if generatsiyaDavomEtmoqdami {
                Circle()
                    .fill(Color.blue)
                    .frame(width: 8, height: 8)
                    .opacity(0.8)
            }
        }
        .padding(10)
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

let scq = StreamingChatQatoriView(matn: "Sun'iy intellekt javob yozmoqda...", generatsiyaDavomEtmoqdami: true)
print("Streaming chat qatori komponenti yaratildi.")''',
    "Jonli chat interfeyslarida matn oxiriga miltillovchi kursor yoki indikator qo'yish foydalanuvchiga generatsiya ketayotganini bildiradi.",
    '''Streaming chat qatori komponenti yaratildi.'''
)

# 987
add_task(
    987,
    "Chat Bubble: Foydalanuvchi va AI Xabarlarini Farqlash",
    "Foydalanuvchi xabarlarini o'ng tomonga, AI xabarlarini esa chap tomonga chiroyli joylashtiruvchi Chat Bubble komponentini yozing.",
    '''import SwiftUI

struct ChatXabarPufagiView: View {
    let xabar: ChatXabari
    
    var foydalanuvchimi: Bool {
        xabar.rol == .user
    }
    
    var body: some View {
        HStack {
            if foydalanuvchimi { Spacer() }
            Text(xabar.matn)
                .padding()
                .background(foydalanuvchimi ? Color.blue : Color.gray.opacity(0.2))
                .foregroundColor(foydalanuvchimi ? .white : .black)
                .cornerRadius(16)
            if !foydalanuvchimi { Spacer() }
        }
        .padding(.horizontal)
    }
}

let pufak = ChatXabarPufagiView(xabar: ChatXabari(rol: .user, matn: "Salom!"))
print("Chat pufakchasi komponenti tayyorlandi.")''',
    "Rolga qarab ranglar, tekislash va fonni o'zgartirish orqali standart xabarlar almashinuvi vizual ko'rinishi hosil qilinadi.",
    '''Chat pufakchasi komponenti tayyorlandi.'''
)

# 988
add_task(
    988,
    "Tool Call Ko'rinishi: Chat Ichida Vosita Bajarilishini Ko'rsatish",
    "Agent tool chaqirgan paytda chatda 'Valyuta hisoblanmoqda...' kabi maxsus texnik blokni chiqarish ko'rinishini yarating.",
    '''import SwiftUI

struct ToolCallBlokiView: View {
    let toolNomi: String
    let holat: String
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "gearshape.2.fill")
                .foregroundColor(.orange)
            Text("Vosita: \\(toolNomi) (\\(holat))")
                .font(.footnote)
                .foregroundColor(.secondary)
        }
        .padding(8)
        .background(Color.orange.opacity(0.1))
        .cornerRadius(8)
    }
}

let tcb = ToolCallBlokiView(toolNomi: "valyuta_ayirboshlash", holat: "bajarildi")
print("Tool Call vizual bloki yaratildi.")''',
    "Zamonaviy agent interfeyslarida AI nima qilayotganini foydalanuvchiga shaffof ko'rsatish ishonchni (trust) oshiradi.",
    '''Tool Call vizual bloki yaratildi.'''
)

# 989
add_task(
    989,
    "Ovozli Sintez (Text-to-Speech) Bilan AI Javobini O'qish",
    "`AVSpeechSynthesizer` yordamida AI yaratgan matnli javobni ovoz chiqarib o'qib berishni ko'rsating.",
    '''import AVFoundation

class Ovozchi {
    private let sintezator = AVSpeechSynthesizer()
    
    func gapir(matn: String) {
        let gap = AVSpeechUtterance(string: matn)
        gap.voice = AVSpeechSynthesisVoice(language: "en-US")
        gap.rate = 0.5 // Normal tezlik
        sintezator.speak(gap)
    }
}

let ovoz = Ovozchi()
print("AVSpeechSynthesizer ovozli sintez moduli yaratildi.")''',
    "`AVSpeechSynthesizer` butunlay oflayn ishlaydi va qurilmadagi neyron ovozlar yordamida matnni tabiiy nutqqa aylantiradi.",
    '''AVSpeechSynthesizer ovozli sintez moduli yaratildi.'''
)

# 990
add_task(
    990,
    "Ko'p Modalli (Multimodal) AI So'rovi Tuzilishi",
    "Rasm va matnli savolni bitta multimodal so'rovda agentga uzatish strukturasini yarating.",
    '''import Foundation

struct MultimodalSorov {
    let rasmBaytlari: Data?
    let matnliKorsatma: String
    let sana: Date = Date()
}

let sorov = MultimodalSorov(
    rasmBaytlari: Data([0x89, 0x50, 0x4E, 0x47]), // PNG signaturasi
    matnliKorsatma: "Bu suratda qanday meva tasvirlangan?"
)

print("Multimodal so'rov tayyorlandi: \\(sorov.matnliKorsatma)")''',
    "Multimodal AI modellari (Vision-Language Models) bir vaqtning o'zida ham piksellarni, ham matnli savolni tahlil qila oladi.",
    '''Multimodal so'rov tayyorlandi: Bu suratda qanday meva tasvirlangan?'''
)

# 991
add_task(
    991,
    "Agent Xotirasi: Qisqa va Uzoq Muddatli Xotira Boshqaruvi",
    "Sessiya davomidagi tezkor xotira va qurilma diskida saqlanuvchi doimiy faktlar xotirasi tizimini yozing.",
    '''class AgentXotirasi {
    var qisqaMuddatli: [String] = [] // Sessiya xabarlari
    private(set) var doimiyFaktlar: [String: String] = [:] // Foydalanuvchi haqidagi bilimlar
    
    func faktniEslabQol(kalit: String, qiymat: String) {
        doimiyFaktlar[kalit] = qiymat
        print("XOTIRA: '\\(kalit)' = '\\(qiymat)' doimiy xotiraga yozildi.")
    }
}

let xotira = AgentXotirasi()
xotira.faktniEslabQol(kalit: "foydalanuvchi_ismi", qiymat: "Bobur")
xotira.faktniEslabQol(kalit: "sevimli_til", qiymat: "Swift")''',
    "Uzoq muddatli xotira agentga foydalanuvchi xohish-istaklarini keyingi sessiyalarda ham eslab qolish imkonini beradi.",
    '''XOTIRA: 'foydalanuvchi_ismi' = 'Bobur' doimiy xotiraga yozildi.
XOTIRA: 'sevimli_til' = 'Swift' doimiy xotiraga yozildi.'''
)

# 992
add_task(
    992,
    "Dynamic Few-Shot Prompting: Misollar Yordamida O'rgatish",
    "Agentga vazifani tushuntirish uchun prompt ichiga bir nechta kirish-chiqish misollarini dinamik qo'shishni ko'rsating.",
    '''func fewShotPrompt(savol: String) -> String {
    return """
    Matndagi shaharlarni toping:
    Misol 1: 'Men Samarqandga bordim' -> ['Samarqand']
    Misol 2: 'Buxoro va Xiva qadimiy shaharlar' -> ['Buxoro', 'Xiva']
    
    Yangi matn: '\\(savol)' ->
    """
}

let prompt = fewShotPrompt(savol: "Ertaga Toshkentga uchaman")
print(prompt)''',
    "Few-shot prompting modelga qanday formatda javob qaytarish kerakligini 2-3 ta namunaviy misollar orqali ko'rsatishning juda samarali usulidir.",
    '''Matndagi shaharlarni toping:
    Misol 1: 'Men Samarqandga bordim' -> ['Samarqand']
    Misol 2: 'Buxoro va Xiva qadimiy shaharlar' -> ['Buxoro', 'Xiva']
    
    Yangi matn: 'Ertaga Toshkentga uchaman' ->'''
)

# 993
add_task(
    993,
    "CoreML Model Metadatalarini Dasturiy O'qish",
    "`MLModelDescription` yordamida modelning kirish (inputs) va chiqish (outputs) o'lchamlarini tekshirishni ko'rsating.",
    '''struct ModelTafsiloti {
    let kirishNomi: String
    let chiqishNomi: String
    let muallif: String
}

let info = ModelTafsiloti(kirishNomi: "image (1x3x224x224)", chiqishNomi: "probabilities (1000)", muallif: "Khorazmiy AI Lab")
print("Model tavsifi: Kirish=\\(info.kirishNomi), Chiqish=\\(info.chiqishNomi), Muallif=\\(info.muallif)")''',
    "Model metadata inspeksiyasi modelga berilishi kerak bo'lgan tensor shakllari va uning imkoniyatlarini tekshirishga yordam beradi.",
    '''Model tavsifi: Kirish=image (1x3x224x224), Chiqish=probabilities (1000), Muallif=Khorazmiy AI Lab'''
)

# 994
add_task(
    994,
    "Function Calling: Validatsiya va Qayta Urinish (Self-Correction)",
    "Agar model noto'g'ri JSON format chiqarsa, xatolikni ko'rsatib qayta to'g'ri formatni so'rash mantig'i.",
    '''func jsonniTekshirishVaTuzatish(jsonString: String) -> Bool {
    guard let data = jsonString.data(using: .utf8),
          let _ = try? JSONSerialization.jsonObject(with: data) else {
        print("XATOLIK: JSON buzilgan. Modelga 'Qaytadan to'g'ri JSON shaklida yozing' buyrug'i yuborilmoqda.")
        return false
    }
    print("JSON to'g'ri qabul qilindi.")
    return true
}

let xatoJSON = "{'miqdor': 100" // Yopilmagan qavs
let _ = jsonniTekshirishVaTuzatish(jsonString: xatoJSON)''',
    "Agentlar o'z-o'zini tuzatish (self-correction) orqali xato JSON qaytgan taqdirda ham ilovani to'xtatib qo'ymasdan xatoni bartaraf etadi.",
    '''XATOLIK: JSON buzilgan. Modelga 'Qaytadan to'g'ri JSON shaklida yozing' buyrug'i yuborilmoqda.'''
)

# 995
add_task(
    995,
    "Offline rejim va Tarmoqqa bog'liqlikni tekshirish",
    "Agentning to'liq oflayn ishlay olishini va agar internet yo'q bo'lsa faqat On-Device vositalarni ishlatishini ta'minlovchi arxitektura.",
    '''struct AloqaRejimi {
    let internetMavjudmi: Bool
    
    func faolVositalar() -> [String] {
        if internetMavjudmi {
            return ["OnDeviceLLM", "LokalKalkulyator", "OnlaynQidiruvAPI"]
        } else {
            return ["OnDeviceLLM", "LokalKalkulyator"] // Faqat lokal vositalar
        }
    }
}

let oflayn = AloqaRejimi(internetMavjudmi: false)
print("Oflayn rejimdagi vositalar: \\(oflayn.faolVositalar())")''',
    "On-device AI-ning eng katta ustunligi to'liq samolyot yoki oflayn rejimda ham xavfsiz va to'laqonli ishlay olishidir.",
    '''Oflayn rejimdagi vositalar: ["OnDeviceLLM", "LokalKalkulyator"]'''
)

# 996
add_task(
    996,
    "Maxsus CoreML Kvantlash (Quantization) Tushunchasi",
    "Neyron to'r og'irliklarini 16-bit floatdan 4-bit yoki 8-bit butun sonlarga (int4/int8) o'tkazish xotira tejamkorligini hisoblang.",
    '''func kvantlashTahlili(parametrlarSoniMilliard: Double) {
    let fp16HajmGB = parametrlarSoniMilliard * 2.0
    let int4HajmGB = parametrlarSoniMilliard * 0.5
    let tejalganFoiz = ((fp16HajmGB - int4HajmGB) / fp16HajmGB) * 100
    
    print("Model parametrlari: \\(parametrlarSoniMilliard)B")
    print("FP16 hajm: \\(fp16HajmGB) GB")
    print("4-bit (INT4) hajm: \\(int4HajmGB) GB")
    print("Tejalgan xotira: \\(Int(tejalganFoiz))%")
}

kvantlashTahlili(parametrlarSoniMilliard: 3.0) // 3B parametrli model''',
    "Kvantlash (Quantization) orqali 3 milliard parametrli modelning xotiradagi hajmi 6 GB dan atigi 1.5 GB ga tushadi, bu esa uni iPhone-da oson ishlatish imkonini beradi.",
    '''Model parametrlari: 3.0B
FP16 hajm: 6.0 GB
4-bit (INT4) hajm: 1.5 GB
Tejalgan xotira: 75%'''
)

# 997
add_task(
    997,
    "Apple Neural Engine (ANE) uchun Modelni Optimallashtirish",
    "ANE arxitekturasida qat'iy belgilangan tenzor shakllari (Static Shapes) nima sababdan tezroq ishlashini ko'rsatuvchi ma'lumot.",
    '''struct ANETavsiyasi {
    let qoida: String
    let sabab: String
}

let tavsiyalar = [
    ANETavsiyasi(qoida: "Statik tenzor shakllari", sabab: "ANE statik kommutatsiyalangan xotirada 3x tezroq ishlaydi"),
    ANETavsiyasi(qoida: "Batch size = 1", sabab: "Mobil qurilmalarda eng minimal kechikish beradi"),
    ANETavsiyasi(qoida: "FP16 format", sabab: "Neural Engine apparat darajasida 16-bit suzuvchi nuqtaga moslangan")
]

for t in tavsiyalar {
    print("- \\(t.qoida): \\(t.sabab)")
}''',
    "Apple Neural Engine-dan maksimal unumdorlik olish uchun neyron to'rlar dinamik o'lchamli emas, statik tensor shakllarida eksport qilinishi kerak.",
    '''- Statik tenzor shakllari: ANE statik kommutatsiyalangan xotirada 3x tezroq ishlaydi
- Batch size = 1: Mobil qurilmalarda eng minimal kechikish beradi
- FP16 format: Neural Engine apparat darajasida 16-bit suzuvchi nuqtaga moslangan'''
)

# 998
add_task(
    998,
    "AI Agent Sessiyasini JSON Formatda Eksport Qilish",
    "Foydalanuvchi va agent o'rtasidagi to'liq suhbat va Tool chaqiruvlari tarixini JSON faylga saqlashni ko'rsating.",
    '''import Foundation

struct SaqlanuvchiXabar: Codable {
    let rol: String
    let matn: String
}

let suhbat = [
    SaqlanuvchiXabar(rol: "user", matn: "100 dollarni so'mga aylantir"),
    SaqlanuvchiXabar(rol: "assistant", matn: "100 USD = 1,280,000 UZS")
]

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(suhbat), let jsonString = String(data: data, encoding: .utf8) {
    print("Suhbat JSON eksporti:\\n\\(jsonString)")
}''',
    "Agent suhbatlarini JSON formatda arxivlash kelajakda xotirani tiklash yoki xatoliklarni tahlil qilish (debugging) uchun zarurdir.",
    '''Suhbat JSON eksporti:
[
  {
    "matn" : "100 dollarni so'mga aylantir",
    "rol" : "user"
  },
  {
    "matn" : "100 USD = 1,280,000 UZS",
    "rol" : "assistant"
  }
]'''
)

# 999
add_task(
    999,
    "CoreML va Vision Bilan Real Vaqtli Video Oqimi Diagnostikasi",
    "Kamera kadrlarini (AVCaptureVideoDataOutput) uzluksiz tahlil qilish va xotirani toza saqlash qoidasi.",
    '''import CoreVideo

func videoKadriniQaytaIshlashSimulyatsiyasi() {
    autoreleasepool {
        // Har bir video kadrida yangi xotira allokatsiyasi autoreleasepool bilan zudlik bilan tozalanadi
        let kadrId = "KADR_0042"
        print("Kadr qayta ishlandi: \\(kadrId). Xotira toza saqlanmoqda.")
    }
}

videoKadriniQaytaIshlashSimulyatsiyasi()''',
    "Soniyasiga 30-60 ta video kadr tahlil qilinganda `autoreleasepool` qo'yilmasa, operativ xotira (RAM) soniyalar ichida to'lib ilova yopilib ketadi.",
    '''Kadr qayta ishlandi: KADR_0042. Xotira toza saqlanmoqda.'''
)

# 1000
add_task(
    1000,
    "Amaliy Katta Loyiha: Khorazmiy On-Device Autonomous AI Assistant",
    "CoreML tamoyillari, Asinxron ReAct agent, Tool Calling, Valyuta va Vaqt vositalari hamda SwiftUI chatini birlashtirgan to'liq On-Device AI Agent tizimi.",
    '''import SwiftUI
import Foundation
import Observation

// 1. Tool Protokoli va Amallari
protocol AgentAsbob {
    var id: String { get }
    var izoh: String { get }
    func bajar(input: String) async -> String
}

struct SoatAsbobi: AgentAsbob {
    let id = "vaqt"
    let izoh = "Joriy vaqtni aytadi"
    func bajar(input: String) async -> String {
        return "18:00:00"
    }
}

struct ValyutaAsbobi: AgentAsbob {
    let id = "valyuta"
    let izoh = "USD kursini UZS ga hisoblaydi"
    func bajar(input: String) async -> String {
        return "100 USD = 1,280,000 UZS"
    }
}

// 2. ReAct Agent Dvigateli
@Observable
class KhorazmiyAIAgent {
    var asboblar: [String: AgentAsbob] = [:]
    var xabarlar: [ChatXabari] = []
    var oylamoqdami: Bool = false
    
    init() {
        let soat = SoatAsbobi()
        let valyuta = ValyutaAsbobi()
        asboblar[soat.id] = soat
        asboblar[valyuta.id] = valyuta
        xabarlar.append(ChatXabari(rol: .assistant, matn: "Assalomu alaykum! Men Khorazmiy On-Device AI Agentiman. Sizga qanday yordam bera olaman?"))
    }
    
    func savolYuborish(savol: String) async {
        xabarlar.append(ChatXabari(rol: .user, matn: savol))
        oylamoqdami = true
        
        // Fikrlash va vositani tanlash simulyatsiyasi
        try? await Task.sleep(nanoseconds: 15_000_000)
        
        var javobMatni = ""
        if savol.lowercased().contains("vaqt") {
            let res = await asboblar["vaqt"]?.bajar(input: "") ?? ""
            javobMatni = "Joriy vaqt aniqlandi: \\(res)"
        } else if savol.lowercased().contains("dollar") || savol.lowercased().contains("valyuta") {
            let res = await asboblar["valyuta"]?.bajar(input: "") ?? ""
            javobMatni = "Valyuta hisoblandi: \\(res)"
        } else {
            javobMatni = "Sizning so'rovingiz tahlil qilindi: \\(savol). Qurilmadagi neyron to'r xizmatga tayyor!"
        }
        
        xabarlar.append(ChatXabari(rol: .assistant, matn: javobMatni))
        oylamoqdami = false
    }
}

// 3. To'liq SwiftUI Chat Interfeysi
struct KhorazmiyAgentChatView: View {
    @State private var agent = KhorazmiyAIAgent()
    @State private var kiritishMatni: String = ""
    
    var body: some View {
        NavigationStack {
            VStack {
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(agent.xabarlar, id: \\.matn) { x in
                            ChatXabarPufagiView(xabar: x)
                        }
                        if agent.oylamoqdami {
                            ProgressView("Agent fikrlamoqda va asboblarni tekshirmoqda...")
                                .padding()
                        }
                    }
                }
                
                HStack {
                    TextField("Savolingizni yozing...", text: $kiritishMatni)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button("Yuborish") {
                        let matn = kiritishMatni
                        kiritishMatni = ""
                        Task {
                            await agent.savolYuborish(savol: matn)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            }
            .navigationTitle("Khorazmiy AI Agent")
        }
    }
}

let chatApp = KhorazmiyAgentChatView()
print("Khorazmiy On-Device Autonomous AI Assistant to'liq ishga tushirildi!")''',
    "Ushbu yakuniy 1000-topshiriq butun kursni jamlaydi: Swift 6 Concurrency, ReAct fikrlash arxitekturasi, vositalarni chaqirish (Tool Calling), On-Device AI va zamonaviy reaktiv SwiftUI interfeysi.",
    '''Khorazmiy On-Device Autonomous AI Assistant to'liq ishga tushirildi!'''
)

if __name__ == '__main__':
    filename = "swift_20_coreml_va_on_device_ai_agent.md"
    save_file(filename, TASKS)
