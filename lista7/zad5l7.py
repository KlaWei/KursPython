import cmath
import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Fractals(Gtk.Window):
    def __init__(self, c):
        super(Fractals, self).__init__()
        self.set_title("Fractal")
        self.set_position(Gtk.WindowPosition.CENTER)
        grid = Gtk.Grid()
        button1 = Gtk.Button(label="OK")
        button1.connect("clicked", self.on_draw)
        self.entryIm = Gtk.Entry()
        self.entryRe = Gtk.Entry()
        labelIm = Gtk.Label()
        labelRe = Gtk.Label()
        labelIm.set_text("Imaginary: ")
        labelRe.set_text("Real: ")
        self.connect("destroy", Gtk.main_quit)
        self.area = Gtk.DrawingArea()
        self.area.set_size_request(500, 500)
        self.area.connect("draw", self.fraktal)

        self.add(grid)
        grid.set_column_spacing(5)
        grid.attach(self.area, 0, 0, 20, 20)
        grid.attach(labelRe, 22, 0, 1, 1)
        grid.attach(self.entryRe, 23, 0, 3, 1)
        grid.attach(labelIm, 22, 1, 1, 1)
        grid.attach(self.entryIm, 23, 1, 3, 1)
        grid.attach(button1, 22, 3, 3, 1)
        self.draw = False
        self.c = c
        self.show_all()

    def on_draw(self, button):
        im = self.entryIm.get_text()
        re = self.entryRe.get_text()

        if im != "" and re != "":
            self.c = complex(float(re), float(im))
        else:
            self.c = complex(-0.70176, -0.3842)

        self.draw = True
        self.queue_draw()
        
    def fraktal(self, widget, cr):
        if self.draw == False:
            cr.set_source_rgb(1, 1, 1)
            cr.paint()
        else:
            width = widget.get_allocation().width
            height = widget.get_allocation().height
            xmax = 2.0
            ymax = 2.0
            xmin = -2.0
            ymin = -2.0
            z = complex(xmin, ymax)
            widthPix = (xmax-xmin)/width
            heightPix = (ymax-ymin)/height

            maxiter = 200
            cr.scale(width/(xmax-xmin), height/(ymax-ymin))
            for i in range(0, height):
                z = complex(xmin, z.imag)
                for j in range(0, width):
                    z1 = complex(z.real, z.imag)
                    iterations = 0
                    while iterations < 200 and (z1.real*z1.real + z1.imag*z1.imag) < 4:
                        z1 = z1*z1 + self.c
                        iterations = iterations + 1

                    if iterations == 200:
                        cr.set_source_rgba(0, 0, 0)
                    else:
                        num = math.sqrt(z1.real*z1.real + z1.imag*z1.imag)
                        color = 256. * math.log2(1.75 + iterations - math.log2(math.log2(num))) / math.log2(maxiter)
                        cr.set_source_rgb(color/255, color/255, 255/255)

                    cr.rectangle(z.real+2.0, z.imag+2.0, widthPix, heightPix)
                    cr.fill()
                    z = complex(z.real + widthPix, z.imag)
                z = complex(z.real, z.imag - heightPix)


if __name__ == "__main__":
    Fractals(complex(-0.70176, -0.3842))
    Gtk.main()
