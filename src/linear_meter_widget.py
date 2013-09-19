import cairo;

class LinearMeterWidget:
    GRAVITY_SOUTH = 0;
    GRAVITY_NORTH = 1;
    GRAVITY_WEST  = 2;
    GRAVITY_EAST  = 3;

    gravity       = None;
    width         = None;
    height        = None;
    color         = None;
    alpha         = None;
    value_monitor = None;
    mask          = None;
    surface       = None;
    cr            = None;

    def __init__(self, value_monitor, width, height, gravity = GRAVITY_SOUTH, color = (0.0,0.0,0.0), alpha = 1.0, mask = None):
        self.value_monitor = value_monitor;
        self.width   = width;
        self.height  = height;
        self.color   = color;
        self.alpha   = alpha;
        self.gravity = gravity;
        self.mask    = mask;
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height);
        self.cr      = cairo.Context(self.surface);

    def refresh(self):
        self.cr.set_operator(cairo.OPERATOR_CLEAR);
        self.cr.paint();
        self.cr.set_operator(cairo.OPERATOR_OVER);
        if (self.mask != None):
            self.cr.mask_surface(self.mask);
        value = self.value_monitor.get();
        if (self.gravity == LinearMeterWidget.GRAVITY_SOUTH):
            bar_length = value * self.height;
            self.cr.rectangle(0, self.height - bar_length, self.width, bar_length);
        elif (self.gravity == LinearMeterWidget.GRAVITY_NORTH):
            bar_length = value * self.height;
            self.cr.rectangle(0, 0, self.width, bar_length);
        elif (self.gravity == LinearMeterWidget.GRAVITY_WEST):
            bar_length = value * self.width;
            self.cr.rectangle(0, 0, bar_length, self.height);
        elif (self.gravity == LinearMeterWidget.GRAVITY_EAST):
            bar_length = value * self.width;
            self.cr.rectangle(self.width - bar_length, 0, bar_length, self.height);
        else:
            raise Exception("gravity not acceptable");
        self.cr.set_source_rgba(self.color[0], self.color[1], self.color[2], self.alpha);
        self.cr.fill();
        # if (self.mask != None):
        #     self.cr.move_to(0, 0);
        #     self.cr.set_source_surface(self.mask);
        #     self.cr.set_operator(cairo.OPERATOR_DEST_IN);
        #     self.cr.paint();

    def get_surface(self):
        return self.surface;
