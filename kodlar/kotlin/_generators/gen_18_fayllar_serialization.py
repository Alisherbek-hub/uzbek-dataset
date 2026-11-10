# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 851
add_task(
    851,
    "File obyekti yaratish va mavjudligini tekshirish",
    "Java va Kotlin da fayllar bilan ishlashning asosi bo'lgan java.io.File obyektini yaratib, uning exists(), isFile va isDirectory xususiyatlarini tekshiring.",
    """
import java.io.File

fun main() {
    val fayl = File("test_fayl.txt")
    println("Fayl nomi: ${fayl.name}")
    println("Fayl mavjudmi: ${fayl.exists()}")
    println("Fayl turi oddiy faylmi: ${fayl.isFile}")
    println("Fayl turi katalogmi: ${fayl.isDirectory}")
}
""",
    "File klassi fayl tizimidagi yo'lni (path) ifodalaydi. U orqali faylning mavjudligi, turi va xususiyatlari tezda tekshiriladi.",
    """
Fayl nomi: test_fayl.txt
Fayl mavjudmi: false
Fayl turi oddiy faylmi: false
Fayl turi katalogmi: false
"""
)

# 852
add_task(
    852,
    "writeText() orqali yangi faylga matn yozish",
    "Kotlin ning qulay kotlin.io kengaytmasi bo'lgan writeText() yordamida yangi matnli fayl yarating va unga ma'lumot yozing.",
    """
import java.io.File

fun main() {
    val fayl = File("salom.txt")
    fayl.writeText("Assalomu alaykum, Kotlin 2.0!\nO'zbekiston IT ta'limi.")
    println("Fayl muvaffaqiyatli yozildi: ${fayl.exists()}")
    println("Fayl hajmi: ${fayl.length()} bayt")
    fayl.delete() // Tozalash
}
""",
    "writeText() faylni ochadi, UTF-8 kodlashida matnni yozadi va oqimni avtomatik ravishda xavfsiz yopadi. Agar fayl avvaldan mavjud bo'lsa, uning ichini butunlay yangilaydi (overwrite).",
    """
Fayl muvaffaqiyatli yozildi: true
Fayl hajmi: ~50 bayt
"""
)

# 853
add_task(
    853,
    "readText() orqali fayl tarkibini butunlay o'qish",
    "readText() kengaytmasidan foydalanib, fayldagi barcha matnni bitta String o'zgaruvchisiga o'qing.",
    """
import java.io.File

fun main() {
    val fayl = File("xabar.txt")
    fayl.writeText("Kotlin dunyosiga xush kelibsiz!")
    
    val matn = fayl.readText()
    println("Fayldan o'qilgan matn: $matn")
    
    fayl.delete()
}
""",
    "readText() kichik va o'rta hajmdagi fayllarni bir qatorda o'qish uchun juda qulay. U resursni avtomatik yopishni (try-finally) o'z ichiga oladi.",
    """
Fayldan o'qilgan matn: Kotlin dunyosiga xush kelibsiz!
"""
)

# 854
add_task(
    854,
    "appendText() orqali fayl oxiriga yangi satr qo'shish",
    "Mavjud matnni o'chirib yubormasdan, faylning oxiriga yangi log yozuvlarini appendText() yordamida qo'shing.",
    """
import java.io.File

fun main() {
    val logFayl = File("audit.log")
    logFayl.writeText("[LOG] 1-yozuv: Tizim ishga tushdi\n")
    
    logFayl.appendText("[LOG] 2-yozuv: Foydalanuvchi kirdi\n")
    logFayl.appendText("[LOG] 3-yozuv: Tranzaksiya amalga oshirildi\n")
    
    println("Audit fayl tarkibi:")
    println(logFayl.readText().trim())
    
    logFayl.delete()
}
""",
    "appendText() fayl oxiriga (append rejimida) yangi matn qo'shadi, bu ayniqsa log yozuvlari va monitoring ma'lumotlarini to'plashda qulaydir.",
    """
Audit fayl tarkibi:
[LOG] 1-yozuv: Tizim ishga tushdi
[LOG] 2-yozuv: Foydalanuvchi kirdi
[LOG] 3-yozuv: Tranzaksiya amalga oshirildi
"""
)

# 855
add_task(
    855,
    "readLines() orqali faylni satrlar ro'yxatiga ajratish",
    "Fayldagi har bir qatorni List<String> to'plamiga o'girib, ularning sonini va birinchi qatorini aniqlang.",
    """
import java.io.File

fun main() {
    val fayl = File("ismlar.txt")
    fayl.writeText("Ali\nVali\nGani\nOlim")
    
    val satrlar: List<String> = fayl.readLines()
    println("Jami satrlar soni: ${satrlar.size}")
    println("Birinchi ism: ${satrlar.first()}")
    println("Oxirgi ism: ${satrlar.last()}")
    
    fayl.delete()
}
""",
    "readLines() faylning har bir qatorini ro'yxat elementiga aylantiradi. Katta hajmli fayllarda xotira tejash uchun forEachLine yoki useLines tavsiya etiladi.",
    """
Jami satrlar soni: 4
Birinchi ism: Ali
Oxirgi ism: Olim
"""
)

# 856
add_task(
    856,
    "forEachLine { } orqali faylni xotirani tejab qatorma-qator o'qish",
    "Katta fayllarni o'qiyotganda butun faylni xotiraga yuklamasdan, har bir qatorni alohida qayta ishlovchi forEachLine dan foydalaning.",
    """
import java.io.File

fun main() {
    val fayl = File("raqamlar.txt")
    fayl.writeText("10\n20\n30\n40")
    
    var yigindi = 0
    fayl.forEachLine { satr ->
        yigindi += satr.trim().toInt()
    }
    
    println("Qatorma-qator hisoblangan yig'indi: $yigindi")
    fayl.delete()
}
""",
    "forEachLine buferlangan o'quvchidan (BufferedReader) foydalanadi va har bir qatorni o'qib bo'lgach xotiradan bo'shatadi, natijada hatto gigabaytli fayllarda ham OutOfMemoryError xatosi yuz bermaydi.",
    """
Qatorma-qator hisoblangan yig'indi: 100
"""
)

