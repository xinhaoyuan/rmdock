gmail_username = "test@gmail.com";
gmail_password = "test-secret.com";

class LambdaMonitor(object):
    lbd = None;
    def __init__(self, lbd):
        self.lbd = lbd;
    def get(self):
        return self.lbd();

import os;
import cairo;

path = os.path.dirname(__file__) + "/..";

gmail_icon = cairo.ImageSurface.create_from_png(path + "/img/gmail-icon-i.png");
data = bytearray(gmail_icon.get_data());
for y in xrange(0, gmail_icon.get_height()):
    for x in xrange(0, gmail_icon.get_width()):
        pos = y * gmail_icon.get_stride() + x * 4;
        data[pos]     = int(data[pos] * 0.7);
        data[pos + 1] = int(data[pos + 1] * 0.7);
        data[pos + 2] = int(data[pos + 2] * 0.7);
        data[pos + 3] = int(data[pos + 3] * 0.7);
gmail_icon = cairo.ImageSurface.create_for_data(
    data, gmail_icon.get_format(), 
    gmail_icon.get_width(), gmail_icon.get_height(), gmail_icon.get_stride());

def config_monitor(mid, rect):
    from meter import Meter;
    from linear_meter_widget import LinearMeterWidget;
    from circle_meter_widget import CircleMeterWidget;
    from surface_widget import SurfaceWidget;
    from pango_widget import PangoWidget;
    from monitor import Monitor;
    from datetime import datetime;
    import math;
    import cairo;

    c = Meter(300, 300);
    c.add_widget(LinearMeterWidget(LambdaMonitor(lambda : Monitor.get().cpu_usage), 
                                   145, 6, color = (1,1,1), alpha = 0.5,
                                   gravity = LinearMeterWidget.GRAVITY_EAST),
                 145, 300, 1, 1);
    c.add_widget(LinearMeterWidget(LambdaMonitor(lambda : Monitor.get().pmem_usage),
                                   145, 6, color = (1,1,1), alpha = 0.5,
                                   gravity = LinearMeterWidget.GRAVITY_WEST),
                 155, 300, -1, 1);
    c.add_widget(CircleMeterWidget(LambdaMonitor(lambda : (datetime.now().time().hour % 12) / 12.0), 
                                   140, 6, -math.pi / 2 + math.pi / 10, -math.pi / 2 - math.pi / 10,
                                   color=(1,1,1), alpha = 0.5, style = CircleMeterWidget.STYLE_SEGMENT),
                 150, 150, 0, 0);
    c.add_widget(CircleMeterWidget(LambdaMonitor(lambda : datetime.now().time().minute / 60.0 + datetime.now().time().second / 3600.0),
                                   128, 10, -math.pi / 2, -math.pi / 2,
                                   color=(1,1,1), alpha = 0.5),
                 150, 150, 0, 0);
    c.add_widget(CircleMeterWidget(LambdaMonitor(lambda : datetime.now().time().second / 60.0),
                                   112, 10, -math.pi / 2 - math.pi / 10, -math.pi / 2 + math.pi / 10,
                                   style=CircleMeterWidget.STYLE_SEGMENT, color=(1,1,1), alpha = 0.5), 
                 150, 150, 0, 0);
    c.add_widget(PangoWidget(LambdaMonitor(lambda :
                                           "<span font='Monospace 25'>" + datetime.now().strftime("%H%M%S") + "</span>\n" +
                                           "<span font='Monospace 20'>" + datetime.now().strftime("%y%m%d") + "</span>"),
                             color=(1,1,1), alpha = 0.5, alignment = "center"), 
                 150, 150, 0, 0);
            
    c.add_widget(PangoWidget(LambdaMonitor(lambda :
                                           "<span font='Monospace 20'>" + str(Monitor.get().gmail_unread_count) + "</span>"),
                             color=(1,1,1), alpha = 0.5, alignment = "center"), 
                 gmail_icon.get_width(), 0, -1, -1);

    c.add_widget(SurfaceWidget(gmail_icon, gmail_icon.get_width(), gmail_icon.get_height()),
                 0, 0, -1, -1);

    c.get_window().move(rect.x + (rect.width - c.width) / 2,
                        rect.y + (rect.height - c.height) / 2);
    c.show();
