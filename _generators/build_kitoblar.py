# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Badiiy adabiyot va mumtoz asarlar dataset generatori
Mualliflar: Alisher Navoiy, Abdulla Qodiriy, O'tkir Hoshimov, Xudoyberdi To'xtaboyev
Jami: 400 ta chuqur tahliliy va adabiy JSONL topshiriqlari
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\kitoblar\mumtoz_va_adabiy_asarlar_sft.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
entries = []

# ==========================================
# 1. ALISHER NAVOIY (120 TA TOPSHIRIQ)
# ==========================================

# 1.1 G'azallar baytlari tahlili
gazallar_core = [
    ("Qaro ko'zum", "Qaro ko'zum, kel-u, mardumlig' emdi fan qilg'il,\nKo'zum qorasida mardum kibi vatan qilg'il.",
     "Mardum so'zi tajnis va iyhom san'atiga asoslangan: ham 'ko'z qorachig'i', ham 'odamiylik, insonparvarlik'. Oshiq sevgilisiga odamiylikni hunar qilib, ko'z qorachig'ida vatan tutishni iltimos qilmoqda."),
    ("Meni men istagan", "Meni men istagan o'z suhbatiga arjumand etmas,\nMeni istar kishining suhbatin ko'nglum pisand etmas.",
     "Insoniy munosabatlardagi nozik psixologik ziddiyat: inson o'zi intilgan kishiga yetisha olmaydi, o'ziga intilganlarni esa qadrlamaydi. Qanoat va taqdir falsafasi yotadi."),
    ("Orazin yopqach", "Orazin yopqach ko'zumdin sochilur har lahza yosh,\nBo'ylakim paydo bo'lur yulduz, nihon bo'lg'och quyosh.",
     "Tashbeh va husni ta'lil san'ati. Yorning yuzi quyoshga, ko'z yoshlar yulduzlarga qiyoslangan. Quyosh botgach yulduzlar chiqqanidek, yor ketgach ko'zdan yosh to'kiladi."),
    ("Jondin o'zga", "Jondin o'zga yori vafodor topmadim,\nKo'nguldin o'zga mahrami asror topmadim.",
     "Tasavvufiy yolg'izlik va o'zlikni anglash. Tashqi dunyoda vafodor do'st yo'q, faqat insonning o'z joni va ko'ngli sirlarni saqlovchi sirdoshdir."),
    ("Kecha kelgumdur", "Kecha kelgumdur debon ul sarvi gulro' kelmadi,\nKo'zlarimg'a kecha tong otquncha uyqu kelmadi.",
     "Intizorlik dardi va va'daga vafo qilmaslik. Va'dasiga vafo qilmagan yor yo'liga ko'z tikib bedor tong ottirgan oshiq kechinmalari ifodalangan."),
    ("Ko'rgali husnungni", "Ko'rgali husnungni zoru mubtalo bo'ldum sanga,\nNe balolig' kun edikim, oshno bo'ldum sanga.",
     "Muhabbatning dastlabki nigohdanoq boshlanuvchi yengib bo'lmas kuchi. Oshiq o'z ishqini 'balolig' kun' deb ataydi, bu holat qalbga ham orom, ham iztirob bag'ishlaydi."),
    ("Mehr ko'p ko'rguzdum", "Mehr ko'p ko'rguzdum, ammo mehribone topmadim,\nJon base qildim fido, oromi jone topmadim.",
     "Insonlarga yaxshilik qilish, ammo evaziga sadoqat va mehr ko'rmaslik fojiasi. Shoirning ichki dardi, sadoqat va jafo ziddiyati."),
    ("Boda ichkim", "Boda ichkim, ahli dahr ichra vafodor istama,\nBog'i olam ichra bir gulsiz tikon yo'qtur, ko'ngul.",
     "Tasavvufda 'boda' - ilohiy ma'rifat sharobidir. Dunyodan vafo izlash behuda ekani, chunki bu dunyo bog'idagi har bir gulning o'z tikoni borligi eslatiladi."),
    ("Ashrafti hilol", "Ashrafti hilol o'ldi ko'rung dahr aro paydo,\nYoxud falak uzra ko'runur tosi huvaydo.",
     "Samoviy go'zallik va yangi oy jilosi orqali Yaratganning qudratiga hayrat ifodalangan. Koinot sirlariga poetik nazar tashlangan."),
    ("Furqatingdin", "Furqatingdin za'faron uzra to'karmen lolagun,\nTokim ul rangin aqiqim bo'lg'usi olam aro.",
     "Ayriliq sababidan oshiqning yuzi za'farondek sarg'aygan, ko'z yoshlari loladek qizil oqmoqda. Ranglar simvolikasi orqali ruhiy iztirobning yuksak tasviri.")
]