# 857
add_task(
    857,
    "useLines { } orqali Sequence asosida faylni samarali filtrlash",
    "Fayl satrlarini dangasa ketma-ketlik (Sequence<String>) sifatida qabul qilib, faqat kerakli satrlarni ajratib oling.",
    """
import java.io.File

fun main() {
    val fayl = File("logs.txt")
    fayl.writeText("INFO: Tizim faol\nERROR: Ulanish uzildi\nINFO: Yangilanish\nERROR: Disk to'ldi")
    
    val xatolar = fayl.useLines { lines ->
        lines.filter { it.startsWith("ERROR") }.toList()
    }
    
    println("Topilgan xatoliklar: $xatolar")
    fayl.delete()
}
""",
    "useLines oqimni xavfsiz ochadi va yopadi, unga berilgan Sequence butun faylni bir vaqtda xotiraga olmasdan faqat kerakli qatorlarni filtrlaydi.",
    """
Topilgan xatoliklar: [ERROR: Ulanish uzildi, ERROR: Disk to'ldi]
"""
)

# 858
add_task(
    858,
    "delete() va deleteRecursively() orqali tozalash",
    "Yaratilgan papka va uning ichidagi barcha fayllarni deleteRecursively() yordamida bitta buyruq bilan o'chirib tashlang.",
    """
import java.io.File

fun main() {
    val papka = File("vaqtinchalik_katalog")
    papka.mkdirs()
    val ichkiFayl = File(papka, "test.txt")
    ichkiFayl.writeText("Sinov matni")
    
    println("Papka mavjudmi: ${papka.exists()}")
    println("Ichki fayl mavjudmi: ${ichkiFayl.exists()}")
    
    val ochirildi = papka.deleteRecursively()
    println("Barcha fayllar rekursiv o'chirildimi: $ochirildi")
    println("Papka endi mavjudmi: ${papka.exists()}")
}
""",
    "Oddiy delete() faqat bo'sh kataloglarni o'chira oladi. deleteRecursively() esa katalog ichidagi barcha fayl va ichki papkalarni to'liq tozalaydi.",
    """
Papka mavjudmi: true
Ichki fayl mavjudmi: true
Barcha fayllar rekursiv o'chirildimi: true
Papka endi mavjudmi: false
"""
)

# 859
add_task(
    859,
    "mkdirs() yordamida ichma-ich joylashgan kataloglar yaratish",
    "Bir necha qavatli ichma-ich papkalar yo'lini (masalan: app/data/cache) bitta amalda barpo eting.",
    """
import java.io.File

fun main() {
    val chuqurPapka = File("app/data/cache")
    val yaratildi = chuqurPapka.mkdirs()
    
    println("Papkalar zanjiri yaratildimi: $yaratildi")
    println("Mavjudligi: ${chuqurPapka.exists()}")
    
    File("app").deleteRecursively() // tozalash
}
""",
    "mkdirs() o'rtadagi barcha mavjud bo'lmagan ota kataloglarni ham birgalikda yaratadi, mkdir() esa faqat bitta oxirgi katalogni yarata oladi.",
    """
Papkalar zanjiri yaratildimi: true
Mavjudligi: true
"""
)

# 860
add_task(
    860,
    "copyTo() yordamida fayl nusxasini yaratish",
    "Bitta fayldan boshqa yangi faylga copyTo(overwrite = true) yordamida ma'lumotlarni ko'chiring.",
    """
import java.io.File

fun main() {
    val manba = File("manba.txt")
    val nusxa = File("nusxa.txt")
    manba.writeText("Asl ma'lumot 123")
    
    manba.copyTo(nusxa, overwrite = true)
    println("Nusxa tarkibi: ${nusxa.readText()}")
    
    manba.delete()
    nusxa.delete()
}
""",
    "copyTo() faylning to'liq nusxasini ko'chirib beradi. overwrite = true parametri agar nishon fayl mavjud bo'lsa uni ustiga yozishga ruxsat beradi.",
    """
Nusxa tarkibi: Asl ma'lumot 123
"""
)

# 861
add_task(
    861,
    "writeBytes() va readBytes() orqali ikkilik (binary) ma'lumotlar bilan ishlash",
    "Xom baytlar massivini (ByteArray) faylga yozib, qayta o'qib olishni namoyish eting.",
    """
import java.io.File

fun main() {
    val binarFayl = File("data.bin")
    val baytlar = byteArrayOf(0x4A, 0x56, 0x4D, 0x01, 0x02)
    
    binarFayl.writeBytes(baytlar)
    val oqilganBaytlar = binarFayl.readBytes()
    
    println("Yozilgan baytlar soni: ${oqilganBaytlar.size}")
    println("Birinchi bayt HEX: 0x${"%02X".format(oqilganBaytlar[0])}")
    
    binarFayl.delete()
}
""",
    "writeBytes va readBytes rasmlar, audio, siqilgan arxivlar yoki boshqa ikkilik fayllarni baytma-bayt uzatish uchun qo'llaniladi.",
    """
Yozilgan baytlar soni: 5
Birinchi bayt HEX: 0x4A
"""
)

# 862
add_task(
    862,
    "File.walkTopDown() orqali katalog daraxtini skanerlash",
    "Katalog ichidagi barcha fayllar va pastki kataloglarni yuqoridan pastga (top-down) qarab ko'rib chiquvchi dastur yozing.",
    """
import java.io.File

fun main() {
    val root = File("loyiha")
    File(root, "src/main").mkdirs()
    File(root, "build").mkdirs()
    File(root, "src/main/App.kt").writeText("fun main() {}")
    
    println("Katalog daraxti:")
    root.walkTopDown().forEach { f ->
        println("- ${f.path} (${if (f.isDirectory) "Papka" else "Fayl"})")
    }
    
    root.deleteRecursively()
}
""",
    "walkTopDown() FileTreeWalk ketma-ketligini qaytaradi. U ota katalogdan boshlab ichki fayllarga qarab iyerarxik aylanadi.",
    """
Katalog daraxti:
- loyiha (Papka)
- loyiha\\build (Papka)
- loyiha\\src (Papka)
- loyiha\\src\\main (Papka)
- loyiha\\src\\main\\App.kt (Fayl)
"""
)

