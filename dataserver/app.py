import websocket
import thread
import time
import random
import getData

import config

WS_HOST = "ws://127.0.0.1/datasocket"
WS_PW = "foobar"
DELAY = 2 #in seconds

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
            time.sleep(config.delay)
            ws.send('{"pw":"' + options.password + '", "data":"' + getData.GetData() + '"}') # sending data in an json format to the server
    thread.start_new_thread(run, ())

def openWS():
    ws = websocket.WebSocketApp(options.url, on_message = on_message, on_error = on_error, on_close = on_close)
    
    ws.on_open = on_open
    
    ws.run_forever()
    
if __name__ == "__main__":
    try:
        openWS()
    except KeyboardInterrupt:
        print "\nServer stopped"
        exit()
