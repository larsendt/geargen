import svgwrite
import sys
import math

class Gear(object):
    def __init__(self, n_teeth, pitch_diameter):
        self.n_teeth = n_teeth
        self.pd = pitch_diameter
        d = self.pd / 10.0
        self.od = self.pd + d
        self.id = self.pd - d
        self.center = (self.od / 2.0, self.od / 2.0)

def docsize(od):
    return ("%fmm" % od, "%fmm" % od)

def tooth(dwg, gear, angle):
    pergear = 360.0 / gear.n_teeth

    left_angle = angle - (pergear / 4.0)
    right_angle = angle + (pergear / 4.0)

    start = (gear.od/2.0, 0)
    end = (gear.od/2.0, gear.od - gear.pd)

    c_rotate = "rotate(%f, %f, %f)" % (angle, gear.od/2.0, gear.od/2.0)
    l_rotate = "rotate(%f, %f, %f)" % (left_angle, gear.od/2.0, gear.od/2.0)
    r_rotate = "rotate(%f, %f, %f)" % (right_angle, gear.od/2.0, gear.od/2.0)
    
    g = dwg.g()

    cl = dwg.line(start=start, end=end, stroke="gray", transform=c_rotate)
    g.add(cl)

    ll = dwg.line(start=start, end=end, stroke="black", transform=l_rotate)
    g.add(ll)

    rl = dwg.line(start=start, end=end, stroke="black", transform=r_rotate)
    g.add(rl)

    return g

def teeth(dwg, gear):
    ret = []
    for i in range(gear.n_teeth):
        angle = i * (360.0 / gear.n_teeth) 
        ret.append(tooth(dwg, gear, angle))
    return ret 

def main():
    gear = Gear(12, 250)

    dwg = svgwrite.Drawing("test.svg", profile="full", size=docsize(gear.od))
    # pitch diameter circle
    dwg.add(dwg.circle(center=gear.center, r=gear.pd/2.0, stroke="gray", fill="none"))
    # outer diameter circle
    dwg.add(dwg.circle(center=gear.center, r=gear.od/2.0, stroke="gray", fill="none"))
    # inner diameter circle
    dwg.add(dwg.circle(center=gear.center, r=gear.id/2.0, stroke="black", fill="none"))

    for tooth in teeth(dwg, gear):
        dwg.add(tooth)

    dwg.save()
    
if __name__ == "__main__":
    main()
