#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

import os.path
import json
import sys
import sqlite3

import math
import config
import log
import time
#is there an error in the config-file?
if config.config_error:
   log.error("there is an error in the config")
   exit()

clients = {}

class SilentErrorHandler(tornado.web.ErrorHandler):
    def _log(self): pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(origin, args):
        return True
        
    def open(self):
        clients[self] = {"send_current_data":True}
    
    def on_close(self):
        del(clients[self]);
    
    def on_message(self,message):
        try:
            json_array = json.loads(message)
        except:
            self.write_message('{"error":"bad_request"}');
            return;
        if json_array.has_key("realtimedata"):
            if json_array["realtimedata"]:
                clients[self] = {"send_current_data":True}
            elif json_array["realtimedata"] == False:
                clients[self] = {"send_current_data":False}
            else:
                self.write_message('{"error":"bad_request"}');
            return

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
        except:
            self.write_message("error bad request")
            log.error("bad request!: (" + message + ")")
            return
        if json_array["pw"] == config.password:
            WindDataWriter(int(json_array["data"]))
            WindDataSender(int(json_array["data"]))
        else:
            self.write_message("error bad request")
            log.error("bad request! (wrong password: " + json_array["pw"] + ")")

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

def RealtimeWindDaterFormater(data):
    data = "{\"mode\":\"update\",\"data\":" + str(data) + "}";
    return data

def WindDataWriter(data):
    c.execute('''INSERT INTO Data VALUES ("''' + str(time.time()) + '''",\'''' + str(data) + '''\')''')
    conn.commit()


def WindDataSender(data):
    for client in clients.keys():
        if clients[client]["send_current_data"] == True:
            client.write_message(RealtimeWindDaterFormater(data))

def main():
    global conn
    global c
    conn = sqlite3.connect(config.db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Data ( Timestamp INTEGER, Data INTEGER);''')
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ""
        log.info("Server stopped")
        exit()

