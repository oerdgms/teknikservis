# Teknik Servis Pro v2.5.0

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
GitHub Actions > Windows Installer workflow ile `TeknikServisPro_v2_5_0_Setup.exe` oluşturulur.
