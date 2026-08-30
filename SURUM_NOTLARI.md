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

- 30/08/2026 tarihli kullanıcı servis/kasa yedeği `backups/` klasörüne eklendi; otomatik geri yükleme yapılmaz.

## v2.3.8 Build Hotfix 1
- Inno Setup artık `dist\TeknikServisPro\db.json` beklemiyor.
- İlk kurulum seed verisi doğrudan `app\db.json` kaynağından alınır ve mevcut `db.json` asla ezilmez.
- 30/08/2026 kasa yedeği kurulumda `%LOCALAPPDATA%\TeknikServisPro\Data\importable-backups` altına güvenli kopya olarak bırakılır.
- Canlı veri ve yedek birbirinden ayrı tutulur.
