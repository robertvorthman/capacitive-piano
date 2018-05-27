# Capacitive Piano

Create your own fruit piano with this python script.  Place 12 apples on a table and create your own midi piano with light effects. [YouTube Video](https://www.youtube.com/watch?v=bnpva2UnOGU)

![piano](https://user-images.githubusercontent.com/4665046/32136897-a5a1127c-bbe4-11e7-8ae4-c0daf9b120b0.gif)

## Features

 * **Simultaneous Key Presses** Play 12 notes at the same time
 * **High Quality Audio** using .sf2 sound fonts and fluidsynth midi synthesizer
 * **HDMI or Analog Audio** use an HDMI cable or the headphone jack for audio
 * **Sustain** Hold down a piano key to sustain instruments like pipe organs
 * **Mode Switch** Connect an optional switch to at GPIO pin and switch between different instruments or even drum kits [**YouTube demo of various modes**](https://www.youtube.com/watch?v=unna7pvTs5E)
 * **Light Effects** Add neopixel lights and each piano key will light up when pressed

# Construction

#### Overview
![piano - overview - annotated](https://user-images.githubusercontent.com/4665046/32144803-8aa0f4d2-bc94-11e7-9233-869050c66674.jpg)

#### Close Up
![piano - close up - annotated](https://user-images.githubusercontent.com/4665046/32144804-8aa8ab28-bc94-11e7-8b34-8f40a3557775.jpg)

#### Breadboard
![piano - breadboard - annotated](https://user-images.githubusercontent.com/4665046/32144853-75433cfc-bc95-11e7-9d2d-66ef99f59182.jpg)

#### Diagram
![Fritzing Diagram](https://user-images.githubusercontent.com/4665046/32137972-67cdc210-bbf8-11e7-9984-8f6c99b6d89f.png)

# Tips
* For best touch sensitivity, minimize distance between fruit and capacitive touch sensor.  For small fruit like apples, no more than two or three feet.  For large objects like pumpkins, 8 inches or less.  Instead of placing the capacitive touch sensor on the breadboard, run long wires (I used cat5 cable) from the breadboard to the table with your fruit, then wire up the capacitive touch sensor as close as possible to the fruit.
* The capacitive touch sensor calibrates when initialized, so do not touch the fruit while starting piano.py until the lights flash orange.  If one of the fruit is stuck on, or unresponsive, stop the script (Ctrl+C) and restart it ```sudo python piano.py``` to recalibrate the sensitivity.
* Protect your neopixels with a capacitor and read the [*Adafruit NeoPixel Überguide - Powering Neopixels section](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)

This is my first Python project so I'm sure the code could be more elegant.

## Required Hardware
* Raspberry Pi 3
* [MPR121 12-key capacitive touch sensor](https://www.amazon.com/gp/product/B00SK8PVNA/ref=oh_aui_search_detailpage)
* 12 conductive objects like fruit or aluminium foil
* Dupont wire jumper cables
* Breadboard
* Speaker (must be amplified, HDMI cable to TV/receiver sounds great, headphone jack has a little background noise but is tolerable)

## Neopixel Hardware
* Neopixel [string](https://www.aliexpress.com/item/50x-WS2812B-Pre-soldered-leds-with-wire-5V-WS2812-IC-Built-in-12cm-Wire-Addressable-Idividually/32243084800.html) or [strip](https://www.amazon.com/ALITOVE-Individually-Addressable-Flexible-Waterproof/dp/B01DLYSH6U) (addressable LEDs such as WS2812 lights)
* Neopixel power supply [see *Adafruit Powering NeoPixels* guide](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)
* [Logic level shifter](https://www.aliexpress.com/item/10pcs-lot-UART-SPI-4-Channel-IIC-I2C-Logic-Level-Converter-Bi-Directional-Module-5V-to/32805164795.html) to convert 3.3v to 5v. **Required** for driving neopixels from a 3.3v source like a Raspberry Pi.
* [Capacitor](https://www.aliexpress.com/item/20PCS-25V-1000UF-Aluminum-electrolytic-capacitor-25-V-1000-UF-25V-1000UF-size-10-17mm/32725883192.html) (1000 µF, 6.3V or higher) to protect the neopixels from being damaged by initial onrush of current

## Optional Hardware
* Momentary button (if switching between multiple instruments)
* 10k resistor

## Software Libraries
* [Adafruit_MPR121](https://learn.adafruit.com/mpr121-capacitive-touch-sensor-on-raspberry-pi-and-beaglebone-black/software) 12-key capacitive touch sensor
* [fluidsynth](https://github.com/FluidSynth/fluidsynth/wiki/GettingStarted)
* [python-mingus](http://bspaans.github.io/python-mingus/) midi synthesizer
* [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) neopixel lights

# Usage
* Install the above software libraries
	*For example: ```sudo apt-get install fluidsynth``` to install fluidsynth
* Edit piano.py
	* fluidsynth.init('path/to/your/soundfont.sf2')
	* LED_COUNT = (number of neopixels)
	* LED_STRIP = (type of neopixel strip)
	* lightSegments = (array of which neopixels should illuminate for each key)
* run ``` sudo python piano.py ``` from terminal
(Sudo is required for python to access the GPIO pins)

### Automatically Run at Startup
* Install [pm2](https://github.com/Unitech/pm2)
* ``` sudo pm2 start piano.py ```
* ``` sudo pm2 save ```
* ```sudo reboot ```
* piano.py will run at startup, neopixels will blink orange when piano is ready

## Sound Fonts

A sound font (.sf2 file) is required for generating audio.  .sf3 files won't work with fluidsynth.  Installing ``fluidsynth using apt-get``` should also download the default sound font to ```/usr/share/sounds/sf2/FluidR3_GM.sf2``` but you can download other sound fonts from [this link](https://musescore.org/en/handbook/soundfonts#list).  I used the [*Arachno* sound font](http://www.arachnosoft.com/main/soundfont.php).  Larger .sf2 files like *Timbres of Heaven* caused an out of memory error when attempting to run piano.py.

### Sound Font Instruments and Banks
A .sf2 file contains dozens or hundreds of instruments, from pianos to drum kits, sometimes organized into seperate "banks".  To find an instrument I liked, I use a free program called [Polyphone](http://polyphone-soundfonts.com/) to open the .sf2 file and browse each instrument.  Clicking the keyboard at the top right of Polyphone lets you preview what each note will sound like.  Once you find an instrument you like, note the preset and bank number, and enter these numbers into the piano.py.  For example, the Arachno sound font has an orchestra drum kit as preset 48 in bank 128.  So to load this instrument into your piano as channel 1, use the following line of code:
```fluidsynth.set_instrument(1, 48, 128)```
![Polyphone](https://user-images.githubusercontent.com/4665046/32144431-14d80a6a-bc8f-11e7-84b1-80e63dfbcf76.png)
