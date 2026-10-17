#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — Master Package Builder (Debian / Arch)
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

DIST_DIR="$DIR/dist"
mkdir -p "$DIST_DIR"

show_help() {
    echo -e "${BLUE}${BOLD}Pars Linux Boot Repair — Package Builder${NC}"
    echo "Usage: ./package.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  --deb             Build Debian / Pars Linux (.deb) package"
    echo "  --arch            Build Arch Linux (.pkg.tar.zst) package"
    echo "  --all             Build both Debian and Arch packages"
    echo "  --clean           Clean dist and build cache before build"
    echo ""
}

clean_artifacts() {
    echo -e "${YELLOW}==>${NC} Cleaning previous build artifacts..."
    rm -rf "$DIST_DIR"/* build/ debian/.debhelper/ debian/parslinux-boot-repair/ 2>/dev/null || true
    rm -f debian/debhelper-build-stamp debian/files *.deb *.pkg.tar.* *.tar.gz 2>/dev/null || true
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓ Clean completed.${NC}"
}

build_deb() {
    echo -e "\n${BLUE}▶ Building Debian / Pars Linux (.deb) package...${NC}"
    VERSION=$(sed -n '1s/^[^(]*(\([^)]*\)).*/\1/p' debian/changelog 2>/dev/null || echo "1.2.0")
    
    if command -v dpkg-buildpackage >/dev/null 2>&1; then
        dpkg-buildpackage -us -uc -b
        PARENT_DIR="$(dirname "$DIR")"
        mv "$PARENT_DIR"/parslinux-boot-repair_*.deb "$DIST_DIR/" 2>/dev/null || true
        mv "$PARENT_DIR"/parslinux-boot-repair_*.buildinfo "$DIST_DIR/" 2>/dev/null || true
        mv "$PARENT_DIR"/parslinux-boot-repair_*.changes "$DIST_DIR/" 2>/dev/null || true
    elif command -v dpkg-deb >/dev/null 2>&1; then
        BUILD_ROOT=$(mktemp -d)
        make install DESTDIR="$BUILD_ROOT" PREFIX=/usr
        mkdir -p "$BUILD_ROOT/DEBIAN"
        cp debian/control "$BUILD_ROOT/DEBIAN/control"
        sed -i 's/${misc:Depends}/libc6/' "$BUILD_ROOT/DEBIAN/control"
        echo "Version: $VERSION" >> "$BUILD_ROOT/DEBIAN/control"
        dpkg-deb --build "$BUILD_ROOT" "$DIST_DIR/parslinux-boot-repair_${VERSION}_all.deb"
        rm -rf "$BUILD_ROOT"
    else
        # Standalone ar/tar based .deb packager (cross-distro support on Arch/Fedora)
        echo -e "${YELLOW}Neither dpkg-buildpackage nor dpkg-deb found; using internal ar/tar builder...${NC}"
        BUILD_ROOT=$(mktemp -d)
        PKG_STAGE=$(mktemp -d)
        make install DESTDIR="$BUILD_ROOT" PREFIX=/usr
        
        # 1. debian-binary
        echo "2.0" > "$PKG_STAGE/debian-binary"
        
        # 2. control.tar.gz
        CONTROL_DIR=$(mktemp -d)
        cp debian/control "$CONTROL_DIR/control"
        sed -i 's/${misc:Depends}/libc6/' "$CONTROL_DIR/control"
        echo "Version: $VERSION" >> "$CONTROL_DIR/control"
        tar -czf "$PKG_STAGE/control.tar.gz" -C "$CONTROL_DIR" .
        
        # 3. data.tar.gz
        tar -czf "$PKG_STAGE/data.tar.gz" -C "$BUILD_ROOT" .
        
        # 4. Pack into .deb using ar
        ar -rc "$DIST_DIR/parslinux-boot-repair_${VERSION}_all.deb" \
            "$PKG_STAGE/debian-binary" \
            "$PKG_STAGE/control.tar.gz" \
            "$PKG_STAGE/data.tar.gz"
            
        rm -rf "$BUILD_ROOT" "$PKG_STAGE" "$CONTROL_DIR"
    fi
    echo -e "${GREEN}✓ Debian package created in $DIST_DIR${NC}"
}

build_arch() {
    echo -e "\n${BLUE}▶ Building Arch Linux (.pkg.tar.zst) package...${NC}"
    if ! command -v makepkg >/dev/null 2>&1; then
        echo -e "${RED}✗ Error: 'makepkg' not found!${NC}"
        return 1
    fi
    makepkg -f --nodeps
    mv parslinux-boot-repair-*.pkg.tar.* "$DIST_DIR/" 2>/dev/null || true
    echo -e "${GREEN}✓ Arch package created in $DIST_DIR${NC}"
}

CLEAN_FIRST=0
TARGET_FORMAT="auto"

for arg in "$@"; do
    case "$arg" in
        -h|--help)
            show_help
            exit 0
            ;;
        --clean)
            CLEAN_FIRST=1
            ;;
        --deb)
            TARGET_FORMAT="deb"
            ;;
        --arch)
            TARGET_FORMAT="arch"
            ;;
        --all)
            TARGET_FORMAT="all"
            ;;
    esac
done

if [ "$CLEAN_FIRST" -eq 1 ]; then
    clean_artifacts
    if [ "$TARGET_FORMAT" == "auto" ] && [ $# -eq 1 ]; then
        exit 0
    fi
fi

if [ "$TARGET_FORMAT" == "auto" ]; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID="${ID:-}"
        DISTRO_LIKE="${ID_LIKE:-}"
        if [[ "$DISTRO_ID" == "debian" || "$DISTRO_ID" == "ubuntu" || "$DISTRO_ID" == "parslinux" || "$DISTRO_LIKE" == *"debian"* ]]; then
            TARGET_FORMAT="deb"
        elif [[ "$DISTRO_ID" == "arch" || "$DISTRO_ID" == "cachyos" || "$DISTRO_ID" == "manjaro" || "$DISTRO_LIKE" == *"arch"* ]]; then
            TARGET_FORMAT="arch"
        elif command -v makepkg &>/dev/null; then
            TARGET_FORMAT="arch"
        elif command -v dpkg-deb &>/dev/null; then
            TARGET_FORMAT="deb"
        fi
    fi
fi

# Ensure translation and gresources are compiled
make build

case "$TARGET_FORMAT" in
    deb)
        build_deb
        ;;
    arch)
        build_arch
        ;;
    all)
        build_deb
        build_arch
        ;;
    *)
        build_deb
        ;;
esac

echo -e "\n${GREEN}==>${NC} Packaging complete! Packages generated:"
ls -lh "$DIST_DIR"