# 863
add_task(
    863,
    "bufferedReader() va printWriter() bilan samarali ishlash",
    "Katta hajmdagi ma'lumotlarni oqim (stream) ko'rinishida buferlab yozish va o'qish usulini qo'llang.",
    """
import java.io.File

fun main() {
    val fayl = File("bufer_test.txt")
    
    fayl.printWriter().use { out ->
        out.println("1-qator bufer orqali")
        out.println("2-qator bufer orqali")
    }
    
    fayl.bufferedReader().use { reader ->
        val qator = reader.readLine()
        println("O'qilgan 1-qator: $qator")
    }
    
    fayl.delete()
}
""",
    "printWriter va bufferedReader katta hajmli ma'lumotlarni bo'laklab (buffer) uzatish orqali eng yuqori kirish-chiqish (I/O) tezligini ta'minlaydi.",
    """
O'qilgan 1-qator: 1-qator bufer orqali
"""
)

# 864
add_task(
    864,
    "AutoCloseable oqimlarda .use { } blokidan xavfsiz foydalanish",
    "Fayl oqimlari (InputStream/OutputStream) bilan ishlaganda xatolik yuz bersa ham oqimni kafolatli yopuvchi use { } kengaytmasini ko'rsating.",
    """
import java.io.File
import java.io.FileInputStream

fun main() {
    val fayl = File("test_use.txt")
    fayl.writeText("Xavfsiz yopilish sinovi")
    
    FileInputStream(fayl).use { input ->
        val birinchiBayt = input.read()
        println("Birinchi bayt ASCII: $birinchiBayt ('${birinchiBayt.toChar()}')")
    } // Bu yerda oqim avtomatik close() bo'ladi
    
    fayl.delete()
}
""",
    "use { } kengaytmasi Java dagi `try-with-resources` ning to'liq ekvivalenti bo'lib, har qanday AutoCloseable yoki Closeable obyektni xavfsiz yopadi.",
    """
Birinchi bayt ASCII: 88 ('X')
"""
)

# 865
add_task(
    865,
    "java.nio.file.Path va java.nio.file.Files bilan ishlash",
    "Zamonaviy Java NIO Path va Files yordamida fayl yo'llarini birlashtirish va matn yozishni amalga oshiring.",
    """
import java.nio.file.Paths
import java.nio.file.Files
import java.io.File

fun main() {
    val path = Paths.get("zamonaviy_fayl.txt")
    Files.writeString(path, "Java NIO va Kotlin uyg'unligi")
    
    val matn = Files.readString(path)
    println("NIO orqali o'qildi: $matn")
    
    Files.deleteIfExists(path)
}
""",
    "Java NIO (java.nio.file) zamonaviy va tezkor operatsion tizim chaqiruvlarini taqdim etadi va Kotlin bilan to'liq 100% integratsiyaga ega.",
    """
NIO orqali o'qildi: Java NIO va Kotlin uyg'unligi
"""
)

# 866
add_task(
    866,
    "Vaqtinchalik fayllar yaratish (createTempFile)",
    "Dastur ishlashi vaqtida kerak bo'ladigan va tizimning vaqtinchalik xotirasida (temp directory) saqlanuvchi fayl hosil qiling.",
    """
import kotlin.io.path.createTempFile
import kotlin.io.path.writeText
import kotlin.io.path.readText
import kotlin.io.path.deleteIfExists

fun main() {
    val tempPath = createTempFile(prefix = "antigravity_", suffix = ".tmp")
    tempPath.writeText("Vaqtinchalik kesh ma'lumotlari")
    
    println("Temp fayl yo'li mavjudmi: ${tempPath.toFile().exists()}")
    println("Tarkibi: ${tempPath.readText()}")
    
    tempPath.deleteIfExists()
    println("Temp fayl tozalandi: ${!tempPath.toFile().exists()}")
}
""",
    "createTempFile operatsion tizimning vaqtinchalik papkasida noyob nomli fayl yaratadi, bu parallel jarayonlarda nom to'qnashuvlarining oldini oladi.",
    """
Temp fayl yo'li mavjudmi: true
Tarkibi: Vaqtinchalik kesh ma'lumotlari
Temp fayl tozalandi: true
"""
)

# 867
add_task(
    867,
    "Fayl kengaytmasi va nomini ajratish (nameWithoutExtension, extension)",
    "Fayl yo'lidan uning kengaytmasini va asosiy nomini aniqlovchi qulay Kotlin xususiyatlaridan foydalaning.",
    """
import java.io.File

fun main() {
    val fayl = File("/data/reports/yillik_hisobot_2026.pdf")
    
    println("To'liq nomi: ${fayl.name}")
    println("Kengaytmasiz nomi: ${fayl.nameWithoutExtension}")
    println("Fayl formati (extension): ${fayl.extension}")
}
""",
    "Kotlin ning File klassiga qo'shgan nameWithoutExtension va extension kengaytmalari matnni qidirish yoki string split qilish ehtiyojini yo'qqa chiqaradi.",
    """
To'liq nomi: yillik_hisobot_2026.pdf
Kengaytmasiz nomi: yillik_hisobot_2026
Fayl formati (extension): pdf
"""
)

# 868
add_task(
    868,
    "Fayllarni hajmi bo'yicha saralab eng kattalarini topish",
    "Katalog ichidagi fayllarni ularning uzunligi (length) bo'yicha kamayish tartibida saralang.",
    """
import java.io.File

fun main() {
    val root = File("test_saralash")
    root.mkdirs()
    File(root, "kichik.txt").writeText("123")
    File(root, "orta.txt").writeText("1234567890")
    File(root, "katta.txt").writeText("123456789012345678901234567890")
    
    val saralanganFayllar = root.listFiles()
        ?.filter { it.isFile }
        ?.sortedByDescending { it.length() }
    
    saralanganFayllar?.forEach { f ->
        println("${f.name} -> ${f.length()} bayt")
    }
    
    root.deleteRecursively()
}
""",
    "sortedByDescending { it.length() } yordamida diskdagi eng ko'p joy egallagan fayllar ro'yxati aniqlanadi.",
    """
katta.txt -> 30 bayt
orta.txt -> 10 bayt
kichik.txt -> 3 bayt
"""
)

