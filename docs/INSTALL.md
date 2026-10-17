# 📦 Pars Linux Boot Repair — Kurulum Kılavuzu

Bu kılavuz, **`parslinux-boot-repair`** uygulamasının farklı Linux dağıtımlarına nasıl kurulacağını ve bağımlılıklarını açıklamaktadır.

---

## 1. Sistem Bağımlılıkları

### Çalışma Zamanı (Runtime) Bağımlılıkları
- `python3` (>= 3.8)
- `python3-gi` (GObject Introspection)
- `gir1.2-gtk-3.0` (GTK+ 3.24)
- `gir1.2-handy-1` (Libhandy 1.x)
- `gir1.2-vte-2.91` (VTE Terminal Emülatörü)
- `polkit-1` (pkexec)
- `efibootmgr`
- `dosfstools` (mkfs.vfat / fsck.vfat)
- `e2fsprogs` (fsck.ext4)
- `btrfs-progs` (BTRFS denetimi)
- `cryptsetup` (LUKS şifre çözme)
- `lvm2` (Mantıksal hacim desteği)
- `zip` (Log arşivleme)

### Derleme Zamanı (Build) Bağımlılıkları
- `make`
- `libglib2.0-dev-bin` (`glib-compile-resources`)
- `gettext` (`msgfmt`, `xgettext`)

---

## 2. Dağıtım Bazlı Kurulum

### Debian / Ubuntu / ParsLinux
```bash
# Bağımlılıkları yükleyin
sudo apt update
sudo apt install -y make libglib2.0-dev-bin gettext python3 python3-gi \
    gir1.2-gtk-3.0 gir1.2-handy-1 gir1.2-vte-2.91 policykit-1 efibootmgr \
    dosfstools e2fsprogs btrfs-progs cryptsetup lvm2 zip

# Paketi derleyin ve kurun
./package.sh --deb
sudo dpkg -i dist/parslinux-boot-repair_*.deb
sudo apt install -f
```

### Arch Linux / CachyOS / Manjaro
```bash
# Bağımlılıkları yükleyin
sudo pacman -S --needed base-devel python python-gobject gtk3 libhandy \
    vte3 polkit efibootmgr dosfstools e2fsprogs btrfs-progs cryptsetup lvm2 zip

# Paketi derleyin ve kurun
./package.sh --arch
sudo pacman -U dist/parslinux-boot-repair-*.pkg.tar.zst
```

### Kaynak Koddan Manuel Kurulum
```bash
make build
sudo make install
```

---

## 3. Sistemden Kaldırma (Uninstall)

```bash
# Makefile ile:
sudo ./uninstall.sh

# Veya Debian paket yöneticisi ile:
sudo apt purge parslinux-boot-repair

# Veya Arch paket yöneticisi ile:
sudo pacman -Rns parslinux-boot-repair
```
