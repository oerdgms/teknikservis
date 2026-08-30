# Teknik Servis Pro v2.3.6 — ÇiftlikPro Runtime Match

## Korunan v2.3.4 / v2.3.5 özellikleri
- Dashboard kartlarıyla Son Servis Hareketleri filtreleme
- Aktif Servis, Onay/Parça, Teslime Hazır, Geciken, Açık Bakiye filtreleri
- Net Kasa kartından Kasa ekranına geçiş
- Servis kayıtlarında Seri No / IMEI araması
- Mobil Seri No / IMEI kamera-barkod/QR okuma
- Mobil hamburger kartlarının tam yüzeyden tıklanması
- Mobil Son Servis Hareketleri kart görünümü
- A5 dikey iki nüsha servis fişi
- Kullanıcı, şifre, logo ve profesyonel ayarlar
- Python backend ve 8972 portu

## v2.3.6 Windows build değişikliği
- PyInstaller giriş noktası artık ek launcher yerine doğrudan app/server.py.
- PyInstaller onedir / COLLECT / exclude_binaries=True / UPX=False korunuyor.
- EXE'ye standart Windows sürüm/künye kaynağı eklendi.
- Inno Setup sade kullanıcı kurulumu olarak korunuyor.
- GitHub Actions build sonrası gerçek /api/health testi yapıyor.
- Artifact içine SHA256 ve build-inventory.txt ekleniyor.

Not: Bu değişiklikler yazılımı antivirüsten gizlemek için değildir. Standart ve şeffaf Windows paketleme yapısını ÇiftlikPro çalışma modeline yaklaştırır. İmzasız yeni EXE'lerde antivirüs yanlış pozitifleri yine mümkün olabilir.
