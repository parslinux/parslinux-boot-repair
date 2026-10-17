#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — Local Development & Execution Script
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

show_help() {
    echo -e "${BLUE}Pars Linux Boot Repair — Development Runner${NC}"
    echo "Usage: ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message and exit"
    echo "  -t, --test        Run the automated test suite"
    echo "  -d, --dev         Run directly without Polkit pkexec escalation"
    echo "  -c, --compile     Compile GResource and locale MO files only"
    echo "  -v, --verbose     Verbose output"
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

RUN_DEV=0
RUN_TEST=0
COMPILE_ONLY=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -t|--test)
            RUN_TEST=1
            shift
            ;;
        -d|--dev|--no-root)
            RUN_DEV=1
            shift
            ;;
        -c|--compile)
            COMPILE_ONLY=1
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

compile_assets

if [ "$COMPILE_ONLY" -eq 1 ]; then
    echo -e "${GREEN}Assets compiled successfully.${NC}"
    exit 0
fi

if [ "$RUN_TEST" -eq 1 ]; then
    echo -e "${YELLOW}==>${NC} Running test suite..."
    python3 -m unittest discover -s tests -v
    exit 0
fi

echo -e "${GREEN}==>${NC} Starting Pars Linux Boot Repair..."
export PATH="$DIR/src/scripts:$PATH"
export PYTHONPATH="$DIR/src:$PYTHONPATH"

if [ "$RUN_DEV" -eq 1 ]; then
    export NO_PKEXEC=1
    python3 src/Main.py "$@"
else
    ./parslinux-boot-repair "$@"
fi
