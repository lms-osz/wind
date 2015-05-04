#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

# tornado/web stuff
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
# libarys
import os.path
import json
import sys
import sqlite3
import math
import time
# own files
import config
import log

if config.config_error:
   log.error("an error occurred, please check the config")
   exit()

clients = {}

# handling an websocket-request at "/ws"
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(origin, args):
        return True
        
    def open(self):
        clients[self] = {"send_current_data":True}
    
    def on_close(self):
        del(clients[self]);
    
    def on_message(self,message):
        try:
            # try get the value of the json string
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

# handling an websocket-request at "/datasocket"
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
            WindDataWriter(json_array)
            WindDataSender(json_array)
        else:
            self.write_message("error bad request")
            log.error("bad request! (wrong password: " + json_array["pw"] + ")")

# handling an http request at "/"
class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

class DocHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("doc.html")

class WebcamHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("webcam.html")

class AboutHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("about.html")

def WindDataWriter(data):
    try:
        conn.execute("INSERT INTO Data VALUES ('" + str(round(time.time())) + "','" + str(data["data"][0]["wind"]) + "','" + str(data["data"][0]["Ubatt"]) + "','" + str(data["data"][0]["Ibatt"]) + "');")
    except Exception:
        pass
    conn.commit()


def WindDataSender(json_array):
    data = "{\"mode\":\"update\",\"data\":[{\"wind\":" + str(json_array["data"][0]["wind"]) + ",\"Ubatt\":" + str(json_array["data"][0]["Ubatt"]) + ",\"Ibatt\":" + str(json_array["data"][0]["Ibatt"]) + "}]}";
    for client in clients.keys():
        if clients[client]["send_current_data"] == True:
            client.write_message(data)

def main():
    log.info("Starting server . . .")
    global conn
    # connecting to the sqlite file
    conn = sqlite3.connect(config.db_file)
    # creating table "data" if not exits
    conn.execute('''CREATE TABLE IF NOT EXISTS Data ( Timestamp INTEGER, Wind INTEGER, Ubatt INTEGER, Ibatt INTEGER, PRIMARY KEY(Timestamp));''')
    # handlers
    handlers = [
        (r"/", IndexHandler),
        (r"/doc", DocHandler),
        (r"/about", AboutHandler),
        (r"/webcam", WebcamHandler),
        (r"/ws", WebSocketHandler),
        (r"/datasocket", DataSocketHandler)
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
        # closing the sqlite file
        conn.close()
        log.info("Server stopped")
        exit()

