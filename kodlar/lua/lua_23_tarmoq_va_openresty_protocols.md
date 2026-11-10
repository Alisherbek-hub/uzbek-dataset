# Khorazmiy AI: Lua - Modul 23
## Mavzu: OpenResty cosocket API, Nginx stream TCP/UDP proksi, Redis va HTTP/WebSockets

### Topshiriq #1101: ngx.socket.tcp() bilan asosiy TCP klient va timeoutlarni boshqarish
**Tavsif:** OpenResty ilovasida tashqi TCP xizmatiga ulanish, so'rov yuborish va javobni to'liq qabul qilish talab etiladi. Nginx worker jarayoni biron bir holatda bloklanib qolmasligi shart.
**Talablar:** `ngx.socket.tcp()` dan foydalanish, ulanish, o'qish va yozish timeoutlarini alohida sozlash, `receive('*l')` orqali satr o'qish va xatoliklarni xavfsiz qayta ishlash.
**Yechim (Lua):**
```lua
-- OpenResty da noblokirovka qiluvchi TCP mijozi
local _M = {}

function _M.query_tcp_service(host, port, payload)
    local tcp = ngx.socket.tcp()
    
    -- Timeout parametrlarini sozlash: ulanish, o'qish, yozish (millisekundlarda)
    tcp:settimeouts(2000, 5000, 5000)
    
    -- Tashqi server bilan ulanish o'rnatish
    local ok, err = tcp:connect(host, port)
    if not ok then
        return nil, "Ulanish xatosi: " .. tostring(err)
    end
    
    -- Ma'lumotlarni yuborish
    local bytes_sent, send_err = tcp:send(payload .. "\r\n")
    if not bytes_sent then
        tcp:close()
        return nil, "Ma'lumot yuborish xatosi: " .. tostring(send_err)
    end
    
    -- Javobni bitta qator shaklida o'qish ('*l' parametri)
    local line, read_err = tcp:receive("*l")
    if not line then
        tcp:close()
        return nil, "O'qish xatosi: " .. tostring(read_err)
    end
    
    -- Ulanishni yopish
    tcp:close()
    return line, nil
end

return _M
```
**Tushuntirish:** OpenResty Cosocket API Nginx event loop (epoll/kqueue) ustiga qurilgan. `tcp:connect()` va `tcp:receive()` chaqirilganda, Lua korutinasi (coroutine) orqaga chekinadi (yield) va OS hodisasi yuz berganda avtomatik qayta uyg'onadi (resume). Bu bitta workerda o'n minglab parallel TCP ulanishlarni CPU va xotirani band qilmasdan bajarish imkonini beradi.

---

### Topshiriq #1102: TCP Cosocket ulanishlar hovuzi (setkeepalive max_idle_timeout va pool_size)
**Tavsif:** Har bir so'rov uchun yangidan TCP ulanish ochish va 3 bosqichli handshake (SYN, SYN-ACK, ACK) bajarish server protsessoriga va tarmoqqa ortiqcha yuklama keltiradi.
**Talablar:** `sock:setkeepalive(timeout, size)` metodidan foydalanish, ulanishni yopmasdan hovuzga qaytarish, hovuz to'lganida xavfsiz yopish.
**Yechim (Lua):**
```lua
-- Ulanishlar hovuzi (Keepalive Connection Pool) boshqaruvi
local _M = {}

local DEFAULT_IDLE_TIMEOUT = 10000 -- 10 soniya kutish
local DEFAULT_POOL_SIZE = 100      -- Hovuzdagi maksimal ochiq soketlar soni

function _M.execute_with_keepalive(host, port, request_data)
    local sock = ngx.socket.tcp()
    sock:settimeouts(1000, 3000, 3000)
    
    local ok, err = sock:connect(host, port)
    if not ok then
        return nil, "Ulanish muvaffaqiyatsiz: " .. tostring(err)
    end
    
    local _, send_err = sock:send(request_data)
    if send_err then
        sock:close()
        return nil, send_err
    end
    
    local response, recv_err = sock:receive("*l")
    if not response then
        sock:close()
        return nil, recv_err
    end
    
    -- Ulanishni yopish o'rniga uni hovuzga qaytaramiz
    local keepalive_ok, keepalive_err = sock:setkeepalive(DEFAULT_IDLE_TIMEOUT, DEFAULT_POOL_SIZE)
    if not keepalive_ok then
        ngx.log(ngx.WARN, "Hovuzga qaytarish xatosi (yopilmoqda): ", keepalive_err)
        sock:close()
    end
    
    return response, nil
end

return _M
```
**Tushuntirish:** `sock:setkeepalive()` chaqirilganda, OpenResty joriy Nginx worker doirasida host va port kombinatsiyasi bo'yicha ulanishni maxsus ro'yxatda saqlaydi. Keyingi `sock:connect()` chaqirilganida, agar bo'sh soket mavjud bo'lsa, tarmoq darajasidagi handshake'larsiz darhol o'sha soket qayta ishlatiladi. Bu kechikishni (latency) 80% gacha kamaytiradi.

---

### Topshiriq #1103: sock:sslhandshake orqali xavfsiz TLS/SSL aloqasini o'rnatish va SNI tekshiruvi
**Tavsif:** Tashqi HTTPS yoki maxsus shifrlangan TCP protokollariga ulanishda shifrlash kalitlarini almashish va serverning haqiqiy domeniga tegishli ekanligini (SNI) tekshirish zarur.
**Talablar:** `sock:sslhandshake(reused_session, server_name, ssl_verify)` dan foydalanish, sessiyani keshlashtirish va xavfsiz TLS o'rnatish.
**Yechim (Lua):**
```lua
-- TLS Handshake va SNI tekshiruvi
local _M = {}

function _M.connect_secure_tls(host, port)
    local sock = ngx.socket.tcp()
    sock:settimeouts(2000, 5000, 5000)
    
    local ok, err = sock:connect(host, port)
    if not ok then
        return nil, "TCP ulanish xatosi: " .. tostring(err)
    end
    
    -- TLS Handshake o'tkazish
    -- Parametrlar: session (nil = yangi), server_name (SNI), ssl_verify (true = sertifikat tekshiruvi)
    local session, ssl_err = sock:sslhandshake(nil, host, true)
    if not session and ssl_err then
        sock:close()
        return nil, "TLS Handshake xatosi: " .. tostring(ssl_err)
    end
    
    ngx.log(ngx.INFO, "Xavfsiz TLS aloqasi muvaffaqiyatli o'rnatildi: ", host)
    return sock, nil
end

return _M
```
**Tushuntirish:** OpenResty ning `sslhandshake()` metodi OpenSSL non-blocking API lari bilan birlashtirilgan. `server_name` parametri zamonaviy bulutli servislarda (Cloudflare, AWS) bitta IP manzilida yuzlab turli domenlar joylashganda to'g'ri sertifikatni tanlash (SNI) uchun qat'iy talab etiladi.

---

### Topshiriq #1104: Asinxron TCP Echo server va mijoz aloqasi protokoli
**Tavsif:** Tarmoq uskunalarini sinovdan o'tkazish va aloqa kanalining kechikishini doimiy baholash uchun yuqori unumdor TCP Echo protokoli kerak.
**Talablar:** TCP ulanishida belgilangan hajmda ma'lumot qabul qilish (`receive(n)`), qabul qilingan ma'lumotni o'zgarishsiz qaytarish va xotira oqishini oldini olish.
**Yechim (Lua):**
```lua
-- TCP Echo xizmati mantiqi
local _M = {}

function _M.handle_echo_session(client_sock)
    client_sock:settimeouts(5000, 5000, 5000)
    
    while true do
        -- 1024 baytlik paketni kutish
        local data, err, partial = client_sock:receive(1024)
        if not data then
            if err == "closed" then
                ngx.log(ngx.INFO, "Mijoz ulanishni yopdi")
                break
            end
            ngx.log(ngx.ERR, "Qabul qilishda xato: ", err)
            break
        end
        
        -- Kelgan ma'lumotni darhol orqaga qaytarish
        local bytes, send_err = client_sock:send(data)
        if not bytes then
            ngx.log(ngx.ERR, "Qaytarishda xatolik: ", send_err)
            break
        end
    end
    
    client_sock:close()
end

return _M
```
**Tushuntirish:** `receive(n)` parametri aniq $n$ bayt yetib kelguncha kutadi. Bu binar protokollarda aniq belgilangan kadrlar (frames) bilan ishlashda qulaydir. `err == 'closed'` tekshiruvi mijoz tomonidan ulanish normal uzilganini ifodalaydi.

---

### Topshiriq #1105: Maxsus binar protokollarni paketlash va parslash (Binar header + payload)
**Tavsif:** Moliyaviy va telemetriya tizimlarida ma'lumotlar JSON o'rniga binar formatda uzatiladi: 2 bayt Sehrli raqam (Magic), 2 bayt Buyruq kodi (Command), 4 bayt Ma'lumot uzunligi (Length), va Payload.
**Talablar:** String pack/unpack funksiyalaridan foydalanish, binar sarlavhani ajratish, payloadni to'liq o'qish.
**Yechim (Lua):**
```lua
-- Binar protokollarni enkoder va dekoderi
local _M = {}

local MAGIC_NUMBER = 0xABCD

--- Paketni tuzish: >I2 (magic) >I2 (cmd) >I4 (length) + payload
function _M.encode_packet(command_id, payload)
    local payload_len = #payload
    -- Big-endian formatida binar qadoqlash
    local header = string.pack(">I2I2I4", MAGIC_NUMBER, command_id, payload_len)
    return header .. payload
end

--- Soketdan paketni ajratib olish
function _M.read_packet(sock)
    -- 1. Avval 8 baytlik sarlavhani o'qish
    local header_data, err = sock:receive(8)
    if not header_data then
        return nil, nil, "Sarlavhani o'qishda xato: " .. tostring(err)
    end
    
    local magic, cmd, length = string.unpack(">I2I2I4", header_data)
    if magic ~= MAGIC_NUMBER then
        return nil, nil, "Noto'g'ri protokol magic raqami"
    end
    
    -- 2. Ko'rsatilgan uzunlikdagi haqiqiy ma'lumotni o'qish
    local payload, payload_err = sock:receive(length)
    if not payload then
        return nil, nil, "Payload o'qishda xato: " .. tostring(payload_err)
    end
    
    return cmd, payload, nil
end

return _M
```
**Tushuntirish:** Lua 5.3 va LuaJIT 2.1 da `string.pack` va `string.unpack` yordamida binar oqimlar C tili tezligida tahlil qilinadi. Big-endian `>I2I2I4` formati tarmoq baytlar tartibiga (Network Byte Order) to'liq mos keladi va JSON parslariga nisbatan 10-15 barobar kamroq CPU resursini talab qiladi.

---

### Topshiriq #1106: Cosocket xatoliklarini boshqarish va eksponentsial kechikish bilan qayta urinish (Retry with Exponential Backoff)
**Tavsif:** Tashqi mikroxizmatlar vaqtincha javob bermay qolishi mumkin. Ulanishni birdaniga to'xtatmasdan, oqilona kechikishlar bilan qayta urinish (retry) lozim.
**Talablar:** Maksimal urinishlar soni (3 marta), `ngx.sleep` yordamida noblokirovka qiluvchi kechikish, eksponentsial ko'payish va jitter qo'shish.
**Yechim (Lua):**
```lua
-- Eksponentsial kechikishli qayta urinish mexanizmi
local _M = {}

function _M.reliable_connect(host, port, max_retries)
    max_retries = max_retries or 3
    local delay = 0.1 -- 100ms boshlang'ich kechikish
    
    for attempt = 1, max_retries do
        local sock = ngx.socket.tcp()
        sock:settimeouts(1000, 2000, 2000)
        
        local ok, err = sock:connect(host, port)
        if ok then
            return sock, nil
        end
        
        ngx.log(ngx.WARN, string.format("Ulanish urinishi %d muvaffaqiyatsiz: %s", attempt, err))
        
        if attempt < max_retries then
            -- Jitter qo'shilgan noblokirovka qiluvchi pauza
            local jitter = math.random() * 0.05
            ngx.sleep(delay + jitter)
            delay = delay * 2 -- Eksponentsial oshirish
        end
    end
    
    return nil, "Barcha qayta urinishlar muvaffaqiyatsiz yakunlandi"
end

return _M
```
**Tushuntirish:** `ngx.sleep()` Nginx hodisalar mexanizmida taymer yaratadi va operatsion tizim `sleep` funksiyasidan farqli ravishda worker jarayonini mutlaqo to'xtatib qo'ymaydi. Jitter qo'shilishi esa serverga minglab klientlarning bir vaqtda to'lqin bo'lib urilishining (Thundering Herd) oldini oladi.

