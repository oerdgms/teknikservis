# Teknik Servis Pro v2.3.8

- Canlı veritabanı program/EXE klasöründen ayrıldı.
- Windows veri yolu: `%LOCALAPPDATA%\\TeknikServisPro\\Data\\db.json`.
- v2.3.7 ve önceki kurulumdaki `db.json`, ilk v2.3.8 açılışında otomatik olarak yeni kalıcı veri klasörüne taşınır/kopyalanır.
- Yedekler ve loglar da kalıcı veri klasörüne alındı.
- HTML/API yanıtlarında `Cache-Control: no-store` etkin; mobilde eski önbellek kaynaklı boş/eski ekran riski azaltıldı.
- Dashboard, Servis Kayıtları, Müşteriler, Stok, Kasa ve Raporlar ekranlarına geçişte veri sunucudan yeniden okunur.
- `/api/diagnostics` ile kullanılan fiziksel DB yolu ve kayıt sayıları doğrulanabilir.
- Dashboard ve Kasa aynı `serviceRecords + cashRecords` verisini kullanmaya devam eder.
- v2.3.4+ özellikleri korunur: Dashboard kart filtreleri, Seri No/IMEI araması, mobil barkod/QR kamera, A5 dikey çift nüsha servis fişi, kullanıcı/şifre/logo, stok/kasa/raporlar.
- Güncellemede mevcut eski `db.json` installer tarafından ezilmez; migration için korunur.
## v2.3.8 Hotfix 1
- Yeni Servis Kaydı / düzenleme / kaydetme işlevleri geri eklendi ve doğrulandı.
- İlk 2.3.8 çalıştırmasında boş kalıcı DB oluşmuşsa, daha zengin eski 2.3.7 DB otomatik kurtarılır.
- Kurtarma öncesi mevcut kalıcı DB otomatik yedeklenir.
- Eski DB kullanıcı içermiyorsa mevcut kullanıcı hesapları korunur.

## v2.3.8 Hotfix 2
- Inno Setup artık `dist\TeknikServisPro\db.json` dosyasını kökte beklemiyor.
- PyInstaller onedir yapısındaki `_internal\db.json` seed dosyası installer ile birlikte doğru şekilde paketleniyor.
- Canlı kullanıcı verisi `%LOCALAPPDATA%\TeknikServisPro\Data\db.json` altında kalmaya devam ediyor ve installer tarafından ezilmiyor.
- GitHub Actions, installer aşamasından önce PyInstaller çıktısında seed `db.json` bulunduğunu doğruluyor.

