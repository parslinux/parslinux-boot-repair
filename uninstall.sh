#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — System Uninstallation Script
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: Root privileges required. Please run with sudo.${NC}"
    exit 1
fi

PREFIX="${PREFIX:-/usr}"
DESTDIR="${DESTDIR:-/}"

echo -e "${BLUE}==>${NC} Removing Pars Linux Boot Repair from ${DESTDIR}${PREFIX}..."

rm -f "${DESTDIR}${PREFIX}/bin/parslinux-boot-repair"
rm -f "${DESTDIR}${PREFIX}/bin/pardus-boot-repair"
rm -f "${DESTDIR}${PREFIX}/bin/check-filesystem"
rm -f "${DESTDIR}${PREFIX}/bin/dump-info-log"
rm -f "${DESTDIR}${PREFIX}/bin/fix-broken-packages"
rm -f "${DESTDIR}${PREFIX}/bin/full-upgrade"
rm -f "${DESTDIR}${PREFIX}/bin/grub-reinstall"
rm -f "${DESTDIR}${PREFIX}/bin/parslinux-chroot"
rm -f "${DESTDIR}${PREFIX}/bin/pardus-chroot"
rm -f "${DESTDIR}${PREFIX}/bin/parslinux-mount-rootfs"
rm -f "${DESTDIR}${PREFIX}/bin/pardus-mount-rootfs"
rm -f "${DESTDIR}${PREFIX}/bin/parslinux-open-luks-lvm"
rm -f "${DESTDIR}${PREFIX}/bin/pardus-open-luks-lvm"
rm -f "${DESTDIR}${PREFIX}/bin/parslinux-reinstall"
rm -f "${DESTDIR}${PREFIX}/bin/pardus-reinstall"
rm -f "${DESTDIR}${PREFIX}/bin/reset-password"
rm -f "${DESTDIR}${PREFIX}/bin/search-operating-system"

rm -rf "${DESTDIR}${PREFIX}/share/parslinux/parslinux-boot-repair"
rm -rf "${DESTDIR}${PREFIX}/share/pardus/pardus-boot-repair"

rm -f "${DESTDIR}${PREFIX}/share/applications/org.parslinux.boot-repair.desktop"
rm -f "${DESTDIR}${PREFIX}/share/applications/tr.org.pardus-boot-repair.desktop"
rm -f "${DESTDIR}${PREFIX}/share/applications/tr.org.parslinux.boot-repair.desktop"

rm -f "${DESTDIR}${PREFIX}/share/polkit-1/actions/org.parslinux.pkexec.parslinux-boot-repair.policy"
rm -f "${DESTDIR}${PREFIX}/share/polkit-1/actions/tr.org.pardus-boot-repair.policy"

rm -f "${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps/parslinux-boot-repair.svg"
rm -f "${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps/pardus-boot-repair.svg"
rm -f "${DESTDIR}${PREFIX}/share/icons/parslinux-boot-repair.svg"
rm -f "${DESTDIR}${PREFIX}/share/icons/pardus-boot-repair.svg"

for lang in tr pt; do
    rm -f "${DESTDIR}${PREFIX}/share/locale/${lang}/LC_MESSAGES/parslinux-boot-repair.mo"
    rm -f "${DESTDIR}${PREFIX}/share/locale/${lang}/LC_MESSAGES/pardus-boot-repair.mo"
done

if [ "$DESTDIR" = "/" ]; then
    update-desktop-database -q 2>/dev/null || true
    gtk-update-icon-cache -q -t -f "${PREFIX}/share/icons/hicolor" 2>/dev/null || true
fi

echo -e "${GREEN}==>${NC} Uninstallation complete."
