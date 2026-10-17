# Pars Linux Projesine Katkıda Bulunma Rehberi

Pars Linux Boot Repair projesine katkıda bulunmak istediğiniz için teşekkür ederiz!

## 🛠️ Geliştirme Ortamı

Projeyi yerel ortamınızda çalıştırmak için:

```bash
git clone https://github.com/parslinux/parslinux-boot-repair.git
cd parslinux-boot-repair

# Gerekli bağımlılıkları derleyin ve yerel modda çalıştırın:
./manage.sh dev

# Testleri çalıştırın:
./manage.sh test
```

## 📝 Kodlama Standartları

1. **Python**: PEP 8 kurallarına uyun.
2. **Bash**: Betiklerin başına `set -e` veya güvenli hata yönetimi ekleyin. `bash -n` ile doğrulayın.
3. **i18n**: Yeni eklenen kullanıcı arayüzü metinlerini `_("...")` ile sarmalayın ve `./update-translations.sh` çalıştırın.
4. **Git Commit**: Açık, anlaşılır ve konvansiyonel commit mesajları kullanın (örn: `feat: add btrfs subvol repair`, `fix: handle nvme partitions in os detector`).

## 🧪 Çekme İstekleri (Pull Requests)

PR göndermeden önce mutlaka `./manage.sh test` komutunun hatasız tamamlandığından emin olun.
