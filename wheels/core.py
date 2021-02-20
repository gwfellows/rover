from solid import *
from solid.utils import *
import sys
from math import cos, radians, sin, pi
from euclid3 import Point3

SEGMENTS = 45


def toroidial_helix_coil(rad=25.4-2, pitch = (2*pi*((6*25.4)/2-(25.4-2/2)-2))/30, outer_rad=(6*25.4)/2-(25.4-2/2)-2, segments=SEGMENTS):
    h = 2*pi*outer_rad
    a = rad
    b = pitch/(2*pi)
    outline = []
    for i in range(segments):
        theta = 2*pi*(i/segments)
        t = (i/segments*h)/b
        x = a*cos(t)+outer_rad
        y = a*sin(t)
        z = 0#b*t
        # then rotate
        x, z = x*cos(theta) - z*sin(theta), x*sin(theta) + z*cos(theta)

        outline.append(Point3(x, y, z))

    return outline


def circle(r=10, segments=SEGMENTS):
    pts = []
    for i in range(segments):
        angle = 2*pi*(i/segments)
        pts.append(Point3(r * cos(angle), r * sin(angle), 0))
    return pts


def core():
    shape = circle(segments=10, r=2)
    path = toroidial_helix_coil(segments = 1000)
    extruded = extrude_along_path(shape_pts=shape, path_pts=path)

    cyl = rot_z_to_y(cylinder(d=(6*25.4)-3*25.4, h=25.4, center=True))
    cyl -= forward(25.4/2-5)(
        rot_z_to_neg_y(cylinder(d1 = 25.4, d2 = 60, h=30, center=False))
    )
    cyl -= rot_z_to_neg_y(cylinder(d = ((1/4)*25.4)+0.3, h=200, center=True))

    for i in range(4):
        cyl -= rotate([0,i*(360/4),0])(
            right(8)(
                rot_z_to_neg_y(
                    cylinder(d=3.3, h=100, center=True)
                    )
            )
        )

    return (cyl-(extruded)).add_param('$fn', SEGMENTS)


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None
    a = core()
    file_out = scad_render_to_file(a, out_dir=out_dir, include_orig_code=True)
    print(f"{__file__}: SCAD file written to: \n{file_out}")