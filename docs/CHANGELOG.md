# 📜 Değişiklik Günlüğü (Changelog)

Tüm önemli değişiklikler bu dosyada belgelenmektedir.

## [1.2.0-parslinux1] - 2026-10-17

### Eklendi
- **ParsLinux Fork**: Proje Pardus kaynağından ParsLinux için çatallandı.
- **ParsLinux Görsel Kimliği**: Modern koyu tema, SVG ikon (`parslinux-boot-repair.svg`) ve GTK3/Libhandy uyarlamaları.
- **ParsLinux EFI Yolu**: `/boot/efi/parslinux/grubx64.efi` öncelikli algılama desteği.
- **Arch Linux & AUR Desteği**: `PKGBUILD` ve `.SRCINFO` dosyaları eklendi.
- **Bağımsız Paketleyici (`package.sh`)**: Hem Debian hem Arch paketlerini tek komutla derleyen çoklu dağıtım motoru.
- **Yönetim Betikleri**: `manage.sh`, `run.sh`, `stop.sh`, `install.sh`, `uninstall.sh`.
- **Otomatik Test Paketi**: 7 adımlı otomatik birim ve entegrasyon test paketi (`tests/test_boot_repair.py`).
- **Geliştirici Modu**: Canlı olmayan (non-live) geliştirme ortamı desteği (`--dev` / `ALLOW_NON_LIVE=1`).
- **Dokümantasyon Seti**: `docs/` altında mimari, CLI, kurulum, test ve katkı rehberleri.

### Değiştirildi
- Tüm betik ve modül isimleri `pardus-*` -> `parslinux-*` olarak güncellendi.
- Eski komut ve policy isimleri geriye dönük uyumluluk sembolik linkleriyle korundu.
- `AppWindow.ui` ve `Main.py` domain bilgileri `parslinux-boot-repair` olarak güncellendi.

---

## [1.1.0] - Upstream Pardus
- Pardus upstream sürümü.
