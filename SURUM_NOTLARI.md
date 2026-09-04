# Sürüm Notları — v2.6.3

## Kurumsal müşteri portalı
- Portal baştan tasarlandı: daha güçlü logo alanı, servis sorgulama kartı, mobil uyum, güven/servis/hız/çözüm ortağı bilgi alanları ve kurumsal alt bölüm.
- Servis sonucu, teklif onayı/red ve zaman çizelgesi aynı güvenli portal akışında korunur.
- Portal logo/firma adı/kuruluş yılı/yıldönümü/slogan/başlık/açıklama bilgilerini merkezi işletme ayarlarından alır.

## Login
- “Beni Hatırla” eklendi.
- İşaretli: 30 gün kalıcı oturum.
- İşaretsiz: tarayıcı oturumu; tarayıcı kapanınca tekrar kullanıcı adı/şifre gerekir.
- Önceki sürümün kalıcı oturumları v2.6.3'e geçişte bir kez geçersiz kılınır.

## Logo
- Paket varsayılanı yüksek çözünürlüklü, halkasız-e Sistem Bilgisayar logosudur.
- Ayarlardan yüklenen logo; login, sol menü, portal ve servis fişinde tek merkezden kullanılır.

## Güvenlik
- Yönetim paneli 8972'de kalır ve internete açılmaz.
- Public 8973 yalnız müşteri portalını sunar; `/api/data` 403 ile engellenir.
