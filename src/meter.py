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

    def add_widget(self, widget, x, y, x_alignment = -1, y_alignment = -1):
        self.widgets.append((widget, x, y, x_alignment, y_alignment));

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
            i[0].prepare_surface(cr);
            sx = 0.0;
            sy = 0.0;
            if (i[3] == -1):
                sx = i[1];
            elif (i[3] == 0):
                sx = i[1] - i[0].get_width() / 2;
            elif (i[3] == 1):
                sx = i[1] - i[0].get_width();
            if (i[4] == -1):
                sy = i[2];
            elif (i[4] == 0):
                sy = i[2] - i[0].get_height() / 2;
            elif (i[4] == 1):
                sy = i[2] - i[0].get_height();
            cr.translate(sx, sy);
            cr.set_source_surface(i[0].get_surface());
            cr.set_operator(cairo.OPERATOR_OVER);
            cr.paint();
            cr.identity_matrix();
