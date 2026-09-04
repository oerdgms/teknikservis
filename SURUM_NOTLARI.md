# Teknik Servis Pro v2.6.0 — Kurumsal Kimlik + Portal UX + Login Hotfix

## Düzeltmeler
- v2.5.2'de eksik kalan `renderAll()` fonksiyonu geri eklendi. Başarılı giriş sonrası tekrar login ekranına düşme sorunu giderildi.

## Kurumsal kimlik
- Sistem Bilgisayar logosu paket içine eklendi ve ayarlarda özel logo yoksa varsayılan olarak kullanılıyor.
- Login, sol menü, A5 servis fişi ve müşteri portalında kurumsal görünüm birleştirildi.
- `2003'ten beri · 23. yıl` ibaresi ana logodan bağımsız kurumsal rozet olarak kullanıldı.

## Müşteri portalı
- Portal başlığı Sistem Bilgisayar kimliğine geçirildi.
- Teklif/onay kartı mobilde daha görünür hale getirildi.
- İşletme telefon/e-posta/adres bilgileri servis sonucu altında gösteriliyor.
- Güvenli token bağlantısı ve Servis No + Telefon yedek sorgulama korunuyor.

## Telefon standardı
- Yeni müşteri ve servis kaydında telefon 05 ile başlayan 11 haneli cep telefonu standardında tutulur.
- Portal aynı normalize edilmiş telefon standardını kullanır.
- Otomatik düzeltilemeyen eski müşteri telefonları Müşteriler ekranında `Telefon düzeltilmeli` olarak işaretlenir.

## Servis kayıtları ve fiş
- Servis Kayıtları ekranında sade tek arama alanı kullanılır.
- A5 iki nüshalı fişte güvenli QR, portal adresi, servis no, telefon ve online takip açıklaması bulunur.
