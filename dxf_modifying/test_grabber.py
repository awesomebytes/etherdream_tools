#! /usr/bin/env python
import dxfgrabber
import dxfwrite


dxffile = dxfgrabber.readfile("Be1.dxf")
print("DXF version: {}".format(dxffile.dxfversion))
header_var_count = len(dxffile.header) # dict of dxf header vars
layer_count = len(dxffile.layers) # collection of layer definitions
block_definition_count = (len(dxffile.blocks)) #  dict like collection of block definitions
entitiy_count = len(dxffile.entities) # list like collection of entities

print "header_var_count:"
print header_var_count
print "layer_count:"
print layer_count
print "block_definition_count:"
print block_definition_count
print "entitiy_count:"
print entitiy_count


for entity in dxffile.entities:
    print entity.dxftype
    if entity.dxftype == "LINE":
        #: :type entity: entities.Line
        print "Start: " + str(entity.start) + " -> " + "End: " + str(entity.end)
    elif entity.dxftype == "ARC":
        #: :type entity: entities.Arc
        print "Center: " + str(entity.center) + " Start angle: " + str(entity.startangle) + " End angle: " + str(entity.endangle)
    else:
        print "Another type of dxftype: " + str(entity.dxftype)    
        
        