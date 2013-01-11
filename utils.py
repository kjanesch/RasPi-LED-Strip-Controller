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
        self.bitsPerColor = bitsPerColor
        self.colordepth = (2**bitsPerColor)**3
        
        for i in range(LEDcount):
            self.lights.append(color(0))
        
        self.reversed = direction
        self.SCK = sck
        self.SDA = sdi
        
        self.bus = IO([], [sck, sdi])
    
    def __len__(self):
        return self.length
                    
    #get an element or elements from the strip.
    #same range/index behavior as set() and dim()
    #returns the color objects for those elements
    def get(self, index, range=0):
        gets = []
        if index is strip.ALL:
            return self.lights
        elif range and isgroup(index):
            for i in range(index[0], index[1]):
                gets.append(self.getOne(i))
        elif isgroup(index):
            for i in index:
                gets.append(self.getOne(i))
        else:
            gets = self.getOne(index)
        
        return gets
    
    #get the element at i if it's in range
    def getOne(self, i):
        if inrange(i, self.length):
            return self.lights[i]
        else:
            return None

    #spit out the strip's contents to the GPIO
    #bit-bangs on the SCK and SDA pins specified in __init__()
    def post(self):
        for light in self.lights:         #light at index 0
            for channel in light.bin():   #red, then green, then blue
                for bit in channel:       #MSB first
                    self.bus.set(self.SCK, 0)
                    self.bus.set(self.SDA, bit)
                    self.bus.set(self.SCK, 1)
        self.bus.set(self.SCK, 0)
        #500us wait to post data

    #grab the size of the strip in bytes (optional: bits)
    def totalsize(self, bits=0):
        if bits:
            return self.length*3*self.bitsPerColor
        else:
            return self.length*3*self.bitsPerColor/8
        
    #slide the lights left or right
    #default behavior is to drop any that get pushed off
    #wrap option allows wrapping
    def slide(self, count, direction=LEFT, wrap = 0):
        newlights = []
        if wrap:
            self.lights = self.lights[direction*count:]+self.lights[:direction*count]
        else:
            if count<0:
                count=abs(count)
                direction = -direction
            
            for i in range(count):
                newlights.append(color(0))
            
            if direction is strip.LEFT:
                self.lights = self.lights[count:]+newlights
            else:
                self.lights = newlights+self.lights[:-count]
    
    #index, individual indicies, or bounding range of indicies
    #value to set light(s)
    #whether or not the multiple indicies specify a range of LEDs
    def set(self, index, rgb, range = 0):
        if index is strip.ALL:
            for li in self.lights:
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
        if index is strip.ALL:
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

    #dim one light by an amount
    #index of a light/color
    #amount (percent) to scale
    def dimOne(self, i, amount):
        if inrange(i, 255):
            li = self.lights[i]
            li.set(i, [bound(0, li.r*amount, 255),\
                       bound(0, li.g*amount, 255),\
                       bound(0, li.b*amount, 255)])
    
    def close(self):
        self.bus.cleanup()

