from gi.repository import GLib, Gtk, Gdk, Pango;
import cairo, pango, pangocairo;

class PangoWidget(object):
    mask               = None;
    markup_monitor     = None;
    color              = None;
    alpha              = None;
    surface            = None;
    alignment          = None;
    old_value          = None;

    def __init__(self, markup_monitor, color = (0.0, 0.0, 0.0), alpha = 1.0, mask = None, alignment = "left"):
        self.markup_monitor = markup_monitor;
        self.mask           = mask;
        self.surface        = None;
        self.color          = color;
        self.alpha          = alpha;
        self.alignment      = alignment;

    def set_alignment(self, alignment):
        self.alignment = alignment;
    
    def prepare_surface(self, ext_cr):
        value = self.markup_monitor.get();
        if (self.old_value == value):
            return;
        else:
            self.old_value = value;
        pangocairo_context = pangocairo.CairoContext(ext_cr)
        layout = pangocairo_context.create_layout();
        layout.set_alignment(self.alignment);
        layout.set_markup(value);
        self.size = layout.get_pixel_size();
        self.surface = ext_cr.get_group_target().create_similar(cairo.CONTENT_COLOR_ALPHA, self.size[0], self.size[1]);
        cr = cairo.Context(self.surface);
        # XXX: dont know whether this way is efficient
        pangocairo_context = pangocairo.CairoContext(cr);
        if (self.mask != None):
            self.cr.mask_surface(self.mask);
        else:
            cr.set_source_rgba(self.color[0], self.color[1], self.color[2], self.alpha);
        pangocairo_context.update_layout(layout);
        pangocairo_context.show_layout(layout);

    def get_width(self):
        return self.size[0];

    def get_height(self):
        return self.size[1];

    def get_surface(self):
        return self.surface;
