# Capacitive Piano

Create your own fruit piano with this python script.  Place 12 apples on a table (or any conductive object) and create your own midi piano with light effects.

## Features

 * Play all 12 keys simultaneously
 * High quality midi audio using .sf2 sound fonts
 * Supports sustain: holding down a key sustains the audio for certain instruments like pipe organs
 * Optional mode button: Switch between different instruments by pressing a push button connected to a GPIO pin
 * Optional lighting effects: each key lights up its own neopixels

## Required Hardware
* Raspberry Pi 3
* MPR121 12-key capacitive touch sensor
* 12 conductive objects like fruit or aluminium foil
* Dupont wire jumper cables
* Breadboard
* Speaker (must be amplified, HDMI cable to TV/receiver sounds great, headphone jack has a little background noise but is tolerable)

## Optional Hardware
* Neopixel string or strip (addressable LEDs such as WS2812 lights)
* Neopixel power supply
* Momentary button

## Software Libraries
* [Adafruit_MPR121] (https://github.com/adafruit/Adafruit_MPR121) 12-key capacitive touch sensor
* [python-mingus] (http://bspaans.github.io/python-mingus/) midi synthesizer
* [rpi_ws281x] (https://github.com/jgarff/rpi_ws281x) neopixel lights

### Usage
* Install the above software libraries
* run ``` sudo python piano.py ``` from terminal
Sudo is required for GPIO access