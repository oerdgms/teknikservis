# Teknik Servis Pro v2.3.7

- v2.3.4 özelliklerinin tamamı korunmuştur.
- Windows build yapısı ÇiftlikPro referansındaki PyInstaller onedir + COLLECT yapısına geçirildi.
- PyInstaller UPX kapalıdır.
- Repo kökünde TeknikServisPro.spec ve installer.iss bulunur.
- Uygulama kaynakları app/ altında tutulur.
- GitHub Actions, installer üretmeden önce gerçek /api/health testi yapar.
- Kurulum dosyası: TeknikServisPro_v2_3_7_Setup.exe

## v2.3.7 - Çalışan EXE Kilidi Hotfix
- Güncelleme öncesi çalışan Teknik Servis Pro, localhost `/api/shutdown` ile kontrollü kapatılır.
- `taskkill` kullanılmaz; kapanma başarısızsa kurulum dosya kopyalamadan önce durur ve kullanıcıyı uyarır.
- Sunucu kapanışında HTTP socket kapatılır ve request thread'leri daemon çalışır; prosesin gerçekten sonlanması sağlanır.
- Mevcut `db.json` güncelleme kurulumunda asla üzerine yazılmaz; yalnızca ilk kurulumda örnek veritabanı oluşturulur.
- v2.3.4/2.3.7 özellikleri korunur: dashboard kart filtreleri, Seri No/IMEI araması, mobil kamera/barkod, mobil UX, A5 çift nüsha fiş, kullanıcı/ayarlar, kasa/stok/raporlar.
