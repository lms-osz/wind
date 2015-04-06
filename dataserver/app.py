#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

import websocket
import thread
import time
import random
import getData

import config

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    time.sleep(2)
    openWS()

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(int(config.delay))
            ws.send('{"pw":"' + config.password + '", "data":"' + str(getData.getData()) + '"}') # sending data in an json format to the server
    thread.start_new_thread(run, ())

def openWS():
    ws = websocket.WebSocketApp(config.url, on_message = on_message, on_error = on_error, on_close = on_close)
    
    ws.on_open = on_open
    
    ws.run_forever()
    
if __name__ == "__main__":
    try:
        openWS()
    except KeyboardInterrupt:
        print "\nServer stopped"
        exit()
