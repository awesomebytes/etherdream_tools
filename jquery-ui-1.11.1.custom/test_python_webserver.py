#!/usr/bin/python
# Example from http://www.acmesystems.it/python_httpserver
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import urlparse
import cgi
import time
import subprocess

import dac
from ILDA import readFrames, readFirstFrame

PORT_NUMBER = 8080

USE_DAC = False

import ctypes
def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

    def __init__(self, dac_object, *args):
        print "Initializing my handler"
        if USE_DAC:
            self.dac_obj = dac_object
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        print "Got a POST"
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        filename = form['file'].filename
        data = form['file'].file.read()
        print "Saving at: " + curdir + sep + filename
        open(curdir + sep  + filename, "wb").write(data)

        uploaded_sentence = "uploaded %s, thanks"%filename
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(uploaded_sentence))
        self.end_headers()
        #self.wfile.write(uploaded_sentence) 
        self.file_to_stream = curdir + sep  + filename

        # Execute the script that plays one file
        if USE_DAC:
            subprocess.Popen(["python", curdir + sep + "reproduce_one_frame_ilda.py", curdir + sep  + filename])
    
    #Handler for the GET requests
    def do_GET(self):
        print "Path: " + str(self.path)
        sendReply = False
 
        if self.path=="/":
            mimetype='text/html'
            self.path="/index.html"
            sendReply = True
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if self.path.endswith(".png"):
            mimetype='image/png'
            sendReply = True
        if self.path.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True

        if "pps" in self.path:
            o = urlparse.urlparse(self.path)
            params_dict = urlparse.parse_qs(o.query)
            print "Parsed parameters:"
            print urlparse.parse_qs(o.query)
            if params_dict.has_key('pps'):
                pps_num = int ( params_dict['pps'][0] ) # it's a list of one element
            else:
                return
            self.send_response(200)
            mimetype='text/html'
            self.send_header('Content-type',mimetype)
            self.end_headers()
            contentToShow="You asked to change PPS to: " + str(pps_num)
            print contentToShow
            # Set the projector PPS!
            if USE_DAC:
                self.dac_obj.update(0, pps_num) # low water mark 0 (???), PPS given
            #set_pps_via_osc(pps_num) # OSC does not work while streaming
            self.wfile.write(contentToShow)
            return

        if sendReply == True:
            #Open the static file requested and send it
            f = open(curdir + sep + self.path) 
            print "  Opening: " + str(curdir + sep + self.path)
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()


        return

dac_obj = None
if USE_DAC:
    print "Trying to find DAC"
    DAC_IP = dac.find_first_dac()
    print "Found DAC at " + str(DAC_IP)
    dac_obj = dac.DAC(DAC_IP)

streamer_thread = None

def HTTP_handler_with_DAC(*args):
    myHandler(dac_obj, *args)

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), HTTP_handler_with_DAC)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()