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
