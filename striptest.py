import time
import utils

RAINBOW = 'rainbow'


def setup():
    strip = utils.strip(32, 21, 22)
    
    rainbowFill(strip)
    
    time.clock()
    
    while time.clock()<2:
        strip.slide(1)
        time.sleep(1.0/16)
    
    pass


def rainbowFill(strip, reverse=0):
    #ramp that mimics the way a primary color changes in RGB with respect to hue
    hueramp = [255]*11+range(210, -1, -42)+[0]*9+range(0, 211, 42)
    r = utils.slide(hueramp, -5)
    g = utils.slide(hueramp,  5)
    b = utils.slide(hueramp, 15)
    
    all = []
    
    for i in len(hueramp):
        all.append([r[i], g[i], b[i]])
    
    if reverse:
        all.reverse()
        
    del r, g, b, hueramp
    
    strip.setAll(all)
    
#a sweeping-back-and-forth effect. has a trail.
def scanner(strip, color, iters, trail=0):
    i = 0
    n = 0
    dir = 1
    color = [42, 245, 143]
    
    strip.set(0, color)
    strip.post()
    
    for n in range(iters):
        time.sleep(1.0/32)

        i+=dir
        strip.dim(strip.ALL, 0.60)
        
        strip.set(i, color)
        
        strip.post()
        
        if i is len(strip) or i is -1:
            dir = -dir
        time.sleep(1.0/30)
