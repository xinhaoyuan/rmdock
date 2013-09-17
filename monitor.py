from gi.repository import GLib;
import psutil;

class Monitor(object):

    cpu_usage = 0;

    instance = None;
    @classmethod
    def get(cls):
        if (cls.instance == None):
            cls.instance = Monitor();
        return cls.instance;

    def refresh_func(self):
        self.cpu_usage = psutil.cpu_percent(interval = 0) / 100.0;
        return True;

    def start(self):
        GLib.timeout_add(500, self.refresh_func);

