# v2.6.5 Hotfix5.1 — QA / QR Güvenlik ve Build Düzeltmeleri

- QR doğrudan takipte `portalToken` tekrar birincil yöntem yapıldı; müşteri telefonu URL içinde taşınmıyor.
- Token eksikse geriye uyumluluk için Servis No + Telefon sorgusuna düşer.
- GitHub Actions health kontrolündeki eski `2.6.5-hf4` beklentisi düzeltildi.
- HTTP server sürüm etiketi ve kaynak dokümantasyonu güncellendi.
- DB `version` yazımındaki 2.60 / 2.65 tutarsızlığı düzeltildi.
- Kaynak ZIP içindeki `__pycache__`/`.pyc` kalıntıları temizlendi.

# v2.6.5 Hotfix5 — QR Doğrudan Servis Takip

- Servis fişi QR bağlantısı kalıcı servis no + müşteri telefonu sorgusuna geçirildi.
- QR okutulduğunda müşteri servis no/telefon yazmadan ilgili servis kaydı otomatik açılır.
- Eski/yenilenmiş portalToken nedeniyle QR'ın boş takip ekranında kalması engellendi.
- Normal takip.sarkislasistem.com girişi manuel Servis No + Telefon sorgusu olarak korunur.
- Canlı data/db ve kullanıcı verilerini değiştiren bir işlem eklenmedi.

# Teknik Servis Pro v2.6.5 Hotfix4

- Müşteri portalında logo artık `https://sarkislasistem.com` ana sayfasına döner.
- Portalda ayrıca görünür **Siteye Dön** butonu eklendi.
- Kurumsal site adresi Ayarlar > İşletme bölümünden değiştirilebilir.
- Kurulumda Windows oturum açılışında arka planda otomatik başlatma seçeneği eklendi (varsayılan açık).
- Otomatik başlangıç tarayıcı penceresi açmaz; masaüstü kısayolu normal şekilde yönetim ekranını açar.
- Kaynak paketten `__pycache__`/`.pyc` kalıntıları temizlendi.
- GitHub kaynak paketindeki seed `db.json` müşteri/servis kayıtlarından arındırıldı; canlı veriler `%LOCALAPPDATA%\TeknikServisPro\Data` altında korunmaya devam eder.