# 869
add_task(
    869,
    "Konfiguratsiya faylini (key=value) o'qib Map ga yuklash",
    "Standart .properties yoki .env fayllari kabi kalit=qiymat juftliklaridan iborat faylni tahlil qilib Map ga o'giring.",
    """
import java.io.File

fun main() {
    val configFile = File("app.env")
    configFile.writeText("APP_NAME=Antigravity\nPORT=8080\nDEBUG=true")
    
    val configMap = mutableMapOf<String, String>()
    configFile.forEachLine { line ->
        if (line.contains("=")) {
            val parts = line.split("=", limit = 2)
            configMap[parts[0].trim()] = parts[1].trim()
        }
    }
    
    println("Yuklangan sozlamalar: $configMap")
    println("Port raqami: ${configMap["PORT"]?.toInt()}")
    
    configFile.delete()
}
""",
    "forEachLine va split yordamida konfiguratsiya fayllari juda tez va sodda tarzda o'qiladi.",
    """
Yuklangan sozlamalar: {APP_NAME=Antigravity, PORT=8080, DEBUG=true}
Port raqami: 8080
"""
)

# 870
add_task(
    870,
    "Matn faylidagi barcha so'zlarni sanash (Word Count)",
    "Fayldagi umumiy so'zlar sonini va eng ko'p uchragan so'zni aniqlovchi dastur tuzing.",
    """
import java.io.File

fun main() {
    val fayl = File("matn.txt")
    fayl.writeText("Kotlin juda tez va Kotlin juda xavfsiz dasturlash tili")
    
    val sozlar = fayl.readText().lowercase().split(Regex("\\s+"))
    val umumiySon = sozlar.size
    val statistika = sozlar.groupingBy { it }.eachCount()
    
    println("Umumiy so'zlar soni: $umumiySon")
    println("So'zlar uchrash chastotasi: $statistika")
    
    fayl.delete()
}
""",
    "groupingBy va eachCount kolleksiya operatsiyalari matn tahlili va chastotaviy lug'at tuzishda keng qo'llaniladi.",
    """
Umumiy so'zlar soni: 8
So'zlar uchrash chastotasi: {kotlin=2, juda=2, tez=1, va=1, xavfsiz=1, dasturlash=1, tili=1}
"""
)

# 871
add_task(
    871,
    "kotlinx.serialization: @Serializable va Json.encodeToString",
    "Kotlin Data Class obyektini rasmiy kotlinx.serialization kutubxonasi yordamida JSON matniga o'giring.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class User(val id: Int, val name: String, val email: String)

fun main() {
    val user = User(1, "Anvar", "anvar@mail.uz")
    val jsonString = Json.encodeToString(user)
    
    println("JSON natijasi: $jsonString")
}
""",
    "@Serializable annotatsiyasi kompilyatsiya vaqtida maxsus serializer yaratadi (reflection ishlatmaydi). Json.encodeToString obyektni tezkor JSON matniga aylantiradi.",
    """
JSON natijasi: {"id":1,"name":"Anvar","email":"anvar@mail.uz"}
"""
)

# 872
add_task(
    872,
    "Json.decodeFromString orqali JSON matnidan obyekt tiklash",
    "JSON formatidagi matnni Json.decodeFromString yordamida Kotlin Data Class obyektiga aylantiring.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class Product(val title: String, val price: Double, val inStock: Boolean)

fun main() {
    val rawJson = "{\\"title\\":\\"Smartfon\\",\\"price\\":450.0,\\"inStock\\":true}"
    val product = Json.decodeFromString<Product>(rawJson)
    
    println("Tiklagan mahsulot: ${product.title}")
    println("Narxi: ${product.price} $, Omborda bormi: ${product.inStock}")
}
""",
    "decodeFromString generic parametr sifatida berilgan sinfga qarab JSON ni to'g'ridan-to'g'ri kuchli tipli (strongly typed) obyektga aylantiradi.",
    """
Tiklagan mahsulot: Smartfon
Narxi: 450.0 $, Omborda bormi: true
"""
)

# 873
add_task(
    873,
    "@SerialName orqali JSON kalit nomini o'zgartirish",
    "Serverdan kelayotgan snake_case (masalan user_registered_at) kalitini Kotlin ning camelCase maydoniga moslang.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName
import kotlinx.serialization.json.Json

@Serializable
data class Account(
    val username: String,
    @SerialName("created_at")
    val createdAt: String,
    @SerialName("is_active")
    val isActive: Boolean
)

fun main() {
    val json = "{\\"username\\":\\"samir\\",\\"created_at\\":\\"2026-01-01\\",\\"is_active\\":true}"
    val acc = Json.decodeFromString<Account>(json)
    
    println("Foydalanuvchi: ${acc.username}, Ro'yxatdan o'tgan: ${acc.createdAt}")
}
""",
    "@SerialName annotatsiyasi JSON dagi aniq kalit nomini belgilaydi, bu orqali Kotlin kodida toza nomlash standartlariga rioya qilish ta'minlanadi.",
    """
Foydalanuvchi: samir, Ro'yxatdan o'tgan: 2026-01-01
"""
)

# 874
add_task(
    874,
    "@Transient orqali maxfiy maydonlarni JSON ga kiritmaslik",
    "Foydalanuvchining maxfiy parolini JSON ga serializatsiya qilinishdan saqlovchi @Transient annotatsiyasini qo'llang.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.Transient
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class SecureUser(
    val login: String,
    @Transient
    val secretToken: String = "maxfiy_token_123"
)

fun main() {
    val user = SecureUser("admin_toshkent", "SuperSecret999")
    val json = Json.encodeToString(user)
    
    println("JSON da maxfiy ma'lumot yo'q: $json")
}
""",
    "@Transient bilan belgilangan maydonlar serializatsiya qilinmaydi va JSON ga chiqmaydi. Bunday maydon doimo standart qiymatga ega bo'lishi shart.",
    """
JSON da maxfiy ma'lumot yo'q: {"login":"admin_toshkent"}
"""
)

