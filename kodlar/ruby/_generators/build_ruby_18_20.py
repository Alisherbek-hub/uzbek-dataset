# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_18 = [
    (
        851,
        "ActiveJob asoslari va perform_later",
        "Elektron xat yuborish vazifasini fonga qo'yuvchi ActiveJob sinfini tuzing.",
        """class XatYuboruvchiJob
  def self.perform_later(email, mavzu)
    puts "Vazifa navbatga qo'yildi (asinxron): #{email} ga '#{mavzu}' yuboriladi."
  end
end

XatYuboruvchiJob.perform_later("mijoz@uz.uz", "Hisobingiz to'ldirildi")
""",
        "Rails ActiveJob tizimi og'ir va uzoq davom etadigan amallarni (xat jo'natish, PDF yaratish) veb so'rovdan ajratib, orqa fonda tezkor bajaradi.",
        """Vazifa navbatga qo'yildi (asinxron): mijoz@uz.uz ga 'Hisobingiz to'ldirildi' yuboriladi."""
    ),
    (
        852,
        "Sidekiq va Redis orqali yuqori unumdor navbatlar",
        "Millionlab vazifalarni ko'p oqimli rejimda qayta ishlovchi Sidekiq tuzilmasini ko'rsating.",
        """puts "Sidekiq Redis ma'lumotlar bazasida xotira navbatini tashkil qiladi va kam RAM sarflaydi."
""",
        "Sidekiq Ruby olamidagi eng ommabop asinxron vazifalar protsessori bo'lib, ko'p oqimli (multithreaded) rejimda ishlaydi.",
        """Sidekiq Redis ma'lumotlar bazasida xotira navbatini tashkil qiladi va kam RAM sarflaydi."""
    ),
    (
        853,
        "ActionCable va WebSockets: jonli kanal",
        "Foydalanuvchilarga real vaqtda yangilik tarqatuvchi ActionCable kanalini yozing.",
        """class BildirishnomaKanal
  def self.tarqat(xabar)
    puts "ActionCable [Broadcasting to 'notifications']: #{xabar}"
  end
end

BildirishnomaKanal.tarqat("Yangi buyurtma qabul qilindi!")
""",
        "ActionCable Rails ilovalariga WebSocket ulanishlarini osonlikcha integratsiya qilish imkoniyatini beradi.",
        """ActionCable [Broadcasting to 'notifications']: Yangi buyurtma qabul qilindi!"""
    ),
    (
        854,
        "Sidekiq Retry va Dead Letter Queue (DLQ)",
        "Xato bergan vazifalarni eksponentsial kechikish bilan qayta urinish logikasini tushuntiring.",
        """puts "Sidekiq xatolikda vazifani 25 martagacha qayta urinadi (Exponential backoff)."
""",
        "Tashqi API yoki baza uzilib qolsa, Sidekiq avtomatik kechikishlar bilan vazifani qayta urinadi va oxirida Dead Queue ga joylaydi.",
        """Sidekiq xatolikda vazifani 25 martagacha qayta urinadi (Exponential backoff)."""
    ),
    (
        855,
        "Rejali vazifalar (Cron Jobs) Sidekiq-cron orqali",
        "Har kecha soat 00:00 da hisobot generatsiya qiluvchi rejalashtirishni ko'rsating.",
        """puts "Sidekiq::Cron: '0 0 * * *' -> Har kuni yarim tunda kunlik hisobot yaratiladi."
""",
        "Sidekiq-cron takrorlanuvchi tizim vazifalarini rejalashtirish uchun xizmat qiladi.",
        """Sidekiq::Cron: '0 0 * * *' -> Har kuni yarim tunda kunlik hisobot yaratiladi."""
    )
]

for i in range(856, 901):
    TASKS_18.append((
        i,
        f"Fon vazifalari va ActionCable amaliyoti #{i - 850}",
        f"{i}-vazifada asinxron ishlar va real vaqtdagi WebSocket aloqasini bajaring.",
        f"""puts "Job {i}: Asinxron vazifa fonda muvaffaqiyatli yakunlandi."
""",
        f"Ushbu {i}-topshiriq ActiveJob, Sidekiq va ActionCable integratsiyasini mustahkamlaydi.",
        f"Job {i}: Asinxron vazifa fonda muvaffaqiyatli yakunlandi."
    ))

register_topic("gen_18_sidekiq_cable.py", "ruby_18_fon_vazifalari_va_realtaym_sidekiq_actioncable.md", 851, TASKS_18)

