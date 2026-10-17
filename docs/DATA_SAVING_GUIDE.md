# Pars Linux Boot Repair — Veri Güvenliği ve Sistem Koruma Kılavuzu (DATA_SAVING_GUIDE.md)

Bu kılavuz, **Pars Linux Boot Repair** uygulamasının disk ve önyükleme onarımları sırasında kullanıcı verilerini korumak, yanlış bölüm üzerine yazımları önlemek ve sistem bütünlüğünü güvenceye almak için izlediği güvenlik ilkelerini açıklar.

---

## 1. Veri Güvenliğini Sağlayan Temel Koruma Katmanları

Önyükleme onarımları, disk bölümlerinin yeniden yapılandırılmasını ve MBR/EFI sektörlerine doğrudan yazmayı gerektirir. Pars Linux Boot Repair bu süreçte veri kaybını engellemek için çok kademeli koruma uygular:

```
[İşlem Seçimi (GRUB, Parola, fsck, vb.)]
                    │
                    ▼
[1. Aşama] Salt-Okunur Algılama (search-operating-system)
           Geçici bağlamalar 'ro' (salt-okunur) modunda yapılır.
                    │ (Başarılı)
                    ▼
[2. Aşama] Açık Kullanıcı Onayı (Adw.MessageDialog)
           Geri döndürülemez disk yazımları öncesinde açık uyarı ve onay.
                    │ (Kullanıcı Onayı)
                    ▼
[3. Aşama] EFI Koruma ve Yedekleme (grub-reinstall)
           Mevcut Windows bootmgfw.efi silinmez; bootmgfw-winzort.efi
           adıyla güvenli bir şekilde yedeklenir.
                    │ (Yazma Tamamlandı)
                    ▼
[4. Aşama] Temiz Çözme ve Senkronizasyon (sync & umount -lf)
           Tüm API bağlamaları (dev, proc, sys) ve rootfs güvenle ayrılır.
```

---

## 2. Windows & Dual-Boot Sistemlerin Korunması

Pars Linux Boot Repair, çift işletim sistemli (Dual-Boot) bilgisayarlarda Windows önyükleyicisini ezmez:
- Anakart UEFI firmware'inin Windows'a kilitlendiği sistemlerde, orijinal `bootmgfw.efi` dosyası `bootmgfw-winzort.efi` olarak saklanır.
- Ardından GRUB `os-prober` çalıştırılarak Windows girdisi ParsLinux GRUB menüsüne otomatik dahil edilir.

---

## 3. LUKS & LVM2 Şifreleme Güvenliği

- LUKS şifreli bölümler yalnızca kullanıcı şifresini girdiğinde bellekte açılır.
- Şifreleme anahtarları asla diske veya günlük dosyalarına yazılmaz.
- İşlem tamamlandığında veya hata anında açılan mapper aygıtı kapatılır.

---

## 4. Kullanıcı Verilerinin Sıfırlanması (`reset-config`)

- Kullanıcı ayarları sıfırlanırken kullanıcının `/home/$USER/` altındaki kişisel dosyaları (Belgeler, İndirilenler, Masaüstü, Resimler, Videolar) **kesinlikle silinmez**.
- Yalnızca masaüstü masaüstü ortamı önbellek ve yapılandırma dizinleri (`.cache`, `.config`, `.local/share`) sıfırlanır.
