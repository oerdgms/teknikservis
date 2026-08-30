# Teknik Servis Pro v2.3.4 — Python Edition

Teknik Servis Pro; servis kabul, müşteri/cihaz geçmişi, teknisyen, kasa, stok, kullanıcı/şifre, işletme ayarları ve A5 çift nüsha servis fişi özelliklerini içeren yerel teknik servis uygulamasıdır.

## v2.3.4 Mobil UX + Installer

Bu sürümde Node.js ve PyInstaller tabanlı özel uygulama EXE'si kullanılmaz. Windows paketi, python.org tarafından yayımlanan resmi Python 3.12 embedded runtime ile çalışır. Masaüstü ve Başlat menüsü kısayolları yine Teknik Servis Pro adı ve özel logosuyla görünür.

Kurulum güncelleme sırasında çalışan v2.3.4+ sunucuya yerel kapanış isteği yollar; eski v2.3.0 `TeknikServisPro.exe` sürecini de kapatır. Böylece `MoveFile failed; code 5` dosya kilidi hatası azaltılır. Mevcut `db.json` güncellemede korunur.

## GitHub Actions ile kurulum

1. Bu klasörün **içeriğini** repository köküne yükleyin.
2. GitHub'da **Actions → Teknik Servis Pro - Windows Kurulum → Run workflow** seçin.
3. Workflow resmi Python embedded runtime'ı indirir ve dağıtım klasörüne ekler.
4. Inno Setup `TeknikServisPro_v2_3_2_Setup.exe` dosyasını üretir.
5. Build tamamlanınca `TeknikServisPro-v2.3.4-Python-Windows-Setup` artifact'ını indirin.

> Not: Kurulum EXE'si kod imzalama sertifikasıyla imzalı değildir. Antivirüs/SmartScreen itibarı konusunda en güçlü kalıcı çözüm Authenticode kod imzalamadır; bu sürüm PyInstaller'ı kaldırarak yanlış pozitif yüzeyini azaltır.


## v2.3.4 Build Hotfix
GitHub Actions PyInstaller derlemesi artık `.spec` dosyasına bağımlı değildir. Workflow gerekli kaynakları kontrol eder ve `python -m PyInstaller` komutunu doğrudan çalıştırır.
