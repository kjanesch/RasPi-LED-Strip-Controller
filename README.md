RasPi-LED-Strip-Controller
==========================
This is/will be a LED strip driver for WS2801-based addressable LED strips like [this one from Sparkfun](https://www.sparkfun.com/products/11272?), with the intent of being customizable for various strip sizes.

I'm also intent on setting up a UDP listener that waits for strip color frames, and ultimately a JavaScript-based webpage (hosted on the Pi, of course) that also allows for simple control of the strip from any mobile or desktop browser. That'll be a bit of a stretch for my currently-absent web programming abilities.


**What's done:**
  - mostly just backend stuff at this point
    - setting individual or multiple lights on the strip at a time
    - converions between various internal datatypes to keep the class usage simple
      - supports setting colors based on hex strings and arrays of ints
  - the actual bit-bang routine to the Raspberry Pi's GPIOs

**What's in progress:**
  - ...testing. Still getting the Pi prepped for that.
  - test routines to see if the classes and bit-banging work. Hardware is still pending to connect Pi and LED strip.
    - scanner
      - tests utils.strip.dim() by making a trail behind the light
    - rainbow fill
      - general test for writing out frames, as well as strip LED population

**What's to do:**
  - the UDP socket client and server to send and receive strip frames or other commands
  
