#!/usr/bin/make -f
DESTDIR ?= /
PREFIX ?= /usr
BIN_DIR := $(DESTDIR)$(PREFIX)/bin
SHARE_DIR := $(DESTDIR)$(PREFIX)/share/parslinux/parslinux-boot-repair
ICON_DIR := $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps
LEGACY_ICON_DIR := $(DESTDIR)$(PREFIX)/share/icons
POLKIT_DIR := $(DESTDIR)$(PREFIX)/share/polkit-1/actions
LOCALE_DIR := $(DESTDIR)$(PREFIX)/share/locale
DESKTOP_DIR := $(DESTDIR)$(PREFIX)/share/applications

.PHONY: all build install buildmo pot gresource version clean run test

all: build

install: gresource version buildmo
	install -d $(BIN_DIR)
	install -m 755 parslinux-boot-repair $(BIN_DIR)/parslinux-boot-repair
	find src/scripts -maxdepth 1 -type f -exec install -m 755 {} $(BIN_DIR)/ \;
	@for link in $$(find src/scripts -maxdepth 1 -type l); do \
		cp -P $$link $(BIN_DIR)/; \
	done
	
	install -d $(SHARE_DIR)
	find src -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cp -a src/* $(SHARE_DIR)/
	find $(SHARE_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find $(SHARE_DIR) -type f -name "*.pyc" -delete 2>/dev/null || true
	
	install -d $(ICON_DIR)
	install -m 644 src/data/images/parslinux-boot-repair.svg $(ICON_DIR)/parslinux-boot-repair.svg
	install -d $(LEGACY_ICON_DIR)
	install -m 644 src/data/images/parslinux-boot-repair.svg $(LEGACY_ICON_DIR)/parslinux-boot-repair.svg
	
	install -d $(POLKIT_DIR)
	install -m 644 src/data/org.parslinux.pkexec.parslinux-boot-repair.policy $(POLKIT_DIR)/org.parslinux.pkexec.parslinux-boot-repair.policy
	
	install -d $(DESKTOP_DIR)
	install -m 644 src/data/org.parslinux.boot-repair.desktop $(DESKTOP_DIR)/org.parslinux.boot-repair.desktop
	ln -sf org.parslinux.boot-repair.desktop $(DESKTOP_DIR)/tr.org.parslinux.boot-repair.desktop

	@for file in $(wildcard po/*.po); do \
		lang=$$(basename $$file .po); \
		install -d $(LOCALE_DIR)/$$lang/LC_MESSAGES/; \
		install -m 644 mo/$$lang.mo $(LOCALE_DIR)/$$lang/LC_MESSAGES/parslinux-boot-repair.mo; \
	done

build: gresource buildmo version

gresource:
	(cd src/data && glib-compile-resources org.parslinux.boot-repair.gresource.xml --target=org.parslinux.boot-repair.gresource)

buildmo:
	@echo "Building .mo files..."
	install -d mo
	@for file in $(wildcard po/*.po); do \
		lang=$$(basename $$file .po); \
		msgfmt -o mo/$$lang.mo $$file; \
	done

version:
	@if [ -f debian/changelog ]; then \
		sed -n '1s/^[^(]*(\([^)]*\)).*/\1/p' debian/changelog > src/__version__; \
	else \
		echo "1.2.0" > src/__version__; \
	fi

pot:
	./update-translations.sh

clean:
	rm -f src/data/*.gresource src/__version__
	rm -rf mo
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run: gresource version
	python3 src/Main.py

test:
	python3 -m unittest discover -s tests -v
