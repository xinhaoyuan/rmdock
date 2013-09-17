from gi.repository import GLib;
import psutil;
from distutils.version import StrictVersion;

class Monitor(object):

    cpu_usage = 0;
    pmem_usage = 0;

    instance = None;
    @classmethod
    def get(cls):
        if (cls.instance == None):
            cls.instance = Monitor();
        return cls.instance;

    def refresh_func(self):
        self.cpu_usage = psutil.cpu_percent(interval = 0) / 100.0;
        if (StrictVersion(psutil.__version__) < StrictVersion("0.6.0")):
            pmem = psutil.phymem_usage();
            self.pmem_usage = float(pmem.used) / pmem.total;
        else:
            vmem = psutil.virtual_memory();
            self.pmem_usage = vmem.available / vmem.total;

        return True;

    def start(self):
        GLib.timeout_add(400, self.refresh_func);

