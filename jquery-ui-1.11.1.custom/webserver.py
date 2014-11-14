#!/usr/bin/python
# Example from http://www.acmesystems.it/python_httpserver
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import urlparse
import cgi
import time
import subprocess

import liblo
import dac
from ILDA import readFrames, readFirstFrame

PORT_NUMBER = 8080

USE_DAC = False


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

    def __init__(self, dac_object, *args):
        print "Initializing my handler"
        if USE_DAC:
            self.dac_obj = dac_object
        BaseHTTPRequestHandler.__init__(self, *args)


    def address_string(self):
        # http://stackoverflow.com/questions/2617615/slow-python-http-server-on-localhost
        # workaround for slow network access (phone)
        host, port = self.client_address[:2]
        #return socket.getfqdn(host) # default, slow, behaviour
        return host

    def do_POST(self):
        print "Got a POST"
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        filename = form['file'].filename
        if form['x_coord'].value == '':
            x_coord = 0.0
        else:
            x_coord = float(form['x_coord'].value) # FieldStorage('x_coord', None, '10')

        if form['y_coord'].value == '':
            y_coord = 0.0
        else:
            y_coord = float(form['y_coord'].value)

        print "\n\n   Translation coords: x_coord: " + str(x_coord) + " y_coord: " + str(y_coord)
        data = form['file'].file.read()
        print "Saving at: " + curdir + sep + 'uploaded/' + filename
        open(curdir + sep + 'uploaded/' + filename, "wb").write(data)

        uploaded_sentence = ""  # Sentence must be empty!! (or js does not work correctly)#"uploaded %s, thanks"%filename
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(uploaded_sentence))
        self.end_headers()
        #self.wfile.write(uploaded_sentence) 

        # If the file has extension dxf, do translation and convert it
        if filename.endswith('.dxf'):
            original_filename = curdir + sep + 'uploaded/' + filename
            if x_coord == 0.0 or y_coord == 0.0:
                print "Not translating anywhere"
            else:
                translation_filename = curdir + sep + 'uploaded/' + filename.replace('.dxf', '') + "_translation.dxf"
                translation_process = subprocess.Popen(["python", curdir + sep + "translation_dxf.py", 
                                  original_filename,
                                  translation_filename,
                                  str(x_coord), str(y_coord) ])
                translation_process.wait()
            ilda_filename = curdir + sep + 'uploaded/' + filename.replace('.dxf', '.ilda')
            
            print "Transforming from dxf to ILDA..."
            dxf_to_ilda_process = subprocess.Popen([curdir + sep + "LaserBoy_dxf_to_ilda_tool", original_filename, ilda_filename])
            dxf_to_ilda_process.wait()
            self.file_to_stream = ilda_filename
        elif filename.endswith('.ilda') or filename.endswith('.ild'):
            self.file_to_stream = curdir + sep + 'uploaded/' + filename
        else:
            print "Error, not a file to stream, doing nothing"
            return
        # Execute the script that plays one file
        if USE_DAC:
            print "Streaming file"
            subprocess.Popen(["python", curdir + sep + "reproduce_one_frame_ilda.py", self.file_to_stream])
        else:
            print "On debug mode, not streaming file"
    
    #Handler for the GET requests
    def do_GET(self):
        print "Path: " + str(self.path)
        sendReply = False
 
        if self.path=="/":
            mimetype='text/html'
            self.path="/index.html"
            self.path="/index2.html"
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

        if "pps=" in self.path:
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

        if  self.path.endswith("stop"):
            self.send_response(200)
            mimetype='text/html'
            self.send_header('Content-type',mimetype)
            self.end_headers()
            if USE_DAC:
                self.dac_obj.stop()
            self.wfile.write("Stopped laser projection")
            return

        if sendReply == True:
            #Open the static file requested and send it
            print "  Opening: " + str(curdir + sep + self.path)
            f = open(curdir + sep + self.path) 
            print "Sending response 200"
            self.send_response(200)
            print "Sending headers"
            self.send_header('Content-type',mimetype)
            print "Sending end headers"
            self.end_headers()
            print "writting file"
            self.wfile.write(f.read())
            print "Closing"
            f.close()
            print "  Sent file."


        return


# Optinally delete all old dxf ilda and ild files:
#subprocess.Popen(["rm *.dxf *.ilda *.ild"])



dac_obj = None
if USE_DAC:
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