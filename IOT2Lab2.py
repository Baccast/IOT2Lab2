#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Change these as desired - they're the pins connected from the
# SPI port on the ADC to the Raspberry Pi
PIN_CLK = 18
PIN_DO = 27
PIN_DI = 22
PIN_CS = 17

# Set up the SPI interface pins
GPIO.setup(PIN_DI, GPIO.OUT)
GPIO.setup(PIN_DO, GPIO.IN)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_CS, GPIO.OUT)

# Read SPI data from ADC8032
def getADC(channel):
    # 1. CS LOW
    GPIO.output(PIN_CS, True)  # Clear last transmission
    GPIO.output(PIN_CS, False)  # Bring CS low

    # 2. Start clock
    GPIO.output(PIN_CLK, False)  # Start clock low

    # 3. Input MUX address
    for i in [1, 1, channel]:  # Start bit + mux assignment
        if i == 1:
            GPIO.output(PIN_DI, True)
        else:
            GPIO.output(PIN_DI, False)

        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)

    # 4. Read 8 ADC bits
    ad = 0
    for i in range(8):
        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)
        ad <<= 1  # Shift bit
        if GPIO.input(PIN_DO):
            ad |= 0x1  # Set first bit

    # 5. Reset
    GPIO.output(PIN_CS, True)

    return ad

if __name__ == "__main__":
    try:
        while True:
            adc0 = getADC(0)
            adc1 = getADC(1)
            print("ADC[0]: {}\t ADC[1]: {}".format(adc0, adc1))
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()