# Provide the base canvas for docks

from gi.repository import Gtk, Gdk, Pango;
import cairo;

class Canvas(Gtk.Window):
    dock_event_listener = None;

    def __init__(self):
        super(Canvas, self).__init__();

    def setup(self, position = None, dock_event_listener = None):
        self.dock_event_listener = dock_event_listener;
        # set basic gtk properties
        self.set_app_paintable(True);
        self.set_decorated(False);
        self.set_resizable(False);
        self.set_skip_taskbar_hint(True);
        self.set_skip_pager_hint(True);
        if (position == "above"):
            self.set_type_hint(Gdk.WindowTypeHint.DOCK);
            self.set_keep_above(True);
        elif (position == "below"):
            self.set_type_hint(Gdk.WindowTypeHint.DESKTOP);
            self.set_keep_below(True);
        else:
            raise Exception("position should be 'above' or 'below'");
        screen = self.get_screen();
        visual = screen.get_rgba_visual();
        if (visual != None and screen.is_composited()):
            self.set_visual(visual);
        # set hooks
        self.drawing_area = Gtk.DrawingArea();
        self.add(self.drawing_area);
        self.drawing_area.connect("draw", self.on_draw);

    def show(self):
        self.show_all();

    def hide(self):
        self.hide();

    def set_size(self, width, height):
        self.drawing_area.set_size_request(width, height);

    def redraw(self):
        self.drawing_area.queue_draw();

    def on_draw(self, widget, cr):
        # make background transparent
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        self.dock_event_listener.draw(cr);

    def get_window(self):
        return super(Gtk.Window, self);
