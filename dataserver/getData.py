import RPi.GPIO as GPIO
import mcp3008

CH = 0  # Analog/Digital-Channel
CLK     = 18 # Clock
DIN     = 24 # Digital in
DOUT    = 23  # Digital out
CS      = 25  # Chip-Select

# Pin-Programmierung
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)

def getData:
    return mcp3008.getAnalogData(CH, CLK, DIN, DOUT, CS)
