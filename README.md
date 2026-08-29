# Sistem Bilgisayar Teknik Servis Pro v2.0

Yerel ağda çalışabilen Node.js tabanlı teknik servis, müşteri, stok ve kasa takip uygulaması.

## Çalıştırma
1. Bilgisayarda Node.js 18+ kurulu olmalı.
2. Klasörde `npm install` çalıştırın.
3. `npm start` çalıştırın.
4. Tarayıcıdan `http://localhost:3000` adresini açın.

## v2.0 ana özellikler
- Gelişmiş servis iş emri ve 9 aşamalı durum akışı
- Öncelik, teknisyen, tahmini teslim, garanti ve servis hareket geçmişi
- Kısmi tahsilat, açık bakiye ve ödeme yöntemi
- Otomatik müşteri / cihaz servis geçmişi
- Yedek parça ve stok yönetimi, kritik stok uyarısı
- Gelir/gider kasa takibi
- Dashboard uyarıları ve raporlar
- Servis ve kasa CSV dışa aktarma
- JSON yedek alma / geri yükleme
- Responsive masaüstü ve mobil arayüz
- Sunucu tarafında son 20 kayıt için otomatik db yedeği

## Veri
Ana veri dosyası `db.json`'dur. Her veri kaydında sunucu `backups/` altında döner yedek oluşturur.


## v2.1 - Profesyonel Ayarlar ve Kullanıcı Güvenliği
- İlk çalıştırmada yönetici hesabı oluşturma
- Kullanıcı adı / şifre ile giriş ve 12 saatlik oturum
- Şifrelerin scrypt ile hash'li saklanması
- Yönetici, Teknisyen ve Kasa kullanıcı rolleri
- Yöneticiye kullanıcı ekleme, rol değiştirme, aktif/pasif ve şifre sıfırlama
- Kullanıcının kendi şifresini değiştirebilmesi
- Firma logosu yükleme / kaldırma; logo menü ve servis fişlerinde kullanılır
- E-posta, vergi dairesi ve vergi/T.C. no işletme alanları
- Ayarlar ekranında İşletme / Kullanıcılar / Güvenlik sekmeleri

> İlk açılışta mevcut servis verileri silinmez. Yalnızca ilk yönetici hesabını oluşturmanız istenir.

## GitHub Actions ile Windows kurulum
1. Bu klasörün içeriğini GitHub deposunun `main` branch'ine yükleyin.
2. GitHub > Actions > `Teknik Servis Pro - Windows Kurulum` workflow'unu açın.
3. `Run workflow` ile manuel çalıştırabilir veya ilgili kaynak dosyalara push yaptığınızda otomatik build alabilirsiniz.
4. Build sonunda `TeknikServisPro-v2.2-Windows-Setup` artifact'ı içinde kurulum EXE'si oluşur.

Kurulum hedef bilgisayara Node.js istemez; Node çalışma zamanı paket içinde taşınır. Güncelleme kurulumlarında mevcut `db.json` korunur.

## A5 servis fişi
Servis detayındaki `Fiş` butonu A5 dikey yazdırma görünümünü açar. Tek A5 sayfada üstte müşteri nüshası, altta servis nüshası ve ortada kesim çizgisi bulunur. Yazıcı ayarlarında kağıt boyutunu A5, yönü Dikey ve ölçeği %100 seçin.
