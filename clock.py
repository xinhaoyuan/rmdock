from gi.repository import GLib, Gtk, Gdk, Pango;

import threading;
import math;
import cairo;
import datetime;
import pango, pangocairo;
from canvas import Canvas;
from monitor import Monitor;

class Clock(object):

  canvas = None;
  handler = None;
  width = None;
  height = None;
  hour_radius = None;
  min_radius = None;
  sec_radius = None;
  padding = 5;
  fill_color = None;
  opacity = None;
  
  def __init__(self, width = 300, height = 300):
    self.canvas = Canvas();
    handler = ClockEventHandler(self);
    self.canvas.setup("below", handler);
    self.canvas.set_size(width, height);
    
    self.width = width;
    self.height = height;
    self.hour_radius = 10;
    self.min_radius = 8;
    self.sec_radius = 6;
    self.padding = 5;
    # self.fill_color = (0.3, 0.7, 0.1);
    self.fill_color = (1.0, 1.0, 1.0);
    self.opacity = 0.5;

  def refresh_thread(self):
    self.canvas.redraw();
    return self.canvas.get_mapped();

  def show(self):
    self.canvas.show();
    GLib.timeout_add(200, self.refresh_thread)

  def hide(self):
    self.canvas.hide();

  def get_window(self):
    return self.canvas.get_window();

class ClockEventHandler(object):
  clock = None;
  left_fill_path = None;

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
      radius = width / 2 - self.clock.padding;
    else:
      radius = height / 2 - self.clock.padding;
    hour_r = self.clock.hour_radius;
    min_r = self.clock.min_radius;
    sec_r = self.clock.sec_radius;
    padding = self.clock.padding;

    # hour
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - hour_r - padding, -math.pi / 2, -math.pi / 2 + math.pi / 6 * hour_12);
    cr.set_line_width(hour_r * 2);
    cr.set_source_rgba(self.clock.fill_color[0], self.clock.fill_color[1], self.clock.fill_color[2], self.clock.opacity);
    cr.stroke();
    # min
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - hour_r * 2 - padding * 2 - min_r, -math.pi / 2, -math.pi / 2 + math.pi / 30 * min_60);
    cr.set_line_width(min_r * 2);
    cr.set_source_rgba(self.clock.fill_color[0], self.clock.fill_color[1], self.clock.fill_color[2], self.clock.opacity);
    cr.stroke();
    # sec
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - (hour_r + min_r) * 2 - padding * 3 - sec_r, -math.pi / 2, -math.pi / 2 + math.pi / 30 * sec_60);
    cr.set_line_width(sec_r * 2);
    cr.set_source_rgba(self.clock.fill_color[0], self.clock.fill_color[1], self.clock.fill_color[2], self.clock.opacity);
    cr.stroke();
    # text
    pangocairo_context = pangocairo.CairoContext(cr)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    layout = pangocairo_context.create_layout();
    layout.set_alignment("center");
    layout.set_markup("<span font='Monospace 24'>" + time.strftime("%H%M%S") + "</span>\n" + 
                      "<span font='Monospace 20'>" + now.strftime("%y%m%d") + "</span>");
    size = layout.get_pixel_size();
    cr.move_to((width - size[0]) / 2, (height - size[1]) / 2);
    cr.set_source_rgba(self.clock.fill_color[0], self.clock.fill_color[1], self.clock.fill_color[2], self.clock.opacity);
    pangocairo_context.update_layout(layout);
    pangocairo_context.show_layout(layout);

    # fill the left bar with cpu usage
    if (self.left_fill_path == None):
      cr.new_path();
      cr.move_to(width / 2, height);
      cr.arc(width / 2, height / 2, radius, math.pi / 2, math.pi);
      cr.line_to(width / 2 - radius, height / 2);
      cr.line_to(0, height / 2);
      cr.line_to(0, height);
      cr.close_path();
      self.left_fill_path = cr.copy_path();
    else:
      cr.new_path();
      cr.append_path(self.left_fill_path);

    cr.save();
    cr.clip();
    bar_length = width / 2 * (Monitor.get().cpu_usage);
    cr.rectangle(width / 2 - bar_length, height / 2, bar_length, height / 2);
    cr.set_source_rgba(self.clock.fill_color[0], self.clock.fill_color[1], self.clock.fill_color[2], self.clock.opacity);
    cr.fill();
    cr.restore();
    


