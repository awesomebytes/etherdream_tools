#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test copy dxf file
# Created: 12.03.2011
# Copyright (C) , Manfred Moitzi
# License: MIT License

import sys
import io
import time

from ezdxf import readfile
import ezdxf

def copydxf(fromfile, tofile):
    starttime = time.time()
    dwg = readfile(fromfile)
    print "dwg is type:" + str(type(dwg))
    translate_x_y(dwg, 50.0, 100.0)
    dwg.saveas(tofile)
    endtime = time.time()
    print('copy time: %.2f seconds' % (endtime-starttime) )

def translate_x_y(dwg, x, y):
    """Given a dwg object, translate x and y coordinates of everything"""
    #: :type dwg: ezdxf.drawing.Drawing
    for entity in dwg.entities:
    	print "Entity of type: " + str(type(entity))
        print entity
        if "Line" in str(type(entity)):
        	print "Modify start and end point"
        elif "Arc" in str(type(entity)):
        	print "Modify center point"
        else:
        	print "I don't know this entity type..."


if __name__=='__main__':
    print "Executing copy"
    copydxf(sys.argv[1], sys.argv[2])
    