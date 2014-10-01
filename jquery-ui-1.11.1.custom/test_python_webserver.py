#!/usr/bin/python
# Example from http://www.acmesystems.it/python_httpserver
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import urlparse

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    # def do_POST(self):
    #     length = int(self.headers['Content-Length'])
    #     print("HEADERS: ", self.headers)
    #     print (str(length))
    #     print (self.rfile.read(length))
    #     mimetype='text/html'
    #     sendReply = True
    #     contentToShow="you made an ajax request!"
    #     self.send_response(200)
    #     self.send_header('Content-type',mimetype)
    #     self.end_headers()
    #     self.wfile.write(contentToShow)
    #     return

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

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()