from gi.repository import GLib;
import psutil;
from distutils.version import StrictVersion;
import config;
from threading import Thread;

import base64;
import urllib2;
from xml.dom.minidom import parse

class Monitor(object):

    cpu_usage = 0;
    pmem_usage = 0;
    gmail_unread_count = 0;
    gmail_monitor = None;

    def __init__(self):
        self.gmail_monitor = GmailMonitor(config.gmail_username, config.gmail_password);
    
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

    def longterm_refresh_func(self):
        self.gmail_monitor.try_refresh();
        self.gmail_unread_count = self.gmail_monitor.get_unread_count();

        return True;        

    def start(self):
        GLib.timeout_add(400, self.refresh_func);
        GLib.timeout_add(2000, self.longterm_refresh_func);

class GmailMonitor(object):
    username = None;
    password = None;
    unread_count = 0;
    processing_thread = None;

    def __init__(self, username, password):
        self.username = username;
        self.password = password;
        self.processing_thread = Thread(target = self.process_feed, args = ());
        self.processing_thread.start();

    def process_feed(self):
        # Build the authentication string
        b64auth = base64.encodestring("%s:%s" % (self.username, self.password))
        auth = "Basic " + b64auth

        # Build the request
        req = urllib2.Request("https://mail.google.com/mail/feed/atom/")
        req.add_header("Authorization", auth)
        handle = urllib2.urlopen(req)

        # Build an XML dom tree of the feed
        dom = parse(handle)
        handle.close()

        # Get the "fullcount" xml object
        count_obj = dom.getElementsByTagName("fullcount")[0]
        # get its text and convert it to an integer
        self.unread_count = int(count_obj.firstChild.wholeText);
    
    def get_unread_count(self):
        return self.unread_count;

    def try_refresh(self):
        if (self.processing_thread != None):
            if (not self.processing_thread.is_alive()):
                self.processing_thread.join();
                self.processing_thread = None;
        if (self.processing_thread == None):
            self.processing_thread = Thread(target = self.process_feed, args = ());
            self.processing_thread.start();
