# Teknik Servis Pro v2.5.1

## CRM / Servis Operasyon Sürümü

- CRM Dashboard: sağdaki Dikkat Gerektirenler kolonu kaldırıldı; Son Servis Hareketleri tam genişlik.
- Dashboard altı: Bugünün İşleri, Tahsilat Bekleyenler ve Teknisyen İş Yükü.
- Servis Operasyon Merkezi: zaman çizelgesi, teklif/onay, stoktan parça, müşteri bildirimi ve portal tek detay ekranında.
- Teklif revizyonları v1/v2/v3 olarak korunur; müşteri portalından veya servis içinden onay/red alınabilir.
- Kullanılan parça stoktan otomatik düşer, servis tutarına işlenir; geri alma stok iadesi yapar.
- WhatsApp/SMS hazır mesaj merkezi ve kopyalama desteği.
- Müşteri Portalı: servis no + telefon ile durum/teklif/zaman çizelgesi, teklif onay/red.
- Teknisyen İş Yükü: aktif, bekleyen, geciken, hazır ve açık bakiye dağılımı; teknisyene göre servis filtresi.
- Kalıcı veri: %LOCALAPPDATA%\TeknikServisPro\Data\db.json.
- v2.4.x verileri geriye uyumlu şekilde korunur.

## Build
GitHub Actions > Windows Installer workflow ile `TeknikServisPro_v2_5_1_Setup.exe` oluşturulur.

## v2.5.1 Secure Customer Portal
- Yönetim uygulaması: `http://127.0.0.1:8972`
- Dış müşteri portalı için güvenli yerel uç: `http://127.0.0.1:8973`
- Tailscale Funnel yalnız 8973 portuna yönlendirilmelidir: `tailscale funnel --bg 8973`
- Her servis kaydına rastgele portal erişim anahtarı üretilir.
- Ayarlar > Dış Müşteri Portalı Adresi alanına Funnel HTTPS adresi girilir.
- WhatsApp/SMS mesajları telefon numarası yerine güvenli token bağlantısını kullanır.
