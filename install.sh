#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — System Installation Script
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

echo -e "${BLUE}==>${NC} Installing Pars Linux Boot Repair into ${DESTDIR}${PREFIX}..."

make install PREFIX="$PREFIX" DESTDIR="$DESTDIR"

# Update system caches if on live root
if [ "$DESTDIR" = "/" ]; then
    echo -e "${BLUE}==>${NC} Updating desktop database and icon caches..."
    update-desktop-database -q 2>/dev/null || true
    gtk-update-icon-cache -q -t -f "${PREFIX}/share/icons/hicolor" 2>/dev/null || true
fi

echo -e "${GREEN}==>${NC} Installation completed successfully!"
echo "Run 'parslinux-boot-repair' from terminal or launch from Applications menu."