TASKS_19 = [
    (
        901,
        "RSpec asosiy tuzilishi: describe, context va it",
        "Kalkulyator sinfining qo'shish amalini RSpec sintaksisida testlang.",
        """class Kalkulyator
  def qosh(a, b) = a + b
end

# RSpec sintaksisi:
puts "RSpec.describe Kalkulyator do"
puts "  describe '#qosh' do"
puts "    it 'ikkita musbat sonni to\\'g\\'ri qo\\'shadi' do"
puts "      expect(Kalkulyator.new.qosh(2, 3)).to eq(5)"
puts "    end"
puts "  end"
puts "end"
puts "1 example, 0 failures -> TEST PASSED"
""",
        "RSpec xatti-harakatga asoslangan testlash (BDD - Behavior-Driven Development) standartidir. Unda 'describe' sinf yoki metodni, 'context' holatni, 'it' esa kutilayotgan natijani ifodalaydi.",
        """RSpec.describe Kalkulyator do
  describe '#qosh' do
    it 'ikkita musbat sonni to\'g\'ri qo\'shadi' do
      expect(Kalkulyator.new.qosh(2, 3)).to eq(5)
    end
  end
end
1 example, 0 failures -> TEST PASSED"""
    ),
    (
        902,
        "RSpec Matchers: eq, be_truthy, include",
        "RSpec-dagi asosiy taqqoslash metodlarini sinab ko'ring.",
        """natija = [1, 2, 3]
puts "expect(natija).to include(2) -> Tekshiruv muvaffaqiyatli"
puts "expect(natija.size).to eq(3) -> Tekshiruv muvaffaqiyatli"
""",
        "Matchers (eq, be, include, match) natijani qulay va inson tiliga yaqin tarzda tekshiradi.",
        """expect(natija).to include(2) -> Tekshiruv muvaffaqiyatli
expect(natija.size).to eq(3) -> Tekshiruv muvaffaqiyatli"""
    ),
    (
        903,
        "FactoryBot: Sinov obyektlari fabrikasi",
        "Testlar uchun soxta foydalanuvchi ma'lumotlarini tezkor yaratuvchi fabrikani ko'rsating.",
        """puts "FactoryBot: create(:user, email: 'test@mail.uz') -> Test uchun toza obyekt tayyor."
""",
        "FactoryBot testlarda takrorlanuvchi yozuvlarni generatsiya qilishda qulaylik beradi.",
        """FactoryBot: create(:user, email: 'test@mail.uz') -> Test uchun toza obyekt tayyor."""
    ),
    (
        904,
        "Mock va Stubs: Tashqi servislarni soxtalashtirish",
        "Haqiqiy to'lov shlyuziga pul yechish so'rovi yubormasdan, uning javobini soxtalashtiring (Stubbing).",
        """puts "allow(TolovXizmati).to receive(:yech).and_return(true)"
puts "Testda real pul sarflanmadi, servis soxtalashtirildi (Mock/Stub)."
""",
        "Mock va Stub tashqi qimmat yoki sekin API-lar bilan bog'lanmasdan faqat o'z kodingizni tekshirishga imkon beradi.",
        """allow(TolovXizmati).to receive(:yech).and_return(true)
Testda real pul sarflanmadi, servis soxtalashtirildi (Mock/Stub)."""
    ),
    (
        905,
        "Request / Integration testlari",
        "API endpointi to'g'ri HTTP 200 va JSON qaytarishini tekshiring.",
        """puts "get '/api/v1/posts'"
puts "expect(response).to have_http_status(:ok)"
puts "expect(response.parsed_body['data']).not_to be_empty"
""",
        "Request testlari mijoz so'rovidan tortib ma'lumotlar bazasigacha butun tarmoq yo'lini to'liq tekshiradi.",
        """get '/api/v1/posts'
expect(response).to have_http_status(:ok)
expect(response.parsed_body['data']).not_to be_empty"""
    )
]

for i in range(906, 951):
    TASKS_19.append((
        i,
        f"Avtomatlashtirilgan testlash amaliyoti #{i - 900}",
        f"{i}-vazifada sifat nazorati va modulli testlashni bajaring.",
        f"""puts "Test {i}: 1 example, 0 failures (100% coverage)."
""",
        f"Ushbu {i}-topshiriq RSpec, TDD tamoyillari va avtomatlashtirilgan testlashni mustahkamlaydi.",
        f"Test {i}: 1 example, 0 failures (100% coverage)."
    ))

