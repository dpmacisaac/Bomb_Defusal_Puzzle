"""
Module 2 - Keypad
This module should have a small 4 character keyboard section connected to the module. Players must determine what order the keys must be pressed in to finish the module by referencing the instruction manual. When the buttons are pressed in the correct order, the green LED connected to this module lights up, signaling it's complete.
"""
from gpiozero import LED

led = LED(10)
led.off() #Set the led off at the beginning

def main(arr, i):
    true_input = "bomb"
    inp = ''

    while inp != true_input.lower():
        inp = input("Enter the keypad:")
        if(inp == true_input.lower()):
            led.on()
            arr[i] = 2
        else:
            arr[i] = 1