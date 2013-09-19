import cairo;

class SurfaceWidget(object):
  surface = None;
  width = None;
  height = None;

  def __init__(self, surface, width, height):
    self.surface = surface
    self.width   = self.width;
    self.height  = self.height;

  def prepare_surface(self, ext_cr):
    pass
  
  def get_width(self):
    return self.width;
  
  def get_height(self):
    return self.height;

  def get_surface(self):
    return self.surface;
