# Pars Linux Boot Repair — Sürüm Yönetim Politikası (VERSION.md)

Bu belge, **Pars Linux Boot Repair** projesinin sürümleme politikasını ve sürüm bilgilerinin kod tabanındaki merkezi eşzamanlama noktalarını tanımlar.

---

## 📌 1. Semantik Sürümleme (SemVer 2.0.0)

Projede `MAJOR.MINOR.PATCH` formatı izlenir:

- **MAJOR (Ana Sürüm):** Geriye dönük uyumsuz köklü mimari değişimler veya büyük sürüm atlamaları (Örn: GTK4 geçişi, `1.x` -> `2.x`).
- **MINOR (Alt Sürüm):** Geriye dönük uyumlu yeni özellikler (Örn: BTRFS subvol desteği, yeni dosya sistemi motoru, `1.1.0` -> `1.2.0`).
- **PATCH (Yama Sürümü):** Geriye dönük uyumlu hata düzeltmeleri ve güvenlik yamaları (`1.2.0` -> `1.2.1`).

---

## 📍 2. Geçerli Sürüm Bilgisi

- **Mevcut Sürüm:** `1.2.0-parslinux1`
- **Yayın Tarihi:** 17 Ekim 2026
- **Kod Adı:** *Leopar Kurtarıcı (Pars Leopard Boot Rescuer)*

---

## 🔄 3. Sürüm Senkronizasyon Noktaları

Sürüm numarası güncellendiğinde aşağıdaki dosyalar eşzamanlı güncellenir:

1. **`debian/changelog`**: İlk satırda `parslinux-boot-repair (X.Y.Z-parslinux1) unstable; urgency=medium`
2. **`PKGBUILD`**: `pkgver=X.Y.Z`
3. **`.SRCINFO`**: `pkgver = X.Y.Z`
4. **`setup.py`**: `version="X.Y.Z"`
5. **`src/__version__`**: `X.Y.Z`
6. **`src/MainGtk4.py` / `src/Main.py`**: `APPVERSION = "X.Y.Z"`
7. **`docs/CHANGELOG.md`**: Yeni sürüm girdisi
