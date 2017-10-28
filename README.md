# Capacitive Piano

Create your own fruit piano with this python script.  Place 12 apples on a table (or any conductive object) and create your own midi piano with light effects.

## Features

 * **Simultaneous key presses** Play 12 notes at the same time
 * **High quality audio** using .sf2 sound fonts and fluidsynth midi synthesizer
 * **Sustain** Hold down a piano key to sustain instruments like pipe organs
 * **Mode Switch** Connect an optional switch to at GPIO pin and switch between different instruments or even drum kits
 * **Light effects** Add neopixel lights and each piano key will light up when pressed

## Required Hardware
* Raspberry Pi 3
* [MPR121 12-key capacitive touch sensor](https://www.amazon.com/gp/product/B00SK8PVNA/ref=oh_aui_search_detailpage)
* 12 conductive objects like fruit or aluminium foil
* Dupont wire jumper cables
* Breadboard
* Speaker (must be amplified, HDMI cable to TV/receiver sounds great, headphone jack has a little background noise but is tolerable)

## Optional Hardware
* Neopixel string or strip (addressable LEDs such as WS2812 lights)
	* [I used this 50 LED string](https://www.aliexpress.com/item/50x-WS2812B-Pre-soldered-leds-with-wire-5V-WS2812-IC-Built-in-12cm-Wire-Addressable-Idividually/32243084800.html)
    * I also tested a 144 LED WS2812B strip
* Neopixel power supply [see *Adafruit Powering NeoPixels* guide](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)
* Logic level shifter to convert 3.3v from Raspberry Pi to 5v required to drive neopixels
* Momentary button (if switching between multiple instruments)

## Software Libraries
* [Adafruit_MPR121](https://github.com/adafruit/Adafruit_MPR121) 12-key capacitive touch sensor
* [python-mingus](http://bspaans.github.io/python-mingus/) midi synthesizer
* [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) neopixel lights

# Usage
* Install the above software libraries
* run ``` sudo python piano.py ``` from terminal
Sudo is required for GPIO access

### Automatically Run at Startup
* Install [pm2] (https://github.com/Unitech/pm2)
* ``` sudo pm2 start piano.py ```
* ``` sudo pm2 save ```
* ```sudo reboot ```
* piano.py will run at startup, neopixels will blink orange when piano is ready

# Construction
Coming soon