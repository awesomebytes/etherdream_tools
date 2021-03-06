etherdream_tools
================

A web interface for the etherdream DAC mostly in Python interfacing with DXF and ILDA files to stream them.
It lets you choose a dxf file to be converted to ILDA (with translation if needed) or an ILDA file and stream it with a laser. Also set the laser PPS dynamically and stop the projection.

![Web interface screenshot](https://raw.githubusercontent.com/awesomebytes/etherdream_tools/master/interface_ss.jpg "Web interface screenshot")

Just run ```web_engine/webserver.py``` and go to [localhost 8080 port](http://localhost:8080) on your browser. By default it needs no DAC connected to test the web interface. To change that go to that file and modify ```USE_DAC = False``` to ```True```.

===

To use you need to have installed the Python libraries (hints for Ubuntu 12.04 Python 2.7):

**liblo**

```sudo apt-get install python-liblo```

**ezdxf**

```sudo pip install ezdxf```

The tool ```sitter.py``` is the official little GUI for finding the DAC IP (and some extra info).

===

In the web_engine folder you can find all the candy:

```ILDA.py``` gives the ability to open ILDA files

```dac.py``` is the interface with etherdream DAC

===

In example_files:

```watch.py``` and ```talk.py``` are the examples provided in [the official j4cDAC repo](https://github.com/j4cbo/j4cDAC) in the tools folder.