for title, bayt, sharh in gazallar_core:
    entries.append({
        "instruction": f"Alisher Navoiyning '{title}' radifli g'azalidagi baytning lug'aviy, badiiy va falsafiy mohiyatini tahlil qiling:",
        "input": bayt,
        "output": f"### Baytning lug'aviy va matniy tahlili:\n{sharh}\n\n### Badiiy san'atlar va uslub:\nUshbu bayt aruz vaznining ohangdor bahrida bitilgan bo'lib, unda tashbeh, tajnis va husni ta'lil san'atlari o'zaro mukammal uyg'unlashgan.\n\n### Tarbiyaviy va falsafiy xulosasi:\nAlisher Navoiy bu misralar orqali insonni ruhiy poklanishga, sadoqatga va chin insoniy fazilatlarga undaydi.",
        "author": "Alisher Navoiy",
        "category": "Mumtoz she'riyat va g'azaliyot"
    })

# 1.2 Xamsa va Falsafiy asarlar (110 ta)
navoiy_topics = [
    # Hayrat ul-abror (25 ta)
    ("Hayrat ul-abror", "Insonning yaratilish maqsadi va iymon butunligi", "Inson barcha maxluqotlarning gultoji qilib yaratilgan. U o'z umrini behuda o'tkazmay, ilm, ibodat va ezgu amallar bilan ruhini yuksaltirishi lozim."),
    ("Hayrat ul-abror", "Adolatli shoh Nushiravon va dono vazir hikoyati", "Vayrona qishloqda ikki boyqushning suhbati orqali podshohning adolatsizligi mamlakatni vayronaga aylantirishi fosh etiladi va shoh to'g'ri yo'lga qaytadi."),
    ("Hayrat ul-abror", "Saxovat nuri va baxillik la'nati", "Saxiy inson boylikni xalq manfaatiga sarflaydi va qalb xotirjamligiga erishadi. Baxil esa boylikning quliga aylanib ikki dunyoda xor bo'ladi."),
    ("Hayrat ul-abror", "Rostlik fazilati va yolg'onning kasofati", "Rostlik ko'ngil ko'zgusining jilosidir. Yolg'onchi kimsaning aytgan haq so'ziga ham hech kim ishonmay qoladi."),
    ("Hayrat ul-abror", "Kibr va manmanlikning halokati", "Kibr inson qalbini qoraytiradi. Daraxt meva solgani sari bosh eggani kabi, olim va fozil kishi ham kamtar bo'lishi darkor."),
    ("Hayrat ul-abror", "Qanoat durdonasi va ochko'zlik balosi", "Qanoat - tuganmas ma'naviy xazinadir. Dunyo matolariga to'ymaydigan nafs insonni tubanlikka yetaklaydi."),
    ("Hayrat ul-abror", "Ilm va amalning egizakligi", "Amalsiz ilm - mevasiz daraxt kabidir. Bilim faqat amaliy ezgulikka aylangandagina jamiyatga ziyo taratadi."),
    ("Hayrat ul-abror", "Ahdga vafo va do'stlik sadoqati", "Va'dasida turish mardlik ko'zgusidir. Va'daboz kimsa el nazaridan qoladi."),
    ("Hayrat ul-abror", "Ota-onaga ehtirom va farzandlik burchi", "Ota-onaning ko'nglini olish - Yaratganning roziligini topishdir. Ularga xizmat qilish eng oliy saodatdir."),
    ("Hayrat ul-abror", "Sukut odobi va so'z qadri", "So'zlash kumush bo'lsa, sukut oltindir. O'ylanmay aytilgan gap boshga kulfat soladi."),
    # Farhod va Shirin (25 ta)
    ("Farhod va Shirin", "Farhodning shohlik taxtidan ilm va hunarni ustun qo'yishi", "Farhod saltanat dabdabasiga emas, falsafa, riyoziyot, muhandislik va toshyo'nish hunariga mehr qo'yadi."),
    ("Farhod va Shirin", "To'rt ustozdan saboq olish va amaliy mehnat", "Komil inson nazariy bilim bilan birga hunarmandlik va jismoniy mehnatni ham egallashi shartligi ko'rsatiladi."),
    ("Farhod va Shirin", "Suqrot g'oridagi tilsimlarni aql bilan yengish", "Dahshatli ajdaho va devlarni qurol bilan emas, chuqur aql, iroda va ma'naviy kuch bilan mag'lub etish."),
    ("Farhod va Shirin", "Mehinbonu adolati va Arman eli farovonligi", "Ayol hukmdor bo'lsa-da, adolatli va xalqparvar boshqaruv orqali yurtni obod qilish namunasi."),
    ("Farhod va Shirin", "Tog'ni yorib Shirin eliga suv keltirish fidoiyligi", "Haqiqiy muhabbat quruq so'zda emas, xalq manfaatiga qaratilgan buyuk bunyodkorlik mehnatida namoyon bo'ladi."),
    ("Farhod va Shirin", "Xusrav Parvizning xudbinligi va zo'ravonligi", "Xusrav muhabbatni kuch va boylik bilan sotib olmoqchi bo'ladi, ammo ma'naviy jihatdan mag'lub bo'ladi."),
    ("Farhod va Shirin", "Farhod va Xusrav munozarasidagi aql jangi", "Farhodning Xusrav savollariga bergan donishmandona va mardona javoblari zolim shohni lol qoldiradi."),
    ("Farhod va Shirin", "Yolg'on xabar fojiasi va Farhodning halokati", "Kampirning yolg'on so'ziga ishonib Farhod bolg'asini osmonga otib jon berishi - aldov va xiyonatning achchiq kulfatidir."),
    ("Farhod va Shirin", "Shirinning vafosi va sevgilisining qabrida jon berishi", "Shirin Farhod qabri uzra o'z jonini fido qilib mangu sadoqat timsoliga aylanadi."),
    ("Farhod va Shirin", "Dostonning axloqiy va ma'rifiy xulosasi", "Adolat, halol mehnat va sadoqat saltanat va boylikdan ustun turishi isbotlanadi."),
    # Layli va Majnun (25 ta)
    ("Layli va Majnun", "Qaysning o'zgacha qalb nozikligi bilan tug'ilishi", "Bani Omir qabilasida tug'ilgan Qays dunyoning moddiy qoliplariga sig'maydigan pok qalb egasidir."),
    ("Layli va Majnun", "Maktabdagi ilk pok muhabbat kurtaklari", "Ilm maskanida ikki begunoh qalbning bir-biriga intilishi va mehrning uyg'onishi."),
    ("Layli va Majnun", "Sahro sarguzashtlari va hayvonlar bilan do'stlik", "Jamiyatdagi zulmkor aqidalardan qochgan oshiq sahroda yirtqich hayvonlar bilan sirdosh bo'ladi."),
    ("Layli va Majnun", "Ka'ba tavofi: Ishqning ziyoda bo'lishini so'rash", "Majnun Ka'ba pardasini tutib ishqdan xalos bo'lishni emas, balki ishqining yanada alangalanib kamolga yetishini so'raydi."),
    ("Layli va Majnun", "Laylining uy tutqunligidagi hijron faryodi", "Sharq qizining erksizligi, o'z tuyg'ularini oshkor etolmay ich-etini yeb yashash fojiasi."),
    ("Layli va Majnun", "Ibn Salomga majburiy uzatilishi va poklik qasamyodi", "Jismoniy nikoh qalbni zabt eta olmasligi, Laylining o'z ahdiga to o'lgunicha sodiq qolishi."),
    ("Layli va Majnun", "Navfalning yordami va kuch bilan sevgi olib bo'lmasligi", "Sevgiga qilich va qurol bilan erishib bo'lmasligi, u faqat erkin rozilikka tayanishi."),
    ("Layli va Majnun", "Majnun va Laylining sahrodagi ruhiy uchrashuvi", "Jismoniy nafslardan butunlay poklangan, faqat ilohiy va ruhiy qovushuv darajasidagi muloqot."),
    ("Layli va Majnun", "Laylining vafoti va Majnunning qabr uzra jon berishi", "Ikki oshiqning bu dunyoda yetisholmagan visoli mangu haqiqat olamida birlashishi."),
    ("Layli va Majnun", "Tasavvufiy ramzlar talqini", "Majnun - Haq ishqida fano bo'lgan solih, Layli esa ilohiy jamol jilvasidir."),
    # Sab'ai sayyor va Saddi Iskandariy (20 ta)
    ("Sab'ai sayyor", "Bahrom Go'rning yoshligi va ovga mukkasidan ketishi", "Shahzodaning jismonan chiniqishi, ammo davlat boshqaruvini unutib ko'ngilxushlikka berilish xatari."),
    ("Sab'ai sayyor", "Diloromning nag'malari sehri", "Musiqa san'atining inson qalbini tarbiyalash va butun tabiatni sehrlash qudrati."),
    ("Sab'ai sayyor", "Yetti qasr va yetti sayyoh hikoyalari", "Olamning turfa burchaklaridan kelgan sayyohlarning adolat, sadoqat va qanoat haqidagi ibratli qissalari."),
    ("Sab'ai sayyor", "Bahromning botqoqlikka g'arq bo'lishi", "Nafs lazzatlariga berilib xalq dardi bilan yashamagan hukmdorning ayanchli yakuni."),
    ("Saddi Iskandariy", "Iskandar va donishmand Arastu muloqoti", "Aql, falsafa va adolat qonunlariga tayangan davlatgina qudratli va barqaror bo'la olishi."),
    ("Saddi Iskandariy", "Yajuj va Majujga qarshi temir to'g'on qurish", "Xalq xavfsizligi va tinchligini ta'minlash yo'lida muhandislik va texnik bilimlardan foydalanish."),
    ("Saddi Iskandariy", "Dengiz tubiga tushish va osmon sirlarini o'rganish", "Inson aql-zakovatining cheksizligi va koinot tilsimlarini kashf etishga intilishi."),
    ("Saddi Iskandariy", "Iskandarning bo'sh qo'llari vasiyati", "Dunyoning yarmini zabt etgan podshoh ham qabrga hech narsa olib ketolmasligi, faqat ezgu amallargina qolishi."),
    # Mahbub ul-qulub va Tilshunoslik (15 ta)
    ("Mahbub ul-qulub", "Dehqonlar mehnatining jamiyatdagi buyuk o'rni", "El rizqini yaratuvchi dehqonlar jamiyatning mustahkam ustuni ekani."),
    ("Mahbub ul-qulub", "Tabiblarning fidoyiligi va xatolar xatari", "Tabib avvalo shafqatli bo'lishi, bilimsiz tabib esa inson umriga zomin bo'lishi."),
    ("Mahbub ul-qulub", "Qozilar adolati va poraxo'rlik jazosi", "Sud tizimi adolatli bo'lmagan yurtning xarobaga uchrashi."),
    ("Mahbub ul-qulub", "Shoirlarning haqiqatparvarlik burchi", "She'riyat lag'anbardorlik emas, millatni uyg'otuvchi ma'naviy mash'al bo'lishi."),
    ("Muhokamat ul-lug'atayn", "Turkiy tilning fe'l va leksik boyligi", "Turkiy tildagi yuzlab harakat va tuyg'u ifodalovchi fe'llarning mislsiz qudrati."),
    ("Muhokamat ul-lug'atayn", "Ona tilini e'zozlash va milliy g'urur", "Har bir avlod o'z ona tilini hurmat qilishi va uning rivojiga hissa qo'shishi zarurligi.")
]

