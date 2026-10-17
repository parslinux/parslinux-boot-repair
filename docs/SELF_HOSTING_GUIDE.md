# Pars Linux Boot Repair — Yerel Depo Barındırma ve Live ISO Entegrasyonu (SELF_HOSTING_GUIDE.md)

Bu kılavuz, **Pars Linux Boot Repair** paketlerini kendi özel APT ve Pacman depolarınızda nasıl barındıracağınızı (`self-hosting`) ve canlı sistem (Live ISO) ortamlarına nasıl dahil edeceğinizi açıklamaktadır.

---

## 1. Özel APT Paket Deposu Barındırma (`reprepro`)

ParsLinux veya Debian tabanlı dağıtım sunucunuzda Boot Repair paketini barındırmak için:

```bash
# Reprepro kurulumu
sudo apt install -y reprepro

# Depoya paket ekleme
cd /var/www/html/parslinux-repo
reprepro -b . includedeb stable /yol/parslinux-boot-repair_1.2.0-parslinux1_all.deb
```

İstemci `/etc/apt/sources.list.d/parslinux.list` yapılandırması:
```ini
deb [trusted=yes] https://repo.parslinux.org/parslinux stable main
```

---

## 2. Özel Arch Linux / Pacman Deposu Barındırma

```bash
# Pacman veritabanı oluşturma ve paket ekleme
cd /var/www/html/parslinux-arch
repo-add parslinux.db.tar.zst parslinux-boot-repair-1.2.0-1-any.pkg.tar.zst
```

İstemci `/etc/pacman.conf` eklemesi:
```ini
[parslinux]
SigLevel = Optional TrustAll
Server = https://repo.parslinux.org/arch/$arch
```

---

## 3. Canlı USB (Live-Build / Live ISO) Entegrasyonu

ParsLinux Canlı ISO kalıbına Boot Repair aracını doğrudan dahil etmek için:

1. `config/package-lists/desktop.list.chroot` dosyasına ekleyin:
   ```text
   parslinux-boot-repair
   ```
2. Otomatik açılış masaüstü kısayolu için:
   ```bash
   cp /usr/share/applications/org.parslinux.boot-repair.desktop config/includes.chroot/etc/skel/Desktop/
   ```
3. `lb build` komutuyla ISO'yu derleyin.
