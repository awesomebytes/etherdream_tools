#!/usr/bin/python
import liblo
import dac

if __name__ == '__main__':
    print "Trying to find DAC"
    DAC_IP = dac.find_first_dac()
    print "Found DAC at " + str(DAC_IP)
    dac_obj = dac.DAC(DAC_IP)
    print "Sending maximum geometry to " + str(DAC_IP)
    target = liblo.Address(DAC_IP, 60000)
    liblo.send(target, "/geom/tl", int(-1), int(1))
    liblo.send(target, "/geom/tr", int(1), int(1))
    liblo.send(target, "/geom/bl", int(-1), int(-1))
    liblo.send(target, "/geom/br", int(1), int(-1))
    
    