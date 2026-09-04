# Teknik Servis Pro v2.5.1

- Secure Customer Portal eklendi.
- Her servis kaydı için tahmin edilmesi zor portalToken oluşturulur ve kalıcı veride saklanır.
- Müşteri takip linkleri `?token=...` kullanır; telefon numarası URL içinde paylaşılmaz.
- Ayrı portal-only sunucu 127.0.0.1:8973 üzerinde çalışır.
- 8973 üzerinden yönetim paneli, kullanıcı API'leri, veri API'si ve ayarlar dış erişime kapalıdır.
- Tailscale Funnel doğrudan 8973 portuna bağlanabilir.
- Ayarlara “Dış Müşteri Portalı Adresi” eklendi; WhatsApp/SMS hazır mesajları bu adresi kullanır.
- Eski Servis No + Telefon sorgulaması portal ana sayfasında geriye dönük olarak kullanılabilir.
