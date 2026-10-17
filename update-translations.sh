#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "Updating translation template (POT)..."
xgettext -o po/parslinux-boot-repair.pot \
    --from-code=utf-8 \
    --package-name="parslinux-boot-repair" \
    --package-version="1.2.0" \
    --msgid-bugs-address="https://parslinux.org" \
    src/data/ui/*.ui src/*.py

cp po/parslinux-boot-repair.pot po/pardus-boot-repair.pot

for po_file in po/*.po; do
    [ -f "$po_file" ] || continue
    lang=$(basename "$po_file" .po)
    echo "Merging $po_file..."
    msgmerge --update --backup=none "$po_file" po/parslinux-boot-repair.pot
done

echo "Compiling MO files..."
mkdir -p mo
for po_file in po/*.po; do
    [ -f "$po_file" ] || continue
    lang=$(basename "$po_file" .po)
    msgfmt -o "mo/$lang.mo" "$po_file"
    echo "Generated mo/$lang.mo"
done

echo "Translations updated successfully!"
