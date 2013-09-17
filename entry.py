#!/usr/bin/env python

from gi.repository import Gtk, Gdk, Pango;
import cairo;
import signal;
from clock import Clock;

def setup():
    clock = Clock();
    clock.show();

    Gtk.main();

if __name__ == "__main__":    
    signal.signal(signal.SIGINT, signal.SIG_DFL);
    setup();
    Gtk.main();
