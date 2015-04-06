#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

import os.path
import json
import thread
import sys
import threading
from threading import Thread

import math
import config
import log
import time
clients = []
global data_global = 0

class SilentErrorHandler(tornado.web.ErrorHandler):
    def _log(self): pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(origin, args):
        return True
        
    def open(self):
        clients.append(self)
    
    def on_close(self):
        clients.remove(self);
    
    def on_message(self,message):
        pass


class DataSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(origin, args):
        return True
        
    def open(self):
        pass
    
    def on_close(self):
        pass
    
    def on_message(self,message):
        try:
            json_array = json.loads(message)
            if json_array["pw"] == config.password:
                 data_global = json_array["data"];
                 WindDataSender(json_array["data"])
            else:
                self.write_message("error bad request")
                log.error("bad request! (wrong password: " + json_array["pw"] + ")")
                return
        except:
            self.write_message("error bad request")
            log.error("bad request!")
            return

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

def RealtimeWindDaterFormater(data):
    data = "{\"mode\":\"update\",\"data\":" + str(data) + "}";
    return data

def writeWindData(data):
    
    pass

def WindDataSender(data):
    writeWindData(data)
    for client in clients:
        client.write_message(RealtimeWindDaterFormater(data))

def main():
    # handlers
    handlers = [
        (r"/", IndexHandler),
        (r"/ws", WebSocketHandler),
        (r"/datasocket", DataSocketHandler),
        (r'/favicon.ico', SilentErrorHandler, dict(status_code=404))
    ]
    # settings
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    if config.ssl == True:
        httpserversettings = dict(
            ssl_options = config.ssl_options,
        )
    else:
        httpserversettings = dict()
    # init and start http-server
    app = tornado.web.Application(handlers, **settings)
    server = tornado.httpserver.HTTPServer(app, **httpserversettings)
    server.listen(config.port)
    
    # ioloop
    tornado.ioloop.IOLoop.instance().start()

hour_wind = open("hour_wind.txt", "w")
day_wind = open("day_wind.txt", "w")
year_wind = open("year_wind.txt", "w")

def hour():
	
	while 1:	

		x=0

		for x in range (0,59):
			hour_wind.write(str(data_global) + "\n")
			hour_wind.flush()
			time.sleep(60)
			#time.sleep(2)			
			x+=1

		hour_wind.seek(0)
		hour_wind.truncate()

def day():
	
	while 1:	
		
		with open("hour_wind.txt") as f:
			numbers = []
			for line in f:
				numbers.append(int(line))
			numbers.sort()
		
		count = len(numbers)
		#max_num = max(numbers)
		#min_num = min(numbers)
		sum_of_nums = sum(numbers)
		median1 = numbers[len(numbers)//2]
		a = str(median1)
		y = 0
		
		for y in range (0,23):
			day_wind.write("%s\n" % (a))
			day_wind.flush()
			time.sleep(3600)
			#time.sleep(2)
			y+=1

		hour_wind.seek(0)
		hour_wind.truncate()

def year():

	while 1:

		with open("day_wind.txt") as g:
			numbers = []

			for line in g:
				numbers.append(int(line))
			numbers.sort()

		count = len(numbers)
		#max_num = max(numbers)
		#min_num = min(numbers)
		sum_of_nums = sum(numbers)
		median2 = numbers[len(numbers)//2]
		b = str(median2)		
		z = 0

		for z in range (0,23):
			year_wind.write("%s\n" % (b))
			year_wind.flush()
			time.sleep(86400)	
			#time.sleep(2)
			z+=1


if __name__ == "__main__":
    try:
        main()
        Thread(target = hour).start()
        Thread(target = day).start()
        Thread(target = year).start()
    except KeyboardInterrupt:
        print ""
        log.info("Server stopped")
        exit()
