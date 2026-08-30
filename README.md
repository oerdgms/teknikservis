# Teknik Servis Pro v2.3.8

**Hotfix4:** İlk açılışta Dashboard verileri API'den yüklenmeden önce boş görünme sorunu giderildi.

Python tabanlı yerel teknik servis yönetim uygulaması.

## Veri güvenliği
Canlı veriler Windows'ta `%LOCALAPPDATA%\\TeknikServisPro\\Data\\db.json` altında tutulur. Program dosyaları güncellense veya kaldırılıp yeniden kurulsa bile bu klasör installer tarafından silinmez.

v2.3.7 ve daha eski sürümden ilk açılışta program, kurulum klasöründeki mevcut `db.json` dosyasını otomatik olarak kalıcı veri klasörüne kopyalar.

## GitHub Actions
Actions > `Teknik Servis Pro - Windows Kurulum` > `Run workflow`.

### Hotfix5
Mobil Seri No / IMEI kamera butonu iPhone/Safari için fotoğrafla barkod/QR tarama yedeği içerir. Canlı tarama desteklenirse kullanılmaya devam eder.
