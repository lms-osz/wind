# Wind

We are using two diffrent programms
- the webserver, written in Python (using tornado)
- the dataserver (we are using an Raspberry PI model 2 and an digital-to-analog converter, the MCP3008)

### Webserver

If you want to install the webserver, you need some python packages:
- tornado
- sqlite3

We created an startup-script (start.sh). You can use it like:

    ./start.sh start
    ./start.sh stop
    ./start.sh restart

It will start the python-server. If you want use this, you can also use this: `python app.py`

The configs:

    [server]
    port=80
    
    [ssl]
    ssl=false
    crt=
    key=
    
    [settings]
    password=foobar
    [database]
    rawData=rawData.db

I think it is very simple to understand