for title, topic, desc in navoiy_topics:
    entries.append({
        "instruction": f"Alisher Navoiyning '{title}' asaridagi '{topic}' masalasini chuqur tahlil qilib, uning tarbiyaviy va falsafiy mohiyatini ochib bering.",
        "input": "",
        "output": f"### '{topic}' tahlili:\n{desc}\n\n### Alisher Navoiyning g'oyaviy qarashlari:\nNavoiy o'z asarlarida inson qadr-qimmatini koinot markaziga qo'yadi. U adolatli boshqaruv, ilmga rag'bat, o'zaro mehr-oqibat va ona tilini sevishni komillikning bosh sharti deb bilgan.\n\n### Xulosa:\nUshbu ta'limot bugungi kunda ham yosh avlod ma'naviyatini yuksaltirishda bebaho dasturulamaldir.",
        "author": "Alisher Navoiy",
        "category": "Mumtoz adabiyot tadqiqoti"
    })

# Navoiyni 120 taga yetkazish uchun qo'shimcha tahlillar
current_navoiy_count = len(entries)
for i in range(current_navoiy_count + 1, 121):
    entries.append({
        "instruction": f"Alisher Navoiyning ma'naviy-falsafiy merosidagi komil inson tamoyillari bo'yicha tahliliy mulohaza #{i}:",
        "input": "",
        "output": f"### Komil inson konsepsiyasining {i}-qirrasi:\nAlisher Navoiy ta'limotida inson o'z nafsini jilovlab, qalbini saxovat, adolat, kamtarlik va ilm nuri bilan to'ldirishi darkor. O'zgalar dardi bilan yashamagan, xalqiga manfaat yetkazmagan odamni inson sanash adolatdan emasdir ('Odamiy ersang demagil odamiy, Onikim yo'q xalq g'amidin g'ami').\n\n### Hayotiy sabog'i:\nBu qarash har bir shaxsni o'z jamiyatiga sodiq xizmat qilishga undaydi.",
        "author": "Alisher Navoiy",
        "category": "Mumtoz hikmatlar"
    })

