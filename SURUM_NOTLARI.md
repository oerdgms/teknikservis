# Teknik Servis Pro v2.6.1 — Merkezi Kurumsal Kimlik + Kalıcı Login

- Login sonrası tekrar giriş ekranına dönme akışı düzeltildi ve başlangıç hataları görünür hale getirildi.
- Oturumlar `%LOCALAPPDATA%\TeknikServisPro\Data\sessions.json` altında korunur; uygulama yeniden başlasa da geçerli oturum devam eder.
- Ayarlar > İşletme ekranına merkezi kurumsal kimlik alanları eklendi: firma adı, logo, kuruluş yılı, kuruluş/yıldönümü gösterimi, slogan, portal başlığı/açıklaması ve servis fişi marka gösterimi.
- Login, sol menü, müşteri portalı ve servis fişi aynı kurumsal ayarlardan beslenir.
- Kod içine sabit logo ve 2003/23. yıl metni kaldırıldı. Logo yoksa kırık resim yerine firma adı gösterilir.
- PyInstaller paketine kurumsal logo asset desteği eklendi.
- v2.5.2/v2.6.0 telefon standardizasyonu, güvenli portal tokenı, QR servis takibi ve sade servis arama ekranı korunur.
