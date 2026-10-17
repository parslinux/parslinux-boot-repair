# Pars Linux Boot Repair — Flatpak Paketleme Kılavuzu (FLATPAK_PACKAGING.md)

Bu kılavuz, **Pars Linux Boot Repair** uygulamasının Flatpak mimarisi ve Flathub standartlarına uyarlanmasını, sandbox izinlerini ve sistem düzeyinde yetkilendirme modellerini açıklamaktadır.

---

## 1. Düşük Seviyeli Sistem Erişim İzinleri

Boot Repair gibi doğrudan disk bölümlerine erişen, blok aygıtlarını formatlayan, GRUB kuran ve `chroot` açan sistem araçları, standart Flatpak sandbox izinlerinin ötesinde yetkilere ihtiyaç duyar:

- `--device=all`: Tüm blok aygıtlarına (`/dev/sd*`, `/dev/nvme*`, `/dev/mapper/*`, `/dev/loop*`) düşük seviyeli I/O erişimi.
- `--filesystem=host`: Barındırıcı sistemin dosya sistemlerini inceleyebilme ve bağlama yapabilme.
- `--talk-name=org.freedesktop.PolicyKit1`: Kök hakları gereken eylemler için barındırıcı Polkit servisiyle iletişim.
- `--system-talk-name=org.freedesktop.UDisks2`: Blok aygıtlarının durumunu ve bağlama noktalarını sorgulama.
- `--socket=wayland` ve `--socket=fallback-x11`: Grafiksel kullanıcı arayüzü desteği.

---

## 2. Flatpak Manifestosu (`org.parslinux.BootRepair.json`)

```json
{
  "app-id": "org.parslinux.BootRepair",
  "runtime": "org.gnome.Platform",
  "runtime-version": "46",
  "sdk": "org.gnome.Sdk",
  "command": "parslinux-boot-repair",
  "finish-args": [
    "--device=all",
    "--filesystem=host",
    "--share=ipc",
    "--socket=wayland",
    "--socket=fallback-x11",
    "--talk-name=org.freedesktop.PolicyKit1",
    "--system-talk-name=org.freedesktop.UDisks2"
  ],
  "modules": [
    {
      "name": "parslinux-boot-repair",
      "buildsystem": "simple",
      "build-commands": [
        "make build",
        "make install PREFIX=/app"
      ],
      "sources": [
        {
          "type": "dir",
          "path": "."
        }
      ]
    }
  ]
}
```

---

## 3. Yerel Test ve Derleme

```bash
# Flatpak derleyicisini çalıştırın:
flatpak-builder --user --install --force-clean build-dir org.parslinux.BootRepair.json

# Flatpak paketini çalıştırın:
flatpak run org.parslinux.BootRepair
```