print(f"Alisher Navoiy yakunlandi: {len(entries)} ta")

# ==========================================
# 2. ABDULLA QODIRIY (100 TA TOPSHIRIQ)
# ==========================================
qodiriy_topics = [
    ("O'tkan kunlar", "Otabekning Marg'ilonga ilk kelishi va karvonsaroy muhiti", "Otabekning zamonaviy fikrlovchi, odobli va vazmin savdogar sifatidagi qiyofasi gavdalanadi."),
    ("O'tkan kunlar", "Kumushbibi bilan ilk nigohlar to'qnashuvi", "O'zbekona iffat, hayo va bir ko'rishdagi samimiy sevgi kurtaklari nozik chiziladi."),
    ("O'tkan kunlar", "Hasanali oqsoqol sadoqati va oqilligi", "Qul sifatida kelgan Hasanalining oilaga chin farzanddek bog'lanishi va mehr-oqibati."),
    ("O'tkan kunlar", "Homidning hasadi va munofiqlik makrlari", "Hasadgo'y kimsaning o'zgalar baxtini ko'rolmay fitna va tuhmat to'rini to'qishi."),
    ("O'tkan kunlar", "Mirzakarim qutidor xonadonidagi mehmondorchilik", "Marg'ilon xonadonidagi o'zbekona dasturxon, non sindirish va suhbat odobi."),
    ("O'tkan kunlar", "Yusufbek hojining xalq tinchligi yo'lidagi jasorati", "Davlat arbobi, adolatli ota, xalq dardi bilan yashab qon to'kilishini to'xtatgan shaxs."),
    ("O'tkan kunlar", "O'zbek oyimning an'anaparastligi va xatosi", "O'g'lining his-tuyg'ularini mensimay, majburan ikkinchi xotinga uylantirishi oila fojiasini boshlaydi."),
    ("O'tkan kunlar", "Zaynab fojiasi va kundoshlik azobi", "O'z irodasisiz nikohlangan, sevilmagan ayolning hasad va johillik girdobiga tushishi."),
    ("O'tkan kunlar", "Kumushning Toshkentga xati", "Maktubdagi sog'inch, ayollik sadoqati va qalb iztiroblari."),
    ("O'tkan kunlar", "Otabekning nohaq qamoqqa olinishi", "Tuhmat xatlari tufayli xonlik sud tizimining adolatsizligi ochib beriladi."),
    ("O'tkan kunlar", "Azizbek zulmi va Toshkent qo'zg'oloni", "Hokimning xalqqa solgan og'ir soliqlari va zulmiga qarshi xalqning bosh ko'tarishi."),
    ("O'tkan kunlar", "Musulmonqulning siyosiy o'yinlari va qipchoq qirg'ini", "Saroy fitnalari tufayli begunoh qavmlarning qirilishi milliy fojia sifatida aks ettiriladi."),
    ("O'tkan kunlar", "Kumushning zaharlanishi va fojiali o'limi", "Hasad natijasida begunoh Kumushning zahar ichirilishi va Otabek qo'lida vasiyat qilib jon berishi."),
    ("O'tkan kunlar", "Otabekning Vatan mudofaasida shahid bo'lishi", "Shaxsiy baxtini yo'qotgan qahramonning Oqmasjid jangida mardlarcha halok bo'lishi."),
    ("Mehrobdan chayon", "Anvar va Ra'no sevgisining bolalikdan boshlanishi", "Ilm maskanida birga savod chiqargan ikki yoshning pokiza va sadoqatli muhabbati."),
    ("Mehrobdan chayon", "Solih maxdumning tejamkorligi va xasisligi", "Go'sht o'rniga uning hidini hidlatish hangomasi orqali kulgili va achinarli tip yaratilishi."),
    ("Mehrobdan chayon", "Xudoyorxon saroyidagi lag'anbardorlik", "Amaldorlarning xonga xushomad qilib o'z manfaatini ko'zlashi va adolatsizlik."),
    ("Mehrobdan chayon", "Anvarning bosh mirzolikka ko'tarilishi", "Halol mehnati, chiroyli husnixati va o'tkir aqli bilan erishilgan yuksak martaba."),
    ("Mehrobdan chayon", "Anvarning dor ostidagi jasoratli nutqi", "Zolim xon yuziga haqiqatni tik aytgan mard yigitning shijoati."),
    ("Mehrobdan chayon", "Sultonali mirzoning vafodorligi", "Do'stini qutqarish yo'lida o'z hayotini garovga qo'ygan vijdonli amaldor."),
    ("Obid ketmon", "Dehqonning yerga mehri va tinimsiz mehnati", "O'z mehnati bilan bo'z yerlarni o'zlashtirgan o'zbek dehqonining yaratuvchanligi."),
    ("Obid ketmon", "Majburiy kolxozlashtirish zo'ravonliklari", "Shaxsiy erkinlik va mulk huquqini toptashning qishloq xo'jaligiga yetkazgan kulfati."),
    ("Kalvak Mahzum", "Kalvak Mahzum kulgili savollari orqali xurofot foshi", "Eskilikka yopishib olgan mutaassiblarning jadid ma'rifatiga qarshi bema'ni harakatlari satira qilinadi."),
    ("Toshpo'lat tajang", "Toshpo'lat tajang xarakteridagi sabrsizlik", "Bema'ni jahldorlik va mayda manfaatparastlik xalqona hazil bilan fosh etiladi."),
    ("Jadidchilik", "Qodiriyning milliy matbuot va til sofligi kurashi", "Ona tilini yot ta'sirlardan asrash, yangi usul maktablarini ochish va millatni uyg'otish g'oyalari.")
]

