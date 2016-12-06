from random import randint
from sense_hat import SenseHat
from evdev import InputDevice, categorize, ecodes
import sys
#Exemple extret d'internet
#https://khanhicetea.com/post/read_input_from_usb_keyboard_in_linux/

CODE_MAP_CHAR = {
    'KEY_MINUS': "-",
    'KEY_SPACE': " ",    
    'KEY_U': "U",
    'KEY_W': "W",
    'KEY_BACKSLASH': "\\",
    'KEY_GRAVE': "`",
    'KEY_NUMERIC_STAR': "*",
    'KEY_NUMERIC_3': "3",
    'KEY_NUMERIC_2': "2",
    'KEY_NUMERIC_5': "5",
    'KEY_NUMERIC_4': "4",
    'KEY_NUMERIC_7': "7",
    'KEY_NUMERIC_6': "6",
    'KEY_NUMERIC_9': "9",
    'KEY_NUMERIC_8': "8",
    'KEY_NUMERIC_1': "1",
    'KEY_NUMERIC_0': "0",
    'KEY_E': "E",
    'KEY_D': "D",
    'KEY_G': "G",
    'KEY_F': "F",
    'KEY_A': "A",
    'KEY_C': "C",
    'KEY_B': "B",
    'KEY_M': "M",
    'KEY_L': "L",
    'KEY_O': "O",
    'KEY_N': "N",
    'KEY_I': "I",
    'KEY_H': "H",
    'KEY_K': "K",
    'KEY_J': "J",
    'KEY_Q': "Q",
    'KEY_P': "P",
    'KEY_S': "S",
    'KEY_X': "X",
    'KEY_Z': "Z",
    'KEY_KP4': "4",
    'KEY_KP5': "5",
    'KEY_KP6': "6",
    'KEY_KP7': "7",
    'KEY_KP0': "0",
    'KEY_KP1': "1",
    'KEY_KP2': "2",
    'KEY_KP3': "3",
    'KEY_KP8': "8",
    'KEY_KP9': "9",
    'KEY_5': "5",
    'KEY_4': "4",
    'KEY_7': "7",
    'KEY_6': "6",
    'KEY_1': "1",
    'KEY_0': "0",
    'KEY_3': "3",
    'KEY_2': "2",
    'KEY_9': "9",
    'KEY_8': "8",
    'KEY_LEFTBRACE': "[",
    'KEY_RIGHTBRACE': "]",    
    'KEY_COMMA': ",",
    'KEY_EQUAL': "=",    
    'KEY_SEMICOLON': ";",
    'KEY_APOSTROPHE': "'",
    'KEY_T': "T",
    'KEY_V': "V",
    'KEY_R': "R",
    'KEY_Y': "Y",
    'KEY_TAB': "\t",
    'KEY_DOT': ".",
    'KEY_SLASH': "/",
}

def parse_key_to_char(val):
    if isinstance(val,list):
        return ""
    elif val in CODE_MAP_CHAR:
        return CODE_MAP_CHAR[val]
    else:
        print(val)
        return ""

sense = SenseHat()
sense.clear()
sense.set_rotation(180)

dev = InputDevice('/dev/input/event1')
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        e = categorize(event)
        if e.keystate == e.key_up:
            sys.stdout.write(parse_key_to_char(e.keycode))
            sys.stdout.flush()
            sense.show_letter(parse_key_to_char(e.keycode),text_colour=[randint(0,255),randint(0,255),randint(0,255)])
