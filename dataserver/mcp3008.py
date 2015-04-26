import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# configuring Pins
pins = {
    "DIN"   : 24,
    "DOUT"  : 23,
    "CLOCK" : 18,
    "SHDN"  : 25
}

GPIO.setup(pins["CLOCK"], GPIO.OUT)
GPIO.setup(pins["DOUT"], GPIO.IN)
GPIO.setup(pins["SHDN"], GPIO.OUT)
GPIO.setup(pins["DIN"], GPIO.OUT)

def clock():
    GPIO.output(pins["CLOCK"], True)
    GPIO.output(pins["CLOCK"], False)

def getTenBit(channel):
    if ((channel > 7) or (channel < 0)):
        return -1
    GPIO.output(pins["SHDN"], True)
    GPIO.output(pins["SHDN"], False)
    GPIO.output(pins["CLOCK"], False)
    
    command = channel
    command |= 0x18
    # config channel
    for i in range(5):
        if (command & 0x10):
            GPIO.output(pins["DIN"], True)
        else:
            GPIO.output(pins["DIN"], False)
        clock();
        command <<= 1
    
    # get data
    adcout = 0
    for i in range(11):
        clock();
        adcout <<= 1
        if (GPIO.input(pins["DOUT"])):
            adcout |= 0x01
    
    return adcout;


if __name__ == "__main__":
    CHANNEL = 1
    import time
    try:
        while(True):
            print str(getTenBit(CHANNEL));
            time.sleep(0.1)
    except KeyboardInterrupt:
        print ""
        exit()

