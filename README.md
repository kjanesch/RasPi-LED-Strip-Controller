RasPi-LED-Strip-Controller
==========================
This is/will be a LED strip driver for WS2801-based addressable LED strips like [this one from Sparkfun](https://www.sparkfun.com/products/11272?), with the intent of being customizable for various strip sizes.

I'm also intent on setting up a UDP listener that waits for strip color frames, and ultimately a JavaScript-based webpage (hosted on the Pi, of course) that also allows for simple control of the strip from any mobile or desktop browser. That'll be a bit of a stretch for my currently-absent web programming abilities.


**What's done:**
  - mostly just backend stuff at this point
    - setting individual or multiple lights on the strip at a time
    - converions between various internal datatypes to keep the class usage simple
      - supports setting colors based on hex strings and arrays of ints

**What's to do:**
  - the actual bit-bang routine to the Raspberry Pi's GPIOs
  - the UDP socket routine that receives commands to set colors
  - 