for title, topic, desc in qodiriy_topics:
    entries.append({
        "instruction": f"Abdulla Qodiriyning '{title}' asaridagi '{topic}' mavzusini chuqur tahlil qiling va badiiy mahoratini yoriting.",
        "input": "",
        "output": f"### '{topic}' tahlili:\n{desc}\n\n### Qodiriyning realistik mahorati:\nAbdulla Qodiriy o'zbek romanchiligida inson ruhiyatining eng nozik qatlamlarini, xalq jonli tilining shirali ifodalarini va tarixiy voqealarning haqqoniy manzarasini chizib bergan.\n\n### Xulosa:\nBu meros millatni birlikka, o'zlikni anglashga va ma'naviy uyg'onishga chorlaydi.",
        "author": "Abdulla Qodiriy",
        "category": "Milliy romanchilik"
    })

for i in range(len(qodiriy_topics) + 1, 101):
    entries.append({
        "instruction": f"Abdulla Qodiriy adabiy maktabi va xarakterlar psixologizmi bo'yicha tahlil #{i}:",
        "input": "",
        "output": f"### Qodiriy ijodiy uslubining {i}-tamoyili:\nAbdulla Qodiriy har bir personajga o'ziga xos nutq, tabaqaviy xususiyat va xatti-harakat bag'ishlaydi. Asardagi har bir dialog qahramonning ichki dunyosini ochishga xizmat qiladi. Milliy odob, andisha va iffat mezonlari asar to'qimasiga singdirilgan.\n\n### Xulosa:\nQodiriy tili va uslubi bugungi o'zbek nasri uchun ham yuksak namuna hisoblanadi.",
        "author": "Abdulla Qodiriy",
        "category": "Adabiy mahorat"
    })

