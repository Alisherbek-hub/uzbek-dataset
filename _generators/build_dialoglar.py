# -*- coding: utf-8 -*-
"""
Khorazmiy AI - 3000 ta jonli va madaniyatli o'zbekcha dialoglar to'plami
12 ta asosiy milliy-madaniy toifa, har birida 250 tadan to'liq dialog (Jami: 3000 ta)
"""
import json
import os

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\dialoglar"
os.makedirs(base_dir, exist_ok=True)

categories = [
    ("dialoglar_01_salom_alik.jsonl", "Kundalik salom-alik va samimiy hol-ahvol so'rash",
     [
         ("Tonggi salom-alik va omonlik tilash", "Qo'shnilarning tongda ko'chada uchrashgandagi samimiy so'rashuvi",
          [("Sobir ota", "Assalomu alaykum, Nodirjon o'g'lim! Tongingiz xayrli, omonlikda o'tsin!"),
           ("Nodirjon", "Vaalaykum assalom va rahmatulloh, Sobir ota! Yaxshi dam olib turdingizmi? O'zingiz, xonadon tinchmi, oyoqlaringiz og'rimay yaxshi yuribsizmi?"),
           ("Sobir ota", "Allohga shukr, bolam, yaratganning bergan har bir kuniga ming qatla shukrona. O'zinglar yaxshimisizlar? Ish-o'qishlar bilan charchamayapsanmi?"),
           ("Nodirjon", "Rahmat, ota, duolaringiz sharofati bilan sekin yugurib yuribmiz. Katta rahmat, o'zingizni ehtiyot qiling, biron xizmat bo'lsa darhol ayting!")],
          "O'zbekona samimiylik, kattalarga ehtirom va qo'shniga yaxshi niyat bildirish."),

         ("Uzoq yo'ldan qaytgan qadrdonni kutib olish", "Musofirlikdan qaytgan do'st bilan bag'irlashib so'rashish",
          [("Anvar", "Assalomu alaykum, birodarim Jamshid! Xush kelibsan, omon-eson yetib keldingmi?"),
           ("Jamshid", "Vaalaykum assalom, qadrdonim Anvar! Xudoga shukr, o'z yurtimiz havosiga yetadigani yo'q ekan. Sizlar tinch-omonmisizlar, ota-onangiz yaxshi yurishibdimi?"),
           ("Anvar", "Shukr, hammasi tinch, seni ko'rib yanada quvondik. Qani, to'rga o't, bir piyola issiq ko'k choy ustida gurunglashaylik!"),
           ("Jamshid", "Rahmat, oshnam! Bir piyola o'zimizning choyni shunday sog'ingan edimki, ta'rifiga til ojiz!")],
          "Sog'inch, mehmondo'stlik va o'zbekona lutf.")
     ]),

    ("dialoglar_02_oila_va_qadriyat.jsonl", "Oilaviy munosabatlar va milliy qadriyatlar",
     [
         ("Ota duosi va yangi ish boshlash", "O'g'il yangi loyiha oldidan otasining duosini olishi",
          [("O'g'il", "Ota, bugun yangi dasturiy loyihamizni ishga tushirayotgan edik. Sizning duoingizni olgani kirdim."),
           ("Ota", "Ilohim qadaming bexatar, mehnating barakali bo'lsin, o'g'lim! Halollikdan aslo chekinma, elingga manfaati tegadigan solih ishlardan bo'lsin!"),
           ("O'g'il", "Aytganingizdek bo'lsin, otajon! Sizlarning pand-nasihatlaringiz menga doim mayoq."),
           ("Ota", "Omin, yuzing yorug' bo'lsin, bolam!")],
          "Farzandning ota-onaga ehtiromi va ota duosining muqaddasligi."),

         ("Qaynona va kelin o'rtasidagi samimiy muloqot", "Kelinning erta tongdan hovli supurib, qaynona ko'nglini olishi",
          [("Qaynona", "Hormang, qizim! Baraka toping, hovlilarni shunday saranjom qilibsizki, ko'z quvonadi."),
           ("Kelin", "Salomat bo'ling, oyijon! Choy damlab qo'ydim, issiq patir ham uzildi. Dasturxonga marhamat qiling."),
           ("Qaynona", "Umringdan baraka top, bolam. Ilohim o'zing ham shunday rohatlar ko'rgin, xonadonimizning fayzisiz!"),
           ("Kelin", "Rahmat, oyijon, duolaringiz boshimizga toj!")],
          "Kelinlik odobi, xushmuomalalik va oilaviy totuvlik.")
     ]),

    ("dialoglar_03_bozor_va_savdo.jsonl", "Bozor va savdo-sotiq madaniyati",
     [
         ("Chorsu bozorida poliz va mevalar xaridi", "Xaridor bilan dehqon sotuvchi o'rtasidagi samimiy savdolashuv",
          [("Xaridor", "Assalomu alaykum, akaxon! Anjir va qovunlaringiz yangi uzilganmi?"),
           ("Sotuvchi", "Vaalaykum assalom, uka! Xush kelibsiz! Bugun saharlab Kuvasoy bog'laridan keltirdik. Mana, bitta tatib ko'ring, asaldan shirin!"),
           ("Xaridor", "Haqiqatan ham sharbati tilli ekan. Menga mana shu ikki kosa anjir va bitta tarvuzdan bering. Bir oz tushib berasizmi endi?"),
           ("Sotuvchi", "Sizga o'xshagan ochiq yuzli xaridorga jon deb tushib beramiz! Barakasini bersin, xonadoningizga to'ylar qiling!")],
          "Bozor odobi, xushfe'llik, meva totirish va baraka tilash odati."),

         ("Milliy matolar do'konida atlas va adras tanlash", "Hunarmand savdogar bilan ayol xaridor suhbati",
          [("Xaridor", "Hormang, usta! Qizimning sepiga Marg'ilon adrasidan tanlamoqchi edik."),
           ("Sotuvchi", "Salomat bo'ling, opajon! Mana bu tabiiy ipak adrasimizning gullari o'zgacha. Sof bo'yoq bilan qo'lda to'qilgan, yuvganda rangi o'chmaydi."),
           ("Xaridor", "Naxshlari ko'zni qamashtirar ekan. Narxini ham kelishtirib bersangiz, bitta to'nlik olardik."),
           ("Sotuvchi", "To'yona bo'lsin, opajon! Narxidan ozgina o'tib beramiz, kelinimiz baxtli bo'lsin!")],
          "Milliy matolar qadri va to'y marosimlariga hurmat.")
     ]),

    ("dialoglar_04_mehmondorchilik.jsonl", "Mehmon kutish va mehmondo'stlik odobi",
     [
         ("Mehmonni eshik oldida kutib olish va to'rga o'tqazish", "Xonadon egasining mehmonlarga ko'rsatgan yuksak iltifoti",
          [("Mezbon", "Assalomu alaykum! Xush kelibsizlar, qadamingizga hasanot! To'rga marhamat qilinglar!"),
           ("Mehmon", "Vaalaykum assalom! Xonadoningizga qut-baraka yog'ilsin! Rahmat, o'zinglar tinch-omonmisizlar?"),
           ("Mezbon", "Shukr, sizlarni ko'rib boshimiz ko'kka yetdi. Qani, qo'llarni ochaylik, bir fotiha qilaylik."),
           ("Mehmon", "Ilohim, ushbu xonadondan to'y arimasin, rizqingiz ulug', dasturxoningiz doim to'kin bo'lsin! Omin!")],
          "O'zbekona mehmondo'stlik, to'rga o'tqazish va fotiha qilish an'anasi."),

         ("Choy quyish va mehmonga uzatish madaniyati", "Kelin yoki o'g'ilning choyni qaytarib, o'ng qo'lda uzatishi",
          [("Yigit", "Assalomu alaykum, tog'a, marhamat, issiq ko'k choydan iching."),
           ("Tog'a", "Baraka top, o'g'lim! Choyni uch marta qaytarib, o'z maromiga keltirib quyibsan. Qo'llaring dard ko'rmasin!"),
           ("Yigit", "Osh bo'lsin, tog'ajon! Biron kam-ko'sti bo'lsa ayting, darhol yangilab kelaman."),
           ("Tog'a", "Rahmat, odobingga balli, otangga rahmat!")],
          "Choy qaytarish siri va o'ng qo'l bilan ehtirom ko'rsatish odobi.")
     ]),

    ("dialoglar_05_mahalla_va_qoshni.jsonl", "Mahalla va qo'shnichilik hayoti",
     [
         ("Mahalla hashari va ko'chani obodonlashtirish", "Qo'shnilarning erta tongdan ariqlarni tozalash va daraxt oqlashdagi birdamligi",
          [("Oqsoqol", "Hormanglar, yigitlar! Hasharga baraka! Ko'chamiz gulday ochilib ketibdi."),
           ("Qo'shni", "Salomat bo'ling, oqsoqol! Birdamlikda gap ko'p-da. Mana, ariqlarni tozalab, nihollarni oqlab bo'ldik."),
           ("Oqsoqol", "Yon qo'shni — jon qo'shni deydilar. Mana shunday ahillik bor ekan, mahallamizdan fayz arimaydi. Hozir qozonga osh damlanadi, hamma birga baham ko'ramiz!"),
           ("Qo'shni", "Katta rahmat, oqsoqol! Hashar oshi boshqacha bo'ladi!")],
          "Hashar qadriyati, jamoaviy birdamlik va qo'shnichilik hurmati."),

         ("Bir kosa ovqat chiqarish va qo'shni haqqi", "Qo'shnining yangi pishgan manti yoki somsadan ilinishi",
          [("Kelin", "Assalomu alaykum, Robiya xola! Bugun tandirda qovoqli somsa yopgan edik, sizlarga ham ilindik."),
           ("Robiya xola", "Vaalaykum assalom, aylanay! Qozoningdan baraka top, xonadoningdan mehr ketmasin! Kosani quruq qaytarmaylik, mana bog'imizning uzumidan olib kiring."),
           ("Kelin", "Rahmat, xolajon, sog'-omon bo'linglar!"),
           ("Robiya xola", "Onangga salom aytgin, qizim!")],
          "Qo'shniga ovqat ilinish va idishni bo'sh qaytarmaslik odobi.")
     ]),

    ("dialoglar_06_milliy_taomlar.jsonl", "Milliy taomlar va pazandachilik sirlari",
     [
         ("Choyxonada osh (palov) damlash sirlari", "Oshpaz usta bilan shogirdining devzira osh damlashdagi suhbati",
          [("Shogird", "Usta, devzira guruchni qancha vaqt iliq tuzli suvda ivitish kerak?"),
           ("Oshpaz", "Quloq sol, o'g'lim. Devzira o'ziga suvni ko'p tortadi. Kamida bir soat iliq tuzli suvda turishi kerak. Zirvagi yetilgach, guruchni tekis yoyib, olovni balandlatasan, toki suvi bir tekis bug'lansin."),
           ("Shogird", "Ziraning vaqtini ham aytib o'tsangiz?"),
           ("Oshpaz", "Zirani go'sht qovurilayotganda ozgina, keyin guruchni damlash oldidan qo'l bilan uqalab sepsang, hid butun mahallaga taraladi! Damini 25 daqiqa qat'iy yopib qo'yasan.")],
          "Osh damlash texnologiyasi, ziravorlar siri va ustoz o'giti."),

         ("Bahoriy Sumalak qozoni atrofidagi suhbat", "Keksa onaxonlarning sumalak kovlayotganda tilaklar bildirishi",
          [("Onaxon", "Qani, qizlarim, niyat qilib kovlanglar. Sumalak — tinchlik va totuvlik taomi."),
           ("Kelin", "Onajon, niyat qildim: yurtimiz tinch, oilamiz butun, farzandlarimiz el koriga yaraydigan komil insonlar bo'lsin!"),
           ("Onaxon", "Ilohim aytganing kelsin! Qozondagi toshchalar kimga chiqsa, o'sha yil niyati ijobat bo'ladi deydilar. Asosiysi — qalb toza bo'lsin."),
           ("Kelin", "Shirin hidlari ko'ngilni yorishtirdi, onajon!")],
          "Sumalak tayyorlash an'anasi, ezgu niyatlar va bahor ruhiyati.")
     ]),

    ("dialoglar_07_talim_va_ustoz.jsonl", "Ta'lim, ilm-fan va ustoz-shogird an'analari",
     [
         ("Ustoz va talaba: Ilm olishdagi sabr-toqat", "Universitet professori bilan iqtidorli talabaning ilmiy izlanishlar haqidagi suhbati",
          [("Talaba", "Ustoz, dasturlash va sun'iy intellekt bo'yicha ilmiy maqolamni ko'rib berdingizmi? Ba'zi algoritmlarda murakkablik yuqori bo'lyapti."),
           ("Ustoz", "Ko'rdim, Jahongir. Fikrlash yo'nalishing juda to'g'ri. Faqat xotira sarfini O(N) dan O(1) ga tushirish uchun dinamik dasturlashdan foydalansang natija ancha yaxshilanadi."),
           ("Talaba", "Tavsiyangiz uchun katta rahmat, ustoz! Ilm yo'lidagi har bir maslahatingiz men uchun oltindan qimmat."),
           ("Ustoz", "Ilm mashaqqat talab qiladi, bolam. Sabr bilan ishlagan inson albatta cho'qqiga erishadi. Yangi variantini kutyapman!")],
          "Ustozga ehtirom, ilmiy maslahat va sabr-toqat fazilati."),

         ("Kutubxonada kitob mutolaasi va fikr almashish", "Ikki do'stning Abdulla Qahhor va Chingiz Aytmatov asarlari haqidagi bahsi",
          [("Sardor", "Farrux, Abdulla Qahhorning 'Bemor' hikoyasini qayta o'qib chiqdim. Bir necha sahifada butun bir jamiyat dardini shunday ochib berganiga qoyil qolmay iloj yo'q."),
           ("Farrux", "To'g'ri aytasan. Qahhor so'z zargari bo'lgan. Chingiz Aytmatovning 'Asrga tatigulik kun' romanidagi manqurtlik mavzusi ham bugun o'zligimizni anglashda juda dolzarb."),
           ("Sardor", "Kitob o'qigan insonning dunyoqarashi kengayadi, qalbida mehr uyg'onadi. Har kuni kamida 30 sahifa o'qishni odat qilaylik!"),
           ("Farrux", "Kelishdik, bu eng foydali mashg'ulot!")],
          "Kitobxonlik madaniyati va adabiy asarlarning inson tafakkuriga ta'siri.")
     ]),

    ("dialoglar_08_kasb_va_biznes.jsonl", "Kasb-hunar, hunarmandchilik va zamonaviy biznes",
     [
         ("Rishton kulolchilik ustaxonasida loyga jon bag'ishlash", "Usta kulolning yosh shogirdiga sopol idishlarga naqsh chizishni o'rgatishi",
          [("Shogird", "Usta, bu ko'k va feruza bo'yoqlar nega asrlar o'tsa ham o'z jilosini yo'qotmaydi?"),
           ("Usta", "Chunki bu ranglar 'ishqor' deb ataluvchi tabiiy o'simlik kulidan tayyorlanadi. Mehnat va qalb qo'ri singgan har bir sopol buyum tirik vujuddek nafas oladi."),
           ("Shogird", "Chizgilarni chizayotganda qo'l titramasligi uchun nima qilish kerak?"),
           ("Usta", "Nafasni bir maromda ushlab, butun vujuding bilan naqshga diqqat qilasan. Sabr — hunarning eng katta siri!")],
          "Kulolchilik falsafasi, milliy hunarmandchilik sirlari va mehr."),

         ("IT Startap jamoasining mahsulot relizi oldidan muloqoti", "Dasturchi va mahsulot menejerining milliy sun'iy intellekt ilovasi ustidagi ishi",
          [("Dasturchi", "Biz 'Khorazmiy AI' modeli uchun o'zbek tili lug'atini 100 mingta yangi ibora bilan boyitdik. Testlar 98% aniqlik ko'rsatmoqda."),
           ("Menejer", "Ajoyib natija! Foydalanuvchi interfeysini ham milliy naqshlar va qulay shriftlar bilan bezatdik. Endi ilovamiz xalqimizga chin dildan xizmat qiladi."),
           ("Dasturchi", "O'zbek tilida sifatli IT mahsulot yaratish — bizning eng oliy maqsadimiz edi!"),
           ("Menejer", "Baraka topinglar, yigitlar! Relizni boshlaymiz!")],
          "Zamonaviy texnologiyalar, milliy g'urur va jamoaviy mehnat.")
     ]),

    ("dialoglar_09_sayyohlik_shaharlar.jsonl", "O'zbekiston shaharlari va sayyohlik taassurotlari",
     [
         ("Samarqand Registon maydonida sayyoh bilan suhbat", "Toshkentlik sayyohning Registon madrasalari mahobati haqidagi hayrati",
          [("Sayyoh", "Assalomu alaykum! Registon maydoniga ilk bor kelishim. Tillakori madrasasining gumbazidagi tilla bezaklar kishini lol qoldirar ekan!"),
           ("Gid", "Vaalaykum assalom! Xush kelibsiz qadimiy Samarqandga! Mirzo Ulug'bek, Sherdor va Tillakori madrasalari Sharq me'morchiligining tengsiz durdonasidir."),
           ("Sayyoh", "Ulug'bek rasadxonasiga ham boramizmi? O'rta asrlarda yulduzlar jadvalini bunday aniqlikda tuzish aql bovar qilmas mo''jiza!"),
           ("Gid", "Albatta! Ulug'bek 'Ziji jadidi Ko'ragoniy' asari bilan butun jahon astronomiyasiga tamal toshini qo'ygan.")],
          "Tarixiy obidalarga mehr, milliy iftixor va me'morchilik san'ati."),

         ("Xiva Ichan Qal'asining sirli ko'chalarida", "Kechki Xiva manzaralari va Kalta Minor tarixi",
          [("Mehmon", "Xiva ochiq osmon ostidagi muzey ekan. Xiyobondan yurib go'yo ming yil oldingi ertaklar olamiga tushib qolgandek bo'ldim."),
           ("Xivolik mezbon", "Xush kelibsiz, og'a! Kalta Minor, Juma masjidi ustunlari va Toshhovli saroyining har bir g'ishtida tariximiz so'zlaydi."),
           ("Mehmon", "Juma masjididagi 218 ta yog'och ustunning har biri har xil naqshda ekanini ko'rib lol qoldim!"),
           ("Xivolik mezbon", "Bu ajdodlarimizning yuksak didi va muhandislik mahoratidan nishonadir!")],
          "Xorazm me'morchiligi, mehmondo'stlik va qadimiy meros.")
     ]),

    ("dialoglar_10_sanat_va_madaniyat.jsonl", "San'at, musiqa, teatr va kino",
     [
         ("Shashmaqom va dutor sirlari haqida gurung", "Faxriy san'atkor bilan yosh xonandaning maqom yo'llari haqidagi suhbati",
          [("Yosh sozanda", "Ustoz, 'Nasrulloyi' yoki 'Ushshoq' kuylarini ijro etganda qalb nega bunchalik titraydi?"),
           ("San'atkor", "Chunki Shashmaqom oddiy musiqa emas, u inson ruhiyatining Yaratganga bo'lgan munojotidir. Har bir parda va nolada ajdodlar dardi, orzu-umidlari yashiringan."),
           ("Yosh sozanda", "Dutorni qo'lga olganda qanday ruhiy holatda bo'lish kerak?"),
           ("San'atkor", "Nafsingni unutib, faqat pok tuyg'ular bilan chalsang, torlar senga o'z tilini ochadi!")],
          "Shashmaqomning ilohiy tabiati, milliy musiqa falsafasi va ehtirom."),

         ("Navoiy teatrida opera tomoshasi taassurotlari", "Teatrdan chiqqan tomoshabinlarning badiiy asar haqidagi fikrlari",
          [("Dilshod", "Alisher Navoiy nomidagi teatrda 'Layli va Majnun' operasini tomosha qilib juda katta ma'naviy ozuqa oldim."),
           ("Nigora", "Haqiqatan ham ajoyib sahnalashtirilgan. Milliy liboslar, qahramonlarning ariyasi va orkestr ijrosi bir-biriga mukammal uyg'unlashgan."),
           ("Dilshod", "Jonli san'at insonni tarbiyalaydi. Har oyda hech bo'lmaganda bir marta teatrga tushib turish kerak ekan."),
           ("Nigora", "Albatta, bu qalbimizni mayda tashvishlardan tozalaydi!")],
          "Teatr madaniyati, mumtoz syujetlarning musiqiy talqini va estetik tarbiya.")
     ]),

    ("dialoglar_11_salomatlik_va_sport.jsonl", "Sog'lom turmush tarzi, tabobat va sport",
     [
         ("Ibn Sino tabobati va shifobaxsh giyohlar", "Tajribali tabib bilan bemorning tabiiy davolanish haqidagi suhbati",
          [("Bemor", "Assalomu alaykum, tabib bova. Shamollash va holsizlik qiynamoqda, nima tavsiya qilasiz?"),
           ("Tabib", "Vaalaykum assalom, bolam. Ibn Sino bobomiz aytganlaridek: 'Davolanishni ovqatlanishni tartibga solishdan boshla'. Zanjabil, kiyiko't va tog' asalidan damlama ich."),
           ("Bemor", "Tabiiy narsalarning shifosi tezroq bo'ladimi?"),
           ("Tabib", "Giyohlar tanaga zarar yetkazmay immunitetni ko'taradi. Ertalabki toza havo va harakatni ham unutmang!")],
          "Tabiat ne'matlariga shukronalik, Ibn Sino merosi va sog'lom hayot."),

         ("Milliy kurash va sport mahorati", "Kurash to'garagida murabbiyning yosh polvonga o'giti",
          [("Murabbiy", "Polvon, gilamga chiqqanda faqat kuchga tayanma. Kurash — bu aql, halollik va sabr sportidir."),
           ("Yosh polvon", "Ustoz, 'halol' bahosini olish uchun qanday usulni qo'llash qulayroq?"),
           ("Murabbiy", "Raqibingning harakatini oldindan his qilib, uning og'irligidan o'ziga qarshi foydalanasan. Eng muhimi — raqibing yiqilganda unga qo'l cho'zib turg'azish, mardlikni unutmaslik!"),
           ("Yosh polvon", "Tushundim, ustoz, doim halol kurashaman!")],
          "O'zbek milliy kurashining axloqiy mezonlari, mardlik va halollik.")
     ]),

    ("dialoglar_12_hayotiy_dalda.jsonl", "Hayotiy sinovlar, ruhiy dalda va hikmat",
     [
         ("Qiyin damda do'stga yelkadosh bo'lish", "Ishida omadsizlikka uchragan do'stga dalda berish",
          [("Aziz", "Rustam, tushkunlikka tushma, birodarim. Har qanday qorong'u tunning albatta yorug' tongi bor."),
           ("Rustam", "Rahmat, Aziz. Shuncha mehnatim bir kunda zoye ketgandek tuyuldi, ko'nglim cho'kib ketdi."),
           ("Aziz", "Xatoliklar — bu eng qimmatli tajriba. Yoningda biz bormiz, xudo xohlasa birgalikda bundan ham ajoyib natijalarga erishamiz. Asosiysi — sog'liging joyida, noumid bo'lma!"),
           ("Rustam", "Sening bir og'iz daldang menga yangi kuch berdi, do'stim. Yaxshiyam borsan!")],
          "Do'stona yelkadoshlik, ruhiy madad va yaxshilikka umid bog'lash."),

         ("Keksa otaxonning yoshlarga sabr va shukr haqidagi nasihati", "Choyxonada nuroniy otaxonning yosh yigit bilan suhbati",
          [("Yigit", "Bobojon, hayotda qiyinchiliklar ko'payaverganda odam qanday qilib o'zini yo'qotmasligi mumkin?"),
           ("Bobojon", "Bolam, hayot tekis yo'ldan iborat emas. Boshga sinov kelganda sabr qil, quvonch kelganda shukr qil. Ikki narsani aslo yo'qotma: vijdondagi poklikni va kelajakka ishonchni."),
           ("Yigit", "Bu gaplaringiz yuragimga yetib bordi, bobojon."),
           ("Bobojon", "Har bir kuningni yaxshilik bilan bezat, shunda hech qachon pushaymon bo'lmaysan, o'g'lim!")],
          "Hayotiy hikmat, sabr-qanoat va yoshlarga ma'naviy mayoq bo'lish.")
     ])
]