# 875
add_task(
    875,
    "ignoreUnknownKeys = true konfiguratsiyasi",
    "Serverdan kutilmagan ortiqcha JSON kalitlari kelganda xato bermasdan ularni o'tkazib yuboruvchi Json parametrini sozlang.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class Client(val name: String)

fun main() {
    val serverJson = "{\\"name\\":\\"Bobur\\",\\"extra_field_1\\":\\"abc\\",\\"extra_field_2\\":999}"
    
    val customJson = Json {
        ignoreUnknownKeys = true
    }
    
    val client = customJson.decodeFromString<Client>(serverJson)
    println("Mijoz nomi: ${client.name}")
}
""",
    "Odatiy holatda noma'lum kalit kelsa kotlinx.serialization SerializationException tashlaydi. ignoreUnknownKeys = true API versiyalari o'zgarganda ilovani barqaror qiladi.",
    """
Mijoz nomi: Bobur
"""
)

# 876
add_task(
    876,
    "prettyPrint = true orqali chiroyli JSON formatlash",
    "JSON natijasini odam o'qishi uchun qulay bo'lgan probel va satrlarga ajratilgan shaklda chiqaring.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class ServerConfig(val host: String, val port: Int)

fun main() {
    val config = ServerConfig("127.0.0.1", 8080)
    
    val prettyJson = Json {
        prettyPrint = true
    }
    
    val formatted = prettyJson.encodeToString(config)
    println(formatted)
}
""",
    "prettyPrint = true konfiguratsiyasi diskka konfiguratsiya yozish yoki loglarni ko'rishda formatlangan ko'rinish beradi.",
    """
{
    "host": "127.0.0.1",
    "port": 8080
}
"""
)

# 877
add_task(
    877,
    "encodeDefaults = true orqali standart qiymatlarni ham chiqarish",
    "Data class da mavjud bo'lgan defolt qiymatlarni JSON da tushirib qoldirmasdan to'liq chiqarishni sozlang.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Setting(val theme: String = "dark", val notifications: Boolean = true)

fun main() {
    val setting = Setting()
    
    val customJson = Json {
        encodeDefaults = true
    }
    
    println("Defoltlar bilan JSON: ${customJson.encodeToString(setting)}")
}
""",
    "encodeDefaults = true bo'lmasa, kotlinx.serialization standart qiymatga teng bo'lgan maydonlarni JSON hajmini tejash uchun chiqarmasligi mumkin.",
    """
Defoltlar bilan JSON: {"theme":"dark","notifications":true}
"""
)

# 878
add_task(
    878,
    "explicitNulls = false orqali null qiymatlarni JSON da qisqartirish",
    "Qiymati null bo'lgan maydonlarni JSON matniga chiqarmaslik orqali trafikni tejash parametrini sozlang.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Profile(val username: String, val bio: String? = null)

fun main() {
    val p = Profile("bekzod", null)
    
    val compactJson = Json {
        explicitNulls = false
    }
    
    println("Null chiqarilmagan JSON: ${compactJson.encodeToString(p)}")
}
""",
    "explicitNulls = false parametrida `bio: null` JSON kaliti chiqarilmaydi va tarmoq trafigi qisqaradi.",
    """
Null chiqarilmagan JSON: {"username":"bekzod"}
"""
)

# 879
add_task(
    879,
    "Kolleksiyalarni (List<T>) JSON ga serializatsiya qilish va tiklash",
    "Bir nechta obyektlardan iborat List to'plamini JSON massiviga o'girish va qayta o'qish dasturini yozing.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Item(val id: Int, val title: String)

fun main() {
    val items = listOf(Item(1, "Qalam"), Item(2, "Daftar"))
    val json = Json.encodeToString(items)
    println("JSON massiv: $json")
    
    val parsedList = Json.decodeFromString<List<Item>>(json)
    println("Qayta tiklangan ro'yxat hajmi: ${parsedList.size}")
}
""",
    "kotlinx.serialization List, Set va Map kolleksiyalarini avtomatik taniy oladi va ularning elementlarini to'g'ri serializatsiya qiladi.",
    """
JSON massiv: [{"id":1,"title":"Qalam"},{"id":2,"title":"Daftar"}]
Qayta tiklangan ro'yxat hajmi: 2
"""
)

# 880
add_task(
    880,
    "Lug'at (Map<String, T>) ni JSON ga serializatsiya qilish",
    "Lug'at to'plamini kalit-qiymat ko'rinishidagi JSON obyektiga o'giring.",
    """
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

fun main() {
    val scores = mapOf("Ali" to 95, "Vali" to 88, "Zafar" to 100)
    val json = Json.encodeToString(scores)
    println("Map JSON: $json")
    
    val restored = Json.decodeFromString<Map<String, Int>>(json)
    println("Vali bali: ${restored["Vali"]}")
}
""",
    "String kalitli Map to'g'ridan-to'g'ri JSON obyektiga (`{ \"Ali\": 95, ... }`) aylanadi.",
    """
Map JSON: {"Ali":95,"Vali":88,"Zafar":100}
Vali bali: 88
"""
)

# 881
add_task(
    881,
    "Ichma-ich (nested) data class larni serializatsiya qilish",
    "Foydalanuvchi va uning manzilidan iborat murakkab iyerarxik obyektni JSON ga o'giring.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Address(val city: String, val street: String)

@Serializable
data class Employee(val name: String, val address: Address)

fun main() {
    val emp = Employee("Rustam", Address("Toshkent", "Amir Temur shoh ko'chasi"))
    val json = Json.encodeToString(emp)
    println("Iyerarxik JSON: $json")
}
""",
    "Ichma-ich joylashgan barcha sinflar @Serializable bilan belgilangan bo'lsa, serializer butun daraxtni to'liq JSON obyektlariga aylantiradi.",
    """
Iyerarxik JSON: {"name":"Rustam","address":{"city":"Toshkent","street":"Amir Temur shoh ko'chasi"}}
"""
)