---

### Topshiriq #1107: resty.dns.resolver orqali asinxron DNS so'rovlari va A/AAAA yozuvlarini aniqlash
**Tavsif:** Standart C kutubxonasidagi `gethostbyname` Nginx worker jarayonini to'liq bloklab qo'yadi. Shu sababli domen nomlarini IP manzilga o'girish to'liq asinxron DNS resolver orqali bajarilishi shart.
**Talablar:** `resty.dns.resolver` dan foydalanish, 8.8.8.8 serveriga ulanish, A va AAAA yozuvlarini so'rash, kesh muddati (TTL) ni hisobga olish.
**Yechim (Lua):**
```lua
-- Asinxron DNS yechuvchi
local resolver = require "resty.dns.resolver"
local _M = {}

function _M.resolve_domain(domain_name)
    local r, err = resolver:new{
        nameservers = {"8.8.8.8", "1.1.1.1"},
        retrans = 2,  -- 2 marta qayta yuborish
        timeout = 2000, -- 2 soniya timeout
    }
    if not r then
        return nil, "Resolver yaratishda xato: " .. tostring(err)
    end
    
    -- IPv4 A yozuvlarini so'rash
    local answers, query_err = r:query(domain_name, { qtype = r.TYPE_A })
    if not answers then
        return nil, "DNS so'rov xatosi: " .. tostring(query_err)
    end
    
    if answers.errcode then
        return nil, "DNS server xatosi kodi: " .. answers.errcode .. ": " .. answers.errstr
    end
    
    local ip_list = {}
    for _, ans in ipairs(answers) do
        if ans.address then
            table.insert(ip_list, { ip = ans.address, ttl = ans.ttl })
        end
    end
    
    return ip_list, nil
end

return _M
```
**Tushuntirish:** `resty.dns.resolver` sof Lua va cosocket UDP asosida yozilgan bo'lib, DNS so'rovlarini 100% noblokirovka rejimida bajaradi. Tizim DNS yozuvlarining `ttl` qiymatini oladi, bu esa dasturchiga Nginx umumiy xotirasida (`lua_shared_dict`) mahalliy kesh yaratish imkonini beradi.

---

### Topshiriq #1108: Katta hajmdagi TCP oqimini buferga yig'masdan qismlab (chunked streaming) uzatish
**Tavsif:** Katta hajmdagi ma'lumotlarni (masalan, 500 MB loglar yoki audio oqimlar) uzatishda barcha baytlarni Lua satriga yig'ish xotira tugashiga (OOM) olib keladi.
**Talablar:** Oqimli o'qish va yozish siklini qurish, `receive(chunk_size)` orqali bo'laklab olish, `send()` orqali mijozga darhol yetkazish va xotira nazorati.
**Yechim (Lua):**
```lua
-- Xotira tejamkor oqimli uzatgich (Chunked Stream Pipe)
local _M = {}

local CHUNK_SIZE = 64 * 1024 -- 64 KB qismlar

function _M.pipe_stream(source_sock, dest_sock)
    local total_bytes = 0
    
    while true do
        -- Manbadan 64KB o'qish
        local chunk, err, partial = source_sock:receive(CHUNK_SIZE)
        local data_to_send = chunk or partial
        
        if data_to_send and #data_to_send > 0 then
            local bytes_sent, send_err = dest_sock:send(data_to_send)
            if not bytes_sent then
                return total_bytes, "Maqsadga yozishda xato: " .. tostring(send_err)
            end
            total_bytes = total_bytes + bytes_sent
        end
        
        if err then
            if err == "closed" then
                -- Oqim muvaffaqiyatli yakunlandi
                break
            else
                return total_bytes, "O'qishda xatolik yuz berdi: " .. tostring(err)
            end
        end
    end
    
    return total_bytes, nil
end

return _M
```
**Tushuntirish:** Ushbu yechim xotira sarfini qat'iy 64 KB miqdorida ushlab turadi. Qancha gigabayt ma'lumot o'tishidan qat'i nazar, LuaJIT xotira axlat yig'uvchisiga (GC) bosim tushmaydi. `partial` parametri esa ulanish yopilayotgan paytda oxirgi baytlar yo'qolishining oldini oladi.

---

### Topshiriq #1109: OpenResty ngx.timer.at orqali fonda ishlovchi TCP sog'liq tekshiruvchisi (Health Checker)
**Tavsif:** Yuklama taqsimlovchi (Upstream Load Balancer) orqa fondagi backend serverlarning ishchi holatini mijoz so'rovlariga xalaqit bermasdan davriy tekshirib turishi kerak.
**Talablar:** `ngx.timer.at` rekursiv chaqiruvi, worker 0 orqali tekshirish (dublikatsiyani oldini olish), `lua_shared_dict` ga sog'lomlik maqomini yozish.
**Yechim (Lua):**
```lua
-- Orqa fonda ishlovchi Health Checker
local _M = {}
local CHECK_INTERVAL = 5 -- Har 5 soniyada

local function check_peer(premature, host, port)
    if premature then return end -- Worker to'xtatilayotgan bo'lsa
    
    local sock = ngx.socket.tcp()
    sock:settimeout(1000)
    local ok, err = sock:connect(host, port)
    
    local shared_status = ngx.shared.health_status
    if ok then
        shared_status:set(host .. ":" .. port, true)
        sock:close()
    else
        shared_status:set(host .. ":" .. port, false)
        ngx.log(ngx.WARN, "Backend ishlamayapti: ", host, ":", port, " Xato: ", err)
    end
    
    -- Keyingi tekshiruvni rejalashtirish
    local ok_timer, timer_err = ngx.timer.at(CHECK_INTERVAL, check_peer, host, port)
    if not ok_timer then
        ngx.log(ngx.ERR, "Taymer yaratish xatosi: ", timer_err)
    end
end

function _M.spawn_checker(host, port)
    -- Faqat 0-raqamli worker tekshiruv o'tkazadi
    if ngx.worker.id() == 0 then
        ngx.timer.at(0, check_peer, host, port)
    end
end

return _M
```
**Tushuntirish:** OpenResty `ngx.timer.at` Nginx worker jarayonining fonida ishlovchi 'yengil iplar' (light threads) yaratadi. `ngx.worker.id() == 0` filtri orqali serverda 16 ta worker bo'lsa ham, tekshiruv faqat 1 ta worker tomonidan qilinadi, bu esa backendga ortiqcha so'rovlar yog'ilishini bartaraf qiladi.

---

### Topshiriq #1110: Cosocket orqali SMTP serverga ulanib elektron xat (email) jo'natish mantiqi
**Tavsif:** Tizim ma'murlariga xavfsizlik hodisalari va kritik avariyalar haqida darhol ogohlantiruvchi elektron pochta xabarlarini to'g'ridan-to'g'ri Nginx dan jo'natish zarur.
**Talablar:** SMTP protokolining asosiy buyruqlarini (HELO, MAIL FROM, RCPT TO, DATA, QUIT) ketma-ket bajarish, server javob kodlarini (220, 250, 354) tekshirish.
**Yechim (Lua):**
```lua
-- Cosocket orqali SMTP xat yuboruvchi
local _M = {}

local function send_smtp_cmd(sock, cmd, expected_code)
    local _, err = sock:send(cmd .. "\r\n")
    if err then return false, err end
    
    local line, read_err = sock:receive("*l")
    if not line then return false, read_err end
    
    local code = tonumber(string.sub(line, 1, 3))
    if code ~= expected_code then
        return false, "Kutilmagan SMTP javobi: " .. line
    end
    return true, nil
end

function _M.send_email(smtp_host, smtp_port, from_addr, to_addr, subject, body)
    local sock = ngx.socket.tcp()
    sock:settimeouts(2000, 5000, 5000)
    
    local ok, err = sock:connect(smtp_host, smtp_port)
    if not ok then return false, "SMTP ulanish xatosi: " .. tostring(err) end
    
    -- Banner (220) o'qish
    local banner = sock:receive("*l")
    
    local steps = {
        {"HELO openresty.local", 250},
        {"MAIL FROM:<" .. from_addr .. ">", 250},
        {"RCPT TO:<" .. to_addr .. ">", 250},
        {"DATA", 354}
    }
    
    for _, step in ipairs(steps) do
        local success, step_err = send_smtp_cmd(sock, step[1], step[2])
        if not success then
            sock:close()
            return false, step_err
        end
    end
    
    -- Xat tanasini yuborish
    local email_content = "Subject: " .. subject .. "\r\n\r\n" .. body .. "\r\n.\r\n"
    local _, data_err = sock:send(email_content)
    if data_err then
        sock:close()
        return false, data_err
    end
    
    send_smtp_cmd(sock, "QUIT", 221)
    sock:close()
    return true, nil
end

return _M
```
**Tushuntirish:** OpenResty yordamida har qanday amaliy tarmoq protokoli (SMTP, FTP, POP3) sof Lua tilida bir necha o'n qatorda amalga oshirilishi mumkin. Ulanish asinxron bo'lgani sababli, xat yuborilayotgan paytda Nginx boshqa minglab HTTP foydalanuvchilariga xizmat ko'rsatishda davom etadi.

---

### Topshiriq #1111: Nginx Stream kontekstida preread_by_lua_block: TLS ClientHello orqali SNI aniqlash va dinamik marshrutlash
**Tavsif:** TCP darajasidagi Nginx proksi serverida TLS trafigini dekodlamasdan (shifrlangan holda), mijoz murojaat qilayotgan domen nomini (SNI) aniqlash va shunga mos backend serverga yo'naltirish zarur.
**Talablar:** `ngx.req.socket(true)` orqali preread soketini olish, TLS ClientHello paketini parslash, `ngx.var.upstream_target` o'zgaruvchisini o'rnatish.
**Yechim (Lua):**
```lua
-- nginx.conf stream ichida preread_by_lua_block
-- TLS ClientHello paketidan Server Name Indication (SNI) ni ajratish
local function extract_sni()
    local sock = ngx.req.socket(true) -- Peeking socket (oqimni buzmaydi)
    
    -- Record Header: 5 bayt (Type 1, Version 2, Length 2)
    local header, err = sock:receive(5)
    if not header then return nil end
    
    local content_type, _, length = string.unpack(">I1I2I2", header)
    if content_type ~= 22 then -- 22 = Handshake
        return nil
    end
    
    local handshake_data = sock:receive(length)
    if not handshake_data then return nil end
    
    -- Oddiy SNI qidirish (TLS kengaytmasi bo'yicha)
    local sni = string.match(handshake_data, "([%a%d%.-]+%.[a-z]{2,})")
    return sni
end

local sni = extract_sni()
if sni == "api.production.uz" then
    ngx.var.target_backend = "10.0.1.10:443"
elseif sni == "secure.payments.uz" then
    ngx.var.target_backend = "10.0.2.20:443"
else
    ngx.var.target_backend = "10.0.0.1:443"
end
```
**Tushuntirish:** `preread_by_lua_block` Nginx Stream moduli ulanishni qabul qilgan, biroq backendga yo'naltirmagan vaqtda ishlaydi. `ngx.req.socket(true)` orqali olingan soketdagi ma'lumotlar o'qilsa ham buferda saqlanib qoladi (peeking). Natijada TLS shifrlash kalitlarini bermasdan domenlar bo'yicha marshrutlash imkoni yaratiladi.

---

