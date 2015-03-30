import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

HIGH = True  # 3,3V
LOW  = False # 0V

# SCI function
def getAnalogData(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    GPIO.output(CSPin, HIGH)    
    GPIO.output(CSPin, LOW)
    GPIO.output(CLKPin, LOW)
        
    cmd = adCh
    cmd |= 0b00011000

    for i in range(5):
        if (cmd & 0x10):
            GPIO.output(DINPin, HIGH)
        else:
            GPIO.output(DINPin, LOW)
        GPIO.output(CLKPin, HIGH)
        GPIO.output(CLKPin, LOW)
        cmd <<= 1
            
    adchvalue = 0
    for i in range(11):
        GPIO.output(CLKPin, HIGH)
        GPIO.output(CLKPin, LOW)
        adchvalue <<= 1
        if(GPIO.input(DOUTPin)):
            adchvalue |= 0x01
    return adchvalue


""""CH = 0  # Analog/Digital-Channel
CLK     = 18 # Clock
DIN     = 24 # Digital in
DOUT    = 23  # Digital out
CS      = 25  # Chip-Select

# Pin-Programmierung
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)

while True:
    print getAnalogData(CH, CLK, DIN, DOUT, CS)
"""
