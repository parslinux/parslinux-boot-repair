# 🐆 Pars Linux Boot Repair — Fork & Modernizasyon Notları

Bu proje, Pardus ekibi tarafından geliştirilen `pardus-boot-repair` projesi temel alınarak **Pars Linux** ekosistemi için çatallanmış (fork), güncellenmiş ve çoklu dağıtım mimarisiyle modernize edilmiş halidir.

---

## 📌 Yapılan Başlıca İyileştirmeler ve Uyarlamalar

1. **Marka ve Görsel Kimlik Dönüşümü**:
   - Eski Pardus logoları ve referansları yerini ParsLinux'un koyu/modern görsel kimliğine, Pars mavisi ve amber/leopar tonlarına bıraktı.
   - `src/data/images/parslinux-boot-repair.svg` sıfırdan vektörel olarak tasarlandı.
   - `.desktop`, `PolicyKit (.policy)` ve `GResource` adlandırmaları `org.parslinux.boot-repair` standartlarına geçirildi.
   - Kod tabanı, sembolik linkler, GResource ve PolicyKit tanımları tamamen bağımsız ve temiz ParsLinux standartlarına kavuşturuldu.
   - Modern GTK4 ve Libadwaita arayüzü (`AppWindowGtk4.ui` ve `MainGtk4.py`) eklendi, geriye dönük uyumluluk için GTK3 desteği korundu.

2. **Gelişmiş EFI & GRUB Algılama**:
   - `search-operating-system` modülü, EFI bölümlerinde `EFI/parslinux/grubx64.efi` girdisini öncelikli tanıyacak şekilde güncellendi.
   - `grub-reinstall` betiği, anakart BIOS'larında sabit kodlanmış Windows önyükleyici baypası için hem `parslinux` hem de `pardus` dizinlerini kapsayacak esnekliğe kavuşturuldu.

3. **Geliştirici Ortamı ve Canlı Olmayan (Non-Live) Mod Desteği**:
   - Orijinal araç yalnızca `boot=live` çekirdek parametresi ile çalışıyordu. Yapılan güncelleme ile `ALLOW_NON_LIVE=1` veya `--dev` bayrağı sayesinde geliştiriciler aracı canlı USB ortamına girmeden test edebilir.
   - Yerel betik dizinleri dinamik olarak `$PATH` içine enjekte edilerek geliştirme ve hata ayıklama kolaylaştırıldı.

4. **Arch Linux ve Çoklu Dağıtım Desteği**:
   - Standart `PKGBUILD` ve `.SRCINFO` dosyaları eklendi.
   - Arch Linux, CachyOS ve Manjaro üzerinde `makepkg` ile `.pkg.tar.zst` paketi derleme yeteneği sağlandı.
   - `package.sh` içerisine `ar` + `tar` tabanlı saf Debian paketi üreticisi eklendi; böylece Arch üzerinde `dpkg-deb` olmadan da doğrudan `.deb` üretilebilmektedir.

5. **Modüler Yönetim ve Otomasyon Betikleri**:
   - `manage.sh`: Tek CLI üzerinden test, çalıştırma, derleme, paketleme ve temizlik yönetimi.
   - `run.sh`: Yerel çalıştırma (`--dev`, `--test`, `--compile` seçenekleri).
   - `stop.sh`: Açık kalan süreçleri temizleme.
   - `install.sh` / `uninstall.sh`: Sistem çapında güvenli kurulum ve kaldırma.
   - `package.sh`: Çift formatlı (`deb` & `arch`) otomatik paketleyici.

6. **Kapsamlı Otomatik Test Paketi (`tests/`)**:
   - Python modülleri ve betiklerinin sözdizimi denetimi.
   - Tüm Bash betiklerinin `bash -n` doğrulaması.
   - PolicyKit ve GResource XML şemalarının XML parser doğrulaması.
   - Mock dizinler üzerinde işletim sistemi algılama mantığı birim testi.

7. **Yerelleştirme (i18n)**:
   - GNU gettext altyapısı `parslinux-boot-repair` domain'ine geçirildi.
   - Türkçe (`tr.po`) ve Portekizce (`pt.po`) çeviriler güncellendi ve derlendi.
   - Otomatik `update-translations.sh` betiği eklendi.

---

## 👥 Katkıda Bulunanlar

- **Pars Linux Ekibi**: Fork, modernizasyon, görsel kimlik, çoklu dağıtım mimarisi ve otomasyon betikleri.
- **Pardus Ekibi (TÜBİTAK ULAKBİM)**: Orijinal `pardus-boot-repair` çekirdek mantığı ve ilk kod tabanı (Ali Rıza Keskin, Fatih Altun).
