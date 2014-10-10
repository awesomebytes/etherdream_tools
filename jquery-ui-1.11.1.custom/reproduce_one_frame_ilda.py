#!/usr/bin/env python
#
# j4cDAC test code
#
# Copyright 2011 Jacob Potter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import ILDA
from ILDA import readFrames, readFirstFrame
import dac

#dac.find_dac()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage:"
        print sys.argv[0] + " filename"
        exit(0)
    filename = sys.argv[1]

    print "Finding DAC..."
    d = dac.DAC(dac.find_first_dac())
    print "DAC found!"
    
    f = open(sys.argv[1], 'rb')
    first_frame = readFirstFrame(f)
    f.close()
    try: 
        d.play_stream(first_frame)
    except Exception, e:
        print "Exception : " + str(e)
        exit(0)