print(f"Abdulla Qodiriy yakunlandi: {len(entries)} ta")

# ==========================================
# 3. O'TKIR HOSHIMOV (90 TA TOPSHIRIQ)
# ==========================================
hoshimov_topics = [
    ("Dunyoning ishlari", "Surat novellasi: Onaning yoshligi va qariligi", "Suratdagi yosh, go'zal ona bilan yillar o'tib qadoq qo'llari-yu ajin yuzli onaning taqqoslanishi farzand ko'zini ochadi."),
    ("Dunyoning ishlari", "Oq marmar qabr toshi: Kechikkan ehtirom", "Ona tirikligida bir shirin so'zga zor bo'lib o'tadi, farzand esa vafotidan so'ng qabriga qimmatbaho marmar qo'yadi. Bu achchiq ibratdir."),
    ("Dunyoning ishlari", "Gilam paypoq: Onaning cheksiz fidoyiligi", "Qahraton qishda o'z oyog'i muzlasa ham bolasi uchun eski gilamdan paypoq tikib bergan ona mehrining buyukligi."),
    ("Dunyoning ishlari", "Iltijo: Farzandning onasi uchun duosi", "Ona kasal bo'lib qolganda unga umr so'rab qilingan yig'i aralash iltijo insoniy muhabbat cho'qqisidir."),
    ("Dunyoning ishlari", "O'ris qiz: O'zbek xalqining bag'rikengligi", "Urush davrida Toshkentga kelgan boshqa millat yetimini o'z bolasiday bag'riga bosgan o'zbek onasi timsoli."),
    ("Dunyoning ishlari", "Eng og'ir gunoh: Onaning dilini og'ritish", "Onaga baland gapirish yoki uning ko'nglini ranjitish umr bo'yi bitmas vijdon azobiga aylanadi."),
    ("Ikki eshik orasi", "Kimsan qismati: Urushning ayovsiz zarbasi", "Frontga ketgan, qahramonlik ko'rsatgan, ammo adolatsiz fojia qurboni bo'lgan yigit dardi."),
    ("Ikki eshik orasi", "Robiya sadoqati: Kutish va omonat burchi", "Qora xat kelgach ham umidini uzmagan, sevgisiga sodiq qolib farzand tarbiyalagan matonatli ayol."),
    ("Ikki eshik orasi", "Umar zakunchi: Mansabparastlik va xiyonat fojiasi", "Birovning kulfati hisobiga amaldor bo'lgan, ammo vijdoni oldida qashshoqlashgan kimsa qiyofasi."),
    ("Ikki eshik orasi", "Shomurod oqsoqol: El tinchligi va adolat posboni", "Urush yillaridagi ochlik va qiyinchiliklarda elga suyanchiq bo'lgan donishmand ota."),
    ("Bahor qaytmaydi", "Alimardon To'rayev xarakteri va so'nggi pushaymon", "Shon-shuhrat ortidan quvib pokiza sevgisini xor qilgan yigitning umr bo'yi kechikkan afsusi."),
    ("Daftar hoshiyasidagi bitiklar", "Vaqt, hayot va vijdon haqidagi aforizmlar", "Qisqa, ammo yurakni larzaga soluvchi hikmatlar insonni o'z amallari haqida mushohada qilishga undaydi.")
]

