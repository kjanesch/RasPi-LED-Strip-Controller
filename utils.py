import RPi.GPIO as GPIO
from random import randint

class IO:
    def __init__(self, ins=None, outs=None):
        GPIO.setmode(GPIO.BOARD)
        for i in ins:
            GPIO.setup(i, GPIO.IN)
        for o in outs:
            GPIO.setup(o, GPIO.OUT)
            
    def set(self, pin, hnl):
        hnl = int(hnl)
        GPIO.output(pin, (GPIO.HIGH if hnl else GPIO.LOW))
        
    def get(self, pin):
        return GPIO.input(pin)
    
    def cleanup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
    
""" RPi GPIO examples
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)                # use Raspberry Pi board pin numbers

    GPIO.setup(12, GPIO.OUT)                # set up GPIO output channel

    GPIO.output(12, GPIO.HIGH)              # set RPi board pin 12 high

    # set up GPIO input with pull-up control
    #   (pull_up_down be PUD_OFF, PUD_UP or PUD_DOWN, default PUD_OFF)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    input_value = GPIO.input(11)            # input from RPi board pin 11

    set_rising_event(11)                    # set up rising edge detection (EXPERIMENTAL)

    if GPIO.event_detected(11):             # check for an event (EXPERIMENTAL)

    # set up falling edge detection (EXPERIMENTAL)
    GPIO.set_rising_event(11, enable=False) # disable rising edge detection (as set above)
    GPIO.set_falling_event(11)

    # set up high detection (EXPERIMENTAL)
    GPIO.set_falling_event(11, enable=False)# disable falling edge detection (as set above)
    GPIO.set_high_event(11)

    # set up low detection (EXPERIMENTAL)
    GPIO.set_high_event(11, enable=False)   # disable high detection (as set above)
    GPIO.set_low_event(11)

    GPIO.setmode(GPIO.BCM)                  # change to BCM GPIO numbering

    GPIO.cleanup()                          # reset every channel that has been set up
end RPi GPIO examples """

class strip:
    ALL = "all"
    LEFT = -1
    RIGHT = 1
    REVERSE = -1
    FORWARD = 1
    
    def __init__(self, LEDcount, sck, sdi, direction=1, bitsPerColor=8, meters = 1):
        self.lights = []
        self.length = LEDcount
        self.lightsPerM = LEDcount*1.0/meters
        self.bitsPerColor = bitsPerCOlor
        self.colordepth = (2**bitsPerColor)**3
        
        for i in range(LEDcount):
            self.lights.append(color(0))
        
        self.reversed = reverse
        self.SCK = sck
        self.SDA = sdi
        
        self.bus = IO([], [sck, sdi])
    
    def __len__(self):
        return self.length
    
    def post(self):
        for light in self.lights:         #light at index 0
            for channel in light.bin():   #red, then green, then blue
                for bit in channel:       #MSB first
                    self.bus.set(self.SCK, 0)
                    self.bus.set(self.SDA, bit)
                    self.bus.set(self.SCK, 1)
        self.bus.set(self.SCK, 0)
        #500us wait to post data
    
    def totalsize(self, bits=0):
        if bits:
            return self.length()*3*self.bitsPerColor
        else:
            return self.length()*3*self.bitsPerColor/8
        
    #slide the lights left or right
    #default behavior is to drop any that get pushed off
    #wrap option allows wrapping
    def slide(self, direction=LEFT, count=1, wrap = 0):
        newlights = []
        if wrap:
            self.lights = self.lights[direction*count:]+self.lights[:direction*count]
        else:
            for i in range(count):
                newlights.append(color(0))
        
            if direction is LEFT:
                self.lights = self.lights[-count:]+newlights
            else:
                self.lights = newlights+self.lights[:-count]
    
    #index, individual indicies, or bounding range of indicies
    #value to set light(s)
    #whether or not the multiple indicies specify a range of LEDs
    def set(self, index, rgb, range = 0):
        if index is ALL:
            for li in lights:
                li.set(rgb)
        
        elif range and isgroup(index):
            for i in range(index[0], index[1]):
                self.lights[i].set(rgb)
        
        elif isgroup(index):
            for i in index:
                self.lights[i].set(rgb)
        
        elif inrange(index, self.length):
            self.lights[index].set(rgb)

    #index, individual indicies, or bounding range of indicies
    #percent to scale light(s)
    #whether or not the multiple indicies specify a range of LEDs
    def dim(self, index, amount, range = 0):
        if index is ALL:
            for i in range(self.length):
                self.dimOne(i, amount)
    
        elif range and isgroup(index):
            for i in range(index[0], index[1]):
                self.dimOne(i, amount)
        
        elif isgroup(index):
            for i in index:
                self.dimOne(i, amount)
        
        elif inrange(index, self.length):
            self.dimOne(index, amount)

    #index of a light/color
    #amount (percent) to scale
    def dimOne(self, i, amount):
        if inrange(i):
            li = self.lights[i]
            li.set(i [bound(li.r()*amount, 255),\
                      bound(li.g()*amount, 255),\
                      bound(li.b()*amount, 255)])
    

