import RPi.GPIO as GPIO
import mcp3008

CLK     = 18 # Clock
DIN     = 24 # Digital in
DOUT    = 23  # Digital out
CS      = 25  # Chip-Select

# Pin-Programmierung
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)


def getData(channel):
    c = mcp3008.getAnalogData(channel, CLK, DIN, DOUT, CS)
    c = c * 0.00322
    c = c / 165
    c = c * 1000
    c = c - 4
    c = c * 50
    c = c / 16
    c = round(c, 2)
    return c
