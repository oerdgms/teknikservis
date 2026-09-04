# Teknik Servis Pro v2.3.9

Python tabanlı yerel teknik servis yönetim uygulaması.

## v2.3.9 – Müşteri + Cihaz Yönetimi

- Müşteri artık kalıcı ana kayıttır; ad/telefon/e-posta/adres/not saklanır.
- Bir müşteriye birden fazla cihaz bağlanabilir.
- Cihazlara `CIH-000001` biçiminde sabit iç servis kodu verilir.
- Yeni servis formunda müşteri arama/seçme ve müşterinin mevcut cihazını seçme vardır.
- Mevcut müşteriye yeni cihaz eklenebilir ve cihaz kartından doğrudan yeni servis açılabilir.
- Seri No / IMEI çakışması kontrol edilir.
- Müşteri kartında cihaz ve servis geçmişi, açık bakiye ve son işlem bilgileri görünür.
- Cihaz kartında durum, model, seri/IMEI ve cihaz notu düzenlenebilir.
- Önceki servis garantisi devam eden cihaz seçildiğinde uyarı verilir.
- Eski servis kayıtları ilk açılışta müşteri/cihaz yapısına otomatik ve geriye uyumlu dönüştürülür.

## Veri güvenliği
Canlı veriler Windows'ta `%LOCALAPPDATA%\TeknikServisPro\Data\db.json` altında tutulur. Program dosyaları güncellense veya kaldırılıp yeniden kurulsa bile bu klasör installer tarafından silinmez.

v2.3.7 ve daha eski sürümden ilk açılışta program, kurulum klasöründeki mevcut `db.json` dosyasını otomatik olarak kalıcı veri klasörüne kopyalar. v2.3.8 verileri aynı kalıcı klasörden doğrudan v2.3.9'a taşınır.

## GitHub Actions
Actions > `Teknik Servis Pro - Windows Kurulum` > `Run workflow`.

Mobil Seri No / IMEI kamera butonunda iPhone/Safari için fotoğrafla barkod/QR tarama yedeği korunmuştur.
