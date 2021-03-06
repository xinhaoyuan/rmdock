#!/usr/bin/env python

from gi.repository import Gtk, Gdk, Pango;
import cairo;
import signal;
from monitor import Monitor;
import config;

def setup():
    Monitor.get().start();
    screen = Gdk.Screen.get_default();
    for i in xrange(0, screen.get_n_monitors()):
        # setup for each monitor
        rect = screen.get_monitor_geometry(i);
        config.config_monitor(i, rect);

if __name__ == "__main__":    
    signal.signal(signal.SIGINT, signal.SIG_DFL);
    setup();
    Gtk.main();
