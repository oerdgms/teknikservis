# Teknik Servis Pro v2.3.8

Python tabanlı yerel teknik servis yönetim uygulaması.

## Veri güvenliği
Canlı veriler Windows'ta `%LOCALAPPDATA%\\TeknikServisPro\\Data\\db.json` altında tutulur. Program dosyaları güncellense veya kaldırılıp yeniden kurulsa bile bu klasör installer tarafından silinmez.

v2.3.7 ve daha eski sürümden ilk açılışta program, kurulum klasöründeki mevcut `db.json` dosyasını otomatik olarak kalıcı veri klasörüne kopyalar.

## GitHub Actions
Actions > `Teknik Servis Pro - Windows Kurulum` > `Run workflow`.
