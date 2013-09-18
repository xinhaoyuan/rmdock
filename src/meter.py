from gi.repository import GLib, Gtk, Gdk, Pango;

import threading;
import math;
import cairo;
import datetime;
import pango, pangocairo;
from canvas import Canvas;
from monitor import Monitor;
import os;

path = os.path.dirname(__file__) + "/..";

class Meter(object):

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
    handler = MeterEventHandler(self);
    self.canvas.setup("below", handler);
    self.canvas.set_size(width, height);
    
    self.width = width;
    self.height = height;
    self.hour_radius = 4;
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

class MeterEventHandler(object):
  meter = None;
  left_fill_path = None;
  right_fill_path = None;
  gmail_icon_surface = None;

  def __init__(self, meter):
    self.meter = meter;

  def draw(self, cr):
    now = datetime.datetime.now()
    time = now.time();
    hour_12 = time.hour % 12;
    min_60 = time.minute;
    sec_60 = time.second;

    width = self.meter.width;
    height = self.meter.height;
    if (height > width):
      radius = width / 2 - self.meter.padding;
    else:
      radius = height / 2 - self.meter.padding;
    hour_r = self.meter.hour_radius;
    min_r = self.meter.min_radius;
    sec_r = self.meter.sec_radius;
    padding = self.meter.padding;

    # hour
    cr.new_path();
    angle_h = -math.pi / 2 + math.pi / 6 * hour_12;
    cr.arc(width / 2, height / 2, radius - hour_r - padding, angle_h + math.pi / 30, angle_h - math.pi / 30);
    cr.set_line_width(hour_r * 2);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    cr.stroke();
    # min
    cr.new_path();
    cr.arc(width / 2, height / 2, radius - hour_r * 2 - padding * 2 - min_r, -math.pi / 2, -math.pi / 2 + math.pi / 1800 * (min_60 * 60 + sec_60));
    cr.set_line_width(min_r * 2);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    cr.stroke();
    # sec
    cr.new_path();
    angle_s = -math.pi / 2 + math.pi / 30 * sec_60;
    cr.arc(width / 2, height / 2, radius - (hour_r + min_r) * 2 - padding * 3 - sec_r, angle_s - math.pi / 10, angle_s + math.pi / 10);
    cr.set_line_width(sec_r * 2);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
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
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    pangocairo_context.update_layout(layout);
    pangocairo_context.show_layout(layout);

    # gmail count
    if (self.gmail_icon_surface == None):
      image_surface = cairo.ImageSurface.create_from_png(path + "/img/gmail-icon-i.png");
      data = bytearray(image_surface.get_data());
      for y in xrange(0, image_surface.get_height()):
        for x in xrange(0, image_surface.get_width()):
          pos = y * image_surface.get_stride() + x * 4;
          data[pos] /= 2
          data[pos + 1] /= 2;
          data[pos + 2] /= 2;
          data[pos + 3] /= 2;
      self.gmail_icon_surface = cairo.ImageSurface.create_for_data(data, image_surface.get_format(), image_surface.get_width(), image_surface.get_height(), image_surface.get_stride());
      image_surface.finish();
                      
    cr.move_to(0,0);
    cr.set_source_surface(self.gmail_icon_surface);
    cr.paint();

    layout.set_alignment("left");
    layout.set_markup("<span font='Monospace 20'>" + str(Monitor.get().gmail_unread_count) + "</span>");
    cr.move_to(self.gmail_icon_surface.get_width(), 0);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    pangocairo_context.update_layout(layout);
    pangocairo_context.show_layout(layout);

    # fill the left bar with cpu usage
    if (self.left_fill_path == None):
      cr.new_path();
      cr.move_to(width / 2 - padding, height);
      cr.arc(width / 2, height / 2, radius, math.pi / 2 + math.asin(float(padding) / radius), math.pi - math.asin(0.5));
      cr.line_to(0, height / 2 + radius / 2);
      cr.line_to(0, height);
      cr.close_path();
      self.left_fill_path = cr.copy_path();
    else:
      cr.new_path();
      cr.append_path(self.left_fill_path);

    cr.save();
    cr.set_source_rgba(1,1,1,0.1);
    cr.fill_preserve();
    cr.clip();
    bar_length = (width / 2 - padding) * (Monitor.get().cpu_usage);
    cr.rectangle((width / 2 - padding) - bar_length, height / 2, bar_length, height / 2);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    cr.fill();
    cr.restore();

    # fill the right bar with cpu usage
    if (self.right_fill_path == None):
      cr.new_path();
      cr.move_to(width / 2 + padding, height);
      cr.arc_negative(width / 2, height / 2, radius, math.pi / 2 - math.asin(float(padding) / radius), math.asin(0.5));
      cr.line_to(width, height / 2 + radius / 2);
      cr.line_to(width, height);
      cr.close_path();
      self.right_fill_path = cr.copy_path();
    else:
      cr.new_path();
      cr.append_path(self.right_fill_path);

    cr.save();
    cr.set_source_rgba(1,1,1,0.1);
    cr.fill_preserve();
    cr.clip();
    bar_length = (width/ 2 - padding) * (Monitor.get().pmem_usage);
    cr.rectangle(width / 2 + padding, height / 2, bar_length, height / 2);
    cr.set_source_rgba(self.meter.fill_color[0], self.meter.fill_color[1], self.meter.fill_color[2], self.meter.opacity);
    cr.fill();
    cr.restore();
    


