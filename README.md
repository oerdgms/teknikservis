# Teknik Servis Pro v2.3.0 — Python Edition

Teknik servis, müşteri, cihaz, stok, kasa, kullanıcı ve raporlama işlemleri için yerel web tabanlı Windows uygulaması.

## v2.3 ile ne değişti?

Node.js altyapısı tamamen kaldırıldı. Program artık Python tabanlı tek `TeknikServisPro.exe` üzerinden yerel sunucuyu başlatır ve tarayıcıyı otomatik açar. Hedef bilgisayarda Python veya Node.js kurulu olması gerekmez.

- Varsayılan adres: `http://127.0.0.1:8972`
- Yerel ağ erişimi: `http://BILGISAYAR-IP:8972`
- Mevcut `db.json` kayıtları korunur.
- Eski v2.2 kullanıcı şifre hash formatı Python sürümünde de okunabilir.
- Son 20 otomatik veri yedeği `backups` klasöründe tutulur.
- Hatalar `logs/server-error.log` dosyasına yazılır.
- A5 dikey, tek sayfada iki nüsha servis fişi korunur.

## GitHub Actions ile Windows kurulum EXE üretme

Repository içeriğini GitHub'a yükleyin. Ardından **Actions → Teknik Servis Pro - Windows Kurulum → Run workflow** yolunu izleyin.

Workflow:
1. Python 3.12 ortamını kurar.
2. PyInstaller ile `TeknikServisPro.exe` üretir.
3. Inno Setup ile `TeknikServisPro_v2_3_0_Setup.exe` oluşturur.
4. Kurulum dosyasını Actions > Artifacts bölümüne yükler.

Kurulum sırasında masaüstü ve Başlat menüsü kısayolları Teknik Servis Pro logosunu kullanır. Güncelleme kurulumunda mevcut `db.json` dosyası üzerine yazılmaz.
