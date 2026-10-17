# Pars Linux Boot Repair — Claude & AI Ajan Geliştirici Kılavuzu (CLAUDE.md)

Bu kılavuz; Claude, Gemini ve diğer otonom AI kodlama asistanlarının **Pars Linux Boot Repair** (`parslinux-boot-repair`) kod tabanında güvenli, tutarlı ve etkili çalışabilmesi için özel olarak hazırlanmıştır.

---

## 1. Kod Tabanı Genel Özeti

Pars Linux Boot Repair; Python 3, modern GTK 4 / Libadwaita (`Adw`), klasik GTK 3 / Libhandy (`Hdy`), gömülü VTE terminal motoru ve güçlü çekirdek Bash/Python kurtarma betiklerinden oluşan bir sistem önyükleme kurtarma aracıdır.

- **Ana Kaynak Kod**: `src/`
  - `MainGtk4.py`: Modern GTK 4 + Libadwaita (`AdwApplicationWindow`, `AdwActionRow`, `AdwStatusPage`, `AdwAboutWindow`) birincil arayüz motoru.
  - `Main.py`: Klasik GTK 3 + Libhandy (`HdyApplicationWindow`) geri uyumluluk motoru.
  - `data/ui/AppWindowGtk4.ui`: Modern GTK 4 / Libadwaita XML arayüz tanımı.
  - `data/ui/AppWindow.ui`: Klasik GTK 3 Libhandy arayüz tanımı.
  - `data/images/`: `parslinux-boot-repair.svg` simge ve görsel varlıkları.
  - `data/*.desktop`: Masaüstü başlatıcı dosyası (`org.parslinux.boot-repair.desktop`).
  - `data/*.policy`: PolicyKit yetkilendirme kuralı (`org.parslinux.pkexec.parslinux-boot-repair.policy`).
  - `data/*.gresource.xml`: GLib GResource derleme şeması.
  - `scripts/`: Kök seviyesinde çalışan çekirdek kurtarma motorları:
    - `grub-reinstall`: BIOS/MBR ve UEFI (amd64/ia32) GRUB önyükleyici kurulumu.
    - `reset-password`: Kök veya normal kullanıcı şifresi sıfırlama (`openssl passwd -6`).
    - `check-filesystem`: fsck.ext4 ve btrfs check --repair motoru.
    - `fix-broken-packages`: Dpkg ve APT bozuk bağımlılık kurtarma.
    - `full-upgrade`: Chroot içinde tam paket güncelleme.
    - `parslinux-chroot`: Sanal API bağlamalarıyla izole chroot kabuğu açıcı.
    - `parslinux-mount-rootfs`: LUKS/LVM2 ve BTRFS subvol ayrıştıran akıllı bağlayıcı.
    - `parslinux-open-luks-lvm`: LUKS şifreli disk ve LVM2 mantıksal hacim çözücü.
    - `parslinux-reinstall`: Canlı medyadan temiz sistem tazeleme motoru.
    - `dump-info-log`: Teşhis günlüklerini ZIP arşivinde toplama motoru.
    - `search-operating-system`: Blok aygıtlarını ve EFI yapılarını tarayıcı.

---

## 2. Geliştirme ve Test Komutları

Yapay zeka asistanları komut çalıştırırken doğrudan `manage.sh` veya `run.sh` kullanmalıdır:

```bash
# Test paketini çalıştırma (Birim & Doğrulama testleri):
./manage.sh test
# veya
python3 -m unittest discover -s tests -v

# Geliştirici modunda çalıştırma (root istemeden):
./manage.sh dev

# Varlıkları derleme (GResource ve Locale MO):
./manage.sh compile

# Paket derleme (Debian ve Arch):
./manage.sh package --all
```

---

## 3. Kodlama ve Mimari Kuralları

1. **İkili UI Desteği:** Yapılan herhangi bir UI mantığı değişikliği hem `MainGtk4.py` (Adw) hem de `Main.py` (Hdy) dosyalarında eşzamanlanmalıdır.
2. **Path Bağımsızlığı:** Betikler çağrılırken mutlak `/usr/bin/` yolları yerine önce `$PATH` ve `src/scripts/` yerel yolları kontrol edilmelidir.
3. **i18n & Çeviri:** Tüm yeni arayüz dizgileri `_("...")` içine alınmalı ve `./update-translations.sh` çalıştırılarak `.pot` şablonu güncellenmelidir.
4. **Veri Güvenliği:** Disk bağlama ve ayırma işlemlerinde mutlaka `umount -lf` ve hata yakalama blokları kullanılmalıdır.
