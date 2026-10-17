# 🧪 Pars Linux Boot Repair — Test Kılavuzu

Bu belge, **`parslinux-boot-repair`** projesinde uygulanan test stratejisini ve testlerin nasıl koşturulacağını açıklamaktadır.

---

## 1. Otomatik Test Paketi (`tests/test_boot_repair.py`)

Projede 7 farklı güvenlik ve entegrasyon birim testi bulunmaktadır:

1. **`test_python_syntax`**: Tüm Python modülleri ve betiklerinin (`Main.py`, `search-operating-system`, `parslinux-mount-rootfs`, `reset-password`, `setup.py`) `py_compile` ile sözdizimi denetimi.
2. **`test_bash_syntax`**: Tüm kabuk betiklerinin (`check-filesystem`, `grub-reinstall`, `parslinux-chroot`, `run.sh`, `package.sh` vb.) `bash -n` ile doğruluk denetimi.
3. **`test_scripts_executable`**: Çekirdek betiklerin çalıştırılabilir (`chmod +x`) izinlerinin kontrolü.
4. **`test_polkit_policy_xml`**: PolicyKit XML şemasının geçerliliği ve `org.parslinux.boot-repair` kuralının doğrulanması.
5. **`test_gresource_xml`**: GResource XML dosyasının geçerliliği ve `/org/parslinux/boot-repair` önek tanımları.
6. **`test_desktop_file_contents`**: XDG Desktop girdisinin geçerli anahtar-değer çiftlerine ve yürütülebilir binary eşleşmesine sahip olması.
7. **`test_os_detection_logic`**: Geçici mock dizinler açılarak (`/tmp/`) ParsLinux EFI, generic Linux `os-release` ve Windows önyükleyici algılama motorunun simülasyonu.

---

## 2. Testleri Koşturma

```bash
# Yönetim betiği ile:
./manage.sh test

# veya run betiği ile:
./run.sh --test

# veya doğrudan Python unittest modülü ile:
python3 -m unittest discover -s tests -v
```

---

## 3. Canlı Sistemde (Live USB) Manuel Test Adımları

1. ParsLinux Canlı USB üzerinden sistemi başlatın.
2. Uygulamayı menüden veya terminalden açın: `parslinux-boot-repair`.
3. Bilgisayara takılı disklerin başarıyla listelendiğini teyit edin.
4. **Gelişmiş Seçenekler** sekmesine geçerek:
   - GRUB yeniden kurulumunu test edin.
   - Dosya sistemi denetimini (fsck) başlatın ve canlı VTE terminal penceresinde çıktıları gözlemleyin.
   - Parola sıfırlama adımlarını doğrulayın.
