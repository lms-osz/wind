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
    print ("disconnected");
    time.sleep(2)
    openWS()

def on_open(ws):
    def run(*args):
        print ("connected");
        
        while True:
            tenBit = 0;
            CHANNEL = 2
            for i in range(int(config.times) + 1):
                tenBit = tenBit + getData.getData(CHANNEL)
                time.sleep((int(config.delay) - 0.0001) / int(config.times))
             
            tenBit = tenBit / int(config.times);
            print(tenBit)
            ws.send('{"pw":"' + config.password + '", "data":"' + str(tenBit) + '"}') # sending data in an json format to the server
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
