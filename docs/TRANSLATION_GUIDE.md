# Pars Linux Boot Repair — Çeviri ve Yerelleştirme Kılavuzu (TRANSLATION_GUIDE.md)

Bu belge, **Pars Linux Boot Repair** uygulamasının çok dilli yapısını (GNU Gettext), `.po` / `.pot` şablonlarını ve projeye yeni bir dil ekleme adımlarını açıklamaktadır.

---

## 🌍 1. Mevcut Desteklenen Diller

- **Türkçe (`tr`)** — Birincil Geliştirme Dili
- **Portekizce (`pt`)** — Uluslararası Topluluk Dili
- **İngilizce (`en`)** — Kod içi referans dili (Varsayılan)

---

## 🛠️ 2. Yeni Bir Dil Ekleme Adımları

Projeye yeni bir dil (örneğin Azerbaycan Türkçesi `az`, İspanyolca `es` veya Almanca `de`) eklemek için:

1. **POT Şablonunu Güncelleyin:**
   ```bash
   ./update-translations.sh
   ```

2. **Yeni PO Dosyasını Oluşturun:**
   ```bash
   cp po/parslinux-boot-repair.pot po/az.po
   ```

3. **Çevirileri Yapın:**
   [Poedit](https://poedit.net/) veya herhangi bir metin düzenleyici ile `po/az.po` dosyasındaki dizgileri çevirin.

4. **Derleyin ve Test Edin:**
   ```bash
   ./update-translations.sh
   ```
   Bu komut otomatik olarak `mo/az.mo` dosyasını derleyecek ve `make install` sırasında `/usr/share/locale/az/LC_MESSAGES/parslinux-boot-repair.mo` konumuna kuracaktır.

---

## 📝 3. Kod İçinde Çevrilebilir Dizgiler

Python dosyalarında gettext kullanımı:
```python
_("We're reinstalling the GRUB boot loader...")
```

Glade / GTK UI XML dosyalarında:
```xml
<property name="label" translatable="yes">Pars Linux Boot Repair</property>
```