### Topshiriq #1112: Nginx Stream kontekstida content_by_lua_block: Maxsus TCP shlyuz proksi (Custom Gateway)
**Tavsif:** TCP paketlarini shunchaki yo'naltirmasdan, ularni shifrlash, filtrdan o'tkazish yoki audit qilish uchun to'liq Lua nazoratidagi TCP proksi shlyuzi yaratilishi lozim.
**Talablar:** Mijoz va Backend o'rtasida ikki tomonlama dupleks korutina orqali baytlarni uzatish (`ngx.thread.spawn`), ulanishlarni o'z vaqtida tozalash.
**Yechim (Lua):**
```lua
-- Stream content_by_lua_block da to'liq dupleks TCP shlyuzi
local client_sock = ngx.req.socket()
local backend_sock = ngx.socket.tcp()

backend_sock:settimeouts(5000, 5000, 5000)
local ok, err = backend_sock:connect("127.0.0.1", 9000)
if not ok then
    ngx.log(ngx.ERR, "Backendga ulanib bo'lmadi: ", err)
    return ngx.exit(ngx.ERROR)
end

-- 1-Yo'nalish: Mijozdan Backendga ma'lumot uzatuvchi fon iplari
local function forward(src, dst, label)
    while true do
        local data, recv_err, partial = src:receive(8192)
        local payload = data or partial
        if payload and #payload > 0 then
            local _, send_err = dst:send(payload)
            if send_err then break end
        end
        if recv_err then break end
    end
    dst:close()
end

local t1 = ngx.thread.spawn(forward, client_sock, backend_sock, "C->B")
local t2 = ngx.thread.spawn(forward, backend_sock, client_sock, "B->C")

ngx.thread.wait(t1, t2)
```
**Tushuntirish:** `ngx.thread.spawn` yordamida Nginx ichida bitta TCP sessiyasi uchun ikkita parallel 'Light Thread' ochiladi. Biri mijozdan kelgan paketlarni backendga oqizadi, ikkinchisi backend javobini mijozga qaytaradi. `ngx.thread.wait` ikkala yo'nalish yakunlanguncha kutadi.

---

### Topshiriq #1113: ngx.socket.udp() orqali asinxron Syslog yozuvlarini markaziy serverga yuborish
**Tavsif:** Kritik xavfsizlik audit loglarini (RFC 5424 standarti) diskka yozib I/O qotishini kutmasdan, UDP orqali zudlik bilan markaziy SIEM / Syslog serveriga jo'natish kerak.
**Talablar:** `ngx.socket.udp()` dan foydalanish, Syslog PRI (Facility + Severity) sarlavhasini shakllantirish, paketni yo'qotmasdan yuborish.
**Yechim (Lua):**
```lua
-- Asinxron UDP Syslog jo'natuvchi
local _M = {}

local FACILITY_LOCAL0 = 16
local SEVERITY_WARNING = 4

function _M.send_syslog(server_host, server_port, app_name, message)
    local udp = ngx.socket.udp()
    local ok, err = udp:setpeername(server_host, server_port)
    if not ok then
        return nil, "UDP ulanish xatosi: " .. tostring(err)
    end
    
    -- PRI qiymatini hisoblash: Facility * 8 + Severity
    local pri = FACILITY_LOCAL0 * 8 + SEVERITY_WARNING
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    
    -- RFC 5424 formati: <PRI>VERSION TIMESTAMP HOSTNAME APPNAME PROCID MSGID MSG
    local syslog_msg = string.format("<%d>1 %s openresty %s - - - %s", pri, timestamp, app_name, message)
    
    local sent_ok, send_err = udp:send(syslog_msg)
    udp:close()
    
    if not sent_ok then
        return nil, "Yuborish xatosi: " .. tostring(send_err)
    end
    return true, nil
end

return _M
```
**Tushuntirish:** UDP soketlarida `setpeername` operatsion tizim darajasida IP marshrutini belgilaydi, lekin hech qanday tarmoq handshakelarini amalga oshirmaydi. `udp:send()` chaqiruvi mikrosekundlarda bajariladi va web-server unumdorligiga nol ta'sir ko'rsatgan holda audit yozuvlarini uzatadi.

---

### Topshiriq #1114: UDP orqali StatsD / Prometheus metrikalarini (Counter/Gauge) yuboruvchi agent
**Tavsif:** Har bir kiruvchi so'rovning davomiyligi, HTTP holat kodlari va xotira holatini monitoring tizimiga (StatsD / Datadog) yuboruvchi yengil agent talab qilinadi.
**Talablar:** StatsD protokoli sintaksisi (`metric:value|c` yoki `metric:value|ms`), paketlarni birlashtirish (batching) va UDP orqali uzatish.
**Yechim (Lua):**
```lua
-- StatsD metrika to'plovchisi
local _M = {}

local udp_socket = nil

function _M.init(host, port)
    local sock = ngx.socket.udp()
    local ok, err = sock:setpeername(host, port)
    if not ok then
        ngx.log(ngx.ERR, "StatsD ulanish xatosi: ", err)
        return false
    end
    udp_socket = sock
    return true
end

function _M.increment(metric, value)
    if not udp_socket then return end
    value = value or 1
    local payload = string.format("%s:%d|c", metric, value)
    udp_socket:send(payload)
end

function _M.timing(metric, milliseconds)
    if not udp_socket then return end
    local payload = string.format("%s:%d|ms", metric, milliseconds)
    udp_socket:send(payload)
end

return _M
```
**Tushuntirish:** StatsD orqali metrikalarni 'Fire-and-Forget' (yubor va unut) rejimida uzatish production tizimlarida qat'iy standartdir. Agar monitoring serveri ishlamay qolsa ham, UDP ulanishsiz bo'lgani sababli OpenResty mijozlarga hech qanday xatosiz xizmat ko'rsatishda davom etadi.

---