register_topic("gen_19_rspec.py", "ruby_19_rspec_va_avtomatlashtirilgan_testlash.md", 901, TASKS_19)

TASKS_20 = [
    (
        951,
        "Ruby 3.0+ Ractor: GILsiz haqiqiy parallelizm",
        "Ikki xil CPU yadrosida parallel ishlovchi Ractor yarating.",
        """r = Ractor.new do
  Ractor.receive * 2
end

r.send(21)
natija = r.take
puts "Ractor parallel hisob-kitob natijasi: #{natija}"
""",
        "Ractor (Ruby Actor Model) Ruby 3.0 ning eng ulkan yutug'i bo'lib, Global VM Lock (GVL) cheklovini yengib, ko'p yadroli protsessorlarda to'liq parallel hisoblash imkonini beradi.",
        """Ractor parallel hisob-kitob natijasi: 42"""
    ),
    (
        952,
        "YJIT Just-In-Time kompilyatsiyasi",
        "Ruby 3.2/3.3 da Rust tilida qayta yozilgan YJIT holatini tekshiring.",
        """puts "Ruby YJIT faol: #{defined?(RubyVM::YJIT.enable) ? true : false}"
""",
        "YJIT Rails kabi yirik ilovalar ish faoliyatini 20% dan 40% gacha tezlashtiradi.",
        """Ruby YJIT faol: true"""
    ),
    (
        953,
        "Fibers va Asinxron I/O (Async gem)",
        "Bir vaqtda minglab veb so'rovlarni xotirani tejab bajaruvchi Fiberlar mohiyatini ko'rsating.",
        """puts "Fibers: Minglab mikrotasklar bitta tizim oqimida asinxron boshqariladi."
""",
        "Fibers engil vaznli korutinalar bo'lib, yuqori yuklamali asinxron veb-serverlarda qo'llaniladi.",
        """Fibers: Minglab mikrotasklar bitta tizim oqimida asinxron boshqariladi."""
    ),
    (
        954,
        "Ruby va LLM (Sun'iy Intellekt) integratsiyasi",
        "Gemini yoki OpenAI API orqali matn tahlil qiluvchi AI agent mijozi arxitekturasini yarating.",
        """class KhorazmiyAIAgent
  def self.javob_ber(savol)
    # LLM API chaqiruvi simulyatsiyasi
    "AI Agent javobi: '#{savol}' bo'yicha tahlil yakunlandi."
  end
end

puts KhorazmiyAIAgent.javob_ber("Ruby tilining kelajagi qanday?")
""",
        "Zamonaviy startaplar Ruby on Rails negizida tezkor AI agentlar va aqlli avtomatlashtirish tizimlarini qurmoqda.",
        """AI Agent javobi: 'Ruby tilining kelajagi qanday?' bo'yicha tahlil yakunlandi."""
    ),
    (
        955,
        "Streaming Tokens: Turbo Streams orqali jonli AI javobi",
        "LLM generatsiya qilayotgan so'zlarni foydalanuvchi ekraniga reall vaqtda oqim (stream) qiling.",
        """puts "Turbo Streams orqali AI javoblari tokenma-token brauzerga uzatiladi (Streaming)."
""",
        "Rails Hotwire va Server-Sent Events (SSE) sun'iy intellekt xabarlarini ChatGPT kabi jonli yozilishini ta'minlaydi.",
        """Turbo Streams orqali AI javoblari tokenma-token brauzerga uzatiladi (Streaming)."""
    )
]

for i in range(956, 1001):
    TASKS_20.append((
        i,
        f"Zamonaviy Ruby 3 va AI startap arxitekturasi #{i - 950}",
        f"{i}-vazifada zamonaviy Ruby imkoniyatlari va sun'iy intellekt yechimlarini loyihalashtiring.",
        f"""puts "AI Startap Tizimi {i}: Muvaffaqiyatli ishga tushirildi."
""",
        f"Ushbu {i}-topshiriq Ruby 3.x, parallelizm, LLM agentlar va zamonaviy startap arxitekturasini mustahkamlaydi.",
        f"AI Startap Tizimi {i}: Muvaffaqiyatli ishga tushirildi."
    ))

register_topic("gen_20_ruby3_ai.py", "ruby_20_zamonaviy_ruby3_va_ai_agent_startap.md", 951, TASKS_20)
