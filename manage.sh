#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — Master Management Automation Script
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

show_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "=========================================================="
    echo "  Pars Linux Boot Repair — Master Management Utility      "
    echo "=========================================================="
    echo -e "${NC}"
}

show_help() {
    show_banner
    echo "Usage: ./manage.sh <COMMAND> [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  run               Launch application (root elevation via pkexec)"
    echo "  dev               Launch application directly without root elevation"
    echo "  test              Run unit and verification test suite"
    echo "  compile           Compile GResource and locale MO translation files"
    echo "  translations      Update POT template and merge/compile translations"
    echo "  package           Build distribution packages (.deb / .pkg.tar.zst)"
    echo "  install           Install to system with sudo (/usr)"
    echo "  uninstall         Remove from system (/usr)"
    echo "  clean             Clean build artifacts, cache, and compiled assets"
    echo "  status            Check system tools and dependencies status"
    echo "  help              Show this help menu"
    echo ""
}

check_status() {
    show_banner
    echo -e "${BLUE}Checking system dependencies for Pars Linux Boot Repair:${NC}"
    echo ""
    deps=(
        "python3"
        "glib-compile-resources"
        "msgfmt"
        "xgettext"
        "pkexec"
        "grub-install"
        "efibootmgr"
        "btrfs"
        "cryptsetup"
        "lvm"
        "fsck.ext4"
    )
    for tool in "${deps[@]}"; do
        if command -v "$tool" >/dev/null 2>&1; then
            echo -e "  [${GREEN}FOUND${NC}] $tool ($(which $tool))"
        else
            echo -e "  [${YELLOW}MISSING${NC}] $tool (optional/runtime only)"
        fi
    done
    echo ""
}

COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
    run)
        ./run.sh "$@"
        ;;
    dev)
        ./run.sh --dev "$@"
        ;;
    test)
        ./run.sh --test "$@"
        ;;
    compile)
        ./run.sh --compile
        ;;
    translations|pot)
        ./update-translations.sh
        ;;
    package)
        ./package.sh "$@"
        ;;
    install)
        sudo ./install.sh "$@"
        ;;
    uninstall)
        sudo ./uninstall.sh "$@"
        ;;
    stop)
        ./stop.sh
        ;;
    clean)
        make clean
        rm -rf dist build *.egg-info
        echo -e "${GREEN}Clean completed.${NC}"
        ;;
    status)
        check_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        show_help
        exit 1
        ;;
esac
