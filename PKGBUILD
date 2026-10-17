# Maintainer: Pars Linux Developers <dev@parslinux.org>
pkgname=parslinux-boot-repair
pkgver=1.2.0
pkgrel=1
pkgdesc="Pars Linux Boot and System Repair utility (GRUB, EFI, Chroot, Password Reset)"
arch=('any')
url="https://parslinux.org"
license=('GPL-3.0-or-later')
provides=('pardus-boot-repair')
conflicts=('pardus-boot-repair')
replaces=('pardus-boot-repair')
depends=(
    'python'
    'python-gobject'
    'gtk3'
    'libhandy'
    'vte3'
    'polkit'
    'efibootmgr'
    'dosfstools'
    'e2fsprogs'
    'btrfs-progs'
    'cryptsetup'
    'lvm2'
    'zip'
)
makedepends=(
    'python-setuptools'
    'gettext'
    'glib2'
)

build() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    make build
}

package() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    make install DESTDIR="$pkgdir" PREFIX=/usr
}
