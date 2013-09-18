#!/usr/bin/env python

from gi.repository import Gtk, Gdk, Pango;
import cairo;
import signal;
from meter import Meter;
from monitor import Monitor;

def setup():
    Monitor.get().start();
    screen = Gdk.Screen.get_default();
    for i in xrange(0, screen.get_n_monitors()):
        # setup a meter for each monitor
        rect = screen.get_monitor_geometry(i);
        c = Meter();
        c.get_window().move(rect.x + (rect.width - c.width) / 2,
                            rect.y + (rect.height - c.height) / 2);
        c.show();
        
    Gtk.main();

if __name__ == "__main__":    
    signal.signal(signal.SIGINT, signal.SIG_DFL);
    setup();
    Gtk.main();
