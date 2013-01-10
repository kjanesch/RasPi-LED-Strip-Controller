import time
import utils

RAINBOW = 'rainbow'


def setup():
    strip = utils.strip(32, 12, 13)
    
    
    
    pass


def rainbowFill(strip, reverse=0):
    hueramp = [255]*10+range(210, -1, -42)+[0]*8+range(0, 211, 42)
    r = range(255, -1, -16)+range(0, 255, 16)
    g = range(0, 255, 16)+range(255, -1, -16)
    b = 
    
    for i in range(len(strip)):
        
        #strip.set(i, 
    

def scanner(strip, color, iters, trail=0):
    i = 0
    n = 0
    dir = 1
    color = [42, 245, 143]
    
    #strip.set(0, color)
    #strip.post()
    
    for n in range(iters):
        time.sleep(1.0/32)

        i+=dir
        #strip.dim(strip.ALL, 0.90)
        
        #strip.set(i, color)
        
        #strip.post()
        
        if i is len(strip) or i is -1:
            dir = -dir
        
