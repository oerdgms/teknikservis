# Teknik Servis Pro v2.3.2

- Mobil hamburger menü öğeleri tam kart yüzeyinden tıklanabilir hale getirildi ve seçim sonrası menü otomatik kapanır.
- Mobil üst bar butonları küçültüldü; başlık için daha fazla alan açıldı.
- Dashboard “Servis Kontrol Merkezi” açıklaması ve yenile butonu mobilde çakışmayacak şekilde düzenlendi.
- “Son Servis Hareketleri” masaüstünde tablo olarak korunurken mobilde kompakt dokunulabilir servis kartlarına dönüştürüldü.
- Mobil servis kartlarında servis no, müşteri, cihaz, durum ve açık bakiye birlikte gösterilir; karta dokununca servis detayı açılır.

# v2.0.0 Sürüm Notları

Mevcut servis kayıtları korunarak orta seviye teknik servis yönetim yapısına geçildi.

- Servis durumları genişletildi: Kayıt Alındı, Arıza Tespit, Müşteri Onayı Bekleniyor, Parça Bekleniyor, İşlemde, Test / Kalite Kontrol, Hazır, Teslim Edildi, İptal / İade.
- Servislere öncelik, teknisyen, tahmini teslim, cihaz türü/fiziksel durum, e-posta, iç servis notu ve garanti alanları eklendi.
- Kısmi tahsilat ve açık bakiye takibi eklendi.
- Durum ve tahsilat değişiklikleri için servis hareket geçmişi eklendi.
- Servislerden otomatik müşteri kartı ve müşteri servis geçmişi oluşturuldu.
- Parça/stok modülü ve kritik stok uyarıları eklendi.
- Dashboard aktif servis, bekleyen onay/parça, hazır, geciken, açık bakiye ve net kasa göstergeleriyle yenilendi.
- Kasa modülüne ödeme yöntemi ve gelişmiş özetler eklendi.
- Servis ve kasa CSV dışa aktarımı eklendi.
- İşletme/fiş ayarları eklendi.
- Fiş iki nüshalı ve garanti bilgili hale getirildi.
- Sunucu veri yazımı daha güvenli hale getirildi ve otomatik döner DB yedekleri eklendi.
- Responsive ERP görünümlü masaüstü/mobil arayüz oluşturuldu.


## v2.1.0
- Ayarlar ekranı profesyonel yönetim merkezine dönüştürüldü.
- Sunucu taraflı kullanıcı girişi ve ilk yönetici kurulumu eklendi.
- Şifreler düz metin yerine scrypt hash olarak saklanıyor.
- Kullanıcı yönetimi: ekleme, rol, aktif/pasif, şifre yenileme.
- Logo yükleme ve servis fişinde logo gösterimi eklendi.
- İşletme profil alanları genişletildi.
- Mevcut servis, stok ve kasa verileriyle geriye uyumluluk korundu.

## v2.2.0
- Servis kayıt fişi A5 dikey yazdırma düzenine geçirildi.
- Tek A5 sayfada müşteri ve servis nüshası olmak üzere 2 kopya yerleştirildi.
- İki nüsha arasına kesim çizgisi eklendi.
- GitHub Actions ile Windows kurulum EXE üretmek için yeni workflow eklendi.
- Kurulum paketi Node.js çalışma zamanını kendi içinde taşır; hedef bilgisayarda ayrıca Node.js kurulumu gerekmez.
- Kullanıcı verisini korumak için güncelleme kurulumlarında mevcut db.json üzerine yazılmaz.

## v2.2.1 - Başlatma Hotfix
- Windows kurulumundan sonra sayfanın açılmaması için başlatıcı yenilendi.
- Varsayılan port 3000 yerine 8972 yapıldı.
- Sunucu açılmadan tarayıcı açılmıyor; `/api/health` ile hazır olma kontrolü yapılıyor.
- Başlatma ve sunucu hataları `logs/startup.log` ve `logs/server-error.log` dosyalarına yazılıyor.
- Sunucu başlatılamazsa kullanıcıya hata penceresi gösteriliyor.
- GitHub Actions installer adı `TeknikServisPro_v2_2_1_Setup.exe` olarak güncellendi.

## v2.2.2 - EXE Başlatıcı ve Kısayol Logosu
- Hatalı VBScript başlatıcı tamamen kaldırıldı.
- `TeknikServisPro.exe` adlı Windows launcher eklendi.
- Launcher PowerShell başlangıç denetimini görünmez şekilde çalıştırır.
- Sunucu `8972` portunda sağlık kontrolünden geçince tarayıcı açılır.
- Başlangıç ve sunucu hata logları `logs` klasörüne yazılır.
- Masaüstü ve Başlat menüsü kısayollarına Teknik Servis Pro logosu eklendi.
- Aynı logo Windows kurulum sihirbazı ve kaldırma kaydında kullanılır.
- GitHub Actions launcher EXE'yi otomatik derleyip Inno Setup kurulumunu üretir.

## v2.3.1 - Python Edition

- Node.js, `node_modules`, npm ve eski launcher zinciri tamamen kaldırıldı.
- Backend Python standart kütüphanesiyle yeniden yazıldı.
- Tek `TeknikServisPro.exe` yerel sunucuyu başlatır ve tarayıcıyı otomatik açar.
- Port 8972 korunur; aynı uygulama zaten çalışıyorsa yeni sunucu açmak yerine mevcut sayfa açılır.
- v2.2 scrypt kullanıcı şifreleriyle geriye uyumluluk korunur.
- Mevcut servis, kasa ve kullanıcı verileri `db.json` üzerinden korunur.
- GitHub Actions artık Python 3.12 + PyInstaller + Inno Setup kullanır.
- Hedef bilgisayarda Python veya Node.js kurulumu gerekmez.
- Masaüstü/Başlat menüsü kısayol logosu korunur.
- A5 dikey iki nüsha servis fişi korunur.

## v2.3.1 — Installer Hotfix
- PyInstaller ile üretilen `TeknikServisPro.exe` kaldırıldı.
- Resmi Python 3.12 embedded runtime kullanılıyor.
- Masaüstü/Başlat menüsü kısayolu Teknik Servis Pro ikonunu koruyor.
- Kurulum öncesi yerel sunucuya temiz kapanış isteği gönderiliyor.
- Eski v2.3.0 `TeknikServisPro.exe` süreci yükseltmede kapatılıyor.
- Eski Node/VBS/launcher dosyaları kurulum sırasında temizleniyor.
- `db.json` güncellemelerde korunuyor.
