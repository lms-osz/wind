# Wind

### dataserver

If you want to install the dataserver, you need some python packages:
- websocket (client libary https://pypi.python.org/pypi/websocket-client/)

We created an startup-script (start.sh). You can use it like:

    ./start.sh start
    ./start.sh stop
    ./start.sh restart

It will start the python-server. If you want use this run `python app.py`

The configs:

    [server]
    url=ws://10.0.0.1/datasocket
    
    [settings]
    delay=500
    times=4
    
    password=foobar
    
    [channels]
    wind=2
    Ubatt=1
    Ibatt=0

I think it is also easy to understand
