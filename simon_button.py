from gpiozero import Button
from gpiozero import LED
class simon_button:
    def __init__(self, button, led, color):
        self.led = led
        self.button = button
        self.color = color

    def turn_light_on(self):
        if not self.led.is_lit:
            self.led.on()

    def turn_light_off(self):
        if self.led.is_lit:
            self.led.off()
