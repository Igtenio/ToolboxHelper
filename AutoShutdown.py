import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import time

ntp_server = "pool.ntp.org"
shutdown_time = "06:00"

class AutoShutdownApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="AutoShutdown")
        self.set_border_width(10)
        self.set_default_size(300, 100)
        
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.add(self.grid)
        
        self.shutdown_time_label = Gtk.Label("Shutdown Time (HH:MM):")
        self.grid.attach(self.shutdown_time_label, 0, 0, 1, 1)
        
        self.shutdown_time_entry = Gtk.Entry()
        self.grid.attach(self.shutdown_time_entry, 1, 0, 1, 1)
        
        self.disable_button = Gtk.Button(label="Disable")
        self.disable_button.connect("clicked", self.on_disable_clicked)
        self.grid.attach(self.disable_button, 0, 1, 1, 1)
        
        self.status_label = Gtk.Label()
        self.grid.attach(self.status_label, 1, 1, 1, 1)
        
        self.ntp_server_label = Gtk.Label("NTP Server:")
        self.grid.attach(self.ntp_server_label, 0, 2, 1, 1)
        
        self.ntp_server_entry = Gtk.Entry()
        self.grid.attach(self.ntp_server_entry, 1, 2, 1, 1)
        
        self.set_ntp_server_button = Gtk.Button(label="Set NTP Server")
        self.set_ntp_server_button.connect("clicked", self.on_set_ntp_server_clicked)
        self.grid.attach(self.set_ntp_server_button, 0, 3, 2, 1)
        
        self.show_all()
        
        self.disable_until = 0
        GLib.timeout_add_seconds(1, self.check_shutdown_time)
        
    def on_disable_clicked(self, widget):
        self.disable_until = int(time.time()) + 6 * 3600
        self.status_label.set_text("Disabled for 6 hours")
        
    def on_set_ntp_server_clicked(self, widget):
        ntp_server = self.ntp_server_entry.get_text()
        subprocess.run(["sudo", "timedatectl", "set-ntp", ntp_server])
        self.status_label.set_text("NTP server set to " + ntp_server)
        
    def check_shutdown_time(self):
        current_time = time.localtime()
        shutdown_time = time.strptime(self.shutdown_time_entry.get_text(), '%H:%M')
        
        if current_time.tm_hour == shutdown_time.tm_hour and current_time.tm_min == shutdown_time.tm_min:
            if self.disable_until < int(time.time()):
                subprocess.run(["sudo", "shutdown", "-h", "now"])
        return True