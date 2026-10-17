#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — Local Development & Execution Script (run.sh)
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

show_help() {
    echo -e "${BLUE}${BOLD}Pars Linux Boot Repair — Local Development Runner${NC}"
    echo "Usage: ./run.sh [OPTIONS] [ARGS...]"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message and exit"
    echo "  -t, --test        Run the automated test suite"
    echo "  --root            Elevate with pkexec/sudo (System Administrator mode)"
    echo "  --gtk3            Force legacy GTK3 + Libhandy interface"
    echo "  --gtk4            Run modern GTK4 + Libadwaita interface (Default)"
    echo "  -c, --compile     Compile GResource and locale MO files only"
    echo ""
}

compile_assets() {
    echo -e "${BLUE}==>${NC} Compiling GResource..."
    (cd src/data && glib-compile-resources org.parslinux.boot-repair.gresource.xml --target=org.parslinux.boot-repair.gresource)
    cp -f src/data/org.parslinux.boot-repair.gresource src/data/tr.org.pardus.boot-repair.gresource 2>/dev/null || true

    echo -e "${BLUE}==>${NC} Generating version stamp..."
    if [ -f debian/changelog ]; then
        sed -n '1s/^[^(]*(\([^)]*\)).*/\1/p' debian/changelog > src/__version__
    else
        echo "1.2.0" > src/__version__
    fi

    if [ -d po ] && [ -x ./update-translations.sh ]; then
        echo -e "${BLUE}==>${NC} Ensuring translation MO files..."
        mkdir -p mo
        for po_file in po/*.po; do
            [ -f "$po_file" ] || continue
            lang=$(basename "$po_file" .po)
            msgfmt -o "mo/$lang.mo" "$po_file" 2>/dev/null || true
        done
    fi
}

RUN_TEST=0
COMPILE_ONLY=0
USE_ROOT=0
UI_MODE="gtk4"
EXTRA_ARGS=()

for arg in "$@"; do
    case "$arg" in
        -h|--help)
            show_help
            exit 0
            ;;
        -t|--test)
            RUN_TEST=1
            ;;
        --root)
            USE_ROOT=1
            ;;
        --gtk3)
            UI_MODE="gtk3"
            ;;
        --gtk4)
            UI_MODE="gtk4"
            ;;
        -c|--compile)
            COMPILE_ONLY=1
            ;;
        *)
            EXTRA_ARGS+=("$arg")
            ;;
    esac
done

compile_assets

if [ "$COMPILE_ONLY" -eq 1 ]; then
    echo -e "${GREEN}✓ Assets compiled successfully.${NC}"
    exit 0
fi

if [ "$RUN_TEST" -eq 1 ]; then
    echo -e "${YELLOW}==>${NC} Running test suite..."
    exec python3 -m unittest discover -s tests -v
fi

export PATH="$DIR/src/scripts:$PATH"
export PYTHONPATH="$DIR/src:$PYTHONPATH"

# Allow root on local display if running with elevation
if [ "$USE_ROOT" -eq 1 ]; then
    if [ -n "$DISPLAY" ] && command -v xhost >/dev/null 2>&1; then
        xhost +si:localuser:root >/dev/null 2>&1 || true
    fi
    echo -e "${GREEN}==>${NC} Starting Pars Linux Boot Repair (Root Mode)..."
    exec ./parslinux-boot-repair "--$UI_MODE" "${EXTRA_ARGS[@]}"
else
    # Default: Run directly in user session for seamless development & preview
    export NO_PKEXEC=1
    if [ "$UI_MODE" == "gtk3" ]; then
        echo -e "${GREEN}==>${NC} Starting Pars Linux Boot Repair (GTK 3 Mode)..."
        exec python3 src/Main.py "${EXTRA_ARGS[@]}"
    else
        echo -e "${GREEN}==>${NC} Starting Pars Linux Boot Repair (GTK 4 / Libadwaita Mode)..."
        exec python3 src/MainGtk4.py "${EXTRA_ARGS[@]}"
    fi
fi
