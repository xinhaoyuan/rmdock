from gi.repository import GLib, Gtk, Gdk, Pango;

import threading;
import math;
import cairo;
import datetime;
import pango, pangocairo;
from canvas import Canvas;

class Clock(object):

  canvas = None;
  handler = None;
  width = None;
  height = None;

  def __init__(self, width = 300, height = 300):
    self.canvas = Canvas();
    handler = ClockEventHandler(self);
    self.canvas.setup("below", handler);
    self.canvas.set_size(width, height);
    self.canvas.set_position(Gtk.WindowPosition.CENTER);
    
    self.width = width;
    self.height = height;

  def refresh_thread(self):
    self.canvas.redraw();
    return self.canvas.get_mapped();

  def show(self):
    self.canvas.show();
    GLib.timeout_add(500, self.refresh_thread)

  def hide(self):
    self.canvas.hide();

class ClockEventHandler(object):
  clock = None;

  def __init__(self, clock):
    self.clock = clock;

  def draw(self, cr):
    now = datetime.datetime.now()
    time = now.time();
    hour_12 = time.hour % 12;
    min_60 = time.minute;
    sec_60 = time.second;

    width = self.clock.width;
    height = self.clock.height;
    if (height > width):
      radius = width / 2;
    else:
      radius = height / 2;
    hour_r = 10;
    min_r = 8;
    sec_r = 6;
    padding = 5;

    # hour
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - hour_r, -math.pi / 2, -math.pi / 2 + math.pi / 6 * hour_12);
    cr.set_line_width(hour_r * 2);
    cr.set_source_rgba(1.0, 1.0, 1.0, 0.5);
    cr.stroke();
    # min
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - hour_r * 2 - padding - min_r, -math.pi / 2, -math.pi / 2 + math.pi / 30 * min_60);
    cr.set_line_width(min_r * 2);
    cr.set_source_rgba(1.0, 1.0, 1.0, 0.5);
    cr.stroke();
    # sec
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - (hour_r + padding + min_r) * 2 - sec_r, -math.pi / 2, -math.pi / 2 + math.pi / 30 * sec_60);
    cr.set_line_width(sec_r * 2);
    cr.set_source_rgba(1.0, 1.0, 1.0, 0.5);
    cr.stroke();
    # text
    pangocairo_context = pangocairo.CairoContext(cr)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    layout = pangocairo_context.create_layout();
    layout.set_alignment("center");
    layout.set_markup("<span font='Monospace 24'>" + time.strftime("%I%M%S") + "</span>\n" + 
                      "<span font='Monospace 20'>" + now.strftime("%y%m%d") + "</span>");
    size = layout.get_pixel_size();
    cr.move_to((width - size[0]) / 2, (height - size[1]) / 2);
    cr.set_source_rgba(1.0, 1.0, 1.0, 0.7);
    pangocairo_context.update_layout(layout)
    pangocairo_context.show_layout(layout)
