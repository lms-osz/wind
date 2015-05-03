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
            Ubatt_tenBit = 0;
            Ibatt_tenBit = 0;
            
            for i in range(int(config.times) + 1):
                wind_tenBit = wind_tenBit + getData.getData(config.windChannel)
                Ubatt_tenBit = Ubatt_tenBit + getData.getData(config.UbattChannel)
                Ibatt_tenBit = Ibatt_tenBit + getData.getData(config.IbattChannel)
                
                time.sleep((int(config.delay) - 0.0501) / int(config.times))
             
            wind_tenBit = wind_tenBit / int(config.times);
            Ubatt_tenBit = Ubatt_tenBit / int(config.times);
            Ibatt_tenBit = Ibatt_tenBit / int(config.times);
            
            
            ws.send('{"pw":"' + config.password + '", "data":[{"wind":' + str(wind_tenBit) + ',"Ubatt":' + str(Ubatt_tenBit) + ',"Ibatt":' + str(Ibatt_tenBit) + '}]}') # sending data in an json format to the server
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
