# Written (poorly) by Gary Schroeder
# TODO for Me
# Change NTP function in on_set_ntp_server_clicked to both enable and set servers
# GUI tweaks.
# Maybe get an icon made up in Paint.
# It's like 1:33am. I hadn't learned PyGObject before this. As someone who'll inevitably learn something that'll doom myself //
# // and/or humanity in my thirst for knowledge, I was okay not knowing this. Some men build time machines to meet people. Some //
# // do it to save lost loves. I want to do it to tell Past-Gary to just tell Heath it sounds like a great time to learn BASH //
# // script programming himself versus volunteering for this. I guess what I'm saying is that I don't regret this, but if the //
# // choice was continuing to exist in this state or causing the sun to go supernova in an attept to gravity swing with a bunch //
# // of whales I stole from San Francisco, I'd invest in krill stocks because Nemo and Bessie gotta pack a few lunches.
# Fucking clean up this mess for production. Oy vey.
# Probably remove some of these notes so a million billion servers aren't burning with my vulgarity. Or don't. I don't know, I'm not a doctor.
# TODO for Tony
# Continue to show infinite patience upon a poor SENG like me. Galileo Galileo figuro.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import time

ntp_server = "pool.ntp.org"
shutdown_time_hour = int(6)
shutdown_time_min = "00"

class ToolboxHelper(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ToolboxHelper")
        self.set_border_width(10)
        self.set_default_size(300, 100)
        
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.add(self.grid)
        
        self.shutdown_time_label = Gtk.Label("Shutdown Time (HH:MM):")
        self.grid.attach(self.shutdown_time_label, 0, 0, 1, 1)
        
        self.shutdown_time_entry = Gtk.Entry()
        self.shutdown_time_entry.set_text(str(shutdown_time_hour) + ":" + shutdown_time_min)
        self.grid.attach(self.shutdown_time_entry, 1, 0, 1, 1)
        
        self.disable_button = Gtk.Button(label="Delay")
        self.disable_button.connect("clicked", self.on_disable_clicked)
        self.grid.attach(self.disable_button, 0, 1, 2, 1)
        
        self.status_label = Gtk.Label()
        self.grid.attach(self.status_label, 1, 1, 1, 1)
        
#        self.ntp_server_label = Gtk.Label("NTP Server:")
#        self.grid.attach(self.ntp_server_label, 0, 2, 1, 1)
        
#        self.ntp_server_entry = Gtk.Entry()
#        self.ntp_server_entry.set_text(ntp_server)
#        self.grid.attach(self.ntp_server_entry, 1, 2, 1, 1)
        
#        self.set_ntp_server_button = Gtk.Button(label="Set NTP Server")
#        self.set_ntp_server_button.connect("clicked", self.on_set_ntp_server_clicked)
#        self.grid.attach(self.set_ntp_server_button, 0, 3, 2, 1)
        
        self.show_all()
        
        self.disable_until = 0
        GLib.timeout_add_seconds(1, self.set_shutdown_time)
        cstoutput = self.check_shutdown_time()
        print(cstoutput)
        if cstoutput == False:
            exit()

    def on_disable_clicked(self, widget):
#       I don't like this, makes it require the program to run. Easier to just set the
#       shutdown time via Linux, and also limits it to a 24 hour period.
#       v2 Changes
#       self.disable_until = int(time.time()) + 6 * 3600
#       self.status_label.set_text("Disabled for 6 hours")
        global shutdown_time_hour
        shutdown_time_hour = int(shutdown_time_hour) + 6
        if shutdown_time_hour >= 24: shutdown_time_hour = int(shutdown_time_hour) - 24
#        if len(self.shutdown_time_hour) == 0: self.shutdown_time_hour = "00"
#        if len(self.shutdown_time_hour) == 1: self.shutdown_time_hour = "0" + shutdown_time_hour
        self.shutdown_time_entry.set_text(str(shutdown_time_hour) + ":" + shutdown_time_min)
        self.set_shutdown_time()
        
    def on_set_ntp_server_clicked(self, widget):
        ntp_server = str(self.ntp_server_entry.get_text())
        subprocess.run(["timedatectl", "set-ntp", ntp_server])
        self.status_label.set_text("NTP server set to " + ntp_server)
        
    def set_shutdown_time(self):
#       v2 Changes
#        current_time = time.localtime()
#        shutdown_time = time.strptime(self.shutdown_time_entry.get_text(), '%H:%M')
#        
#        if current_time.tm_hour == shutdown_time.tm_hour and current_time.tm_min == shutdown_time.tm_min:
#            if self.disable_until < int(time.time()):
#                subprocess.run(["shutdown", "-P", "5"])
#        return True
        subprocess.run(["shutdown", "-c"])
#        time.sleep(3)
        subprocess.run(["shutdown", "-P", str(shutdown_time_hour) + ":" + shutdown_time_min])
    
    def check_shutdown_time(self):
        # Run the command to get the scheduled shutdown time
        try:
            output = subprocess.check_output("date --date @$(head -1 /run/systemd/shutdown/scheduled |cut -c6-15)", shell=True)
        except subprocess.CalledProcessError:
            self.status_label.set_text("Failed to get scheduled shutdown time")
            self.set_shutdown_time()
            return False
        
        # Parse the output to get the scheduled shutdown hour
        scheduled_hour = int(output.decode("utf-8").strip().split()[3].split(":")[0])
        print(scheduled_hour)
        
        # Check if the scheduled shutdown hour is one of the valid ones
        if scheduled_hour == 6:
            return True
        elif scheduled_hour == 12:
            return True
        elif scheduled_hour == 18:
            return True
        elif scheduled_hour == 0:
            return True
        else:
            self.status_label.set_text("Scheduled shutdown time is not valid")
            self.set_shutdown_time()
            return False

win = ToolboxHelper()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()