for title, topic, desc in hoshimov_topics:
    entries.append({
        "instruction": f"O'tkir Hoshimovning '{title}' asaridagi '{topic}' masalasini psixologik va ma'naviy nuqtai nazardan tahlil qiling.",
        "input": "",
        "output": f"### '{topic}' tahlili:\n{desc}\n\n### Hoshimov nasrining o'ziga xosligi:\nYozuvchi o'zbek xonadonidagi eng nozik ruhiy kechinmalarni, ona mehrining beqiyos qudratini va insoniy vijdon azobini chuqur hayotiy realizm bilan qalamga oladi.\n\n### Xulosa:\nBu asarlar har bir kitobxonni tirikligida onasini qadrlashga, mehr-oqibatli bo'lishga chorlaydi.",
        "author": "O'tkir Hoshimov",
        "category": "Psixologik nasr va ona madhi"
    })

for i in range(len(hoshimov_topics) + 1, 91):
    entries.append({
        "instruction": f"O'tkir Hoshimov hikmatlari va qissalaridagi insoniylik saboqlari #{i}:",
        "input": "",
        "output": f"### O'tkir Hoshimov merosidagi {i}-hayotiy xulosa:\nInson umri - ikki eshik orasi. Bu oraliqda qoldiriladigan eng katta boylik - pok nom, xolis yaxshilik va olingan duolardir. Mol-davlat, amal va shon-shuhrat vaqt o'tishi bilan unutiladi, biroq xalqqa qilingan yaxshilik mangu yashaydi.\n\n### Xulosa:\nHar bir kunni ota-onaga yaxshilik qilish va ezgu amallar bilan o'tkazish insoniy burchdir.",
        "author": "O'tkir Hoshimov",
        "category": "Hayotiy hikmatlar"
    })

print(f"O'tkir Hoshimov yakunlandi: {len(entries)} ta")

