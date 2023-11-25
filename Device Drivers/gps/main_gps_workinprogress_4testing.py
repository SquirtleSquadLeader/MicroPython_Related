"""

DECLARE / USE CLASSES MORE EFFECTIVELY... OR ELIMINATE THEM AND BRING FUNCTIONALITY INTO GPS CLASS.
"""

from machine import UART, Pin, SPI, I2C
from micropython import const
from gps.gps import GPS, UpdateRate
from sdcard.sdcard import SDCard
import time, os

# Define pin numbers for board
PPS = const(17)
FIX = const(18)
GPS_EN = const(33)
SDCS = const(3)

# Define pin objects
pps = Pin(PPS, Pin.IN)
fix = Pin(FIX, Pin.IN)
gps_en_pin = Pin(PPS, Pin.OUT)
cs = Pin(SDCS, Pin.OUT) # 1 - High Impedance, 0 - LO

# IRQ Flag
data_ready = False
pps_pulse = False

# Hardware Communication Protocols
uart = UART(1, 9600, tx = 43 , rx = 44)
spi = SPI(1, baudrate=400_000, sck=Pin(36), mosi=Pin(35), miso=Pin(37))

# Hardware Peripheral Instantiations
gps = GPS(uart, 1, 2, gps_en_pin)

# Service Routine
def gps_service_routine(pin_object):
    gps.data_ready = True
    
def pps_service_routine(pin_object):
    pps_pulse = True
  
# Hardware Interrupts
pps_interrupt = pps.irq(handler=pps_service_routine, trigger=Pin.IRQ_RISING)
gps_interrupt = fix.irq(handler=gps_service_routine, trigger=Pin.IRQ_RISING)

def init_gps(gps):
    pass
    
def consume_output(gps):
    # Attempt to pull one line from buffer
    output = gps.read()
    
    # If output was present and passes checksum
    if output != None and gps.verify_output(output) == True:
        gps.sort_sentence(output)
    
    else:
        print('No line consumed')
        pass

def consume_all_output(gps):
    # Pull all data from buffer 
    output = gps.readall()
    
    # If buffer empty, skip following code
    if output == None:
        return
    
    # Split into list of sentences
    try:
        output = output.split('$')
    except:
        # Error handling
        pass
    
    # Process each sentence in output and store values in class
    for sentence in range(0, len(output)):
        # Valid
        try:
            if gps.verify_output(output[sentence]) == True:
                gps.sort_sentence(output[sentence])
                #print('sorted')
            
            # Invalid 
            else:
                # Skip sentence and continue
                #print('skipped')
                pass
        except:
            # Error handling
            pass
        
    
"""""""""
TEST CODE BELOW
"""""""""

while True:
    if gps.data_ready == True:
        consume_all_output(gps)
        gps.data_ready = False
    if pps_pulse == True:
        print('pps')
        pps_pulse = False