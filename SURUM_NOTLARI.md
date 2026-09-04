# Teknik Servis Pro v2.3.9 – Müşteri + Cihaz Yönetimi

- Müşteriler artık kalıcı ana kayıtlardır; mevcut servislerden ilk açılışta otomatik oluşturulur.
- Her müşteriye birden fazla cihaz bağlanabilir; cihazlara `CIH-000001` biçiminde iç servis kodu verilir.
- Yeni servis formunda müşteri adı/telefonu ile arama, mevcut müşteri seçimi ve müşterinin kayıtlı cihazını seçme eklendi.
- Mevcut müşteriye yeni cihaz ekleyip doğrudan servis kaydı açılabilir.
- Seri No / IMEI başka müşterinin cihazında kayıtlıysa yeni kayıt engellenir.
- Müşteri kartında cihaz sayısı, servis sayısı, açık bakiye, cihaz bazlı son işlem ve servis geçmişi gösterilir.
- Müşteri kartında ad/telefon/e-posta/adres/not düzenlenebilir.
- Cihaz kartında durum, tür, model, seri/IMEI ve cihaz notu düzenlenebilir.
- Cihaz kartından tek dokunuşla yeni servis açılabilir.
- Önceki servis garantisi devam eden cihaz seçildiğinde uyarı gösterilir.
- v2.3.8 Hotfix5 veri, başlangıç ve iPhone kamera düzeltmeleri korunur.

# Teknik Servis Pro v2.3.8 Hotfix4

- İlk açılışta Dashboard'un boş görünmesine neden olan eksik `populateStatuses()` fonksiyonu eklendi.
- Başlangıç sırası düzeltildi: oturum kontrolü → `/api/data` yükleme → normalize/render → Dashboard.
- İlk veri yükleme hatasında tek seferlik tekrar deneme ve konsol tanılama eklendi.
- `/api/auth/status` isteğine `cache: no-store` eklendi.
- Hotfix3 kalıcı yedek geri yükleme ve veri klasörü yapısı korunur.
- Başlangıç testinde tespit edilen eksik `renderServices()` ve `deleteService()` fonksiyonları da geri getirildi; Servis Kayıtları ekranı ve silme işlemi tekrar aktif.

# Teknik Servis Pro v2.3.8 Hotfix3

- Yedek geri yükleme artık backend üzerinden doğrudan kalıcı Data\db.json dosyasına yazılır.
- Geri yükleme sonrası diskten tekrar okunarak servis/kasa/stok kayıt sayıları doğrulanır.
- Doğrulama başarısızsa kullanıcıya başarı mesajı verilmez.
- Eski DB kurtarma/migration mantığı artık süreç başlangıcında yalnızca bir kez çalışır; normal veri okumalarında canlı DB üzerine yazamaz.
- DB yazımında flush + fsync + atomic replace kullanılır.
- Diagnostics veri dosyası, boyut, PID ve kayıt sayılarını gösterir.

# Teknik Servis Pro v2.3.8

- Canlı veritabanı program/EXE klasöründen ayrıldı.
- Windows veri yolu: `%LOCALAPPDATA%\\TeknikServisPro\\Data\\db.json`.
- v2.3.7 ve önceki kurulumdaki `db.json`, ilk v2.3.9 açılışında otomatik olarak yeni kalıcı veri klasörüne taşınır/kopyalanır.
- Yedekler ve loglar da kalıcı veri klasörüne alındı.
- HTML/API yanıtlarında `Cache-Control: no-store` etkin; mobilde eski önbellek kaynaklı boş/eski ekran riski azaltıldı.
- Dashboard, Servis Kayıtları, Müşteriler, Stok, Kasa ve Raporlar ekranlarına geçişte veri sunucudan yeniden okunur.
- `/api/diagnostics` ile kullanılan fiziksel DB yolu ve kayıt sayıları doğrulanabilir.
- Dashboard ve Kasa aynı `serviceRecords + cashRecords` verisini kullanmaya devam eder.
- v2.3.4+ özellikleri korunur: Dashboard kart filtreleri, Seri No/IMEI araması, mobil barkod/QR kamera, A5 dikey çift nüsha servis fişi, kullanıcı/şifre/logo, stok/kasa/raporlar.
- Güncellemede mevcut eski `db.json` installer tarafından ezilmez; migration için korunur.
## v2.3.9 Hotfix 1
- Yeni Servis Kaydı / düzenleme / kaydetme işlevleri geri eklendi ve doğrulandı.
- İlk 2.3.9 çalıştırmasında boş kalıcı DB oluşmuşsa, daha zengin eski 2.3.7 DB otomatik kurtarılır.
- Kurtarma öncesi mevcut kalıcı DB otomatik yedeklenir.
- Eski DB kullanıcı içermiyorsa mevcut kullanıcı hesapları korunur.

## v2.3.9 Hotfix 2
- Inno Setup artık `dist\TeknikServisPro\db.json` dosyasını kökte beklemiyor.
- PyInstaller onedir yapısındaki `_internal\db.json` seed dosyası installer ile birlikte doğru şekilde paketleniyor.
- Canlı kullanıcı verisi `%LOCALAPPDATA%\TeknikServisPro\Data\db.json` altında kalmaya devam ediyor ve installer tarafından ezilmiyor.
- GitHub Actions, installer aşamasından önce PyInstaller çıktısında seed `db.json` bulunduğunu doğruluyor.

## v2.3.9 Hotfix5 – iPhone/Safari Seri No Kamera Düzeltmesi
- iPhone/Safari ve HTTP/Tailscale bağlantılarında `BarcodeDetector` bulunmadığında kamera butonunun işlemsiz kalması düzeltildi.
- Canlı tarama desteklenmeyen cihazlarda kamera butonu artık doğrudan telefonun fotoğraf/kamera seçicisini açar.
- Çekilen/seçilen fotoğraftaki QR, Data Matrix ve yaygın 1D barkodlar `html5-qrcode` ile taranıp Seri No / IMEI alanına yazılır.
- HTTPS/secure context bulunan destekli tarayıcılarda mevcut canlı barkod tarama korunur.
- Kod okunamazsa kullanıcıya yeniden yakın/net fotoğraf çekme veya elle giriş mesajı gösterilir.
