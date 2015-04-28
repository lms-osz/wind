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
        print ("connected.....");
        
        while True:
            wind_tenBit = 0;
            Uakku_tenBit = 0;
            Iakku_tenBit = 0;
            
            for i in range(int(config.times) + 1):
                wind_tenBit = wind_tenBit + getData.getData(config.windChannel)
                Uakku_tenBit = Uakku_tenBit + getData.getData(config.UakkuChannel)
                Iakku_tenBit = Iakku_tenBit + getData.getData(config.IakkuChannel)
                
                time.sleep((int(config.delay) - 0.0501) / int(config.times))
             
            wind_tenBit = wind_tenBit / int(config.times);
            Uakku_tenBit = Uakku_tenBit / int(config.times);
            Iakku_tenBit = Iakku_tenBit / int(config.times);
            
            
            ws.send('{"pw":"' + config.password + '", "data":[{"wind":' + str(wind_tenBit) + ',"Uakku":' + str(Uakku_tenBit) + ',"Iakku":' + str(Iakku_tenBit) + '}]}') # sending data in an json format to the server
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
