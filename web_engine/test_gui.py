#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This example shows text which 
is entered in a QtGui.QLineEdit
in a QtGui.QLabel widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys
from PyQt4 import QtGui, QtCore

#!/usr/bin/python
import liblo
import dac

USE_DAC = False

class Example(QtGui.QWidget):
    
    def __init__(self, target):
        super(Example, self).__init__()
        self.target = target
        
        self.initUI()
        
    def initUI(self):      

        #self.lbl = QtGui.QLabel(self) # text
        #self.qle_tl_x_name = QtGui.QTextItem(self)
        #self.qle_tl_x_name.se
        self.qle_tl_x = QtGui.QLineEdit(self) # line edit
        self.qle_tl_x.setText("1.0")
        self.qle_tl_y = QtGui.QLineEdit(self)
        self.qle_tl_y.setText("1.0")
        self.qle_tr = QtGui.QLineEdit(self) 
        self.qle_bl = QtGui.QLineEdit(self) 
        self.qle_br = QtGui.QLineEdit(self) 
        
        self.qle_tl_x.move(40, 50)
        self.qle_tl_y.move(120, 50)
        self.qle_tr.move(60, 150)
        self.qle_bl.move(60, 200)
        self.qle_br.move(60, 250)
        #self.lbl.move(60, 40)

        self.qle_tl_x.textChanged[str].connect(self.onChanged_tl_x)
        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QtGui.QLineEdit')
        self.show()
        
    def onChanged_tl_x(self, text):
        float_val = float(text)
        tl_y = self.qle_tl_y.text()
        float_tl_y = float(tl_y)
        print "Sending:" + str(float_val) + " to tl_x and tl_y was: " + str(float_tl_y)
        if USE_DAC:
            liblo.send(target, "/geom/tl", float(-1), float(1))
        
def main(target):
    
    app = QtGui.QApplication(sys.argv)
    ex = Example(target)
    sys.exit(app.exec_())


if __name__ == '__main__':
    target = None
    if USE_DAC:
        print "Trying to find DAC"
        DAC_IP = dac.find_first_dac()
        print "Found DAC at " + str(DAC_IP)
        dac_obj = dac.DAC(DAC_IP)
        print "Sending maximum geometry to " + str(DAC_IP)
        target = liblo.Address(DAC_IP, 60000)
        liblo.send(target, "/geom/tl", float(-1), float(1))
        liblo.send(target, "/geom/tr", float(1), float(1))
        liblo.send(target, "/geom/bl", float(-1), float(-1))
        liblo.send(target, "/geom/br", float(1), float(-1))
    print "Starting GUI"
    main(target)