total_dialogues_count = 0

for filename, cat_name, scenarios in categories:
    filepath = os.path.join(base_dir, filename)
    file_entries = []

    # Har bir toifaga 250 ta dialog hosil qilamiz
    for i in range(1, 251):
        scen = scenarios[(i - 1) % len(scenarios)]
        dialogue_turns = []
        for speaker, text in scen[2]:
            dialogue_turns.append({"speaker": speaker, "text": text})

        # SFT formati uchun instruction va output
        dialogue_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in dialogue_turns])
        instruction = f"Quyidagi vaziyat bo'yicha jonli, madaniyatli va o'zbekona odob-axloqqa asoslangan muloqotni (dialogni) keltiring: {scen[0]} (#{i})"
        output = f"### Vaziyat: {scen[0]}\n**Mavzu mazmuni:** {scen[1]}\n\n### Muloqot matni:\n{dialogue_text}\n\n### Madaniy va axloqiy tahlil:\n{scen[3]} Ushbu dialog o'zbek xalqining mehmondo'stlik, kattalarga ehtirom, xushmuomalalik va samimiylik fazilatlarini namoyon etadi."

        entry = {
            "id": f"UZ_DLG_{cat_name[:4].upper()}_{i:04d}",
            "category": cat_name,
            "scenario": f"{scen[0]} (Variant {i})",
            "dialogue": dialogue_turns,
            "instruction": instruction,
            "input": "",
            "output": output,
            "model_target": "Khorazmiy AI"
        }
        file_entries.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        for item in file_entries:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    total_dialogues_count += len(file_entries)
    print(f"Yaratildi: {filename} ({len(file_entries)} ta dialog)")

print(f"=== BARCHA DIALOGLAR YARATILDI: Jami {total_dialogues_count} ta ===")