# 882
add_task(
    882,
    "Sealed class larni polimorfik serializatsiya qilish",
    "Sealed iyerarxiyasini JSON ga o'girganda avtomatik 'type' diskriminatori qo'shilishini namoyish eting.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
sealed interface PaymentMethod {
    @Serializable
    data class Card(val cardNumber: String) : PaymentMethod
    @Serializable
    data class Cash(val currency: String) : PaymentMethod
}

fun main() {
    val payment: PaymentMethod = PaymentMethod.Card("8600-1234-5678-9012")
    val json = Json.encodeToString(payment)
    println("Polimorfik JSON: $json")
    
    val restored = Json.decodeFromString<PaymentMethod>(json)
    println("Tiklagan tur: ${restored.javaClass.simpleName}")
}
""",
    "kotlinx.serialization sealed klasslar uchun avtomatik `type` maydonini hosil qiladi va tiklash paytida to'g'ri subklassga o'giradi.",
    """
Polimorfik JSON: {"type":"PaymentMethod.Card","cardNumber":"8600-1234-5678-9012"}
Tiklagan tur: Card
"""
)

# 883
add_task(
    883,
    "Faylga JSON obyekti saqlash va fayldan tiklash",
    "File operatsiyalari va kotlinx.serialization ni birlashtirib, obyektni faylga saqlab qayta o'quvchi xizmat yozing.",
    """
import java.io.File
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class AppState(val version: String, val lastLogin: Long)

fun main() {
    val file = File("app_state.json")
    val state = AppState("2.0.0", System.currentTimeMillis())
    
    file.writeText(Json.encodeToString(state))
    println("Faylga saqlandi: ${file.readText()}")
    
    val loadedState = Json.decodeFromString<AppState>(file.readText())
    println("Fayldan tiklangan versiya: ${loadedState.version}")
    
    file.delete()
}
""",
    "Fayl va JSON integratsiyasi mahalliy sozlamalar (settings) va kesh ma'lumotlarini saqlashning eng ommabop usulidir.",
    """
Faylga saqlandi: {"version":"2.0.0","lastLogin":~}
Fayldan tiklangan versiya: 2.0.0
"""
)

# 884
add_task(
    884,
    "CSV faylini o'qib, uni Data Class ro'yxatiga o'girish",
    "Vergul bilan ajratilgan (CSV) formatdagi fayldan foydalanuvchilar ro'yxatini hosil qiling.",
    """
import java.io.File

data class CsvUser(val id: Int, val name: String, val city: String)

fun main() {
    val csvFile = File("users.csv")
    csvFile.writeText("id,name,city\n1,Alisher,Samarqand\n2,Nodira,Toshkent")
    
    val userList = csvFile.useLines { lines ->
        lines.drop(1) // sarlavhani tashlab yuborish
            .map { line ->
                val cols = line.split(",")
                CsvUser(cols[0].toInt(), cols[1], cols[2])
            }.toList()
    }
    
    println("CSV dan olingan foydalanuvchilar soni: ${userList.size}")
    userList.forEach { println("- ${it.name} (${it.city})") }
    
    csvFile.delete()
}
""",
    "CSV fayllarni qatorma-qator o'qib bo'laklash (split) va xotiradagi modellashtirilgan sinflarga aylantirish sodda va qulay.",
    """
CSV dan olingan foydalanuvchilar soni: 2
- Alisher (Samarqand)
- Nodira (Toshkent)
"""
)

# 885
add_task(
    885,
    "Data Class ro'yxatini CSV formatida faylga eksport qilish",
    "Kolleksiyadagi ma'lumotlarni CSV formatidagi matnli faylga yozib bering.",
    """
import java.io.File

data class Book(val isbn: String, val title: String, val price: Double)

fun main() {
    val books = listOf(
        Book("978-1", "O'tkan Kunlar", 45000.0),
        Book("978-2", "Mehrobdan Chayon", 42000.0)
    )
    
    val outFile = File("books_export.csv")
    outFile.printWriter().use { writer ->
        writer.println("ISBN,Title,Price")
        books.forEach { b ->
            writer.println("${b.isbn},${b.title},${b.price}")
        }
    }
    
    println("Eksport qilingan CSV:")
    println(outFile.readText().trim())
    outFile.delete()
}
""",
    "printWriter yordamida sarlavha va ma'lumot qatorlari CSV formatida chiroyli eksport qilinadi.",
    """
Eksport qilingan CSV:
ISBN,Title,Price
978-1,O'tkan Kunlar,45000.0
978-2,Mehrobdan Chayon,42000.0
"""
)

# 886
add_task(
    886,
    "Log faylini tahlil qilib xatoliklar (ERROR) sonini hisoblash",
    "Audit log faylidagi qatorlarni sanab, nechta ERROR va nechta WARN borligini hisoblang.",
    """
import java.io.File

fun main() {
    val log = File("server.log")
    log.writeText("INFO: Ishga tushdi\nWARN: Xotira kam qoldi\nERROR: Ulanish uzildi\nERROR: DB xatosi")
    
    var errorCount = 0
    var warnCount = 0
    
    log.forEachLine { line ->
        if (line.startsWith("ERROR")) errorCount++
        if (line.startsWith("WARN")) warnCount++
    }
    
    println("Jami ERROR: $errorCount ta, Jami WARN: $warnCount ta")
    log.delete()
}
""",
    "Fayllarni qatorma-qator tahlil qilish orqali xizmat jurnallaridagi nosozliklar statistikasi osongina chiqariladi.",
    """
Jami ERROR: 2 ta, Jami WARN: 1 ta
"""
)

# 887
add_task(
    887,
    "Faylni Base64 shifrlab saqlash va qayta tiklash",
    "Matnni Base64 algoritmi bilan kodlab faylga yozish va qayta dekodlash dasturini yozing.",
    """
import java.io.File
import java.util.Base64

fun main() {
    val original = "O'zbekiston - kelajagi buyuk davlat"
    val encoded = Base64.getEncoder().encodeToString(original.toByteArray())
    
    val file = File("secret.b64")
    file.writeText(encoded)
    
    val fromFile = file.readText()
    val decoded = String(Base64.getDecoder().decode(fromFile))
    
    println("Shifrlangan matn: $fromFile")
    println("Qayta tiklangan matn: $decoded")
    
    file.delete()
}
""",
    "Base64 kodlash baytlarni ASCII formatida xavfsiz saqlash va uzatish imkonini beradi.",
    """
Shifrlangan matn: Tyd6YmVraXN0b24gLSBrZWxhamFnaSBidXl1ayBkYXZsYXQ=
Qayta tiklangan matn: O'zbekiston - kelajagi buyuk davlat
"""
)

# 888
add_task(
    888,
    "JSON massivini qatorma-qator faylga yozish (NDJSON formati)",
    "Har bir JSON obyektini alohida qatorda saqlovchi (Newline Delimited JSON) formatini yarating.",
    """
import java.io.File
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Event(val id: Int, val name: String)

fun main() {
    val events = listOf(Event(1, "Boshlanish"), Event(2, "Yuklanish"), Event(3, "Yakun"))
    val ndjsonFile = File("events.ndjson")
    
    ndjsonFile.printWriter().use { writer ->
        events.forEach { e ->
            writer.println(Json.encodeToString(e))
        }
    }
    
    println("NDJSON tarkibi:")
    println(ndjsonFile.readText().trim())
    ndjsonFile.delete()
}
""",
    "NDJSON formati katta hajmdagi voqealar (events) oqimini butun faylni ochmasdan qatorma-qator o'qish uchun juda samarali hisoblanadi.",
    """
NDJSON tarkibi:
{"id":1,"name":"Boshlanish"}
{"id":2,"name":"Yuklanish"}
{"id":3,"name":"Yakun"}
"""
)

# 889
add_task(
    889,
    "JSON formatlash validatsiyasi va xatoliklarni ushlash",
    "Buzilgan JSON matni kelganda SerializationException ni ushlab xavfsiz xabar qaytaring.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.SerializationException

@Serializable
data class Config(val timeout: Int)

fun main() {
    val invalidJson = "{\\"timeout\\": \\"not_a_number\\"}"
    
    try {
        Json.decodeFromString<Config>(invalidJson)
    } catch (e: SerializationException) {
        println("JSON formati noto'g'ri: ${e.message}")
    }
}
""",
    "SerializationException JSON tiplari va Kotlin xususiyatlari mos kelmaganda yuzaga keladi va try-catch orqali xavfsiz boshqariladi.",
    """
JSON formati noto'g'ri: Failed to parse type 'Int' for input 'not_a_number'
"""
)

