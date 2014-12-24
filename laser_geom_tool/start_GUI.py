#!/usr/bin/python
import sys
from PyQt4 import QtCore, QtGui
from laser_borders import Ui_laser_main
import liblo

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_laser_main()
        self.ui.setupUi(self)
        # here we connect signals with our slots
        QtCore.QObject.connect(self.ui.button_send,QtCore.SIGNAL("clicked()"), self.send_message)
        QtCore.QObject.connect(self.ui.button_searchdac,QtCore.SIGNAL("clicked()"), self.search_dac)

        self.dac_ip = None

    def send_message(self):
        tl_x = float ( self.ui.tl_x.value() )
        tl_y = float ( self.ui.tl_y.value() )
        tr_x = float ( self.ui.tr_x.value() )
        tr_y = float ( self.ui.tr_y.value() )
        bl_x = float ( self.ui.bl_x.value() )
        bl_y = float ( self.ui.bl_y.value() )
        br_x = float ( self.ui.br_x.value() )
        br_y = float ( self.ui.br_y.value() )
        print "Sending:"
        print "tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y"
        print tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y
        print "Sending to: " + str(self.ui.edit_ip.text())
        target = liblo.Address(str(self.ui.edit_ip.text()), 60000)
        liblo.send(target, "/geom/tl", tl_x, tl_y)
        liblo.send(target, "/geom/tr", tr_x, tr_y)
        liblo.send(target, "/geom/bl", bl_x, bl_y)
        liblo.send(target, "/geom/br", br_x, br_y)

    def search_dac(self):
        import dac
        self.dac_ip = dac.find_first_dac()
        print "Found DAC at " + str(self.dac_ip)
        self.ui.edit_ip.setText(str(self.dac_ip))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())