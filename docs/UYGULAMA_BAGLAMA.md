# Pars Linux Boot Repair — Masaüstü ve Sistem Uygulama Bağlama Kılavuzu (UYGULAMA_BAGLAMA.md)

Bu doküman, **Pars Linux Boot Repair** uygulamasının Linux masaüstü ortamlarına (GNOME, KDE Plasma, XFCE), sistem menülerine, XDG standartlarına ve PolicyKit yetkilendirme mekanizmasına nasıl entegre edildiğini açıklar.

---

## 1. Masaüstü Giriş Dosyası (`.desktop`)

Uygulamanın sistem menüsünde, uygulama arama çubuğunda ve kurtarma araçları kategorisinde görünmesini sağlayan dosya:
`/usr/share/applications/org.parslinux.boot-repair.desktop`

```ini
[Desktop Entry]
Name=Pars Linux Boot Repair
Name[tr]=Pars Linux Başlangıç Onarma
GenericName=Boot Repair
GenericName[tr]=Başlangıç Onarma
Comment=Pars Linux boot and system repair tool (GRUB, EFI, Chroot, Password Reset)
Comment[tr]=Pars Linux önyükleme ve sistem onarma aracı (GRUB, EFI, Chroot, Parola Sıfırlama)
Exec=parslinux-boot-repair
Icon=parslinux-boot-repair
Terminal=false
Type=Application
Categories=System;Settings;GTK;X-ParsLinux-Apps;
StartupWMClass=org.parslinux.boot-repair
Keywords=boot;repair;grub;efi;mbr;chroot;rescue;recovery;onarma;baslangic;
X-ParsLinux-Apps=true
```

---

## 2. PolicyKit (pkexec) Yetkilendirme Kuralı

Uygulama doğrudan disk donanımına yazım yaptığı için Polkit aracılığıyla grafiksel yönetici parolası ister:
`/usr/share/polkit-1/actions/org.parslinux.pkexec.parslinux-boot-repair.policy`

- **Action ID:** `org.parslinux.boot-repair`
- **Exec Path:** `/usr/bin/parslinux-boot-repair`
- **İzin Seviyesi:** `auth_admin` (Kullanıcıdan yönetici parolası istenir)
- **GUI Desteği:** `<annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>`

---

## 3. Sistem İkonu Entegrasyonu

Vektörel SVG ikon aşağıdaki konumlara yerleştirilir:
- `/usr/share/icons/hicolor/scalable/apps/parslinux-boot-repair.svg`
- `/usr/share/icons/parslinux-boot-repair.svg`

Kurulum sonrasında simge önbelleği otomatik güncellenir:
```bash
gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
update-desktop-database -q
```
