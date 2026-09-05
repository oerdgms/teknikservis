# Sürüm Notları — v2.6.4 Hotfix2

## Müşteri Portalı
- Servis durumu rozeti CRM görünümüne yaklaştırıldı.
- "Teslim Edildi" durumu artık yeşil, dikdörtgene yakın, metni tam ortalanmış ve onay ikonlu görünür.
- Diğer durumlar için de uyumlu durum renkleri/ikonları eklendi.

## Servis Fişi / Baskı
- A5 baskı düzeni dikeyden yataya çevrildi.
- Tek A5 yatay sayfaya iki fiş kopyası yan yana yerleştirildi: Müşteri Nüshası + Servis Nüshası.
- Ortaya dikey kesim çizgisi eklendi.
- QR kodlu müşteri portalı, servis no, telefon, ücretler, garanti ve imza alanları korunuyor.
- Amaç: minimum kağıt kullanımıyla iki nüshayı tek A5 yaprakta üretmek.

## Teknik
- Uygulama sürümü 2.6.4-hf1'e yükseltildi.
- Python derleme ve JavaScript sözdizimi kontrolleri tamamlandı.

## Hotfix1 — A5 Tek Yaprak + Gerçek SMS API
- A5 yatay baskı 210×148 mm tek fiziksel sayfaya sabitlendi; iki nüsha yan yana, ortada kesim alanı.
- Baskı CSS kenar boşluğu 0 ve içeride güvenli 4 mm pay ile yeniden kuruldu.
- Ayarlar > SMS sekmesi eklendi. İleti Merkezi ve Netgsm servis sağlayıcı bilgileri kullanıcı tarafından tanımlanabilir.
- Üst çubukta tüm modüllerden erişilen global SMS düğmesi eklendi.
- Servis listesi ve müşteri kartlarına bağlamsal SMS düğmeleri eklendi.
- Müşteri Bilgilendirme Merkezi içindeki SMS artık cihazdaki sms: bağlantısını açmak yerine sunucu API üzerinden gerçek gönderim yapar.
- Gönderim sonucu servis hareketlerine ve SMS loguna işlenir.
- API kimlik bilgileri yalnız yerel uygulama verisinde saklanır; müşteri portalı API'sine açılmaz.
