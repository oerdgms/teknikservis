# Teknik Servis Pro v2.6.5 Hotfix5.1

Kaynak paket. Windows kurulum dosyası GitHub Actions + Inno Setup ile üretilir.

## Portlar
- Yönetim: `127.0.0.1:8972`
- Müşteri portalı / Cloudflare Tunnel: `127.0.0.1:8973`

## Canlı veri
Canlı işletme verisi kaynak/kurulum klasöründe tutulmaz. Windows'ta `%LOCALAPPDATA%\TeknikServisPro\Data` kullanılır. Kaynak içindeki `app/db.json` yalnızca temiz ilk-kurulum seed dosyasıdır.

## Otomatik başlatma
Kurulumdaki “Windows oturumu açıldığında Teknik Servis Pro'yu otomatik başlat” seçeneği varsayılan olarak açıktır. Başlangıç kısayolu `--background` parametresiyle çalışır ve tarayıcı açmaz.

## Hotfix5.1 QA
- QR bağlantısında güvenli `portalToken` önceliklidir; yalnızca token yoksa Servis No + Telefon yedeği kullanılır.
- Eski servis kayıtlarında eksik token sunucu tarafından otomatik tamamlanır.
- GitHub Actions health sürüm kontrolü Hotfix5.1 ile eşleştirildi.
- Veritabanı sürüm yazımı 2.65 ile tutarlı hale getirildi.
- `__pycache__` ve `.pyc` kalıntıları kaynak paketinden çıkarıldı.
