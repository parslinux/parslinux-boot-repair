# 💻 Pars Linux Boot Repair — Komut Satırı (CLI) Kılavuzu

Pars Linux Boot Repair, grafiksel arayüzünün (GUI) yanı sıra doğrudan terminalden veya kurtarma kabuğundan çağrılabilecek güçlü bağımsız CLI araçları sunar.

---

## 1. Ana Başlatıcı: `parslinux-boot-repair`

```bash
# Grafik arayüzü PolicyKit yetkilendirmesi ile başlatır
parslinux-boot-repair

# Geliştirici modunda (root istemeden yerel test için)
NO_PKEXEC=1 python3 src/Main.py
# veya
./manage.sh dev
```

---

## 2. Çekirdek Kurtarma Betikleri

Tüm çekirdek betikler `/usr/bin/` altında kurulur veya kaynak repo içinde `src/scripts/` altında çalıştırılabilir:

### `parslinux-chroot`
Hedef kök bölüme gerekli tüm sanal dosya sistemlerini bağlayarak güvenli bir chroot kabuğu açar.
```bash
# Kullanım:
sudo parslinux-chroot /dev/sdX1 [KOMUT]

# Örnek: Doğrudan bash kabuğu açma
sudo parslinux-chroot /dev/sda2 /bin/bash

# Örnek: Kurulu sistemde paket güncelleme
sudo parslinux-chroot /dev/nvme0n1p2 apt update
```

### `parslinux-mount-rootfs`
Hedef diski çözer (LUKS/LVM/BTRFS) ve `DESTDIR` dizinine bağlar.
```bash
export disk="sda2"
export DESTDIR="/mnt"
sudo -E parslinux-mount-rootfs
```

### `grub-reinstall`
Hedef bölümdeki GRUB önyükleyicisini onarır ve MBR/EFI kayıtlarını yeniler.
```bash
export disk="sda2"
export mbr="sda"
sudo -E grub-reinstall
```

### `reset-password`
Kök veya seçilen sistem kullanıcısının parolasını sıfırlar.
```bash
export disk="sda2"
export user="pars"
export pass1="yenisifre123"
export pass2="yenisifre123"
sudo -E reset-password
```

### `check-filesystem`
Seçilen bölümün dosya sistemini denetler ve onarır.
```bash
export disk="sda1"
sudo -E check-filesystem
```

### `fix-broken-packages`
Hedef kurulu sistemdeki bozuk paket bağımlılıklarını (`dpkg --configure -a`, `apt install -f`) tamir eder.
```bash
export disk="sda2"
sudo -E fix-broken-packages
```

### `dump-info-log`
Sorun teşhisi için sistem ve donanım günlüklerini ZIP arşivinde toplar.
```bash
export disk="sda2"
sudo -E dump-info-log /tmp/logs
# Çıktı: /tmp/logs/system-log.zip
```

### `search-operating-system`
Sistemdeki kurulu işletim sistemlerini ve EFI yapılarını listeler.
```bash
sudo search-operating-system
```

---

## 3. Yönetim Otomasyon Betiği: `./manage.sh`

| Komut | Açıklama |
| :--- | :--- |
| `./manage.sh run` | Uygulamayı root yetkisiyle başlatır |
| `./manage.sh dev` | Uygulamayı yerel test modunda açar |
| `./manage.sh test` | 7 adımlı otomatik birim test paketini çalıştırır |
| `./manage.sh package` | Otomatik Debian ve Arch paketlerini derler (`dist/`) |
| `./manage.sh install` | Sisteme doğrudan kurar (`sudo make install`) |
| `./manage.sh uninstall` | Sistemden tamamen kaldırır |
| `./manage.sh clean` | Derleme ve test artıklarını temizler |
| `./manage.sh status` | Sistem araçları ve bağımlılıkların durumunu gösterir |
