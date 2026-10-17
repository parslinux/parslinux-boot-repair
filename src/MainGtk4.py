#!/usr/bin/env python3
"""Pars Linux Boot Repair — Modern GTK 4 & Libadwaita Implementation."""

import sys
import os
import re
import gi
import subprocess
import gettext
import shutil

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib, Vte

APP_DIR = os.path.dirname(os.path.realpath(__file__))

# Prioritize local scripts directory in PATH
scripts_dir = os.path.join(APP_DIR, "scripts")
if os.path.isdir(scripts_dir):
    os.environ["PATH"] = f"{scripts_dir}:{os.environ.get('PATH', '')}"

import importlib.util
from importlib.machinery import SourceFileLoader
search_os_path = os.path.join(APP_DIR, "scripts/search-operating-system")
if not os.path.exists(search_os_path):
    search_os_path = shutil.which("parslinux-search-operating-system") or shutil.which("search-operating-system") or "/usr/bin/search-operating-system"

try:
    loader = SourceFileLoader("search_operating_systems", search_os_path)
    spec = importlib.util.spec_from_loader("search_operating_systems", loader)
    if spec:
        search_operating_system = importlib.util.module_from_spec(spec)
        loader.exec_module(search_operating_system)
    else:
        raise ImportError("Could not load spec for search-operating-system")
except Exception:
    class DummyOS:
        def search_operating_system(self):
            return []
    search_operating_system = DummyOS()

try:
    gettext.install("parslinux-boot-repair", "/usr/share/locale/")
except Exception:
    pass

APPVERSION = "1.2.0"
try:
    with open(os.path.join(APP_DIR, "__version__"), encoding="utf-8") as version_file:
        APPVERSION = version_file.readline().strip() or APPVERSION
except OSError:
    pass

gresource_candidates = [
    os.path.join(APP_DIR, "data/org.parslinux.boot-repair.gresource"),
    "/usr/share/parslinux/parslinux-boot-repair/data/org.parslinux.boot-repair.gresource",
]
for gres in gresource_candidates:
    if os.path.exists(gres):
        try:
            resource = Gio.resource_load(gres)
            Gio.Resource._register(resource)
            break
        except Exception:
            pass


