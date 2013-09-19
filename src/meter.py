import cairo;
from canvas import Canvas;
from gi.repository import GLib;

class Meter(object):

    canvas  = None;
    widgets = None;
    height  = None;
    width   = None;

    def __init__(self, width, height):
        self.canvas = Canvas();
        handler = MeterEventHandler(self);
        self.canvas.setup("below", handler);
        self.canvas.set_size(width, height);
        self.width = width;
        self.height = height;
        self.widgets = [];

    def add_widget(self, widget, x, y):
        self.widgets.append((widget, x, y));
            

    def refresh_func(self):
        self.canvas.redraw();
        return self.canvas.get_mapped();

    def show(self):
        self.canvas.show();
        GLib.timeout_add(200, self.refresh_func);

    def hide(self):
        self.canvas.hide();
        
    def get_window(self):
        return self.canvas.get_window();

class MeterEventHandler(object):
    meter = None;
    
    def __init__(self, meter):
        self.meter = meter;
        
    def draw(self, cr):
        for i in self.meter.widgets:
            i[0].refresh();
            cr.translate(i[1], i[2]);
            cr.set_source_surface(i[0].get_surface());
            cr.set_operator(cairo.OPERATOR_OVER);
            cr.paint();
            cr.identity_matrix();
