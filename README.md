# Teknik Servis Pro v2.3.8

Python tabanlı yerel teknik servis yönetim uygulaması.

## Veri güvenliği
Canlı veriler Windows'ta `%LOCALAPPDATA%\\TeknikServisPro\\Data\\db.json` altında tutulur. Program dosyaları güncellense veya kaldırılıp yeniden kurulsa bile bu klasör installer tarafından silinmez.

v2.3.7 ve daha eski sürümden ilk açılışta program, kurulum klasöründeki mevcut `db.json` dosyasını otomatik olarak kalıcı veri klasörüne kopyalar.

## GitHub Actions
Actions > `Teknik Servis Pro - Windows Kurulum` > `Run workflow`.


## Dahili yedek
- `backups/teknik_servis_kasa_yedek_2026-08-30.json` kullanıcının 30/08/2026 tarihli servis/kasa yedeğidir.
- Bu dosya yalnızca yedek/referans içindir; kurulum sırasında canlı veritabanının üzerine otomatik yazılmaz.
- Gerekirse uygulamadaki **Yedek Yükle** işleviyle kullanıcı tarafından geri yüklenebilir.
