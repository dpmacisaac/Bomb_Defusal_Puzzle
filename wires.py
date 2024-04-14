"""
Module 1 - Wires
This module should have a series of four wires on it that stretch from one side of the module to the other. Players must determine which of the wires they need to cut by speaking to the player with the instruction manual. When the correct wire is cut, the green LED connected to this module lights up signaling it"s complete.
Module 1.5 - Wires Alternative
Players are provided with a bundle of short wires with 3.5mm jacks on either end.  Each wire is a unique color or pattern. Players must use the instruction manual to plug wire into the module in the correct order. There should be no indication of “incorrect” placement, only correct placement. This should be the green  LED connected to the module lighting up when players have placed the wires correctly.
"""

# GPIO Pins 0, 5, 6, 13

from gpiozero import InputDevice
from signal import pause

wire1 = InputDevice(0)
wire2 = InputDevice(5)
wire3 = InputDevice(6)
wire4 = InputDevice(13)


def main(arr, i):
    unplugged1 = False
    unplugged2 = False
    passed = 1
    while(not unplugged1):
        if wire2.value == 0 or wire3.value == 0 or wire4.value == 0:
            unplugged1 = True
        if wire1.value == 0:
            unplugged1 = True
            passed = 2

    if wire1.value == 1:
        arr[i] = 1

    while(not unplugged2):
        if wire2.value == 0 or wire4.value == 0:
            unplugged2 = True
        if wire3.value == 0:
            unplugged2 = True
            passed = 2

    arr[i] = passed