class color:
    def __init__(self, rgb=None, g=None, b=None):
        self.set(rgb, g, b)

    def __str__(self):
	return str(self.dec())    
    
    #sets the light to a random color
    def setRandom(self):
        self.set(randint(0, 255),\
                 randint(0, 255),\
                 randint(0, 255))
    
    #val:   how bright the white is
    #warm:  if it's warm white  #TODO: this
    def setWhite(self, val, warm=None):
        if warm:
            self.r = bound(0, int(val*1.05), 255)
            self.g = bound(0, int(val*1.05), 255)
            self.b = bound(0, int(val*0.95), 255)
        else:
            self.r = bound(0, int(val), 255)
            self.g = bound(0, int(val), 255)
            self.b = bound(0, int(val), 255)

    #rgb: white (int, no g or b), red (int and g and b), or [red, green, blue]
    #g: green (if red is int)
    #b: blue  (if red is int)
    def set(self, rgb=None, g=None, b=None):
        if rgb is not None:
            if (not g) and (not b):
                #rgb is in hex string (eg [0x|#]FF0022)
                if sametype(rgb, "a"):
                    rgb = unhex(rgb, splitbytes=1)
                
                #rgb is [red, green, blue]
                if isgroup(rgb) and len(rgb) is 3:
                    self.r = bound(0, int(rgb[0]), 255)
                    self.g = bound(0, int(rgb[1]), 255)
                    self.b = bound(0, int(rgb[2]), 255)
                #int type, no g or b
                #set all three color channels to white 
                elif not isgroup(rgb):
                    self.setWhite(rgb)
            #red, green, blue are separate args
            else:
                self.r = bound(0, int(rgb),255)
                self.g = bound(0, int(g),  255)
                self.b = bound(0, int(b),  255)
        #no values specified. set to "off"
        else:
            self.r = 0
            self.g = 0
            self.b = 0
    #dual-purpose getter/setter for r
    def r(self, r=None):
        if r is not None:
            self.r = bound(0, int(r), 255)
        return self.r
    
    #dual-purpose getter/setter for g
    def g(self, g=None):
        if g is not None:
            self.g = bound(0, int(g), 255)
        return self.g
    
    #dual-purpose getter/setter for b
    def b(self, b=None):
        if b is not None:
            self.b = bound(0, int(b), 255)
        return self.b
    
    #get the color as decimal values [r, g, b]
    def dec(self):
        return [self.r, self.g, self.b]
    #get the color expressed as binary values [0bR, 0bG, 0bB]
    def bin(self):
        return [nicebin(self.r), nicebin(self.g), nicebin(self.b)]
    #get the color expressed as a hex string RRGGBB
    #array=1: [RR, GG, BB] 
    #hash=1:  #RRGGBB      (web use)
    def hex(self, array=0, hash=0):
        if array:
            return [nicehex(self.r), nicehex(self.g), nicehex(self.b)]
            
        return ("#" if hash else "")+nicehex(self.r)+nicehex(self.g)+nicehex(self.b)

#slide/rotate the contents of list
#direction is direction to shift (positive=left when count is positive)
#count is number of elements to shift
def slide(list, direction, count):
    return list[direction*count:]+list[:direction*count]

#put an upper bound on a value (0-high)
def bound(i, high):
    return boundInt(0, i, high)
    

#specify an upper and lower bound for a value
def bound(low, i, high):
    if i<low:
        i=low
    if i>high:
        i=high
    return int(i)

#check if two types match
def sametype(o, r):
    return (type(o) is type(r))
     
"""
see if i is in range of 0-r
"""   
def inrange(i, r):
    return (0<=i<r)

"""
see if the type of o is that of a list or tuple
"""
def isgroup(o):
    return (type(o) in [type(tuple()), type(list())])

"""
make a nicely-formatted binary value of n
auto-pads to multiples of 8 bits unless otherwise specified by nbits
set noprefix to 0 to have binary value prefixed with "0b"
"""
def nicebin(n, noprefix=1, nbits=0):
    b = bin(n).replace("0b", "")
    
    #pad out to the nearest byte worth of bits
    if not nbits:
        if len(b)%8 is 0:
            nbits = len(b)
        else:
            nbits = len(b)+(8 - len(b)%8)
    
    #fill dem zeroes
    b = b.zfill(nbits)
    
    #optional prefix 
    if not noprefix:
        b = "0b"+b
        
    return b

"""
make a nicely-formatted hex value for n
auto pads to the nearest byte unless specified by nnibs
set noprefix to 0 to have value prefixed by "0x"
"""
def nicehex(n, noprefix=1, nnibs=0):
    h = hex(n).replace("0x", "")
    
    #pad out to the nearest byte's worth of nybbles
    if not nnibs:
        if len(h)%2 is 0:
            nnibs = len(h)
        else:
            nnibs = len(h)+(2 - len(h)%2)
    
    #fill dem zeroes
    h = h.zfill(nnibs)
    
    #optional prefix 
    if not noprefix:
        h = "0x"+h
        
    return h

"""
convert hex value h to a list of bytes
"""
def unhex(h, splitbytes = 1):
    #remove any "0x" or "#" from the string
    h = h.replace("0x", "").strip("#")
    
    if not splitbytes:
        return int(h, 16)
    
    bytes = []
    for i in range(0, len(h), 2):
        bytes.append(int(h[i:i+2], 16))
    return bytes
