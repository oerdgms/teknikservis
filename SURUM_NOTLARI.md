## v2.5.2 — Portal Takip + Telefon Standardı + Sade Servis Arama
- Müşteri telefonları `05XX XXX XX XX` maskesiyle girilir; kayıt sırasında 05 ile başlayan 11 haneli cep telefonu doğrulaması zorunludur.
- Veritabanında telefonlar standart `05XXXXXXXXX` biçiminde tutulur; eski geçerli kayıtlar otomatik normalize edilir.
- Müşteri portalı telefon sorgusu aynı standardı kullanır ve +90 / 10 haneli eski biçimleri normalize eder.
- Servis Kayıtları ekranındaki durum, ödeme, öncelik ve teknisyen açılır filtreleri kaldırıldı; tek hızlı arama alanı servis no, müşteri, telefon, cihaz, seri no, teknisyen, durum ve öncelikte arar.
- A5 iki nüshalı servis fişine “Servisinizi Online Takip Edin” alanı eklendi. Güvenli portal token bağlantısından QR kod oluşturulur; portal adresi, servis no ve telefon ayrıca basılır.
- Varsayılan müşteri portalı adresi `https://takip.sarkislasistem.com` olarak ayarlandı.

# Teknik Servis Pro v2.5.2

- Secure Customer Portal eklendi.
- Her servis kaydı için tahmin edilmesi zor portalToken oluşturulur ve kalıcı veride saklanır.
- Müşteri takip linkleri `?token=...` kullanır; telefon numarası URL içinde paylaşılmaz.
- Ayrı portal-only sunucu 127.0.0.1:8973 üzerinde çalışır.
- 8973 üzerinden yönetim paneli, kullanıcı API'leri, veri API'si ve ayarlar dış erişime kapalıdır.
- Tailscale Funnel doğrudan 8973 portuna bağlanabilir.
- Ayarlara “Dış Müşteri Portalı Adresi” eklendi; WhatsApp/SMS hazır mesajları bu adresi kullanır.
- Eski Servis No + Telefon sorgulaması portal ana sayfasında geriye dönük olarak kullanılabilir.
