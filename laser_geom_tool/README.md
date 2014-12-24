This is a GUI for sending OSC messages with the coordinates of the corners to the
etherdream DAC as explained: http://ether-dream.com/userguide.html

![GUI screenshot](https://raw.githubusercontent.com/awesomebytes/etherdream_tools/master/laser_geom_tool/GUI_screenshot.png "GUI PyQt4 screenshot")

Done with PyQt4 using designer (5.3).

Tested with the tool (that comes with the liblo library, sudo apt-get install python-liblo):
	dump_osc 60000


Maybe needed:

	sudo apt-get install pyqt-tools pyqt4-dev-tools

To generate a new library of the GUI if you edit laser_borders.ui with Qt designer:

	pyuic4 laser_borders.ui > laser_borders.py

Bonus: Learnt how to do it following the following tutorials:

http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/

http://www.rkblog.rk.edu.pl/w/p/extending-pyqt4-text-editor/
