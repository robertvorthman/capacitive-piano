import time
import Adafruit_MPR121.MPR121 as MPR121 #12-key capacitive switch sensor
from sys import exit
from neopixel import * #colored lights
#midi player libraries
from mingus.core import notes, chords 
from mingus.containers import * 
from mingus.midi import fluidsynth
import RPi.GPIO as GPIO #for GPIO switch

#fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")
fluidsynth.init('/home/pi/Documents/Halloween Piano/soundFonts/Arachno SoundFont - Version 1.0.sf2',"alsa") #custom sound font sounds slightly better than FluidR3_GM.sf2, but file size is larger

#assign instruments to separate channel numbers (1 is hammond organ, 2 is steel guitar, etc...)
fluidsynth.set_instrument(1, 16) #16 hammond organ 
fluidsynth.set_instrument(2, 26) #26 steel guitar
fluidsynth.set_instrument(3, 0, 128) #0 Bank 128 standard drums
fluidsynth.set_instrument(4, 114) #114 steel drums
fluidsynth.set_instrument(5, 48, 128) #48 bank 128 orchestra drum kit
fluidsynth.set_instrument(6, 25, 128) #25 bank 128 TR-808 drum kit
fluidsynth.set_instrument(7, 102) #102 echo drops
fluidsynth.set_instrument(8, 11) #11 vibraphone
fluidsynth.set_instrument(9, 13) #13 xylophone
fluidsynth.set_instrument(10, 55) #55 orchestra hit
fluidsynth.set_instrument(11, 86) #5th saw wave
fluidsynth.set_instrument(12, 88) #fantasia
#instrument numbers: https://www.midi.org/specifications/item/gm-level-1-sound-set
#Use Polysynth desktop application to open sf2 files and find instrument and bank numbers

#setup GPIO button as input
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
modeButtonLastPushed = time.time() 
print "Push Button Ready"

#each mode has a name which is printed to the python terminal output, each mode plays different sounds
modes = ['96tears', 'steelDrum', 'drumKit', 'techno', 'echoDrops', 'vibraphone', 'xylophone', 'orchestraHit', 'fifthSawWave', 'fantasia']
currentMode = 0
notes = [['','','','','D-6', 'D#-6', 'E-6', 'G-6', 'A#-7', 'B-7', 'C-7', 'D-7'], #96 tears
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #steel drum
['F-2', 'C-2', 'D-2', 'B-3', 'F-1', 'E-1', 'C#-2', 'D#-2', 'F#-3', 'A#-3', 'C-5', 'A#-1'], #drum kit orchestra
['F-2', 'C-2', 'D-2', 'B-3', 'F-1', 'E-1', 'C#-2', 'D#-2', 'F#-3', 'A#-3', 'C-5', 'A#-1'], #drum kit techno
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #echoDrops
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #vibraphone
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #xylophone
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #orchestraHit
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #fifthSawWave
['A-4','B-4','C-4','D-4','E-4', 'F-4', 'G-4', 'A-5', 'A#-5', 'B-5', 'C-5', 'D-5'], #fantasia
]

#map which channels each mode uses (96tears uses instrument channel 1 through 3, steeldrum uses channel 4, etc...) 
modeChannels = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#define special notes and chords for 96tears modes
drumBass = Note('C', 2)
drumSnare = Note('E', 2)
chordG = NoteContainer(['G-2', 'B-3', 'D-3'])
chordC7 = NoteContainer(['C-3', 'E-3', 'G-3', 'Bb-3'])
print "Sounds Ready."

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
#LED_PIN       = 18      # GPIO pin connected to the pixels (18 uses PWM!). using pin 18 prevents use of analog audio, but fine for HDMI audio
#LED_PIN       = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0). using pin 10 prevents use of SDA bus for capacitive switches
LED_PIN        = 21      # GPIO pin 21 uses PCM, allows both HDMI and analog audio
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#map which neopixels illuminate for each capacitive switch (switch 1 lights up pixels 1 through 4, switch 2 lights up pixels 6 through 10, etc...)
lightSegments = [[0,4], [6,10], [12,14], [16,18], [19,22], [24,26], [27,30], [31,33], [35,37], [39,40], [42,44], [45,49]]

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()
print "Lights Ready."



#initialize 12-key capacitive switch sensor
cap = MPR121.MPR121()
if not cap.begin():
    print 'Error initializing MPR121.  Check your wiring!'
    sys.exit(1)

#plays note and turns off neopixels
def activateKey(key):
    if currentMode > 0 or key > 3:
        fluidsynth.play_Note(Note(notes[currentMode][key]), modeChannels[currentMode], 70)
        print notes[currentMode][key]
    #the 96tears mode is unlike other modes in that the first two switches are drums and the next two switches play chords
    elif key == 0:
        fluidsynth.play_Note(drumSnare, 3, 90)
        print "Snare"  
    elif key == 1:
        fluidsynth.play_Note(drumBass, 3, 127)   
        print "Bass"
    elif key == 2:
        fluidsynth.play_NoteContainer(chordC7, 2, 60)    
        print "Chord C7"  
    elif key == 3:
        fluidsynth.play_NoteContainer(chordG, 2, 60)
        print "Chord G"
    
    #calculate neopixel color, each key is a different shade of the rainbow
    positionProduct = key*255
    notesLength = len(notes[currentMode])
    wheelPosition = positionProduct/notesLength
    #print "Color:", wheelPosition
    for i in range(strip.numPixels()):
        if i >= lightSegments[key][0] and i <= lightSegments[key][1]:
            strip.setPixelColor(i, wheel(wheelPosition))
    strip.show()

#stops note and turns off neopixels
def deactivateKey(key):
    if currentMode > 0 or key > 3:
        fluidsynth.stop_Note(Note(notes[currentMode][key]), modeChannels[currentMode])
    elif key == 0:
        fluidsynth.stop_Note(drumSnare, 3)
    elif key == 1:
        fluidsynth.stop_Note(drumBass, 3)    
    elif key == 2:
        fluidsynth.stop_NoteContainer(chordC7, 2)
    elif key == 3:
        fluidsynth.stop_NoteContainer(chordG, 2)
    
    for i in range(strip.numPixels()):
        if i >= lightSegments[key][0] and i <= lightSegments[key][1]:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def changeMode(channel):
    global modeButtonLastPushed
    global currentMode
    now = time.time()
    if now - modeButtonLastPushed >= 0.3: #debounce button press for 0.3 seconds so that holding down the button (even momentarily while pressing button) doesn't rapidly switch modes
        stopAllNotes()
        currentMode += 1
        modesCount = len(modes)
        temp = currentMode + 1
        if (currentMode + 1) > len(modes):
            currentMode -= len(modes)
        print "Change Mode", modes[currentMode]
    modeButtonLastPushed = now

def stopAllNotes():
    for i in range(12):
        deactivateKey(i)

last_touched = cap.touched()
print "Switches Ready."

#when GPIO button on pin 20 is pressed (voltage rises from low to high), change mode
GPIO.add_event_detect(20, GPIO.RISING, callback=changeMode) 

#flash lights when ready
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255,165,0))
strip.show()
time.sleep(1)
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0,0,0))
strip.show()

#listen for touch events on 12-key capacitive switch sensor
while True:
    try:
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                #print '{0} touched!'.format(i)
                activateKey(i)
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                #print '{0} released!'.format(i)
                deactivateKey(i)
        # Update last state and wait a short period before repeating.
        last_touched = current_touched
        time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()