# Teknik Servis Pro v2.6.0

Sistem Bilgisayar için kurumsal kimlik, müşteri portalı ve servis operasyonu sürümü.

## Öne çıkanlar
- Login sonrası ana ekranı çizen `renderAll()` hotfix'i; giriş döngüsü giderildi.
- Sistem Bilgisayar kurumsal logo kullanımı: login, sol menü, servis fişi ve müşteri portalı.
- 2003'ten beri / 23. yıl kurumsal vurgusu (ana logodan bağımsız rozet).
- Müşteri portalında daha belirgin teklif Onayla/Reddet alanı ve iletişim bilgileri.
- Müşteri telefonları 05XX XXX XX XX standardında; geçersiz eski kayıtlar Müşteriler ekranında uyarı rozeti alır.
- Servis kayıtlarında sade tek arama alanı; eski durum/ödeme/öncelik/teknisyen açılır filtreleri yok.
- A5 iki nüshalı servis fişinde güvenli token QR kodu, takip.sarkislasistem.com, Servis No + Telefon yedek sorgulama bilgisi.
- Public portal yalnız 8973 üzerinden çalışır; yönetim API'leri dışarıya kapalı kalır.

## Kurulum
GitHub Actions > Windows Installer workflow ile `TeknikServisPro_v2_6_0_Setup.exe` oluşturulur. Canlı veritabanı `%LOCALAPPDATA%\TeknikServisPro\Data\db.json` altında korunur.
