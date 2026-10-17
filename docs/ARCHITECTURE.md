# 🏛️ Pars Linux Boot Repair — Sistem & Mimari Mimarisi

Bu belge, **`parslinux-boot-repair`** aracının dahili çalışma prensiplerini, çekirdek bileşenlerini ve modüller arası veri akışını açıklamaktadır.

---

## 1. Mimari Katmanlar

```
+-------------------------------------------------------------------+
|               KULLANICI ARAYÜZÜ (GUI LAYER)                       |
|   - GTK 3.24 + Libhandy 1.x (Modern GNOME / Responsive Layout)    |
|   - HdyDeck, HdyCarousel, HdyStatusPage                           |
|   - VTE Terminal Widget (Gömülü Canlı Konsol Çıktısı)             |
+---------------------------------+---------------------------------+
                                  |
               PolicyKit (pkexec) | Yetkilendirme Köprüsü
                                  v
+-------------------------------------------------------------------+
|               UYGULAMA KONTROLÖRÜ (CONTROLLER)                    |
|   - src/Main.py (Pencere Yaşam Döngüsü & Sinyal Yönlendirici)     |
|   - Otomatik Donanım & Disk Taraması (search-operating-system)     |
|   - VTE Süreç Yöneticisi (Async spawn & signal handlers)          |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|               ÇEKİRDEK BETİK MOTORU (CORE SCRIPTS)                |
|   - parslinux-mount-rootfs : Kök dosya sistemi, fstab, API mounts |
|   - parslinux-open-luks-lvm: LUKS şifreli disk & LVM2 çözücü     |
|   - parslinux-chroot       : Unshare + PID izoleli Chroot         |
|   - grub-reinstall         : BIOS/MBR + UEFI önyükleyici onarımı  |
|   - reset-password         : Shadow / OpenSSL SHA-512 şifreleme   |
|   - check-filesystem       : fsck.ext4 / btrfs check --repair     |
|   - fix-broken-packages    : Dpkg yapılandırma & APT onarım       |
|   - dump-info-log          : Sistem teşhis günlükleri (ZIP)       |
+-------------------------------------------------------------------+
```

---

## 2. Temel Modüller ve Görevleri

### A. Arayüz Katmanı (`src/Main.py` & `src/data/ui/AppWindow.ui`)
- **Libhandy Entegrasyonu:** Mobil ve masaüstü form faktörlerine uyum sağlayan uyarlanabilir (adaptive) pencereler.
- **VTE Terminal:** Kullanıcının arka planda dönen `chroot`, `grub-install` veya `fsck` komutlarını canlı olarak izlemesine olanak tanıyan gömülü terminal emülatörü.
- **Durum Sayfaları (`HdyStatusPage`):** Kullanıcı dostu işlem bildirimleri, dönen yükleme animasyonları ve hata/başarı durum ikonları.

### B. Disk & Bölüm Algılama (`src/scripts/search-operating-system`)
1. `/sys/block/*` altındaki tüm blok aygıtlarını (SATA `/dev/sd*`, NVMe `/dev/nvme*`, eMMC `/dev/mmcblk*`, sanallaştırma `/dev/vd*`) tarar.
2. Bölümleri salt-okunur (`ro`) geçici olarak `/tmp/` altına bağlar.
3. `/etc/os-release` veya `EFI/<vendor>/grubx64.efi` varlığını denetler.
4. ParsLinux, Pardus, Debian, Arch ve Windows sistemlerini tespit ederek kullanıcıya sunar.

### C. Güvenli Kök Bağlama (`src/scripts/parslinux-mount-rootfs`)
- LUKS şifreli bölümler tespit edildiğinde şifre çözme oturumu açar.
- LVM2 Volume Group (VG) ve Logical Volume (LV) yapılarını etkinleştirir (`vgchange -ay`).
- BTRFS alt hacimlerini (`subvolumes`) algılayarak doğru kök alt hacmini bağlar.
- Çekirdek API dosya sistemlerini (`/dev`, `/dev/pts`, `/proc`, `/sys`, `/sys/firmware/efi/efivars`) bağlar.
- Hedef sistemin `/etc/fstab` dosyasına göre `/boot` ve `/boot/efi` bölümlerini otomatik tespit edip yerine bağlar.

### D. Önyükleme Onarımı (`src/scripts/grub-reinstall`)
- UEFI platformunu (`64-bit` vs `32-bit`) `/sys/firmware/efi/fw_platform_size` üzerinden otomatik saptar.
- Hedef sistemde `grub-efi-amd64-bin`, `grub-efi-ia32-bin` veya `grub-pc-bin` paketlerini doğrular.
- Sabit kodlanmış Windows Boot Manager önyükleyicisine sahip üretici anakartları için `/boot/efi/parslinux/bootx64.efi` dosyasını `bootmgfw.efi` olarak güvenle kopyalar.
- `update-initramfs -u` ve `grub-mkconfig -o /boot/grub/grub.cfg` çalıştırır.

---

## 3. Güvenlik ve İzolasyon Modeli

1. **PolicyKit Yetkilendirmesi:** `parslinux-boot-repair` başlatılırken `org.parslinux.boot-repair` kuralı tetiklenir. Yalnızca yetkili yönetici (admin/wheel/sudo) şifresi ile çalışır.
2. **Chroot İzolasyonu:** Komutlar `unshare --fork --pid chroot` ile ayrı bir süreç alanında koşturulur; böylece canlı sistemin kendi çekirdek süreçleri korunur.
3. **Temiz Kapanma ve Unmount Garantisi:** Betikler tamamlandığında veya hata durumunda bağlanan tüm `/dev`, `/sys`, `/proc` ve kök dizinler `umount -lf` ile sistemden temizlenir.