# 890
add_task(
    890,
    "Fayllarni oxirgi tahrirlangan vaqti bo'yicha saralash",
    "File.lastModified() xususiyatidan foydalanib, eng yangi faylni aniqlang.",
    """
import java.io.File

fun main() {
    val f1 = File("eski.txt")
    f1.writeText("Eski")
    Thread.sleep(50L)
    val f2 = File("yangi.txt")
    f2.writeText("Yangi")
    
    val files = listOf(f1, f2)
    val latest = files.maxByOrNull { it.lastModified() }
    
    println("Eng so'nggi yangilangan fayl: ${latest?.name}")
    
    f1.delete()
    f2.delete()
}
""",
    "lastModified() millisekundlarda oxirgi o'zgartirish vaqtini qaytaradi va keshni eskirganini tekshirishda ishlatiladi.",
    """
Eng so'nggi yangilangan fayl: yangi.txt
"""
)

# 891
add_task(
    891,
    "Fayldagi so'zlarni almashtirish (Search & Replace in File)",
    "Fayl ichidagi eski matnni yangisiga almashtirib qayta saqlang.",
    """
import java.io.File

fun main() {
    val file = File("matn_almashtir.txt")
    file.writeText("Java yaxshi til, lekin Kotlin undan ancha qulay!")
    
    val text = file.readText()
    val updated = text.replace("Java", "Eski til")
    file.writeText(updated)
    
    println("Yangilangan fayl: ${file.readText()}")
    file.delete()
}
""",
    "readText(), replace() va writeText() yordamida fayl ichidagi matnlarni tezkor almashtirish amalga oshiriladi.",
    """
Yangilangan fayl: Eski til yaxshi til, lekin Kotlin undan ancha qulay!
"""
)

