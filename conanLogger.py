#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging
import sys
import datetime




class S(BaseHTTPRequestHandler):
#using now() to get current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    timeString = str(current_time)
    timeString = timeString.replace(":", "-")
    logfileName="conanchatlog.txt"+"_"+str(timeString)+".txt"
    logfile=logfileName
    logging.basicConfig(filename=logfile,
        filemode='a',
        format='%(asctime)s, %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logstring = str(format(self.path))
        logstring = logstring.replace("/?sender=", "")
        logstring = logstring.replace("&message=", ": ")
        logstring = logstring.replace("%20", " ")
        logstring = logstring.replace("%2C", ",")
        logstring = logstring.replace("%2E", ".")
        logstring = logstring.replace("%28", "(")
        logstring = logstring.replace("%29", ")")
        logstring = logstring.replace("%21", "!")
        logstring = logstring.replace("%3F", "?")
        logstring = logstring.replace("%2B", "+")
        logstring = logstring.replace("%0A", " NEWLINE: ")
        logstring = logstring.replace("%2A", "*")
        logstring = logstring.replace("%27", "'")
        logstring = logstring.replace("%2F", "/")
        logstring = logstring.replace("%22", "\"")
        logstring = logstring.replace("%3A", ":")
        logstring = logstring.replace("%3C", "<")
        logstring = logstring.replace("%3E", ">")
        logstring = logstring.replace("%3B", ";")
        logstring = logstring.replace("%3D", "=")
        logstring = logstring.replace("%2D", "-")
        logstring = logstring.replace("%7E", "~")
        logging.info(logstring)
        #self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
