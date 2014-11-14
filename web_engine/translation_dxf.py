#!/usr/bin/env python
#coding:utf-8
# Based on the example copydxf from   mozman -- <mozman@gmx.at>

import sys
import time

from ezdxf import readfile

def translation_dxf(fromfile, tofile, x, y):
    starttime = time.time()
    dwg = readfile(fromfile)
    #print "dwg is type:" + str(type(dwg))
    translation_x_y(dwg, x, y)
    dwg.saveas(tofile)
    endtime = time.time()
    print('Operation time: %.2f seconds' % (endtime-starttime) )

def translation_x_y(dwg, x, y):
    """Given a dwg object, translate x and y coordinates of everything"""
    x = float(x)
    y = float(y)
    #: :type dwg: ezdxf.drawing.Drawing
    for entity in dwg.entities:
        #print "Entity of type: " + str(entity.dxftype())
        if "LINE" == entity.dxftype():
            # This is madness for accesing!
            sx, sy, sz = entity.get_dxf_attrib('start') # I found it in the docs, I actually couldnt find it in attribs
            ex, ey, ez = entity.get_dxf_attrib('end')
            #print "Initial Start -> End"
            #print str((sx, sy, sz)) + " -> " + str((ex, ey, ez))
            
            entity.set_dxf_attrib('start', (sx + x, sy + y, sz))
            entity.set_dxf_attrib('end', (ex + x, ey + y, ez))
            
            #print "Modified Start -> End (+" + str(x) + ", +" + str(y) + ")"
            #print str(entity.get_dxf_attrib('start')) + " -> " + str(entity.get_dxf_attrib('end'))
            #print
        elif "ARC" == entity.dxftype():
            cx, cy, cz = entity.get_dxf_attrib('center')
            #print "Initial center"
            #print str((cx, cy, cz))
            
            entity.set_dxf_attrib('center', (cx + x, cy + y, cz))

            #print "Modified center (+" + str(x) + ", +" + str(y) + ")"
            #print entity.get_dxf_attrib('center')
            #print
        else:
            print "I don't know this entity type..."


if __name__=='__main__':
    print "Executing translation..."
    if len(sys.argv) != 5:
        print "Usage:"
        print sys.argv[0] +  " input.dxf output.dxf x_coords y_coords"
        print "\n I.E.:\n" + sys.argv[0] + " /home/me/mydxf.dxf /home/me/translationeddxf.dxf 50 100"
    else:
        translation_dxf(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    