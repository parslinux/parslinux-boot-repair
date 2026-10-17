#!/usr/bin/env python3
"""Pars Linux Boot Repair - setup.py package installation script."""

import os
import subprocess
from setuptools import setup, find_packages

changelog = "debian/changelog"
version = "1.2.0"
if os.path.exists(changelog):
    try:
        head = open(changelog).readline()
        version = head.split("(")[1].split(")")[0]
    except Exception:
        pass

# Ensure src/__version__ exists
os.makedirs("src", exist_ok=True)
with open("src/__version__", "w") as f:
    f.write(version)

# Compile gresource if not already compiled
try:
    subprocess.run([
        "glib-compile-resources",
        "src/data/org.parslinux.boot-repair.gresource.xml",
        "--target=src/data/org.parslinux.boot-repair.gresource"
    ], check=False)
except Exception:
    pass

def create_mo_files():
    podir = "po"
    mo = []
    if not os.path.isdir(podir):
        return mo

    for po in os.listdir(podir):
        if po.endswith(".po"):
            lang = po.split(".po")[0]
            os.makedirs(f"mo/{lang}/LC_MESSAGES", exist_ok=True)
            mo_file = f"mo/{lang}/LC_MESSAGES/parslinux-boot-repair.mo"
            msgfmt_cmd = f"msgfmt {podir}/{po} -o {mo_file}"
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(
                (
                    f"share/locale/{lang}/LC_MESSAGES",
                    [mo_file],
                )
            )
    return mo

data_files = [
    ("share/applications/", ["src/data/org.parslinux.boot-repair.desktop"]),
    ("share/polkit-1/actions/", ["src/data/org.parslinux.pkexec.parslinux-boot-repair.policy"]),
    ("share/icons/hicolor/scalable/apps/", ["src/data/images/parslinux-boot-repair.svg"]),
    ("share/icons/", ["src/data/images/parslinux-boot-repair.svg"]),
    (
        "share/parslinux/parslinux-boot-repair/data",
        [
            "src/data/org.parslinux.boot-repair.gresource",
            "src/data/org.parslinux.boot-repair.desktop",
            "src/data/org.parslinux.pkexec.parslinux-boot-repair.policy",
        ],
    ),
    (
        "share/parslinux/parslinux-boot-repair/data/images",
        ["src/data/images/parslinux-boot-repair.svg"],
    ),
    (
        "share/parslinux/parslinux-boot-repair/data/ui",
        ["src/data/ui/AppWindow.ui"],
    ),
    (
        "share/parslinux/parslinux-boot-repair/src",
        [
            "src/Main.py",
            "src/__version__",
        ],
    ),
] + create_mo_files()

scripts = [
    "parslinux-boot-repair",
    "src/scripts/check-filesystem",
    "src/scripts/dump-info-log",
    "src/scripts/fix-broken-packages",
    "src/scripts/full-upgrade",
    "src/scripts/grub-reinstall",
    "src/scripts/parslinux-chroot",
    "src/scripts/parslinux-mount-rootfs",
    "src/scripts/parslinux-open-luks-lvm",
    "src/scripts/parslinux-reinstall",
    "src/scripts/reset-password",
    "src/scripts/search-operating-system",
]

setup(
    name="parslinux-boot-repair",
    version=version,
    packages=find_packages(),
    scripts=scripts,
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Pars Linux Developers",
    author_email="dev@parslinux.org",
    description="Pars Linux boot and system repair utility.",
    license="GPLv3+",
    keywords="boot repair grub efi uefi chroot pars parslinux",
    url="https://parslinux.org",
)
