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
