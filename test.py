from gpiozero import LED
from signal import pause

led = LED()

led.blink()

pause()