# 892
add_task(
    892,
    "isLenient = true parametri orqali noaniq JSON larni qabul qilish",
    "Qo'shtirnoqsiz kalitlar yoki yumshoq sintaksisdagi JSON larni isLenient parametri orqali muvaffaqiyatli o'qish.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class FlexibleData(val key: String)

fun main() {
    val lenientJson = Json { isLenient = true }
    // Qoidaga to'liq rioya qilmagan JSON
    val raw = "{ key: 'qiymat' }"
    
    val res = lenientJson.decodeFromString<FlexibleData>(raw)
    println("Yumshoq o'qilgan natija: ${res.key}")
}
""",
    "isLenient = true qat'iy bo'lmagan, kotirovkalarsiz yozilgan yoki nostandart JSON matnlarini o'qish imkonini beradi.",
    """
Yumshoq o'qilgan natija: qiymat
"""
)

# 893
add_task(
    893,
    "coerceInputValues = true orqali noma'lum enum qiymatini boshlang'ichga o'tkazish",
    "Serverdan noma'lum enum kelganda xato bermasdan boshlang'ich default qiymatga tushirish.",
    """
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

enum class UserRole { USER, ADMIN, UNKNOWN }

@Serializable
data class RoleData(val role: UserRole = UserRole.UNKNOWN)

fun main() {
    val json = Json { coerceInputValues = true }
    val incoming = "{\\"role\\":\\"SUPER_USER\\"}"
    
    val data = json.decodeFromString<RoleData>(incoming)
    println("Qabul qilingan xavfsiz rol: ${data.role}")
}
""",
    "coerceInputValues = true yangi yoki mos kelmaydigan qiymatlarni avtomatik ravishda Data Class dagi standart qiymatga qaytaradi.",
    """
Qabul qilingan xavfsiz rol: UNKNOWN
"""
)

# 894
add_task(
    894,
    "Fayl tizimida qidiruv: kengaytmasi bo'yicha fayllarni saralash",
    "Katalog ichidagi barcha '.kt' kengaytmali fayllarni topuvchi filtr dastur yozing.",
    """
import java.io.File

fun main() {
    val dir = File("kodlar")
    dir.mkdirs()
    File(dir, "Main.kt").writeText("")
    File(dir, "Utils.kt").writeText("")
    File(dir, "README.md").writeText("")
    
    val kotlinFiles = dir.listFiles { _, name -> name.endsWith(".kt") }
    println("Topilgan Kotlin fayllari:")
    kotlinFiles?.forEach { println("- ${it.name}") }
    
    dir.deleteRecursively()
}
""",
    "listFiles(FilenameFilter) filtri faqat mos keladigan nomga ega fayllarni qaytaradi.",
    """
Topilgan Kotlin fayllari:
- Main.kt
- Utils.kt
"""
)

# 895
add_task(
    895,
    "Ob-havo stansiyasi ma'lumotlarini JSON faylida arxivlash",
    "Har kungi ob-havo o'lchovlarini JSON formatida faylga saqlovchi arxivator yarating.",
    """
import java.io.File
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class WeatherRecord(val city: String, val tempC: Double, val date: String)

fun main() {
    val archive = File("weather_archive.json")
    val data = listOf(
        WeatherRecord("Toshkent", 28.5, "2026-06-15"),
        WeatherRecord("Samarqand", 26.0, "2026-06-15")
    )
    
    archive.writeText(Json { prettyPrint = true }.encodeToString(data))
    println("Ob-havo arxivi saqlandi: ${archive.length()} bayt")
    println(archive.readText().trim())
    
    archive.delete()
}
""",
    "Massiv ko'rinishidagi yozuvlarni prettyPrint bilan saqlash tahlil va saqlash uchun juda qulay.",
    """
Ob-havo arxivi saqlandi: ~ bayt
[
    {
        "city": "Toshkent",
        "tempC": 28.5,
        "date": "2026-06-15"
    },
    {
        "city": "Samarqand",
        "tempC": 26.0,
        "date": "2026-06-15"
    }
]
"""
)

# 896
add_task(
    896,
    "Fayldan faqat juft sonlarni o'qib yangi faylga yozish",
    "Katta raqamlar ro'yxatidan faqat juftlarini saralab boshqa faylga o'tkazing.",
    """
import java.io.File

fun main() {
    val input = File("barcha_sonlar.txt")
    val output = File("juft_sonlar.txt")
    input.writeText("1\n2\n3\n4\n5\n6")
    
    output.printWriter().use { writer ->
        input.forEachLine { line ->
            val num = line.trim().toInt()
            if (num % 2 == 0) writer.println(num)
        }
    }
    
    println("Saralangan juft sonlar: ${output.readLines()}")
    input.delete()
    output.delete()
}
""",
    "forEachLine va printWriter kombinatsiyasi xotirani ortiqcha band qilmasdan ma'lumotlarni filtrlab yangi faylga ko'chiradi.",
    """
Saralangan juft sonlar: [2, 4, 6]
"""
)

# 897
add_task(
    897,
    "Fayl nomini o'zgartirish (renameTo)",
    "Fayl nomini eski nomdan yangi nomga renameTo() yordamida o'zgartiring.",
    """
import java.io.File

fun main() {
    val oldFile = File("eski_nom.txt")
    val newFile = File("yangi_nom.txt")
    oldFile.writeText("Fayl tarkibi")
    
    val muvaffaqiyat = oldFile.renameTo(newFile)
    println("Nom o'zgardimi: $muvaffaqiyat")
    println("Eski fayl mavjudmi: ${oldFile.exists()}")
    println("Yangi fayl mavjudmi: ${newFile.exists()}")
    
    newFile.delete()
}
""",
    "renameTo() fayl nomini tezkor o'zgartiradi yoki boshqa katalogga ko'chiradi.",
    """
Nom o'zgardimi: true
Eski fayl mavjudmi: false
Yangi fayl mavjudmi: true
"""
)

# 898
add_task(
    898,
    "Fayl satrlarini teskari tartibda saqlash (Reversed File)",
    "Fayl ichidagi barcha qatorlarni teskari tartibda (oxiridan boshiga) qayta yozuvchi algoritm tuzing.",
    """
import java.io.File

fun main() {
    val f = File("tartib.txt")
    f.writeText("1-qator\n2-qator\n3-qator")
    
    val teskari = f.readLines().reversed()
    f.writeText(teskari.joinToString("\n"))
    
    println("Teskari tartibdagi fayl:")
    println(f.readText())
    
    f.delete()
}
""",
    "readLines().reversed() fayl satrlarini teskari qilib joinToString orqali qayta yozadi.",
    """
Teskari tartibdagi fayl:
3-qator
2-qator
1-qator
"""
)

# 899
add_task(
    899,
    "Bo'sh papkalarni aniqlash va o'chirish",
    "Katalog ichidagi bo'sh papkalarni aniqlab, ularni xavfsiz o'chiruvchi dastur tuzing.",
    """
import java.io.File

fun main() {
    val boshPapka = File("bosh_papka")
    boshPapka.mkdirs()
    
    val ichkiFayllar = boshPapka.listFiles()
    if (ichkiFayllar != null && ichkiFayllar.isEmpty()) {
        println("Papka bo'sh ekanligi aniqlandi, o'chirilmoqda...")
        boshPapka.delete()
    }
    
    println("Papka mavjudmi: ${boshPapka.exists()}")
}
""",
    "listFiles() massivi bo'sh bo'lsa (isEmpty), papka ichida hech narsa yo'qligini bildiradi va oddiy delete() bilan o'chirish mumkin.",
    """
Papka bo'sh ekanligi aniqlandi, o'chirilmoqda...
Papka mavjudmi: false
"""
)

# 900
add_task(
    900,
    "18-qism xulosasi: To'liq fayl boshqaruvi va JSON asosidagi mini ma'lumotlar bazasi",
    "Faylga JSON orqali ma'lumot qo'shish (insert), o'qish (select) va ID bo'yicha qidirish imkonini beruvchi to'liq faylli ma'lumotlar bazasi dvigatelini yarating.",
    """
import java.io.File
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

@Serializable
data class Article(val id: Int, val title: String, val author: String)

class JsonFileDatabase(private val file: File) {
    private val json = Json { prettyPrint = true; ignoreUnknownKeys = true }
    
    init {
        if (!file.exists()) {
            file.writeText("[]")
        }
    }
    
    fun getAll(): List<Article> {
        val text = file.readText()
        return json.decodeFromString(text)
    }
    
    fun insert(article: Article) {
        val current = getAll().toMutableList()
        current.add(article)
        file.writeText(json.encodeToString(current))
    }
    
    fun findById(id: Int): Article? {
        return getAll().find { it.id == id }
    }
}

fun main() {
    val dbFile = File("articles_db.json")
    val db = JsonFileDatabase(dbFile)
    
    db.insert(Article(1, "Kotlin 2.0 yangiliklari", "Alisher"))
    db.insert(Article(2, "Jetpack Compose asoslari", "Madina"))
    
    println("Bazada jami maqolalar: ${db.getAll().size} ta")
    val topilgan = db.findById(2)
    println("ID #2 topildi: ${topilgan?.title} (${topilgan?.author})")
    
    dbFile.delete() // Tozalash
}
""",
    "Ushbu yakuniy modulda kotlin.io (writeText, readText) va kotlinx.serialization imkoniyatlari to'liq birlashtirilib, mustaqil ishlaydigan faylli mini ma'lumotlar bazasi dvigateli (JSON Database Engine) amalga oshirildi.",
    """
Bazada jami maqolalar: 2 ta
ID #2 topildi: Jetpack Compose asoslari (Madina)
"""
)

save_file("kotlin_18_fayllar_va_serialization.md", tasks)
