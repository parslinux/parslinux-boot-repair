# Pars Linux Boot Repair — Geliştirme İlerleme Raporu (progress.md)

Bu belge, **Pars Linux Boot Repair** (`parslinux-boot-repair`) projesinin geliştirme aşamalarını, tamamlanan görevleri, mevcut durumunu ve gelecek hedeflerini dinamik olarak izlemektedir.

---

## 1. Genel İlerleme Özeti

- **Proje Adı**: Pars Linux Boot Repair (`parslinux-boot-repair`)
- **Kaynak Proje**: `pardus-boot-repair` (v1.1.0 Upstream)
- **Proje Durumu**: Kararlı, Modernize Edilmiş ve Tamamlanmış
- **Geçerli Sürüm**: `1.2.0-parslinux1`
- **Arayüz Desteği**: %100 Saf GTK 4 + Libadwaita (Varsayılan) + GTK 3 Libhandy (Geri Uyumluluk)
- **Birim Testleri**: 8/8 Test Başarılı (%100 Geçti)
- **Paketleme**: Debian (`.deb`) ve Arch Linux (`.pkg.tar.zst` / `PKGBUILD`) Tamamlandı
- **Dokümantasyon**: Eksiksiz Master Dokümantasyon Seti

---

## 2. Tamamlanan Aşamalar (Milestones)

### [x] Faz 0: Kaynak İnceleme ve Çatallama (Fork)
- [x] `pardus/pardus-boot-repair` deposundan klonlandı.
- [x] Kod tabanındaki Pardus bağımlılıkları ve referansları analiz edildi.
- [x] Uzak depo `git@github.com:parslinux/parslinux-boot-repair.git` olarak yapılandırıldı.

### [x] Faz 1: Çekirdek Betiklerin Dönüştürülmesi
- [x] `parslinux-chroot`, `parslinux-mount-rootfs`, `parslinux-open-luks-lvm`, `parslinux-reinstall` adlandırmaları yapıldı.
- [x] Eski pardus sembolik bağları, XML şemaları ve kalıntıları temizlenerek saf ParsLinux yapısına kavuşturuldu.
- [x] `search-operating-system`: EFI bölümlerinde `EFI/parslinux/grubx64.efi` öncelikli tanıma eklendi.
- [x] `grub-reinstall`: Sabit kodlanmış Windows UEFI baypası hem `parslinux` hem `pardus` hedeflerine genişletildi.

### [x] Faz 2: Marka, İkon ve Varlıkların Yenilenmesi
- [x] Modern SVG simgesi (`parslinux-boot-repair.svg`) tasarlandı.
- [x] XDG Masaüstü dosyası (`org.parslinux.boot-repair.desktop`) oluşturuldu.
- [x] PolicyKit yetki kuralı (`org.parslinux.pkexec.parslinux-boot-repair.policy`) yazıldı.
- [x] GLib GResource XML derleme şeması güncellendi.

### [x] Faz 3: Modern GTK 4 + Libadwaita Dönüşümü
- [x] `AppWindowGtk4.ui`: Modern `AdwApplicationWindow`, `AdwActionRow`, `AdwClamp`, `AdwStatusPage` ile sıfırdan oluşturuldu.
- [x] `src/MainGtk4.py`: Libadwaita ve GTK 4 VTE (v3.91) motoru yazıldı.
- [x] `parslinux-boot-repair`: Varsayılan olarak GTK 4 çalıştıran, istenirse `--gtk3` ile geri uyumluluk sağlayan akıllı başlatıcıya dönüştürüldü.

### [x] Faz 4: Çift Dağıtım Paketleme Motoru
- [x] Debian (`.deb`): Bağımsız `ar` + `tar` motoruyla Arch üzerinde bile sıfır bağımlılıkla deb paketi üretebilme.
- [x] Arch Linux: Standart `PKGBUILD` ve `.SRCINFO` dosyaları hazırlandı.
- [x] `package.sh`: Hem debian hem arch formatını tek tıkla `dist/` klasörüne çıkaran sistem.

### [x] Faz 5: Otomatik Test ve CI/CD Altyapısı
- [x] `tests/test_boot_repair.py`: 8 bağımsız birim ve entegrasyon testi yazıldı.
- [x] Python ve Bash sözdizimi, PolicyKit XML, GResource XML, GTK4 UI XML ve mock işletim sistemi algılama testleri başarıyla doğrulandı.

### [x] Faz 6: Master Dokümantasyon Paketi ve Temizlik
- [x] Master proje standardında 18 markdown dokümanı `docs/` altında hazırlandı.
- [x] Pardus kaynaklı tüm eski artıklar, atıl symlink'ler ve şemalar temizlendi.
- [x] Master yol haritası (`PARSLINUX_FORK_PLANI.md`) üzerinde ilgili madde tamamlandı olarak güncellendi.
