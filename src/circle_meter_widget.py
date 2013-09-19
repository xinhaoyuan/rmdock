import cairo;
import math;

class CircleMeterWidget:
    STYLE_TAIL = 0;
    STYLE_SEGMENT = 1;

    value_monitor = None;
    radius        = None;
    width         = None;
    angle_opt1    = None;
    angle_opt2    = None;
    style         = None;
    color         = None;
    alpha         = None;
    mask          = None;
    surface       = None;
    cr            = None;

    def __init__(self, value_monitor, radius, width, angle_opt1, angle_opt2, style = STYLE_TAIL, color = (0.0,0.0,0.0), alpha = 1.0, mask = None):
        self.value_monitor = value_monitor;
        self.radius        = radius;
        self.width         = width;
        self.angle_opt1    = angle_opt1;
        self.angle_opt2    = angle_opt2
        self.style         = style;
        self.color         = color;
        self.alpha         = alpha;
        self.mask          = mask;
        self.surface       = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.radius * 2, self.radius * 2);
        self.cr            = cairo.Context(self.surface);

    def refresh(self):
        self.cr.set_operator(cairo.OPERATOR_CLEAR);
        self.cr.paint();
        self.cr.set_operator(cairo.OPERATOR_OVER);
        if (self.mask != None):
            self.cr.mask_surface(self.mask);
        value = self.value_monitor.get();
        if (self.style == CircleMeterWidget.STYLE_TAIL):
            self.cr.arc(self.radius, self.radius, self.radius - self.width / 2.0, self.angle_opt1, math.pi * 2 * value + self.angle_opt2);
            self.cr.set_line_width(self.width);
        elif (self.style == CircleMeterWidget.STYLE_SEGMENT):
            self.cr.arc(self.radius, self.radius, self.radius - self.width / 2.0, math.pi * 2 * value + self.angle_opt1, math.pi * 2 * value + self.angle_opt2);
            self.cr.set_line_width(self.width);
        else:
            raise Exception("style not acceptable: " + self.style);
        self.cr.set_source_rgba(self.color[0], self.color[1], self.color[2], self.alpha);
        self.cr.stroke();
        # if (self.mask != None):
        #     self.cr.move_to(0, 0);
        #     self.cr.set_source_surface(self.mask);
        #     self.cr.set_operator(cairo.OPERATOR_DEST_IN);
        #     self.cr.paint();

    def get_surface(self):
        return self.surface;