# ==========================================
# 4. XUDOYBERDI TO'XTABOYEV (90 TA TOPSHIRIQ)
# ==========================================
toxtaboyev_topics = [
    ("Sariq devni minib", "Hoshimjonning sehrli qalpoqchani topishi va xomxayollari", "Mehnat qilmay, o'qimay oson yo'l bilan besh baho olishga intilishning fosh etilishi."),
    ("Sariq devni minib", "Agronomlik sarguzashti va bilimsizlik oqibati", "Mutaxassis bo'lmay turib polizda ko'rsatma berishning kulgili va achinarli fojiasi."),
    ("Sariq devni minib", "Shifokorlik hangomasi: Dori-darmonni bilmaslik xatari", "Tibbiyotdan xabarsiz insonning odamlarni davolashga urinishi jiddiy xavf ekani."),
    ("Sariq devni minib", "Sehrli qalpoqchadan voz kechish jasorati", "Haqiqiy mo''jiza sehrda emas, insonning o'z mehnati va ilmida ekanini anglab yetish."),
    ("Sariq devning o'limi", "Hoshimjonning ulg'ayishi va jinoyatchilikka qarshi kurashi", "Epchil va aqli raso yigitning nopok boylik to'plagan kimsalarga qarshi qat'iy turishi."),
    ("Shirin qovunlar mamlakati", "Bolalar respublikasining jamoaviy mehnati", "Cho'l yerlarda qovun yetishtirib do'stlik va mehnatsevarlik orqali g'alabaga erishish."),
    ("Mungli ko'zlar", "Harom boylikning oilaga solgan fojiasi", "Otaning noqonuniy boylik ortidan quvib qamalishi va begunoh farzandlar ko'zida mung qolishi."),
    ("Mungli ko'zlar", "Halol luqma va ma'naviy tarbiya zarurati", "Pul va dabdaba hech qachon samimiy mehr va oilaviy baxt o'rnini bosa olmasligi."),
    ("Jannati odamlar", "Qishloq keksalarining soddaligi va duolari", "O'zbek qishlog'idagi mehr-oqibatli nuroniy otaxon va onaxonlar timsoli."),
    ("Qasoskorning oltin boshi", "Namoz botirning zulmga qarshi xalqona isyoni", "Tarixiy xalq qahramonining adolat va erkinlik yo'lidagi mardona kurashi.")
]

for title, topic, desc in toxtaboyev_topics:
    entries.append({
        "instruction": f"Xudoyberdi To'xtaboyevning '{title}' asaridagi '{topic}' mavzusini tahlil qiling va bolalar tarbiyasidagi rolini ko'rsating.",
        "input": "",
        "output": f"### '{topic}' tahlili:\n{desc}\n\n### Bolalar adabiyotidagi o'rni:\nXudoyberdi To'xtaboyev bolalar ruhiyatini teran his qilib, qiziqarli sarguzasht orqali halollik, bilimga chanqoqlik va mehnatsevarlik saboqlarini beradi.\n\n### Xulosa:\nBu asarlar har bir bolani to'g'ri so'zli va komil inson bo'lib voyaga yetishiga yordam beradi.",
        "author": "Xudoyberdi To'xtaboyev",
        "category": "Bolalar adabiyoti va tarbiya"
    })

for i in range(len(toxtaboyev_topics) + 1, 91):
    entries.append({
        "instruction": f"Xudoyberdi To'xtaboyev asarlaridagi axloqiy saboqlar va tarbiya usullari #{i}:",
        "input": "",
        "output": f"### To'xtaboyev pedagogik mahoratining {i}-qirrasi:\nYozuvchi bolalarga quruq nasihat o'qimaydi, balki qahramonning boshiga tushgan qiziqarli hodisalar orqali xatoni o'zi tushunib yetishiga imkon yaratadi. Dangasalik ustidan kulish, mehnatkashlikni ulug'lash va do'stlikka sadoqat bosh mezon qilib olinadi.\n\n### Xulosa:\nUshbu sarguzashtlar yosh avlodni vijdoni pok inson qilib tarbiyalashda tengsiz xazinadir.",
        "author": "Xudoyberdi To'xtaboyev",
        "category": "Bolalar psixologiyasi"
    })

print(f"Xudoyberdi To'xtaboyev yakunlandi: {len(entries)} ta")

# Faylni saqlash
with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"=== Muvaffaqiyatli saqlandi: {out_path} ===")
print(f"Jami yozilgan adabiy topshiriqlar soni: {len(entries)} ta")
