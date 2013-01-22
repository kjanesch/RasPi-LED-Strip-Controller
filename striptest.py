import time
import utils
from random import randint


RAINBOW = 'rainbow'


def setup():
    strip = utils.strip(32, 21, 22)
    
    rainbowFill(strip)
    
    time.clock()
    
    #test sliding the contents of the strip
    while time.clock()<2:
        strip.slide(1)
        strip.post()
        time.sleep(1.0/16)
    
    pass

def randomLights(strip, iters):
    for n in range(iters):
        rgb = [randint(0, 255),\
               randint(0, 255),\
               randint(0, 255)]
        i = randint(0, 32)
        
        strip.set(i, rgb)
        
        time.sleep(1.0/5)


def rainbowFill(strip, reverse=0):
    #ramp that mimics the way a primary color changes in RGB with respect to hue
    hueramp = [255]*11+range(210, -1, -42)+[0]*9+range(0, 211, 42)
    r = utils.slide(hueramp, -5)
    g = utils.slide(hueramp,  5)
    b = utils.slide(hueramp, 15)
    
    all = []
    
    for i in range(len(hueramp)):
        all.append([r[i], g[i], b[i]])
    
    if reverse:
        all.reverse()
        
    del r, g, b, hueramp
    
    strip.setAll(all)
    
#a sweeping-back-and-forth effect. has a trail option.
def scanner(strip, color, iters, trail=1):
    i = 0
    previ = 0
    n = 0
    dir = 1
    color = [42, 245, 143]
    
    strip.set(0, color)
    strip.post()
    
    for n in range(iters):
        
        time.sleep(1.0/32)
        
        if not trail:
            strip.set(previ, 0)
        else:
            strip.dim(strip.ALL, 0.60)

        previ = i
        i+=dir
        
        strip.set(i, color)
        
        strip.post()
        
        if i is len(strip)-1 or i is 0:
            dir = -dir
