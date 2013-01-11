RasPi-LED-Strip-Controller
==========================
This is/will be a LED strip driver for WS2801-based addressable LED strips like [this one from Sparkfun](https://www.sparkfun.com/products/11272?), with the intent of being customizable for various strip sizes. For pushing bits around, this uses the [RPi.GPIO package](http://pypi.python.org/pypi/RPi.GPIO).

I'm also intent on setting up a UDP listener that waits for strip color frames, and ultimately a JavaScript-based webpage (hosted on the Pi, of course) that also allows for simple control of the strip from any mobile or desktop browser. That'll be a bit of a stretch for my currently-absent web programming abilities.


**What's done:**
  - mostly just backend stuff at this point
    - setting individual or multiple lights on the strip at a time
    - converions between various internal datatypes to keep the class usage simple
      - supports setting colors based on hex strings and arrays of ints
  - the actual bit-bang routine to the Raspberry Pi's GPIOs

**What's in progress:**
  - ...testing. Got the basics working (no errors), but still lack the hardware to connect and power the strip.
  - Writing test routines to see if the classes and bit-banging work. Hardware is still pending to connect Pi and LED strip.
    - scanner
      - tests utils.strip.dim() by making a trail behind the light
    - rainbow fill
      - general test for writing out frames, as well as strip LED population

**What's to do:**
  - the UDP socket client and server to send and receive strip frames or other commands
  - complete documentation in case someone else wants to use this


__Usage:__ (as of 1/11/2013)
```python
#all the necessary setup
#strip initializes to all LEDs off
import utils
st = utils.strip(32, sda, sck)

#output:
st.post()                                 #push the contents to the strip

#setting one or more LEDs
#st.set(i, rgb, range?)
#rgb can be a list/tuple of integers ( [200, 50, 20] ) or a six-character hex string ('#AF0144')

st.set(2, rgb)                 #set one LED to one color
st.set([2, 3, 4, 5], rgb)      #set LEDs at indicies 2, 3, 4, and 5 to a color
st.set([1, 10], rgb, range=1)  #set all LEDs between 1 and 10 to a color

st.get(2).setWhite(200[, warm?])          #set the LED at 2 to red, green, and blue values of 200
                                          #setting warm to 1 yellows (warms) the light some
st.get(2).setRandom()                     #set the LED at 2 to a randomly-generated color

st.dim(i, amount, range?)                 #dim/brighten the LED(s) by some value (where 1.0 = 100%)
                                          #same index behavior as set()

st.get(i, range?)                         #same index behavior as set() and dim(). returns a utils.color object


#when exiting:
st.close()                                #releases RPi GPIO pins

```
