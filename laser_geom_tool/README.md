This is a GUI for sending osc messages with the coordinates of the corners to the
etherdream DAC as explained: http://ether-dream.com/userguide.html

![GUI screenshot](https://raw.githubusercontent.com/awesomebytes/etherdream_tools/master/laser_geom_tool/GUI_screenshot.png "GUI PyQt4 screenshot")

Done with PyQt4 using designer (5.3).

Maybe needed:
sudo apt-get install pyqt-tools pyqt4-dev-tools

To generate a new library of the GUI:

pyuic4 laser_borders.ui > laser_borders.py

