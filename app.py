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
import MySQLdb

import config
import log

clients = []

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
                 WindDataSender(json_array["data"])
            else:
                self.write_message("error bad request")
                return
        except:
            self.write_message("error bad request")
            return

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

def RealtimeWindDaterFormater(data):
    data = data
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
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print ""
        log.info("Server stopped")
 

if __name__ == "__main__":
    main()