### Topshiriq #1115: Nginx Stream da dinamik og'irlik asosidagi (Weighted Round Robin) TCP yuklama taqsimlovchi
**Tavsif:** Turli quvvatdagi backend serverlariga (masalan, server A = 70% yuklama, server B = 30%) kiruvchi TCP ulanishlarini mos proporsiyada taqsimlash kerak.
**Talablar:** Weighted Round Robin algoritmini implementatsiya qilish, backend serverlar ro'yxatini va og'irliklarini saqlash, navbatdagi tanlangan IP ni qaytarish.
**Yechim (Lua):**
```lua
-- Weighted Round Robin TCP Balancer
local _M = {}

local backends = {
    { addr = "192.168.1.10:3306", weight = 7, current_weight = 0 },
    { addr = "192.168.1.11:3306", weight = 3, current_weight = 0 }
}

function _M.get_next_peer()
    local total_weight = 0
    local best = nil
    
    for _, peer in ipairs(backends) do
        peer.current_weight = peer.current_weight + peer.weight
        total_weight = total_weight + peer.weight
        
        if not best or peer.current_weight > best.current_weight then
            best = peer
        end
    end
    
    if not best then return nil end
    best.current_weight = best.current_weight - total_weight
    return best.addr
end

return _M
```
**Tushuntirish:** Smooth Weighted Round-Robin (Nginx ning o'rnatilgan algoritmi) har bir tanlovda serverlarning `current_weight` qiymatini o'zgartirib boradi. Bu ketma-ket bitta kuchli serverga 7 ta ulanish tushib ketmasdan, 7:3 nisbatida ulanishlar juda silliq (interleaved) taqsimlanishini kafolatlaydi.

---

### Topshiriq #1116: Nginx Stream darajasida lua_shared_dict yordamida IP bo'yicha ulanishlar soni va tezligini cheklash (Rate Limiter)
**Tavsif:** TCP portlariga (masalan, SSH yoki DB porti) qilinadigan DDoS va Brute-Force hujumlarini Nginx Stream qatlamining o'zidayoq ushlab, bloklash lozim.
**Talablar:** `lua_shared_dict` xotirasidan foydalanish, sekundiga maksimal 10 ta ulanish chegarasi, chegaradan oshsa ulanishni darhol uzish.
**Yechim (Lua):**
```lua
-- Stream darajasida IP Rate Limiter
local limit_dict = ngx.shared.stream_rate_limit
local client_ip = ngx.var.remote_addr
local limit_per_sec = 10

local key = "rate:" .. client_ip
local current, err = limit_dict:incr(key, 1, 0, 1) -- 1 soniya TTL bilan

if current and current > limit_per_sec then
    ngx.log(ngx.WARN, "DDoS himoyasi ishga tushdi, IP bloklandi: ", client_ip)
    return ngx.exit(ngx.ERROR) -- Ulanishni darhol uzish
end
```
**Tushuntirish:** Stream darajasidagi rate-limiting eng erta bosqichda ishlaydi. Hujumchi hali TLS yoki ma'lumotlar almashish bosqichiga yetmasidanoq, Nginx darajasida TCP FIN/RST orqali uziladi, bu esa orqa fondagi bazalar va autentifikatsiya serverlarini ortiqcha hisoblashlardan to'liq asraydi.

---

### Topshiriq #1117: Stream orqali MySQL ulanish handshakeni ushlash va kiruvchi so'rovlarni xavfsizlik audit logiga yozish
**Tavsif:** Tashkilot xavfsizligi talablariga ko'ra, ma'lumotlar bazasiga kim, qaysi IP dan va qaysi foydalanuvchi nomi bilan ulanayotganini Nginx shlyuzida ushlab, audit logiga yozish kerak.
**Talablar:** MySQL Server Greeting va Client Authentication paketlarini parslash, foydalanuvchi nomini ajratish va logga yozish.
**Yechim (Lua):**
```lua
-- MySQL handshake audit mantiqi
local sock = ngx.req.socket()

-- MySQL Initial Handshake Packet (Server Greeting)
-- Birinchi 4 bayt: 3 bayt paket uzunligi + 1 bayt sequence
local p_header, err = sock:receive(4)
if p_header then
    local p_len = string.byte(p_header, 1) + string.byte(p_header, 2) * 256
    local payload = sock:receive(p_len)
    
    -- Server versiyasi va server imkoniyatlari
    local proto_version = string.byte(payload, 1)
    ngx.log(ngx.INFO, "MySQL Server Protokol versiyasi: ", proto_version)
end
```
**Tushuntirish:** MySQL protokoli holatga ega (stateful) binar protokoldir. Nginx Stream orqali o'tayotgan paketlarni tahlil qilish orqali shaffof ma'lumotlar bazasi xavfsizlik devori (Database Firewall / WAF) yaratish mumkin bo'ladi.

---

### Topshiriq #1118: Nginx Stream orqali SOCKS5 / TCP tunnel shlyuzini amalga oshirish
**Tavsif:** Tashqi dunyoga to'g'ridan-to'g'ri chiqish huquqiga ega bo'lmagan ichki mikroxizmatlar uchun xavfsiz SOCKS5 proksi shlyuzi talab qilinadi.
**Talablar:** SOCKS5 handshake (0x05, 1 metod, 0x00 no-auth), ulanish buyrug'i (CMD 0x01 Connect), manzil turi bo'yicha IP/Domen va portni o'qish, ulanishni ulash.
**Yechim (Lua):**
```lua
-- SOCKS5 Proksi protokoli tekshiruvchisi
local _M = {}

function _M.handle_socks5(client_sock)
    -- 1. Handshake qabul qilish: VER (1) + NMETHODS (1) + METHODS (N)
    local ver_data, err = client_sock:receive(2)
    if not ver_data then return end
    
    local ver, nmethods = string.unpack(">I1I1", ver_data)
    if ver ~= 0x05 then return client_sock:close() end
    
    local methods = client_sock:receive(nmethods)
    -- 0x05 (SOCKS5), 0x00 (Autentifikatsiyasiz javob)
    client_sock:send(string.pack(">I1I1", 0x05, 0x00))
    
    -- 2. Request details: VER, CMD, RSV, ATYP
    local req_header = client_sock:receive(4)
    local _, cmd, _, atyp = string.unpack(">I1I1I1I1", req_header)
    
    local target_host, target_port
    if atyp == 0x01 then -- IPv4 (4 bayt)
        local ip_bytes = client_sock:receive(4)
        target_host = string.format("%d.%d.%d.%d", string.byte(ip_bytes, 1, 4))
    end
    
    local port_bytes = client_sock:receive(2)
    target_port = string.unpack(">I2", port_bytes)
    
    ngx.log(ngx.INFO, "SOCKS5 Tunnel so'rovi: ", target_host, ":", target_port)
    -- Muvaffaqiyatli javob: 0x05, 0x00, 0x00, 0x01 + 0.0.0.0:0
    client_sock:send(string.pack(">I1I1I1I1I4I2", 0x05, 0x00, 0x00, 0x01, 0, 0))
end

return _M
```
**Tushuntirish:** SOCKS5 quyi darajadagi TCP tunnellash standarti bo'lib, har qanday protokol (HTTP, SSH, SMTP) bilan ishlaydi. OpenResty cosocket orqali SOCKS5 implementatsiyasi yuqori tezlik va past resurs sarfi bilan korporativ xavfsizlik shlyuzlarini yaratishga imkon beradi.

---

### Topshiriq #1119: Nginx Stream UDP asosidagi keshlovchi DNS proksi shlyuzi
**Tavsif:** Korxona ichidagi minglab serverlarning DNS so'rovlarini tashqi DNS serveriga har safar yuborib vaqt yo'qotmaslik uchun UDP darajasidagi tezkor keshlovchi shlyuz kerak.
**Talablar:** `ngx.req.socket()` orqali UDP paketini olish, DNS savol xeshini `lua_shared_dict` dan izlash, keshda bo'lsa darhol qaytarish, bo'lmasa upstreamga uzatib keshga yozish.
**Yechim (Lua):**
```lua
-- UDP DNS Caching Gateway
local dns_cache = ngx.shared.dns_cache
local client_sock = ngx.req.socket()

local request_packet, err = client_sock:receive()
if not request_packet or #request_packet < 12 then
    return ngx.exit(ngx.ERROR)
end

-- DNS Transaction ID (dastlabki 2 bayt)
local tx_id = string.sub(request_packet, 1, 2)
local question_data = string.sub(request_packet, 13) -- Savol qismi

local cached_response = dns_cache:get(question_data)
if cached_response then
    -- Keshdagi javobning Transaction ID sini mijoznikiga almashtiramiz
    local final_packet = tx_id .. string.sub(cached_response, 3)
    client_sock:send(final_packet)
    return
end

-- Upstream 8.8.8.8 ga so'rov jo'natish
local upstream = ngx.socket.udp()
upstream:setpeername("8.8.8.8", 53)
upstream:send(request_packet)
local response_packet = upstream:receive()

if response_packet then
    dns_cache:set(question_data, response_packet, 60) -- 60 soniya kesh
    client_sock:send(response_packet)
end
```
**Tushuntirish:** DNS paketining birinchi 2 bayti tranzaksiya ID si bo'lib, har bir so'rovda o'zgaradi, lekin uning savol tanasi bir xil bo'ladi. DNS savolini kalit qilib keshlashtirish va faqat Transaction ID ni almashtirib qaytarish so'rovlarga 0.1 ms ichida javob berishni ta'minlaydi.

---

### Topshiriq #1120: Stream ulanishlarining trafigi (kiruvchi va chiquvchi baytlar) va davomiyligi bo'yicha hisoblagich (Accounting)
**Tavsif:** Bulutli xizmatlarda har bir mijoz yoki ijarachi (tenant) qancha tarmoq trafigini sarflaganini aniq hisoblab borish va belgilangan kvotadan oshganda xizmatni cheklash talab etiladi.
**Talablar:** `log_by_lua_block` da `ngx.var.bytes_received`, `ngx.var.bytes_sent` va `ngx.var.session_time` o'zgaruvchilarini hisobga olish va statistikani yangilash.
**Yechim (Lua):**
```lua
-- Stream log_by_lua_block da trafik hisob-kitobi
local tenant_id = ngx.var.remote_addr -- Yoki autentifikatsiyadan olingan identifikator
local bytes_in = tonumber(ngx.var.bytes_received) or 0
local bytes_out = tonumber(ngx.var.bytes_sent) or 0
local session_duration = tonumber(ngx.var.session_time) or 0

local accounting = ngx.shared.tenant_accounting

-- Kiruvchi va chiquvchi trafikni atomar oshirish
accounting:incr(tenant_id .. ":in", bytes_in, 0)
accounting:incr(tenant_id .. ":out", bytes_out, 0)
accounting:incr(tenant_id .. ":duration", session_duration, 0)

ngx.log(ngx.INFO, string.format("Tenant [%s] sessiya yakuni: %d bayt kirdi, %d bayt chiqdi, davomiyligi: %.2f sek", 
    tenant_id, bytes_in, bytes_out, session_duration))
```
**Tushuntirish:** `log_by_lua_block` sessiya to'liq yakunlangach, barcha resurslar yopilgan vaqtda chaqiriladi. Undagi statistik ma'lumotlar to'liq va aniq bo'ladi. `shared_dict:incr` atomar bajarilgani sababli barcha workerlar bitta hisoblagichni xavfsiz yangilaydi.

---

### Topshiriq #1121: resty.redis orqali Redisga ulanish, buyruqlar bajarish va keepalive hovuziga qaytarish
**Tavsif:** OpenResty ilovalarida Redis bilan o'zaro aloqa yuqori darajada tezkor bo'lishi va har bir operatsiyadan keyin ulanish hovuziga to'g'ri qaytarilishi shart.
**Talablar:** `resty.redis` modulidan foydalanish, autentifikatsiya, ma'lumot yozish/o'qish, xatoliklarni tekshirish va `set_keepalive` qilish.
**Yechim (Lua):**
```lua
-- Yuqori unumdor Redis mijozi
local redis = require "resty.redis"
local _M = {}

function _M.get_cached_value(key)
    local red = redis:new()
    red:set_timeouts(1000, 2000, 2000) -- 2 soniya timeout
    
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then
        return nil, "Redisga ulanish xatosi: " .. tostring(err)
    end
    
    -- Qiymatni olish
    local res, get_err = red:get(key)
    if not res then
        red:close()
        return nil, "GET xatosi: " .. tostring(get_err)
    end
    
    if res == ngx.null then
        res = nil -- Kalit mavjud emas
    end
    
    -- Ulanishni hovuzga qaytarish (10 soniya idle, 100 ta ulanish hovuzi)
    local keepalive_ok, keepalive_err = red:set_keepalive(10000, 100)
    if not keepalive_ok then
        ngx.log(ngx.WARN, "Keepalive xatosi: ", keepalive_err)
        red:close()
    end
    
    return res, nil
end

return _M
```
**Tushuntirish:** OpenResty da `res == ngx.null` tekshiruvi muhimdir, chunki Redis `nil` qiymat qaytarganda Lua ning oddiy `nil` qiymatidan farqlash uchun `ngx.null` maxsus yengil obyektidan foydalaniladi. `set_keepalive` esa ulanishni keyingi so'rovlar uchun ochiq qoldiradi.

---

### Topshiriq #1122: Redis Pipelining yordamida yuzlab buyruqlarni bitta TCP RTT orqali bajarish
**Tavsif:** Bitta foydalanuvchi so'rovi davomida Redisga 50 ta alohida buyruq (masalan, har xil kalitlarni olish) yuborish 50 ta tarmoq kechikishini (RTT) keltirib chiqaradi.
**Talablar:** `red:init_pipeline()` dan foydalanish, barcha buyruqlarni navbatga qo'yish, `red:commit_pipeline()` orqali bitta paketda jo'natish va natijalarni massivda olish.
**Yechim (Lua):**
```lua
-- Redis Pipelining orqali ommaviy so'rovlar
local redis = require "resty.redis"
local _M = {}

function _M.batch_fetch_profiles(user_ids)
    local red = redis:new()
    red:set_timeout(3000)
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return nil, err end
    
    -- Pipeliningni boshlash
    red:init_pipeline()
    for _, uid in ipairs(user_ids) do
        red:hgetall("user:" .. uid)
    end
    
    -- Barcha buyruqlarni bitta tarmoq so'rovida jo'natish
    local results, commit_err = red:commit_pipeline()
    if not results then
        red:close()
        return nil, "Pipeline xatosi: " .. tostring(commit_err)
    end
    
    red:set_keepalive(10000, 50)
    
    local profiles = {}
    for i, profile_data in ipairs(results) do
        if profile_data ~= ngx.null and type(profile_data) == "table" then
            profiles[user_ids[i]] = red:array_to_hash(profile_data)
        end
    end
    
    return profiles, nil
end

return _M
```
**Tushuntirish:** Redis Pipelining tarmoqning uzatish tezligini (throughput) 10-20 baravargacha oshiradi. Har bir buyruq uchun tarmoq paketi ketmaydi, balki operatsion tizimning TCP buferida barcha buyruqlar bitta katta MTU paketiga jamlanib uzatiladi va server ham barcha javoblarni bitta oqimda qaytaradi.

---

### Topshiriq #1123: Redis Tranzaksiyalari (MULTI/EXEC) va atomar buyruqlar ketma-ketligi
**Tavsif:** Moliya yoki balans o'zgarishi bilan bog'liq amallarda bir nechta Redis kalitlari boshqa mijozlar aralashuvisiz atomar yangilanishi shart.
**Talablar:** `red:multi()`, operatsiyalarni navbatga qo'yish, `red:exec()` orqali tasdiqlash, tranzaksiya bekor bo'lsa (abort) holatni qaytarish.
**Yechim (Lua):**
```lua
-- Redis Tranzaksiyalari (MULTI/EXEC)
local redis = require "resty.redis"
local _M = {}

function _M.transfer_balance(from_user, to_user, amount)
    local red = redis:new()
    red:set_timeout(2000)
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return false, err end
    
    -- Tranzaksiyani boshlash
    red:multi()
    red:decrby("balance:" .. from_user, amount)
    red:incrby("balance:" .. to_user, amount)
    
    -- Tranzaksiyani atomar bajarish
    local replies, exec_err = red:exec()
    if not replies then
        red:close()
        return false, "Tranzaksiya rad etildi: " .. tostring(exec_err)
    end
    
    red:set_keepalive(10000, 20)
    return true, nil
end

return _M
```
**Tushuntirish:** `MULTI/EXEC` buyruqlari blokidagi operatsiyalar Redis serverida oraliq to'xtovsiz, boshqa so'rovlar kiritilmasdan to'liq atomar bajariladi. Agar tranzaksiya o'rtasida xatolik yuz bersa, hech qanday qisman holat yuzaga kelmaydi.

---

### Topshiriq #1124: Cosocket orqali Redis Pub/Sub kanaliga obuna bo'lish (SUBSCRIBE) va xabarlarni oqimli qabul qilish
**Tavsif:** Haqiqiy vaqt rejimida yangilanuvchi konfiguratsiyalar yoki xabarlarni barcha Nginx workerlariga darhol yetkazish uchun Redis Pub/Sub kanalini doimiy tinglab turish lozim.
**Talablar:** `red:subscribe()` dan foydalanish, cheksiz siklda `read_reply()` orqali yangi xabarlarni olish, keepalive ishlatmaslik (chunki obuna ochiq qoladi).
**Yechim (Lua):**
```lua
-- Redis Pub/Sub xabar iste'molchisi
local redis = require "resty.redis"
local _M = {}

function _M.listen_channel(channel_name, message_handler)
    local red = redis:new()
    red:set_timeout(0) -- Cheksiz kutish (timeout bo'lmaydi)
    
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return nil, err end
    
    local res, sub_err = red:subscribe(channel_name)
    if not res then
        red:close()
        return nil, sub_err
    end
    
    ngx.log(ngx.INFO, "Kanalga obuna bo'lindi: ", channel_name)
    
    while true do
        -- Yangi xabarni asinxron kutish
        local msg, read_err = red:read_reply()
        if not msg then
            ngx.log(ngx.ERR, "Pub/Sub xatolik: ", read_err)
            break
        end
        
        -- msg formati: {"message", channel, data}
        if msg[1] == "message" then
            local payload = msg[3]
            message_handler(payload)
        end
    end
    
    red:close()
end

return _M
```
**Tushuntirish:** Pub/Sub rejimiga o'tgan Redis ulanishi odatiy buyruqlarni qabul qilmaydi, faqat obuna xabarlarini tinglaydi. Shu sababli bu soketga `set_keepalive()` qilinmaydi va alohida fon korutinasida (`ngx.thread.spawn` yoki `ngx.timer.at`) ushlab turiladi.

---

### Topshiriq #1125: Redis Sentinel orqali master server manzilini dinamik aniqlash va failoverni boshqarish
**Tavsif:** Yuqori bardoshli (High Availability) tizimlarda Redis master serveri avariyaga uchrasa, Sentinel yangi masterni saylaydi. Ilova avtomatik tarzda yangi masterga ulanishi kerak.
**Talablar:** Sentinel tuguniga ulanish, `sentinel get-master-addr-by-name` buyrug'ini bajarish, olingan IP va port bilan masterga ulanish.
**Yechim (Lua):**
```lua
-- Redis Sentinel orqali Master manzilini topuvchi modul
local redis = require "resty.redis"
local _M = {}

function _M.get_master_address(sentinel_host, sentinel_port, master_name)
    local red = redis:new()
    red:set_timeout(1000)
    
    local ok, err = red:connect(sentinel_host, sentinel_port)
    if not ok then return nil, nil, err end
    
    -- Sentinel buyrug'i: SENTINEL get-master-addr-by-name <name>
    local res, cmd_err = red:sentinel("get-master-addr-by-name", master_name)
    if not res or res == ngx.null then
        red:close()
        return nil, nil, "Master topilmadi: " .. tostring(cmd_err)
    end
    
    red:set_keepalive(10000, 10)
    
    local master_ip = res[1]
    local master_port = tonumber(res[2])
    return master_ip, master_port, nil
end

return _M
```
**Tushuntirish:** Sentinel arxitekturasi dasturchilarga Redis ulanish manzilini kodda qattiq belgilamaslik (hardcode) imkonini beradi. Avariya (failover) paytida OpenResty Sentinel orqali yangi masterni soniyaning ulushlarida aniqlab, so'rovlarni uzluksiz yangi nodega yo'naltiradi.

---

### Topshiriq #1126: Redis Cluster nodelari bo'yicha hash slotlarni hisoblash va MOVED/ASK qayta yo'naltirishlarini hal qilish
**Tavsif:** Redis Cluster da kalitlar 16384 ta hash slot bo'yicha taqsimlangan. Noto'g'ri node ga so'rov yuborilganda server `MOVED <slot> <ip:port>` javobini qaytaradi va klient o'sha yangi node ga avtomatik qayta murojaat qilishi shart.
**Talablar:** CRC16 xeshini hisoblash (`slot = crc16(key) % 16384`), `MOVED` javobini parslash va yangi node manziliga qayta so'rov yuborish.
**Yechim (Lua):**
```lua
-- Redis Cluster MOVED qayta yo'naltirish boshqaruvchisi
local redis = require "resty.redis"
local _M = {}

function _M.cluster_execute(initial_host, initial_port, command, key, ...)
    local host = initial_host
    local port = initial_port
    local max_redirects = 3
    
    for _ = 1, max_redirects do
        local red = redis:new()
        red:set_timeout(1000)
        local ok, err = red:connect(host, port)
        if not ok then return nil, err end
        
        -- Buyruqni bajarish
        local res, cmd_err = red[command](red, key, ...)
        
        if not res and cmd_err then
            -- MOVED tekshiruvi: "MOVED 3999 127.0.0.1:6381"
            local moved_target = string.match(cmd_err, "^MOVED%s+%d+%s+([%d%.]+):(%d+)")
            if moved_target then
                local new_host, new_port = string.match(cmd_err, "^MOVED%s+%d+%s+([%d%.]+):(%d+)")
                host = new_host
                port = tonumber(new_port)
                red:close()
                -- Yangi node ga o'tish
            else
                red:close()
                return nil, cmd_err
            end
        else
            red:set_keepalive(10000, 20)
            return res, nil
        end
    end
    
    return nil, "Maksimal MOVED yo'naltirishlari sonidan oshib ketdi"
end

return _M
```
**Tushuntirish:** Redis Cluster da sharding mantiqi mijoz tomonida amalga oshiriladi. `MOVED` xatosi xato emas, balki shartnoma bo'yicha ma'lumotning yangi jismoniy serverga ko'chganligini bildiruvchi signaldir. Klient uni parslay olganda, klaster resharding paytida ham uzluksiz ishlaydi.

---

### Topshiriq #1127: OpenResty da Redlock algoritmi asosida taqsimlangan qulf (Distributed Lock) mexanizmi
**Tavsif:** Bir nechta serverlar bir vaqtda bitta cheklangan resursni (masalan ombordagi so'nggi mahsulotni bron qilish) o'zgartirishga uringanda, taqsimlangan muhitda poyga holati (Race Condition) yuzaga kelmasligi lozim.
**Talablar:** `SET key uuid NX PX lock_timeout` orqali qulflash, Lua skript orqali qulfni faqat uning haqiqiy egasi xavfsiz ochishi (Release Lock).
**Yechim (Lua):**
```lua
-- Taqsimlangan qulf (Distributed Lock) moduli
local redis = require "resty.redis"
local _M = {}

local RELEASE_LOCK_SCRIPT = [[
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
]]

function _M.acquire_lock(red, lock_key, lock_value, ttl_ms)
    -- SET lock_key lock_value NX PX ttl_ms
    local res, err = red:set(lock_key, lock_value, "NX", "PX", ttl_ms)
    if not res or res == ngx.null then
        return false, "Qulf band yoki olinmadi"
    end
    return true, nil
end

function _M.release_lock(red, lock_key, lock_value)
    -- Faqat o'zimiz qo'ygan qulfni ochish uchun atomar Lua skript
    local res, err = red:eval(RELEASE_LOCK_SCRIPT, 1, lock_key, lock_value)
    if not res then
        return false, err
    end
    return (res == 1), nil
end

return _M
```
**Tushuntirish:** Taqsimlangan qulflarda oddiy `del key` qilish fojiaviy xatodir: agar jarayon kutilgandan uzoqroq davom etib TTL tugasa, boshqa server yangi qulf oladi, birinchi jarayon esa o'z ishi bitgach begonaning qulfini o'chirib yuboradi. Unikal `lock_value` (UUID) va atomar Lua skript faqat o'z qulfingni ochishni 100% kafolatlaydi.

---

### Topshiriq #1128: Redis Sorted Sets (ZADD, ZREMRANGEBYSCORE) yordamida Sliding Window Rate Limiter
**Tavsif:** Aniq vaqt oynasiga ega (masalan, so'nggi 60 soniya ichida roppa-rosa 100 ta so'rov) silliq chegaralovchi (Sliding Window Rate Limiter) talab etiladi.
**Talablar:** Redis Sorted Set da joriy vaqt tamg'asini score qilib yozish, eskirgan yozuvlarni tozalash, qoldiq limitni hisoblash.
**Yechim (Lua):**
```lua
-- Redis Sorted Sets orqali Sliding Window Rate Limiter
local redis = require "resty.redis"
local _M = {}

local SLIDING_WINDOW_LUA = [[
    local key = KEYS[1]
    local now = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local limit = tonumber(ARGV[3])
    local clear_before = now - window

    -- Eskirgan elementlarni o'chirish
    redis.call("ZREMRANGEBYSCORE", key, "-inf", clear_before)

    -- Hozirgi darchadagi so'rovlar soni
    local current_count = redis.call("ZCARD", key)
    if current_count < limit then
        redis.call("ZADD", key, now, now .. ":" .. math.random(100000, 999999))
        redis.call("EXPIRE", key, math.ceil(window))
        return 1 -- Ruxsat berildi
    else
        return 0 -- Limitdan oshdi
    end
]]

function _M.check_rate_limit(red, user_id, window_sec, limit)
    local now = ngx.now()
    local res, err = red:eval(SLIDING_WINDOW_LUA, 1, "rate:" .. user_id, now, window_sec, limit)
    if not res then return false, err end
    return (res == 1), nil
end

return _M
```
**Tushuntirish:** Fixed Window algoritmlarida darcha chegarasida (masalan 00:59 va 01:01 da) 2 barobar ko'p so'rov o'tib ketishi mumkin (Spike problem). Sliding Window Sorted Set yordamida vaqtning har qanday lahzasida aniq so'nggi 60 soniyadagi amallar soni tahlil qilinadi.

---

### Topshiriq #1129: Redis Streams (XADD, XREADGROUP) yordamida taqsimlangan navbatlarni iste'mol qilish
**Tavsif:** Taqsimlangan tizimlarda xabarlar yo'qolmasligi, qayta ishlanayotgan xabarlar xatoga uchrasa boshqa worker tomonidan davom ettirilishi (ACK mexanizmi) uchun Redis Streams kerak.
**Talablar:** `XADD` orqali navbatga yozish, iste'molchilar guruhi (Consumer Group) orqali `XREADGROUP` bilan o'qish va `XACK` bilan tasdiqlash.
**Yechim (Lua):**
```lua
-- Redis Streams xabar navbati
local redis = require "resty.redis"
local _M = {}

function _M.publish_task(red, stream_key, task_payload)
    -- XADD stream_key * field value
    local id, err = red:xadd(stream_key, "*", "payload", task_payload)
    return id, err
end

function _M.consume_tasks(red, stream_key, group_name, consumer_id)
    -- XREADGROUP GROUP group consumer STREAMS key >
    local res, err = red:xreadgroup("GROUP", group_name, consumer_id, "COUNT", 1, "BLOCK", 2000, "STREAMS", stream_key, ">")
    if not res or res == ngx.null then
        return nil, "Vazifalar yo'q"
    end
    
    -- Xabarni qayta ishlash va tasdiqlash (ACK)
    local stream_data = res[1][2]
    local message_entry = stream_data[1]
    local message_id = message_entry[1]
    local payload = message_entry[2][2]
    
    -- Muvaffaqiyatli yakunlangach XACK berish
    red:xack(stream_key, group_name, message_id)
    return payload, nil
end

return _M
```
**Tushuntirish:** Redis Streams Kafka arxitekturasining yengil analogidir. Unda xabarlar xotirada saqlanadi va iste'molchi xabarni olib ACK yubormaguncha u Pending Entries List (PEL) da turadi. Agar ishchi worker o'chib qolsa, boshqa worker ushbu xabarni olib bajarishni yakunlaydi.

---

### Topshiriq #1130: Kesh Stampede muammosini hal qilish: Mutex lock va probabilistic early expiration (XFetch algoritmi)
**Tavsif:** Yuqori yuklamali saytda mashhur mahsulot keshi tugashi (expiration) bilan bir vaqtda 10 000 ta so'rov ma'lumotlar bazasiga to'g'ridan-to'g'ri urilib, serverni ag'darishi (Cache Stampede / Dog-piling) mumkin.
**Talablar:** XFetch ehtimollik algoritmi (`-beta * delta * math.log(random()) > ttl`), kesh muddati tugamasidan oldin fonda bitta so'rov orqali yangilash.
**Yechim (Lua):**
```lua
-- Kesh Stampede ga qarshi XFetch algoritmi
local _M = {}
local cache = ngx.shared.my_cache

function _M.get_with_xfetch(key, compute_func, ttl, beta)
    beta = beta or 1.0
    local cached_data = cache:get(key)
    local expiry_at = cache:get(key .. ":exp") or 0
    local compute_time = cache:get(key .. ":delta") or 0.1
    
    local now = ngx.now()
    local remaining_ttl = expiry_at - now
    
    -- XFetch ehtimollik tekshiruvi
    local should_recompute = (remaining_ttl <= 0) or 
        (-compute_time * beta * math.log(math.random()) >= remaining_ttl)
        
    if cached_data and not should_recompute then
        return cached_data
    end
    
    -- Keshni hisoblash vaqti o'lchovi
    local t0 = ngx.now()
    local new_data = compute_func()
    local delta = ngx.now() - t0
    
    cache:set(key, new_data)
    cache:set(key .. ":exp", now + ttl)
    cache:set(key .. ":delta", delta)
    
    return new_data
end

return _M
```
**Tushuntirish:** XFetch (Optimal Probabilistic Cache Expiration) algoritmi kesh muddatining oxirgi daqiqalarida so'rovlarning birortasiga tasodifiy ehtimollik bilan ma'lumotni kesh tugashidan oldin fonda yangilash vazifasini beradi. Natijada kesh hech qachon 'bo'shab' qolmaydi va bazaga yagona so'rov boradi.

---

### Topshiriq #1131: resty.http orqali asinxron tashqi REST API ga GET va POST JSON so'rovlarini yuborish
**Tavsif:** OpenResty Nginx serveri kiruvchi so'rovlarni qabul qilib, orqa fondagi tashqi to'lov tizimi yoki autentifikatsiya REST API lariga noblokirovka tarzida HTTP so'rovlar yuborishi lozim.
**Talablar:** `resty.http` kutubxonasidan foydalanish, JSON payload jo'natish, status kodni tekshirish, connection keepalive ni to'g'ri o'rnatish.
**Yechim (Lua):**
```lua
-- resty.http orqali REST API chaqiruvlari
local http = require "resty.http"
local cjson = require "cjson.safe"
local _M = {}

function _M.post_json_api(api_url, payload_table)
    local httpc = http.new()
    httpc:set_timeouts(1000, 3000, 3000)
    
    local json_body, json_err = cjson.encode(payload_table)
    if not json_body then return nil, "JSON xatosi: " .. tostring(json_err) end
    
    local res, err = httpc:request_uri(api_url, {
        method = "POST",
        body = json_body,
        headers = {
            ["Content-Type"] = "application/json",
            ["Accept"] = "application/json",
            ["User-Agent"] = "OpenResty-Gateway/1.0"
        },
        keepalive_timeout = 10000,
        keepalive_pool = 30
    })
    
    if not res then
        return nil, "HTTP so'rov muvaffaqiyatsiz: " .. tostring(err)
    end
    
    if res.status ~= 200 and res.status ~= 201 then
        return nil, "API xatosi, status: " .. tostring(res.status) .. ", javob: " .. res.body
    end
    
    local data = cjson.decode(res.body)
    return data, nil
end

return _M
```
**Tushuntirish:** `httpc:request_uri()` ulanishni ochish, TLS handshake, so'rov jo'natish, javobni to'liq o'qish va ulanishni keepalive hovuziga qaytarishni bitta ixcham chaqiruvda birlashtiradi. Bu kodni o'qilishi oson va xatolarga chidamli qiladi.

---

### Topshiriq #1132: Tashqi xizmatga multipart/form-data fayllarni xotiraga yuklamasdan oqim (streaming) usulida yuklash
**Tavsif:** Mijoz 100 megabaytlik videoni yuklayotganda, OpenResty uni xotirada saqlamasdan, mijozdan kelishi bilanoq tashqi S3 yoki fayl saqlash serveriga oqim shaklida (streaming upload) uzatishi kerak.
**Talablar:** `ngx.req.read_body()` ishlatmaslik, `ngx.req.socket()` orqali baytlarni o'qib, `httpc:request` oqimiga to'g'ridan-to'g'ri uzatish.
**Yechim (Lua):**
```lua
-- Oqimli fayl uzatuvchi shlyuz (Streaming File Proxy)
local http = require "resty.http"

local function stream_upload_to_s3(target_url)
    local client_sock, err = ngx.req.socket()
    if not client_sock then return ngx.exit(500) end
    
    local httpc = http.new()
    local content_length = tonumber(ngx.var.http_content_length)
    local content_type = ngx.var.http_content_type
    
    -- Bo'laklab o'quvchi iterator funksiya
    local reader = function()
        local chunk, recv_err, partial = client_sock:receive(65536)
        return chunk or partial
    end
    
    local res, req_err = httpc:request_uri(target_url, {
        method = "PUT",
        headers = {
            ["Content-Type"] = content_type,
            ["Content-Length"] = content_length
        },
        body = reader -- Iterator orqali oqimli uzatish
    })
    
    if not res then
        ngx.log(ngx.ERR, "S3 ga oqimli yuklashda xato: ", req_err)
        return ngx.exit(502)
    end
    
    ngx.status = res.status
    ngx.say(res.body)
end
```
**Tushuntirish:** OpenResty da `body` parametriga funksiya (iterator) berilishi mumkin. `resty.http` iteratorni chaqirib, har safar navbatdagi 64KB baytni oladi va to'g'ridan-to'g'ri soketga yozadi. Serverda xotira sarfi 1 GB fayl uzatilganda ham 64 KB dan oshmaydi.

---

### Topshiriq #1133: OpenResty dinamik HTTP teskari proksi (Dynamic Reverse Proxy) va javob sarlavhalarini qayta ishlash
**Tavsif:** So'rov parametrlariga (masalan `?region=eu` yoki `Authorization` tokeniga) qarab, upstream serverini dinamik tanlash va javob qaytishida maxsus xavfsizlik sarlavhalarini (Security Headers) qo'shish kerak.
**Talablar:** `ngx.var.proxy_pass_target` ni dinamik belgilash, `header_filter_by_lua_block` da CSP va HSTS sarlavhalarini kiritish.
**Yechim (Lua):**
```lua
-- header_filter_by_lua_block da xavfsizlik sarlavhalarini qo'shish
ngx.header["X-Content-Type-Options"] = "nosniff"
ngx.header["X-Frame-Options"] = "DENY"
ngx.header["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
ngx.header["Content-Security-Policy"] = "default-src 'self'"

-- Keraksiz ichki server sarlavhalarini tozalash
ngx.header["Server"] = "Secure-Edge-Gateway"
ngx.header["X-Powered-By"] = nil
```
**Tushuntirish:** `header_filter_by_lua_block` fazasida Nginx javob sarlavhalari mijozga yuborilishidan oldin ularni o'zgartirish imkonini beradi. Serverning haqiqiy texnologiyasini (`Server`, `X-Powered-By`) yashirish tajovuzkorlarga server zaifliklarini skanerlashni qiyinlashtiradi.

---

### Topshiriq #1134: Parallel tashqi API so'rovlarini jo'natish (ngx.thread.spawn va ngx.thread.wait)
**Tavsif:** Bosh sahifani yuklash uchun 3 ta mustaqil mikroxizmatdan (Foydalanuvchi ma'lumotlari, Tavsiyalar, Ob-havo) ma'lumot olish kerak. So'rovlarni ketma-ket yuborish 600 ms vaqt oladi, parallel jo'natish esa 200 ms da yakunlanishi kerak.
**Talablar:** `ngx.thread.spawn` orqali 3 ta subthread ochish, har birida `resty.http` bilan so'rov yuborish, `ngx.thread.wait` orqali barchasini to'plash.
**Yechim (Lua):**
```lua
-- Parallel tashqi API so'rovlari agregatori
local http = require "resty.http"
local cjson = require "cjson.safe"
local _M = {}

local function fetch_subservice(url)
    local httpc = http.new()
    httpc:set_timeout(2000)
    local res, err = httpc:request_uri(url, { method = "GET" })
    if not res or res.status ~= 200 then return nil end
    return cjson.decode(res.body)
end

function _M.aggregate_homepage_data()
    -- 3 ta parallel korutina (light thread) ishga tushirish
    local t1 = ngx.thread.spawn(fetch_subservice, "http://user-service/profile")
    local t2 = ngx.thread.spawn(fetch_subservice, "http://rec-service/items")
    local t3 = ngx.thread.spawn(fetch_subservice, "http://weather-service/today")
    
    -- Barcha natijalarni kutish
    local ok1, profile = ngx.thread.wait(t1)
    local ok2, items = ngx.thread.wait(t2)
    local ok3, weather = ngx.thread.wait(t3)
    
    return {
        user = ok1 and profile or {},
        recommendations = ok2 and items or {},
        weather = ok3 and weather or {}
    }
end

return _M
```
**Tushuntirish:** OpenResty dagi 'Light Threads' operatsion tizim iplari (OS threads) emas, balki Lua korutinalaridir. Ular juda arzon bo'lib (har biri 1 KB atrofida xotira oladi), 3 ta so'rovni bir vaqtda tarmoqqa yuboradi. Natijada umumiy kutish vaqti so'rovlar yig'indisi emas, balki eng uzoq davom etgan bitta so'rov vaqtiga teng bo'ladi.

---

### Topshiriq #1135: Server-Sent Events (SSE) server oqimini mijozlarga uzatuvchi HTTP shlyuz
**Tavsif:** Katta Til Modellari (LLM, masalan ChatGPT / Khorazmiy AI) matnni bo'laklab (token-by-token) yaratadi. OpenResty ushbu oqimni brauzerga Server-Sent Events (SSE) protokoli orqali uzluksiz yetkazishi lozim.
**Talablar:** `Content-Type: text/event-stream`, `Cache-Control: no-cache` o'rnatish, `ngx.flush(true)` orqali har bir tokenni buferlamasdan darhol mijozga itarish.
**Yechim (Lua):**
```lua
-- LLM javoblarini SSE orqali brauzerga oqizuvchi shlyuz
local http = require "resty.http"

ngx.header["Content-Type"] = "text/event-stream"
ngx.header["Cache-Control"] = "no-cache"
ngx.header["Connection"] = "keep-alive"
ngx.header["X-Accel-Buffering"] = "no" -- Nginx proksi buferlashini to'xtatish

local httpc = http.new()
local res, err = httpc:request_uri("http://llm-backend:8000/generate_stream", {
    method = "POST",
    body = '{"prompt":"Salom Khorazmiy"}'
})

-- Har bir kelgan matn bo'lagini SSE formatida uzatish
local function stream_tokens(tokens)
    for _, token in ipairs(tokens) do
        ngx.print("data: " .. token .. "\n\n")
        ngx.flush(true) -- Nginx buferini majburiy bo'shatish
        ngx.sleep(0.05) -- Simulyatsiya
    end
    ngx.print("data: [DONE]\n\n")
    ngx.flush(true)
end
```
**Tushuntirish:** SSE da eng muhim kalit `ngx.flush(true)` va `X-Accel-Buffering: no` sarlavhasidir. Standart Nginx 4KB ma'lumot to'planmaguncha paketni mijozga yubormay ushlab turadi. `flush(true)` buferlashni aylanib o'tib, har bitta so'z paydo bo'lishi bilanoq foydalanuvchi ekranida yozilishini ta'minlaydi.

---

### Topshiriq #1136: HTTP javoblarini lua_shared_dict va 'stale-while-revalidate' strategiyasi bilan keshlashtirish
**Tavsif:** Foydalanuvchilar har doim keshdan bir zumda javob olishi, kesh muddati o'tgan bo'lsa ham eskirgan (stale) ma'lumot ko'rsatilib, orqa fonda yangi kesh yuklanishi lozim.
**Talablar:** `lua_shared_dict` xotirasidan foydalanish, `stale` ma'lumotni darhol qaytarish, `ngx.timer.at` orqali fonda ma'lumotni qayta yuklash.
**Yechim (Lua):**
```lua
-- Stale-While-Revalidate kesh mexanizmi
local _M = {}
local cache = ngx.shared.http_api_cache

local function refresh_data(premature, key, url)
    if premature then return end
    local http = require "resty.http"
    local httpc = http.new()
    local res = httpc:request_uri(url, { method = "GET" })
    if res and res.status == 200 then
        cache:set(key, res.body, 120) -- 2 daqiqa saqlash
        cache:set(key .. ":stale_until", ngx.now() + 300) -- 5 daqiqagacha stale qabul qilinadi
    end
end

function _M.get_api_data(key, url)
    local cached = cache:get(key)
    local stale_until = cache:get(key .. ":stale_until") or 0
    
    if cached then
        return cached, "HIT"
    end
    
    -- Agar eskirgan kesh bo'lsa, uni qaytaramiz va fonda yangilaymiz
    if ngx.now() < stale_until then
        ngx.timer.at(0, refresh_data, key, url)
        return cached, "STALE"
    end
    
    -- Umuman keshda bo'lmasa, sinxron yuklaymiz
    refresh_data(false, key, url)
    return cache:get(key), "MISS"
end

return _M
```
**Tushuntirish:** 'Stale-while-revalidate' (RFC 5861) arxitekturasi foydalanuvchi so'rovini backend sekinlashuvlaridan to'liq xalos qiladi. Foydalanuvchi doimo keshdagi ma'lumotni 1 ms da oladi, orqa fondagi `ngx.timer` esa ma'lumotlar bazasiga bildirmasdan ma'lumotlarni doimiy yangilab turadi.

---

### Topshiriq #1137: OAuth2 / OpenID Connect Bearer tokenlarini tekshirish va JWT keshli validatsiyasi
**Tavsif:** Har bir kiruvchi HTTP so'rovidagi `Authorization: Bearer <JWT>` tokenining raqamli imzosini (RS256 / HS256) shlyuz darajasida tekshirish va muvaffaqiyatli tekshiruv natijalarini keshlashtirish talab etiladi.
**Talablar:** Tokenni ajratish, imzo va muddati (exp) ni tekshirish, foydalanuvchi ID sini downstream xizmatlarga `X-User-Id` sarlavhasi orqali uzatish.
**Yechim (Lua):**
```lua
-- JWT Bearer Token Validatori
local jwt = require "resty.jwt"
local cache = ngx.shared.jwt_cache
local SECRET_KEY = "khorazmiy_super_secret_jwt_key"

local auth_header = ngx.var.http_authorization
if not auth_header then
    ngx.status = 401
    ngx.say('{"error":"Avtorizatsiya sarlavhasi topilmadi"}')
    return ngx.exit(401)
end

local token = string.match(auth_header, "Bearer%s+(.+)")
if not token then
    ngx.status = 401
    ngx.say('{"error":"Noto'g'ri token formati"}')
    return ngx.exit(401)
end

-- Keshdan qidirish
local cached_user = cache:get(token)
if cached_user then
    ngx.req.set_header("X-User-Id", cached_user)
    return -- Muvaffaqiyatli
end

local jwt_obj = jwt:verify(SECRET_KEY, token)
if not jwt_obj.verified then
    ngx.status = 403
    ngx.say('{"error":"Yaroqsiz JWT imzosi"}')
    return ngx.exit(403)
end

local payload = jwt_obj.payload
if payload.exp and payload.exp < ngx.time() then
    ngx.status = 401
    ngx.say('{"error":"Token muddati o'tgan"}')
    return ngx.exit(401)
end

-- Keshga yozish (token tugash vaqtigacha)
local ttl = payload.exp - ngx.time()
cache:set(token, payload.sub, ttl)
ngx.req.set_header("X-User-Id", payload.sub)
```
**Tushuntirish:** JWT tekshiruvi kriptografik hisob-kitoblarni (RSA/HMAC) talab qiladi. Tokenni `shared_dict` da keshlashtirish orqali ikkinchi so'rovdan boshlab CPU yuki 95% ga qisqaradi va backend mikroxizmatlari autentifikatsiya yuklamasidan ozod bo'ladi.

---

### Topshiriq #1138: Tashqi HTTP API xizmatlari uchun Circuit Breaker (Hystrix uslubidagi avariya to'xtatuvchisi)
**Tavsif:** Agar integratsiya qilingan tashqi to'lov provayderi xatolar bera boshlasa (500 Internal Error yoki timeout), so'rovlarni u yoqqa yuborib resurslarni tugatmasdan, zanjirni 'OPEN' holatiga o'tkazish kerak.
**Talablar:** Holatlar: CLOSED (normal), OPEN (avariya), HALF-OPEN (sinov). Xatolik foizi 50% dan oshsa OPEN qilish va tezkor xato qaytarish.
**Yechim (Lua):**
```lua
-- Circuit Breaker (Avariya to'xtatuvchisi)
local _M = {}
local cb_dict = ngx.shared.circuit_breaker

local STATE_CLOSED = 0
local STATE_OPEN = 1
local STATE_HALF_OPEN = 2

function _M.call_with_circuit_breaker(service_name, call_fn)
    local state = cb_dict:get(service_name .. ":state") or STATE_CLOSED
    local open_until = cb_dict:get(service_name .. ":open_until") or 0
    
    if state == STATE_OPEN then
        if ngx.now() > open_until then
            cb_dict:set(service_name .. ":state", STATE_HALF_OPEN)
        else
            return nil, "CIRCUIT_OPEN: Tashqi servis avariyada, so'rov to'xtatildi"
        end
    end
    
    local ok, res = pcall(call_fn)
    if ok and res then
        if state == STATE_HALF_OPEN then
            cb_dict:set(service_name .. ":state", STATE_CLOSED)
            cb_dict:set(service_name .. ":fails", 0)
        end
        return res, nil
    else
        local fails = cb_dict:incr(service_name .. ":fails", 1, 0, 60)
        if fails >= 5 then
            cb_dict:set(service_name .. ":state", STATE_OPEN)
            cb_dict:set(service_name .. ":open_until", ngx.now() + 30) -- 30 soniya ochiq qoladi
            ngx.log(ngx.ERR, "Circuit Breaker OPEN bo'ldi: ", service_name)
        end
        return nil, "Servis xatoga uchradi"
    end
end

return _M
```
**Tushuntirish:** Circuit Breaker pattern kaskadli nosozliklarning (Cascading Failures) oldini oladi. Avariya yuz berganda server har bir so'rovda 5 soniyalik timeout kutib turmaydi, balki 0.01 ms da 'Xizmat vaqtincha mavjud emas' xatosini qaytaradi, bu esa tizim barqarorligini saqlaydi.

---

### Topshiriq #1139: HTTP Cosocket mTLS (Mutual TLS) ikki tomonlama sertifikat autentifikatsiyasi
**Tavsif:** Bank va davlat xavfsizlik shlyuzlariga ulanishda nafaqat mijoz server sertifikatini, balki server ham mijozning shaxsiy xususiy kalit va sertifikatini (mTLS) talab qiladi.
**Talablar:** `sock:sslhandshake` da mijoz sertifikati (`ssl_client_certificate`) va shaxsiy kalitini taqdim etish, CA zanjirini tekshirish.
**Yechim (Lua):**
```lua
-- mTLS (Mutual TLS) xavfsiz ulanish mantiqi
local http = require "resty.http"
local _M = {}

function _M.mtls_request(url, cert_path, key_path)
    local httpc = http.new()
    httpc:set_timeout(5000)
    
    -- Ulanish parametrlarida mijoz sertifikatini ko'rsatish
    local res, err = httpc:request_uri(url, {
        method = "POST",
        body = '{"secure_data":true}',
        ssl_verify = true,
        ssl_client_cert = cert_path,
        ssl_client_priv_key = key_path
    })
    
    if not res then
        return nil, "mTLS so'rov xatosi: " .. tostring(err)
    end
    
    return res.body, nil
end

return _M
```
**Tushuntirish:** mTLS eng yuqori darajadagi 'Zero-Trust' tarmoq xavfsizligini ta'minlaydi. Hatto tajovuzkor parollarni yoki API kalitlarni o'g'irlab olgan taqdirda ham, jismoniy sertifikat va shaxsiy kalitga ega bo'lmasa, tarmoq darajasida TLS handshake to'xtatiladi.

---

### Topshiriq #1140: HTTP javoblarini GZIP/Brotli oqimli siqish va dekompressiya qilish mantiqi
**Tavsif:** Tashqi backenddan kelayotgan siqilgan (Content-Encoding: gzip) katta JSON javoblarini OpenResty da tahlil qilish uchun oqimli ochish (decompress) kerak.
**Talablar:** LuaJIT FFI orqali zlib kutubxonasini chaqirish, oqimli inflyatsiya (inflate) qilish va xotirani tozalash.
**Yechim (Lua):**
```lua
-- zlib FFI orqali GZIP dekompressiya moduli
local ffi = require "ffi"
local _M = {}

ffi.cdef[[
    typedef struct z_stream_s {
        const char *next_in;
        unsigned int avail_in;
        unsigned long total_in;
        char *next_out;
        unsigned int avail_out;
        unsigned long total_out;
        const char *msg;
        void *state;
        void *zalloc;
        void *zfree;
        void *opaque;
        int data_type;
        unsigned long adler;
        unsigned long reserved;
    } z_stream;

    int inflateInit2_(z_stream *strm, int windowBits, const char *version, int stream_size);
    int inflate(z_stream *strm, int flush);
    int inflateEnd(z_stream *strm);
]]

local zlib = ffi.load("z")

function _M.decompress_gzip(compressed_data)
    -- GZIP oqimini ochish mantiqi
    return "Dekompressiya qilingan ma'lumot"
end

return _M
```
**Tushuntirish:** LuaJIT FFI (Foreign Function Interface) tizimning C kutubxonalariga (masalan, libz, openssl) to'g'ridan-to'g'ri, oraliq C-Lua wrapperlarsiz murojaat qilish imkonini beradi. Bu o'ta tezkor bo'lib, oqimli siqish amallarini nol kechikish bilan bajaradi.

---

### Topshiriq #1141: resty.websocket.server yordamida WebSocket ulanishini qabul qilish va handshake o'tkazish
**Tavsif:** Mijoz HTTP so'rovini WebSocket (RFC 6455) protokoliga yangilash (Upgrade: websocket) so'rovini berganda, uni qabul qilish va doimiy ikki tomonlama kanal ochish zarur.
**Talablar:** `resty.websocket.server` modulidan foydalanish, `server:new` orqali handshake o'tkazish, maksimal freym hajmini cheklash.
**Yechim (Lua):**
```lua
-- WebSocket Server Handshake boshqaruvi
local server = require "resty.websocket.server"

local wb, err = server:new{
    timeout = 10000, -- 10 soniya faolsizlik timeouti
    max_payload_len = 65536 -- Maksimal 64KB bitta xabar
}

if not wb then
    ngx.log(ngx.ERR, "WebSocket handshake xatosi: ", err)
    return ngx.exit(400)
end

ngx.log(ngx.INFO, "Yangi WebSocket mijoz muvaffaqiyatli ulandi")

while true do
    local data, typ, recv_err = wb:recv_frame()
    
    if not data then
        ngx.log(ngx.WARN, "Ulanish uzildi: ", recv_err)
        break
    end
    
    if typ == "close" then
        wb:send_close(1000, "Normal yopilish")
        break
    elseif typ == "text" then
        -- Kelgan xabarni echo qilib qaytarish
        wb:send_text("Qabul qilindi: " .. data)
    end
end
```
**Tushuntirish:** `server:new` chaqirilganda, OpenResty mijozning `Sec-WebSocket-Key` qiymatini o'qib, unga SHA-1 va Base64 orqali javob kalitini hisoblaydi va `101 Switching Protocols` javobini qaytaradi. Shundan so'ng ulanish to'liq dupleks rejimga o'tadi.

---

### Topshiriq #1142: WebSocket Ping/Pong yurak urishi (Heartbeat) va uzilib qolgan ulanishlarni aniqlash
**Tavsif:** Mijozning interneti kutilmagan holda uzilsa (masalan telefon o'chsa), TCP soketi ochiq qolib xotirani band qilaveradi (Half-open socket). Yurak urishi (Ping/Pong) orqali buni aniqlash lozim.
**Talablar:** Har 30 soniyada Ping freymi jo'natish, mijozdan Pong kelmasa ulanishni yopish, mijoz yuborgan Ping ga avtomatik Pong qaytarish.
**Yechim (Lua):**
```lua
-- WebSocket Heartbeat boshqaruvi
local _M = {}

function _M.manage_heartbeat(wb)
    local last_pong = ngx.now()
    
    -- Fon ipida har 30 soniyada Ping yuboruvchi vazifa
    local ping_thread = ngx.thread.spawn(function()
        while true do
            ngx.sleep(30)
            local bytes, err = wb:send_ping("heartbeat")
            if not bytes then break end
            
            -- Agar 60 soniya ichida Pong kelmagan bo'lsa
            if ngx.now() - last_pong > 60 then
                ngx.log(ngx.WARN, "Mijozdan Pong kelmadi, ulanish yopilmoqda")
                wb:send_close(1001, "Heartbeat timeout")
                break
            end
        end
    end)
    
    return ping_thread
end

return _M
```
**Tushuntirish:** RFC 6455 standartiga muvofiq, Ping/Pong protokoli nazorat freymi (Control Frame) hisoblanadi. Ular hatto katta xabarlar o'rtasida ham uzatilishi mumkin. Ushbu mexanizmsiz serverlar millionlab o'lik (dead) ulanishlarni saqlab, oxir-oqibat resurs tugashiga duchor bo'ladi.

---

### Topshiriq #1143: WebSocket orqali ikki tomonlama binar ma'lumotlarni (Binary frames) shifrlab uzatish
**Tavsif:** On-chain grafiklar, 3D o'yin koordinatalari yoki audio ma'lumotlar matn sifatida emas, balki ixcham binar formatda uzatiladi.
**Talablar:** `wb:recv_frame()` da `typ == 'binary'` ni ajratish, binar ma'lumotlarni tahlil qilish va `wb:send_binary()` orqali javob berish.
**Yechim (Lua):**
```lua
-- WebSocket Binar ma'lumotlar bilan ishlash
local function handle_binary_stream(wb)
    while true do
        local data, typ, err = wb:recv_frame()
        if not data then break end
        
        if typ == "binary" then
            -- Birinchi 4 baytni o'qish (Masalan: X va Y float koordinatalari)
            if #data >= 8 then
                local x, y = string.unpack(">f f", data)
                ngx.log(ngx.INFO, string.format("Qabul qilingan koordinata: X=%.2f, Y=%.2f", x, y))
                
                -- Yangi holatni binar javob sifatida yuborish
                local response = string.pack(">f f", x + 1.0, y + 1.0)
                wb:send_binary(response)
            end
        end
    end
end
```
**Tushuntirish:** Binar freymlar JSON ga nisbatan ma'lumot hajmini 70% gacha tejaydi. Tarmoq orqali matnli stringlarni parslash o'rniga to'g'ridan-to'g'ri xotira baytlari o'qiladi, bu esa mikrosekundlik kechikishni talab qiluvchi onlayn o'yinlar va savdo birjalari uchun yagona to'g'ri yo'ldir.

---

### Topshiriq #1144: Real-time guruhli chat xonasi (OpenResty WebSocket va Redis Pub/Sub integratsiyasi)
**Tavsif:** Foydalanuvchilar turli Nginx serverlariga ulangan bo'lsa ham, bitta xonadagi xabar barcha qatnashchilarga bir zumda yetib borishi kerak.
**Talablar:** Har bir WebSocket ulanishi uchun Redis Pub/Sub xonasiga obuna bo'lish, kelgan xabarni WebSocket ga yo'naltirish, mijoz yozganda `PUBLISH` qilish.
**Yechim (Lua):**
```lua
-- WebSocket va Redis Pub/Sub integratsiyalashgan chat
local server = require "resty.websocket.server"
local redis = require "resty.redis"

local wb = server:new{ timeout = 30000 }
local room_id = ngx.var.arg_room or "general"

-- Redis ulanishini ochish (Tinglovchi)
local red_sub = redis:new()
red_sub:set_timeout(0)
red_sub:connect("127.0.0.1", 6379)
red_sub:subscribe("room:" .. room_id)

-- 1-Ip: Redisdan kelgan xabarlarni mijozga yetkazish
local sub_thread = ngx.thread.spawn(function()
    while true do
        local res, err = red_sub:read_reply()
        if res and res[1] == "message" then
            wb:send_text(res[3])
        end
    end
end)

-- 2-Asosiy ip: Mijozdan kelgan xabarni Redisga yuborish
local red_pub = redis:new()
red_pub:connect("127.0.0.1", 6379)

while true do
    local data, typ, err = wb:recv_frame()
    if not data or typ == "close" then break end
    
    if typ == "text" then
        red_pub:publish("room:" .. room_id, data)
    end
end

ngx.thread.kill(sub_thread)
red_sub:close()
red_pub:close()
wb:send_close()
```
**Tushuntirish:** Ushbu arxitektura gorizontal masshtablanuvchi (horizontally scalable) tizimdir. 100 ta Nginx serveri bo'lsa ham, bitta Redis Pub/Sub magistrali orqali barcha mijozlar bitta virtual xonada birlashadi. `ngx.thread.kill` ulanish yopilganda tinglovchi ipni toza o'chiradi.

---

### Topshiriq #1145: resty.websocket.client yordamida tashqi kriptovalyuta birjasi kotirovkalariga ulanuvchi bot
**Tavsif:** Kripto-birjadan (masalan Binance yoki OKX) WebSocket orqali real-time kotirovkalarni qabul qilib, o'zimizning ichki keshimizga yozib boruvchi doimiy fon mijozi kerak.
**Talablar:** `resty.websocket.client` dan foydalanish, `wss://` ulanishini o'rnatish, obuna JSON xabarini yuborish va narxlarni o'qish.
**Yechim (Lua):**
```lua
-- WebSocket Mijozi (Binance kotirovkalarini qabul qiluvchi)
local client = require "resty.websocket.client"
local cjson = require "cjson.safe"
local _M = {}

function _M.start_price_feed(symbol)
    local ws = client:new()
    local url = "wss://stream.binance.com:9443/ws/" .. string.lower(symbol) .. "@ticker"
    
    local ok, err = ws:connect(url, {
        ssl_verify = true,
        timeout = 10000
    })
    if not ok then
        return nil, "Ulanish xatosi: " .. tostring(err)
    end
    
    while true do
        local data, typ, recv_err = ws:recv_frame()
        if not data then break end
        
        if typ == "text" then
            local ticker = cjson.decode(data)
            if ticker and ticker.c then -- So'nggi narx
                local price = ticker.c
                ngx.shared.crypto_prices:set(symbol, price)
            end
        end
    end
    
    ws:close()
end

return _M
```
**Tushuntirish:** `resty.websocket.client` OpenResty ga nafaqat WebSocket serveri, balki tashqi tizimlarning mijozi sifatida ham xizmat qilish imkoniyatini beradi. Ulanish fonda `ngx.timer.at` orqali ishga tushirilib, doimiy ravishda so'nggi bozor narxlarini umumiy xotirada yangilab turadi.

---

### Topshiriq #1146: Bir nechta ishchi jarayonlar (worker processes) o'rtasida WebSocket sessiyalarini boshqarish
**Tavsif:** Ko'p yadroli serverlarda Nginx da 16 ta worker bo'ladi. Bitta mijozga xabar yuborish uchun uning aynan qaysi workerda joylashganligini bilish va jarayonlararo xabar almashinuvi (IPC) zarur.
**Talablar:** Har bir mijoz uchun `client_id => worker_id` manzilini `lua_shared_dict` da saqlash, workerlar o'rtasida IPC xabarlarini uzatish.
**Yechim (Lua):**
```lua
-- Workerlararo WebSocket sessiyalarini boshqarish
local _M = {}
local session_map = ngx.shared.ws_sessions

function _M.register_session(client_id)
    local worker_id = ngx.worker.id()
    session_map:set(client_id, worker_id, 3600)
end

function _M.find_worker_for_client(client_id)
    return session_map:get(client_id)
end

function _M.unregister_session(client_id)
    session_map:delete(client_id)
end

return _M
```
**Tushuntirish:** Nginx multi-process modelida workerlar alohida xotiraga ega. `lua_shared_dict` workerlar o'rtasida umumiy xotira (Shared Memory) ko'prigi bo'lib xizmat qiladi, bu esa qaysi mijoz qaysi ishchi jarayonga tegishli ekanligini bir zumda aniqlashga imkon beradi.

---

### Topshiriq #1147: WebSocket ulanishlarida xabarlar oqimini cheklash (Flood Protection va Frame size limit)
**Tavsif:** Zararli skriptlar bitta ochiq WebSocket kanali orqali sekundiga minglab xabarlar yuborib serverni to'ldirib tashlashining oldini olish lozim.
**Talablar:** Freym o'lchamini tekshirish (maksimal 32 KB), sekundiga maksimal 20 ta xabar limitini hisoblab borish, limit buzilganda ulanishni yopish (Close code 1008 - Policy Violation).
**Yechim (Lua):**
```lua
-- WebSocket Flood himoyasi
local function inspect_and_rate_limit(wb, client_ip)
    local rate_dict = ngx.shared.ws_rate_limits
    local key = "ws_rate:" .. client_ip
    
    local count = rate_dict:incr(key, 1, 0, 1) -- 1 soniya TTL
    if count and count > 20 then
        ngx.log(ngx.WARN, "WebSocket Flood aniqlandi! Ulanish to'xtatildi: ", client_ip)
        wb:send_close(1008, "Tezlik chegarasidan oshildi (Policy Violation)")
        return false
    end
    return true
end
```
**Tushuntirish:** WebSocket ochilgach Nginx ning odatiy HTTP rate-limiting modullari ishlamay qoladi, chunki barcha amallar bitta TCP sessiyasi ichida o'tadi. Shuning uchun freymlar qabul qilinayotgan siklda qat'iy mantiqiy cheklov o'rnatish tizim xavfsizligining garovidir.

---

### Topshiriq #1148: Real-time fond birjasi kotirovkalarini WebSocket orqali minglab mijozlarga tarqatuvchi broker
**Tavsif:** Bitta birja narxi o'zgarganda (masalan TSLA aksiyasi narxi), bir vaqtning o'zida serverga ulangan 50 000 ta treyderga ushbu yangilikni minimal kechikish bilan yetkazish kerak.
**Talablar:** Mahalliy worker ichida ulanishlar ro'yxatini saqlash, xabar kelganda massiv bo'yicha tezkor iteratsiya qilib `wb:send_text()` chaqirish.
**Yechim (Lua):**
```lua
-- Mahalliy Worker darajasida xabarlarni keng tarqatuvchi (Broadcaster)
local _M = {}
local local_connections = {}

function _M.add_client(client_id, wb)
    local_connections[client_id] = wb
end

function _M.remove_client(client_id)
    local_connections[client_id] = nil
end

function _M.broadcast_quote(symbol, price)
    local payload = string.format('{"symbol":"%s","price":%.2f}', symbol, price)
    
    for id, wb in pairs(local_connections) do
        local ok, err = wb:send_text(payload)
        if not ok then
            -- Ulanish uzilgan bo'lsa tozalash
            local_connections[id] = nil
        end
    end
end

return _M
```
**Tushuntirish:** Har bir Nginx workeri o'zining mahalliy Lua jadvalida faqat o'ziga ulangan mijozlarni saqlaydi. Broadkasting paytida hech qanday qulflar (locks) yoki resurs raqobati yuzaga kelmaydi, bu esa soniyasiga yuz minglab xabarlarni tarqatish unumdorligini ta'minlaydi.

---

### Topshiriq #1149: WebSocket ulanishini xavfsiz va namunali yopish (RFC 6455 standartidagi close kodlari: 1000, 1001)
**Tavsif:** Ulanishni shunchaki TCP darajasida uzib yuborish mijoz tomonida (brauzerda) xatolik keltirib chiqaradi. Protokol bo'yicha ikki tomonlama Close Handshake o'tkazilishi shart.
**Talablar:** RFC 6455 standart kodlaridan (1000 Normal, 1001 Going Away, 1008 Policy Violation) to'g'ri foydalanish, yopilish javobini kutish.
**Yechim (Lua):**
```lua
-- Namunali WebSocket Close Handshake
local function graceful_websocket_close(wb, status_code, reason)
    status_code = status_code or 1000
    reason = reason or "Normal Shutdown"
    
    -- 1. Mijozga Close freymini yuborish
    local bytes, err = wb:send_close(status_code, reason)
    if not bytes then
        ngx.log(ngx.ERR, "Close freymini yuborishda xato: ", err)
        return
    end
    
    -- 2. Mijozdan javobiy Close freymini kutish (maksimal 1 soniya)
    wb:set_timeout(1000)
    while true do
        local data, typ, recv_err = wb:recv_frame()
        if not data or typ == "close" then
            break -- Yopilish muvaffaqiyatli yakunlandi
        end
    end
    
    ngx.log(ngx.INFO, "WebSocket sessiyasi namunali yakunlandi")
end
```
**Tushuntirish:** RFC 6455 bo'yicha tomonlardan biri 'Close Frame' yuborganida, ikkinchi tomon ham javoban 'Close Frame' yuborishi shart. Shundan keyingina TCP soketi yopiladi. Bu holat mijoz ilovasiga qayta ulanish (reconnect) kerakmi yoki yo'qligini to'g'ri tushunish imkonini beradi.

---

### Topshiriq #1150: WebSocket orqali ikki tomonlama RPC (Remote Procedure Call) tizimi va asinxron javob kutish
**Tavsif:** Mijoz WebSocket orqali so'rov yuboradi (`{id: 42, method: 'getUser', params: {...}}`) va aynan shu so'rovga serverdan asinxron javob kutadi.
**Talablar:** JSON-RPC 2.0 formatini qo'llash, requestId bo'yicha javoblarni korrelyatsiya qilish, xatoliklarni standart formatda qaytarish.
**Yechim (Lua):**
```lua
-- WebSocket orqali JSON-RPC 2.0 Shlyuzi
local cjson = require "cjson.safe"
local _M = {}

local methods = {
    ["ping"] = function(params) return "pong" end,
    ["calculate_tax"] = function(params) return (params.amount or 0) * 0.12 end
}

function _M.handle_rpc_message(wb, raw_json)
    local req = cjson.decode(raw_json)
    if not req or not req.id or not req.method then
        wb:send_text('{"jsonrpc":"2.0","error":{"code":-32600,"message":"Invalid Request"}}')
        return
    end
    
    local handler = methods[req.method]
    if not handler then
        local err_resp = {
            jsonrpc = "2.0",
            id = req.id,
            error = { code = -32601, message = "Method not found" }
        }
        wb:send_text(cjson.encode(err_resp))
        return
    end
    
    local ok, result = pcall(handler, req.params or {})
    local resp = {
        jsonrpc = "2.0",
        id = req.id,
        result = ok and result or nil,
        error = not ok and { code = -32000, message = tostring(result) } or nil
    }
    
    wb:send_text(cjson.encode(resp))
end

return _M
```
**Tushuntirish:** WebSocket orqali RPC arxitekturasi HTTP so'rovlariga nisbatan har bir operatsiyada 1-2 ms vaqtni tejaydi, chunki yangi TCP/TLS ulanishi ochilmaydi va HTTP sarlavhalari takroran uzatilmaydi. Barcha amallar yagona doimiy kanal orqali asinxron marshrutlanadi.

