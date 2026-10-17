#!/usr/bin/env python3
"""Pars Linux Boot Repair - Comprehensive Automated Test Suite."""

import os
import sys
import unittest
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from importlib.machinery import SourceFileLoader

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
SCRIPTS_DIR = os.path.join(SRC_DIR, "scripts")
DATA_DIR = os.path.join(SRC_DIR, "data")


class TestParsLinuxBootRepair(unittest.TestCase):
    def test_python_syntax(self):
        """Ensure all Python scripts and modules compile without syntax errors."""
        python_files = [
            os.path.join(SRC_DIR, "Main.py"),
            os.path.join(SRC_DIR, "MainGtk4.py"),
            os.path.join(SCRIPTS_DIR, "parslinux-mount-rootfs"),
            os.path.join(SCRIPTS_DIR, "reset-password"),
            os.path.join(SCRIPTS_DIR, "search-operating-system"),
            os.path.join(ROOT_DIR, "setup.py"),
        ]
        for py_path in python_files:
            if os.path.exists(py_path):
                res = subprocess.run(
                    [sys.executable, "-m", "py_compile", py_path],
                    capture_output=True,
                    text=True
                )
                self.assertEqual(res.returncode, 0, f"Syntax error in {py_path}: {res.stderr}")

    def test_bash_syntax(self):
        """Ensure all Bash scripts pass bash -n validation."""
        bash_scripts = [
            os.path.join(ROOT_DIR, "parslinux-boot-repair"),
            os.path.join(SCRIPTS_DIR, "check-filesystem"),
            os.path.join(SCRIPTS_DIR, "dump-info-log"),
            os.path.join(SCRIPTS_DIR, "fix-broken-packages"),
            os.path.join(SCRIPTS_DIR, "full-upgrade"),
            os.path.join(SCRIPTS_DIR, "grub-reinstall"),
            os.path.join(SCRIPTS_DIR, "parslinux-chroot"),
            os.path.join(SCRIPTS_DIR, "parslinux-open-luks-lvm"),
            os.path.join(SCRIPTS_DIR, "parslinux-reinstall"),
            os.path.join(ROOT_DIR, "run.sh"),
            os.path.join(ROOT_DIR, "stop.sh"),
            os.path.join(ROOT_DIR, "install.sh"),
            os.path.join(ROOT_DIR, "uninstall.sh"),
            os.path.join(ROOT_DIR, "package.sh"),
            os.path.join(ROOT_DIR, "manage.sh"),
            os.path.join(ROOT_DIR, "update-translations.sh"),
        ]
        for script in bash_scripts:
            if os.path.exists(script) and not os.path.islink(script):
                res = subprocess.run(["bash", "-n", script], capture_output=True, text=True)
                self.assertEqual(res.returncode, 0, f"Bash syntax error in {script}: {res.stderr}")

    def test_scripts_executable(self):
        """Ensure critical scripts have executable permissions."""
        scripts = [
            os.path.join(ROOT_DIR, "parslinux-boot-repair"),
            os.path.join(ROOT_DIR, "run.sh"),
            os.path.join(ROOT_DIR, "manage.sh"),
            os.path.join(SCRIPTS_DIR, "parslinux-chroot"),
            os.path.join(SCRIPTS_DIR, "parslinux-mount-rootfs"),
            os.path.join(SCRIPTS_DIR, "parslinux-reinstall"),
            os.path.join(SCRIPTS_DIR, "grub-reinstall"),
        ]
        for s in scripts:
            self.assertTrue(os.access(s, os.X_OK), f"Script {s} is not executable!")

    def test_polkit_policy_xml(self):
        """Validate PolicyKit XML structure."""
        policy_file = os.path.join(DATA_DIR, "org.parslinux.pkexec.parslinux-boot-repair.policy")
        self.assertTrue(os.path.exists(policy_file), "Policy file missing")
        tree = ET.parse(policy_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "policyconfig")
        actions = root.findall("action")
        self.assertGreater(len(actions), 0, "No actions defined in policy file")
        action_ids = [a.get("id") for a in actions]
        self.assertIn("org.parslinux.boot-repair", action_ids)

    def test_gresource_xml(self):
        """Validate GResource XML configuration."""
        gres_xml = os.path.join(DATA_DIR, "org.parslinux.boot-repair.gresource.xml")
        self.assertTrue(os.path.exists(gres_xml), "GResource XML missing")
        tree = ET.parse(gres_xml)
        root = tree.getroot()
        self.assertEqual(root.tag, "gresources")
        prefixes = [g.get("prefix") for g in root.findall("gresource")]
        self.assertIn("/org/parslinux/boot-repair", prefixes)

    def test_gtk4_ui_xml(self):
        """Validate GTK4 AppWindowGtk4.ui XML structure."""
        ui_file = os.path.join(DATA_DIR, "ui", "AppWindowGtk4.ui")
        self.assertTrue(os.path.exists(ui_file), "AppWindowGtk4.ui missing")
        tree = ET.parse(ui_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "interface")
        window = root.find(".//object[@id='window_main']")
        self.assertIsNotNone(window)
        self.assertEqual(window.get("class"), "AdwApplicationWindow")

    def test_desktop_file_contents(self):
        """Ensure desktop entry contains valid metadata."""
        desktop_file = os.path.join(DATA_DIR, "org.parslinux.boot-repair.desktop")
        self.assertTrue(os.path.exists(desktop_file), "Desktop file missing")
        with open(desktop_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Name=Pars Linux Boot Repair", content)
        self.assertIn("Exec=parslinux-boot-repair", content)
        self.assertIn("Icon=parslinux-boot-repair", content)
        self.assertIn("StartupWMClass=org.parslinux.boot-repair", content)

    def test_os_detection_logic(self):
        """Simulate operating system detection logic on mock directories."""
        search_os_path = os.path.join(SCRIPTS_DIR, "search-operating-system")
        mod = SourceFileLoader("search_os", search_os_path).load_module()

        with tempfile.TemporaryDirectory() as tmp:
            # 1. ParsLinux EFI test
            efi_dir = os.path.join(tmp, "EFI", "parslinux")
            os.makedirs(efi_dir, exist_ok=True)
            with open(os.path.join(efi_dir, "grubx64.efi"), "w") as f:
                f.write("mock")
            self.assertEqual(mod.detect_os(tmp), "ParsLinux (EFI)")

            # 2. Linux os-release test
            etc_dir = os.path.join(tmp, "etc")
            os.makedirs(etc_dir, exist_ok=True)
            with open(os.path.join(etc_dir, "os-release"), "w") as f:
                f.write('NAME="ParsLinux GNU/Linux"\nVERSION="1.0"\n')
            self.assertEqual(mod.detect_os(tmp), "ParsLinux GNU/Linux")

            # 3. Windows detection test
            os.remove(os.path.join(etc_dir, "os-release"))
            os.remove(os.path.join(efi_dir, "grubx64.efi"))
            win_dir = os.path.join(tmp, "Windows", "System32")
            os.makedirs(win_dir, exist_ok=True)
            with open(os.path.join(win_dir, "ntoskrnl.exe"), "w") as f:
                f.write("mock")
            self.assertEqual(mod.detect_os(tmp), "Windows")


if __name__ == "__main__":
    unittest.main()