class color:
    def __init__(self, rgb=None, g=None, b=None):
        self.set(rgb, g, b)
    
    def setRandom(self):
        self.set(randint(0, 255),\
                 randint(0, 255),\
                 randint(0, 255))
    
    #val:   how bright the white is
    #warm:  if it's warm white  #TODO: this
    def setWhite(self, val, warm=None):
        self.r = int(val*1.05)
        self.g = int(val*1.05)
        self.b = int(val*0.95)
    
    #rgb:   red, or 
    def set(self, rgb=None, g=None, b=None):
        if rgb is not None:
            if (not g) and (not b):
                #rgb is in hex string (eg [0x|#]FF0022)
                if sametype(rgb, "a"):
                    rgb = unhex(rgb, splitbytes=1)
                
                if isgroup(rgb) and len(rgb) is 3:
                    self.r = int(rgb[0])
                    self.g = int(rgb[1])
                    self.b = int(rgb[2])
                elif not isgroup(rgb):
                    setWhite(rgb)

            else:
                self.r = int(rgb)
                self.g = int(g)
                self.b = int(b)
        
        else:
            self.r = 0
            self.g = 0
            self.b = 0
    
    def r(self, r=None):
        if r is not None:
            self.r = int(r)
        return self.r
    
    def g(self, g=None):
        if g is not None:
            self.g = int(g)
        return self.g
    
    def b(self, b=None):
        if b is not None:
            self.b = int(b)
        return self.b
        
    def bin(self):
        return [nicebin(self.r), nicebin(self.g), nicebin(self.b)]
        
    def hex(self, array=0, hash=0):
        if array:
            return [nicehex(self.r), nicehex(self.g), nicehex(self.b)]
            
        return ("#" if hash else "")+nicehex(self.r)+nicehex(self.g)+nicehex(self.b)

def slide(list, direction, count):
    return list[direction*count:]+list[:direction*count]

def bound(i, high):
    return boundInt(0, i, high)
    
def bound(low, i, high):
    if i<low:
        i=low
    if i>high:
        i=high
    return int(i)
        
def sametype(o, r):
    return (type(o) is type(r))
     
"""
"""   
def inrange(i, r):
    return (0<=i<r)

def isgroup(o):
    return (type(o) in [type(tuple()), type(list())])
    
def nicebin(n, noprefix=1, nbits=0):
    b = bin(n).replace("0b", "")
    
    #pad out to the nearest byte worth of bits
    if not nbits:
        nbits = len(b)+(8 - len(b)%8)
    
    #fill dem zeroes
    b = b.zfill(nbits)
    
    #optional prefix 
    if not noprefix:
        b = "0b"+b
        
    return b
    
def nicehex(n, noprefix=1, nnibs=0):
    h = hex(n).replace("0x", "")
    
    #pad out to the nearest byte's worth of nybbles
    if not nnibs:
        nnibs = len(h)+(2 - len(b)%2)
    
    #fill dem zeroes
    h = h.zfill(nnibs)
    
    #optional prefix 
    if not noprefix:
        h = "0x"+h
        
    return h

#
def unhex(h, splitbytes = 1)
    #remove any "0x" or "#" from the string
    h = h.replace("0x", "").strip("#")
    
    if not splitbytes:
        return int(h, 16)
    
    bytes = []
    for i in range(0, len(h), 2):
        bytes.append(int(h[i:i+2], 16))
    return bytes