class ApplicationGtk4(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.parslinux.boot-repair",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )
        GLib.set_prgname("parslinux-boot-repair")
        self.builder = None
        self.window = None

    def do_activate(self):
        if not self.window:
            self.build_ui()
        self.window.present()

    def build_ui(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_resource("/org/parslinux/boot-repair/ui/AppWindowGtk4.ui")

        self.window = self.builder.get_object("window_main")
        self.window.set_application(self)
        self.deck = self.builder.get_object("deck_main")

        # pages
        self.page_main = self.builder.get_object("box_page_main")
        self.page_questions = self.builder.get_object("box_page_questions")
        self.page_advanced = self.builder.get_object("box_page_advanced")
        self.page_loading = self.builder.get_object("box_page_loading")

        # questions page
        self.carousel_questions = self.builder.get_object("carousel_questions")
        self.button_questions_mainpage = self.builder.get_object("button_mainpage1")
        self.button_questions_continue = self.builder.get_object("button_questions_continue")
        self.titlebar_page_questions = self.builder.get_object("titlebar_page_questions")

        # loading page
        self.btn_go_mainpage = self.builder.get_object("button_loading_to_mainpage")
        self.btn_close_logs = self.builder.get_object("button_close_logs")
        self.btn_show_log = self.builder.get_object("button_show_log")
        self.btn_copy_logs = self.builder.get_object("button_copy_logs")
        self.status_page = self.builder.get_object("page_status")
        self.spinner_loading = self.builder.get_object("spinner_page_loading")
        self.box_vte = self.builder.get_object("box_vte")

        # Vte Terminal (GTK4 Vte 3.91)
        self.vte_terminal = Vte.Terminal()
        self.vte_terminal.set_hexpand(True)
        self.vte_terminal.set_vexpand(True)
        self.box_vte.append(self.vte_terminal)

        # Connect signals
        btn_about = self.builder.get_object("button_about")
        if btn_about:
            btn_about.connect("clicked", self.on_button_about_clicked)

        btn_mainpage = self.builder.get_object("button_mainpage")
        if btn_mainpage:
            btn_mainpage.connect("clicked", self.on_button_mainpage_clicked)

        self.button_questions_mainpage.connect("clicked", self.on_button_mainpage_clicked)
        self.btn_go_mainpage.connect("clicked", self.on_button_mainpage_clicked)
        self.btn_show_log.connect("clicked", self.on_button_show_log_clicked)
        self.btn_close_logs.connect("clicked", self.on_button_close_logs_clicked)
        self.btn_copy_logs.connect("clicked", self.on_button_copy_logs_clicked)

        # Quick rows
        self.connect_row("row_reinstall_grub", self.on_row_reinstall_grub_activated)
        self.connect_row("row_reset_password", self.on_row_reset_password_activated)
        self.connect_row("row_fix_broken", self.on_row_fix_broken_activated)
        self.connect_row("row_update", self.on_row_update_activated)
        self.connect_row("row_advanced_options", self.on_row_advanced_options_activated)

        # Advanced rows
        self.connect_row("row_reinstall", self.on_row_reinstall_activated)
        self.connect_row("row_repair_filesystem", self.on_row_repair_filesystem_activated)
        self.connect_row("row_reset_config", self.on_row_reset_config_activated)
        self.connect_row("row_dump_log", self.on_row_dump_log_activated)
        self.connect_row("row_chroot", self.on_row_chroot_activated)

        # Custom styling
        self.load_styles()

    def connect_row(self, row_id, handler):
        row = self.builder.get_object(row_id)
        if row:
            row.connect("activated", handler)

    def load_styles(self):
        css_provider = Gtk.CssProvider()
        css_data = """
        .dim-label { opacity: 0.7; font-size: 0.9em; }
        .boxed-list { border-radius: 12px; }
        .error { color: #e01b24; font-size: 0.85em; }
        """
        try:
            css_provider.load_from_data(css_data.encode("utf-8"))
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception:
            pass

    def on_button_about_clicked(self, widget):
        about = Adw.AboutWindow(
            transient_for=self.window,
            application_name=_("Pars Linux Boot Repair"),
            application_icon="parslinux-boot-repair",
            developer_name="Pars Linux Project",
            version=APPVERSION,
            copyright="© 2026 Pars Linux Project",
            license_type=Gtk.License.GPL_3_0,
            website="https://parslinux.org",
            issue_url="https://github.com/parslinux/parslinux-boot-repair/issues",
            comments=_("Pars Linux Boot Repair — Helps to repair broken systems and restore GRUB/EFI bootloader."),
            developers=[
                "Pars Linux Developers & Contributors",
                "Ali Rıza Keskin",
                "Edip H. <edip@medip.dev>",
                "Fatih Altun",
            ],
            artists=["Pars Linux Design Team"],
        )
        about.present()

    def on_button_mainpage_clicked(self, widget):
        if self.deck.get_visible_child() == self.page_loading and self.spinner_loading.get_spinning():
            self.ask_confirmation_dialog(
                _("Are you sure you want to stop the operation?"),
                on_confirmed=lambda: self.terminate_and_return()
            )
            return
        self.deck.set_visible_child(self.page_main)

    def terminate_and_return(self):
        try:
            pid = self.vte_terminal.get_pty().get_fd()
            if pid:
                pass
        except Exception:
            pass
        self.deck.set_visible_child(self.page_main)

    def on_row_advanced_options_activated(self, widget):
        self.deck.set_visible_child(self.page_advanced)

    def update_status_page(self, title, icon_name, description, stop_spinner=False, enable_mainpage=True):
        self.status_page.set_title(title)
        self.status_page.set_icon_name(icon_name)
        self.status_page.set_description(description)
        self.btn_go_mainpage.set_sensitive(enable_mainpage)
        if stop_spinner:
            self.spinner_loading.set_spinning(False)
            self.spinner_loading.set_visible(False)
        else:
            self.spinner_loading.set_visible(True)
            self.spinner_loading.set_spinning(True)
        self.on_button_close_logs_clicked(None)

    def on_button_show_log_clicked(self, widget):
        self.status_page.set_visible(False)
        self.box_vte.set_visible(True)
        self.btn_show_log.set_visible(False)
        self.btn_close_logs.set_visible(True)

    def on_button_close_logs_clicked(self, widget):
        self.status_page.set_visible(True)
        self.box_vte.set_visible(False)
        self.btn_show_log.set_visible(True)
        self.btn_close_logs.set_visible(False)

    def on_button_copy_logs_clicked(self, widget):
        text = ""
        try:
            text = self.vte_terminal.get_text_range(0, 0, self.vte_terminal.get_row_count(), 0, None)[0]
        except Exception:
            pass
        display = Gdk.Display.get_default()
        if display:
            clipboard = display.get_clipboard()
            clipboard.set(text)

    def ask_confirmation_dialog(self, message, on_confirmed):
        dialog = Adw.MessageDialog(
            transient_for=self.window,
            heading=_("Confirmation Required"),
            body=message,
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("confirm", _("Continue"))
        dialog.set_response_appearance("confirm", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        def on_response(dlg, response_id):
            if response_id == "confirm" and on_confirmed:
                on_confirmed()

        dialog.connect("response", on_response)
        dialog.present()

    def vte_command(self, command, post_func, ask_user_confirm=True, environ=[]):
        def execute():
            try:
                env_vars = [f"{k}={v}" for k, v in os.environ.items()] + environ
                if isinstance(command, str):
                    cmd_list = ["/bin/bash", "-c", command]
                else:
                    cmd_list = command

                self.vte_terminal.spawn_async(
                    Vte.PtyFlags.DEFAULT,
                    os.environ.get("HOME", "/root"),
                    cmd_list,
                    env_vars,
                    GLib.SpawnFlags.SEARCH_PATH,
                    None,
                    None,
                    -1,
                    None,
                    self.vte_cb
                )

                def on_exited(term, status):
                    self.vte_exited(term, status, post_func)

                self.vte_terminal.connect("child-exited", on_exited)
            except Exception as e:
                self.update_status_page(
                    _("Operation Failed"),
                    "dialog-error-symbolic",
                    _("An error occurred while executing command: {}").format(str(e)),
                    True, True
                )

        if ask_user_confirm:
            self.ask_confirmation_dialog(
                _("Are you sure you want to continue? This action may modify system partitions."),
                on_confirmed=execute
            )
        else:
            execute()

    def vte_cb(self, terminal, pid, error):
        if error:
            self.update_status_page(_("Error Spawning Process"), "dialog-error-symbolic", str(error), True, True)

    def vte_exited(self, terminal, status, post_func):
        if status == 0:
            if post_func:
                post_func()
        else:
            self.update_status_page(
                _("Operation Failed"),
                "dialog-error-symbolic",
                _("The operation failed with exit code {}. Check logs for details.").format(status),
                True, True
            )

    # ------------------ Core Actions ------------------

    def on_row_reinstall_grub_activated(self, widget):
        def pre():
            self.update_status_page(_("Detecting Partitions"), "content-loading-symbolic", _(
                "We're scanning your system to locate available partitions."), False, False)
            self.partitions = self.list_partitions()
            if not self.partitions:
                self.update_status_page(_("Unable to Detect Partitions"), "dialog-error-symbolic", _(
                    "No partitions detected on your disk."), True, True)
                return

            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Rootfs Partition"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                if not self.rootfs:
                    return
                return self.process_partition(after_rootfs, self.rootfs)

            mbrs = self.list_mbr()
            if not mbrs:
                self.update_status_page(_("Unable to Detect Disks"), "dialog-error-symbolic", _(
                    "No physical disks found for GRUB MBR."), True, True)
                return
            self.mbr_page = self.new_page_listbox(_("Choose Target Disk for GRUB"), mbrs, ["" for _ in mbrs], after_mbr)

        def after_mbr(widget=None, userdata=None):
            self.mbr = self.mbr_page.get_selected_title()
            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Reinstalling GRUB Bootloader"), "content-loading-symbolic", _(
                "Reinstalling GRUB to ensure your system starts properly. Once complete, your computer will boot into ParsLinux as usual."), False, False)

            envs = [f"disk={self.rootfs.name}", f"mbr={self.mbr}"]
            if getattr(self.rootfs, "root_subvol", None):
                envs.append(f"subvolume={self.rootfs.root_subvol}")

            self.vte_command("grub-reinstall", post, environ=envs)

        def post():
            self.update_status_page(_("GRUB Reinstallation Completed"), "emblem-ok-symbolic", _(
                "GRUB bootloader successfully reinstalled. You may now reboot into ParsLinux."), True, True)

        self.row_init_func(pre)

    def on_row_reset_password_activated(self, widget):
        def pre():
            self.update_status_page(_("Detecting Partitions"), "content-loading-symbolic", _(
                "Scanning partitions..."), False, False)
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Partition to Reset Password"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            users = self.list_users(self.rootfs)
            self.user_page = self.new_page_listbox(_("Select User"), users, ["" for _ in users], after_user)

        def after_user(widget=None, userdata=None):
            self.user = self.user_page.get_selected_title()
            self.password_page = self.new_page_password_input(after_password)

        def after_password(widget=None):
            pass1 = self.password_page.entry.get_text()
            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Resetting Password"), "content-loading-symbolic", _(
                "Resetting password for user. You will be able to log in with your new password."), False, False)
            envs = [f"disk={self.rootfs.name}", f"user={self.user}", f"pass1={pass1}", f"pass2={pass1}"]
            if getattr(self.rootfs, "root_subvol", None):
                envs.append(f"subvolume={self.rootfs.root_subvol}")
            self.vte_command("reset-password", post, environ=envs)

        def post():
            self.update_status_page(_("Password Reset Successful"), "emblem-ok-symbolic", _(
                "User password has been updated successfully."), True, True)

        self.row_init_func(pre)

    def on_row_fix_broken_activated(self, widget):
        self.simple_partition_action(
            _("Fixing Broken Packages"),
            "fix-broken-packages",
            _("Package Repair Completed"),
            _("Broken packages have been fixed.")
        )

    def on_row_update_activated(self, widget):
        self.simple_partition_action(
            _("Updating System Packages"),
            "full-upgrade",
            _("System Update Completed"),
            _("All system packages have been upgraded.")
        )

    def on_row_repair_filesystem_activated(self, widget):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.repair_page = self.new_page_listbox(_("Choose Partition for Filesystem Repair"), names, oses, after_part)

        def after_part(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.repair_page.get_selected_title()
                part = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_part, part)
            else:
                part = partition

            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Repairing Filesystem on {}").format(part.path), "content-loading-symbolic", _(
                "Checking and repairing filesystem errors..."), False, False)
            envs = [f"disk={part.name}"]
            self.vte_command("check-filesystem", post, environ=envs)

        def post():
            self.update_status_page(_("Filesystem Repair Successful"), "emblem-ok-symbolic", _(
                "The filesystem has been checked and repaired successfully."), True, True)

        self.row_init_func(pre)

    def on_row_chroot_activated(self, widget):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Partition for Chroot"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            users = ["root"] + self.list_users(self.rootfs)
            self.user_page = self.new_page_listbox(_("Select User for Chroot"), users, ["" for _ in users], after_user)

        def after_user(widget=None, userdata=None):
            self.user = self.user_page.get_selected_title()
            self.deck.set_visible_child(self.page_loading)
            self.on_button_show_log_clicked(None)
            self.update_status_page(_("Chroot Session Active"), "utilities-terminal-symbolic", _("Interactive chroot shell"), False, False)

            envs = [f"disk={self.rootfs.name}"]
            if getattr(self.rootfs, "root_subvol", None):
                envs.append(f"subvolume={self.rootfs.root_subvol}")

            chroot_bin = "parslinux-chroot" if os.path.exists(os.path.join(APP_DIR, "scripts/parslinux-chroot")) else (shutil.which("parslinux-chroot") or "parslinux-chroot")
            self.vte_command([chroot_bin, f"/dev/{self.rootfs.name}", "su", "-", self.user], post, False, environ=envs)

        def post():
            self.update_status_page(_("Chroot Session Ended"), "emblem-ok-symbolic", _("Chroot process concluded."), True, True)

        self.row_init_func(pre)

    def on_row_dump_log_activated(self, widget):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Partition for Log Extraction"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            out_dir = os.environ.get("HOME", "/tmp")
            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Extracting System Logs"), "content-loading-symbolic", _("Collecting logs into archive..."), False, False)
            envs = [f"disk={self.rootfs.name}"]
            self.vte_command(f"dump-info-log {out_dir}", post, environ=envs)

        def post():
            out_path = os.path.join(os.environ.get("HOME", "/tmp"), "system-log.zip")
            self.update_status_page(_("Logs Successfully Extracted"), "emblem-ok-symbolic", _(
                "Logs saved to: {}").format(out_path), True, True)

        self.row_init_func(pre)

    def on_row_reset_config_activated(self, widget):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Partition"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            users = self.list_users(self.rootfs)
            self.user_page = self.new_page_listbox(_("Select User to Reset Config"), users, ["" for _ in users], after_user)

        def after_user(widget=None, userdata=None):
            self.user = self.user_page.get_selected_title()
            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Resetting Configuration"), "content-loading-symbolic", _(
                "Erasing user custom configurations in home directory..."), False, False)

            envs = [f"disk={self.rootfs.name}"]
            chroot_bin = "parslinux-chroot" if os.path.exists(os.path.join(APP_DIR, "scripts/parslinux-chroot")) else (shutil.which("parslinux-chroot") or "parslinux-chroot")
            self.vte_command([chroot_bin, f"/dev/{self.rootfs.name}", "su", self.user, "-c", "cd ; rm -rvf .dbus .cache .local .config"], post, environ=envs)

        def post():
            self.update_status_page(_("Configuration Reset Successful"), "emblem-ok-symbolic", _(
                "User desktop configurations have been reverted to defaults."), True, True)

        self.row_init_func(pre)

    def on_row_reinstall_activated(self, widget):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Partition to Reinstall"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            mbrs = self.list_mbr()
            self.mbr_page = self.new_page_listbox(_("Choose Grub Disk"), mbrs, ["" for _ in mbrs], after_mbr)

        def after_mbr(widget=None, userdata=None):
            self.mbr = self.mbr_page.get_selected_title()
            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(_("Reinstalling System"), "content-loading-symbolic", _(
                "Reinstalling system image from live media..."), False, False)

            envs = [f"disk={self.rootfs.name}", f"mbr={self.mbr}"]
            reinstall_cmd = "parslinux-reinstall" if os.path.exists(os.path.join(APP_DIR, "scripts/parslinux-reinstall")) else (shutil.which("parslinux-reinstall") or "parslinux-reinstall")
            self.vte_command(reinstall_cmd, post, environ=envs)

        def post():
            self.update_status_page(_("System Reinstallation Completed"), "emblem-ok-symbolic", _(
                "Fresh system installation has completed."), True, True)

        self.row_init_func(pre)

    def simple_partition_action(self, running_title, script_name, done_title, done_desc):
        def pre():
            self.partitions = self.list_partitions()
            names = [p.name for p in self.partitions]
            oses = [p.operating_system or "Unknown" for p in self.partitions]
            self.rootfs_page = self.new_page_listbox(_("Choose Target Partition"), names, oses, after_rootfs)

        def after_rootfs(widget=None, userdata=None, partition=None):
            if partition is None:
                selected = self.rootfs_page.get_selected_title()
                self.rootfs = next((p for p in self.partitions if p.name == selected), None)
                return self.process_partition(after_rootfs, self.rootfs)

            self.deck.set_visible_child(self.page_loading)
            self.update_status_page(running_title, "content-loading-symbolic", _("Processing..."), False, False)
            envs = [f"disk={self.rootfs.name}"]
            if getattr(self.rootfs, "root_subvol", None):
                envs.append(f"subvolume={self.rootfs.root_subvol}")
            self.vte_command(script_name, post, environ=envs)

        def post():
            self.update_status_page(done_title, "emblem-ok-symbolic", done_desc, True, True)

        self.row_init_func(pre)

    def row_init_func(self, pre_func):
        self.clear_carousel()
        self.deck.set_visible_child(self.page_loading)
        GLib.idle_add(pre_func)

    def clear_carousel(self):
        while self.carousel_questions.get_n_pages() > 0:
            page = self.carousel_questions.get_nth_page(0)
            self.carousel_questions.remove(page)

    def process_partition(self, pending_func, part):
        if not part:
            return None
        if part.is_luks:
            self.unlock_luks(part, self.process_partition, pending_func)
            return None
        if part.is_lvm:
            self.mount_lvm(part, self.process_partition, pending_func)
            return None
        if part.is_btrfs:
            subvols = self.list_subvolumes(part)
            if subvols:
                self.subvol_page = self.new_page_listbox(
                    _("Choose BTRFS Subvolume"), subvols, ["" for _ in subvols],
                    lambda w, u: self.after_subvol_selected(part, pending_func)
                )
                return None
        pending_func(None, None, part)

    def after_subvol_selected(self, part, pending_func):
        part.root_subvol = self.subvol_page.get_selected_title()
        pending_func(None, None, part)

    def unlock_luks(self, part, next_func, pending_func):
        pass_page = self.new_page_password_input(
            lambda w: self.do_unlock_luks(part, pass_page.entry.get_text(), next_func, pending_func),
            title=_("Enter LUKS Passphrase for {}").format(part.name)
        )

    def do_unlock_luks(self, part, passphrase, next_func, pending_func):
        luks_name = f"luks-{part.name}"
        proc = subprocess.run(
            ["cryptsetup", "open", part.path, luks_name],
            input=f"{passphrase}\n",
            capture_output=True,
            text=True
        )
        if proc.returncode == 0:
            part.name = f"mapper/{luks_name}"
            part.path = f"/dev/mapper/{luks_name}"
            part.is_luks = False
            next_func(pending_func, part)
        else:
            self.update_status_page(_("LUKS Decryption Failed"), "dialog-error-symbolic", proc.stderr or _("Wrong passphrase."), True, True)

    def mount_lvm(self, part, next_func, pending_func):
        vg_names = subprocess.getoutput("vgdisplay --colon | cut -d: -f1").splitlines()
        if not vg_names:
            next_func(pending_func, part)
            return
        vg = vg_names[0].strip()
        subprocess.run(["vgchange", "-ay", vg], check=False)
        lvs = subprocess.getoutput(f"lvdisplay --colon | grep ':{vg}:' | cut -d: -f1").splitlines()
        lv_names = [os.path.basename(lv) for lv in lvs if lv.strip()]
        if lv_names:
            self.lv_page = self.new_page_listbox(_("Select Logical Volume"), lv_names, ["" for _ in lv_names],
                lambda w, u: self.after_lv_selected(vg, next_func, pending_func))
        else:
            next_func(pending_func, part)

    def after_lv_selected(self, vg, next_func, pending_func):
        selected_lv = self.lv_page.get_selected_title()
        part = Partition()
        part.name = f"{vg}/{selected_lv}"
        part.path = f"/dev/{vg}/{selected_lv}"
        part.is_lvm = False
        next_func(pending_func, part)

    # ------------------ Helper Widgets ------------------

    def new_page_listbox(self, title, items, subtitles, on_continue):
        self.clear_carousel()
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.set_margin_start(24)
        page.set_margin_end(24)

        clamp = Adw.Clamp(maximum_size=600)
        page.append(clamp)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        clamp.set_child(inner_box)

        lbl = Gtk.Label(label=title)
        lbl.add_css_class("title-2")
        lbl.set_halign(Gtk.Align.START)
        inner_box.append(lbl)

        listbox = Gtk.ListBox()
        listbox.add_css_class("boxed-list")
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        inner_box.append(listbox)

        rows = []
        for i, itm in enumerate(items):
            sub = subtitles[i] if i < len(subtitles) else ""
            row = Adw.ActionRow(title=itm, subtitle=sub)
            row.set_activatable(True)
            listbox.append(row)
            rows.append(row)

        if rows:
            listbox.select_row(rows[0])

        def get_selected_title():
            selected_row = listbox.get_selected_row()
            return selected_row.get_title() if selected_row else ""

        page.get_selected_title = get_selected_title
        page.listbox = listbox

        try:
            self.button_questions_continue.disconnect_by_func(self.current_continue_handler)
        except Exception:
            pass

        self.current_continue_handler = lambda btn: on_continue(None, None)
        self.button_questions_continue.connect("clicked", self.current_continue_handler)

        self.carousel_questions.append(page)
        self.deck.set_visible_child(self.page_questions)
        return page

    def new_page_password_input(self, on_continue, title=_("Enter New Password")):
        self.clear_carousel()
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.set_margin_start(24)
        page.set_margin_end(24)

        clamp = Adw.Clamp(maximum_size=500)
        page.append(clamp)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        clamp.set_child(inner_box)

        lbl = Gtk.Label(label=title)
        lbl.add_css_class("title-2")
        lbl.set_halign(Gtk.Align.START)
        inner_box.append(lbl)

        entry1 = Gtk.PasswordEntry()
        entry1.set_placeholder_text(_("New Password"))
        inner_box.append(entry1)

        entry2 = Gtk.PasswordEntry()
        entry2.set_placeholder_text(_("Confirm Password"))
        inner_box.append(entry2)

        warn_lbl = Gtk.Label(label=_("Passwords do not match"))
        warn_lbl.add_css_class("error")
        warn_lbl.set_visible(False)
        inner_box.append(warn_lbl)

        page.entry = entry1
        page.entry_second = entry2

        def validate_and_continue(btn):
            p1 = entry1.get_text()
            p2 = entry2.get_text()
            if p1 and p1 == p2:
                on_continue(page)
            else:
                warn_lbl.set_visible(True)

        try:
            self.button_questions_continue.disconnect_by_func(self.current_continue_handler)
        except Exception:
            pass

        self.current_continue_handler = validate_and_continue
        self.button_questions_continue.connect("clicked", self.current_continue_handler)

        self.carousel_questions.append(page)
        self.deck.set_visible_child(self.page_questions)
        return page

    # ------------------ System Inspection Helpers ------------------

    def list_partitions(self):
        parts = []
        try:
            detected_oses = search_operating_system.search_operating_system()
        except Exception:
            detected_oses = []

        os_map = {d.get("part"): d.get("os") or d.get("label") for d in detected_oses if d.get("part")}

        output = subprocess.getoutput("lsblk -rno NAME,TYPE,FSTYPE")
        for line in output.splitlines():
            parts_info = line.split()
            if len(parts_info) >= 2:
                name = parts_info[0]
                ptype = parts_info[1]
                fstype = parts_info[2] if len(parts_info) > 2 else ""

                if ptype in ("part", "crypt", "lvm"):
                    p = Partition()
                    p.name = name
                    p.path = f"/dev/{name}"
                    p.fstype = fstype
                    p.operating_system = os_map.get(p.path, "")
                    p.is_luks = (fstype == "crypto_LUKS")
                    p.is_lvm = (fstype == "LVM2_member")
                    p.is_btrfs = (fstype == "btrfs")
                    parts.append(p)
        return parts

    def list_mbr(self):
        output = subprocess.getoutput("lsblk -dno NAME,TYPE")
        disks = []
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "disk":
                disks.append(parts[0])
        return disks

    def list_users(self, rootfs):
        tmp_mnt = f"/tmp/user_scan_{os.getpid()}"
        os.makedirs(tmp_mnt, exist_ok=True)
        users = []
        try:
            subprocess.run(["mount", "-o", "ro", rootfs.path, tmp_mnt], check=True, stderr=subprocess.DEVNULL)
            passwd_file = os.path.join(tmp_mnt, "etc/passwd")
            if os.path.exists(passwd_file):
                with open(passwd_file, "r") as f:
                    for line in f:
                        fields = line.strip().split(":")
                        if len(fields) >= 3 and fields[2].isdigit():
                            uid = int(fields[2])
                            if uid >= 1000 and uid != 65534:
                                users.append(fields[0])
        except Exception:
            pass
        finally:
            subprocess.run(["umount", "-l", tmp_mnt], check=False, stderr=subprocess.DEVNULL)
            shutil.rmtree(tmp_mnt, ignore_errors=True)
        return users or ["pars"]

    def list_subvolumes(self, part):
        tmp_mnt = f"/tmp/subvol_scan_{os.getpid()}"
        os.makedirs(tmp_mnt, exist_ok=True)
        subvols = []
        try:
            subprocess.run(["mount", "-o", "ro", part.path, tmp_mnt], check=True, stderr=subprocess.DEVNULL)
            lines = subprocess.getoutput(f"btrfs subvolume list {tmp_mnt}").splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 9:
                    subvols.append(parts[8])
        except Exception:
            pass
        finally:
            subprocess.run(["umount", "-l", tmp_mnt], check=False, stderr=subprocess.DEVNULL)
            shutil.rmtree(tmp_mnt, ignore_errors=True)
        return subvols


class Partition:
    def __init__(self):
        self.name = ""
        self.path = ""
        self.fstype = ""
        self.operating_system = ""
        self.is_luks = False
        self.is_lvm = False
        self.is_btrfs = False
        self.root_subvol = None


def main():
    app = ApplicationGtk4()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
