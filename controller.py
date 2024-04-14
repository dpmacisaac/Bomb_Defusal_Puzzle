import threading
import subprocess
import time
import RPi.GPIO as GPIO
import time
import wires
import simon
import keypad

# TIMER STUFF

GPIO.setmode(GPIO.BCM)

pins = (-1,21,20,16,19,26,12,1,7,8,11,9,25)
segments = (11,7,4,2,1,10,5)
digits = (12,9,8,6)
colon = 3

for segment in segments:
    GPIO.setup(pins[segment], GPIO.OUT)
    GPIO.output(pins[segment], 0)

for digit in digits:
    GPIO.setup(pins[digit], GPIO.OUT)
    GPIO.output(pins[digit], 1)

GPIO.setup(pins[colon], GPIO.OUT)
GPIO.output(pins[colon], 1)

NUMBERS = {-2:(0,0,0,0,0,0,1),
    -1:(0,0,0,0,0,0,0),
    0:(1,1,1,1,1,1,0),
    1:(0,1,1,0,0,0,0),
    2:(1,1,0,1,1,0,1),
    3:(1,1,1,1,0,0,1),
    4:(0,1,1,0,0,1,1),
    5:(1,0,1,1,0,1,1),
    6:(1,0,1,1,1,1,1),
    7:(1,1,1,0,0,0,0),
    8:(1,1,1,1,1,1,1),
    9:(1,1,1,1,0,1,1)}

def pause(timeleft):
    while True:
        starttime = time.time()
        currenttime = time.time()

        while currenttime - starttime < 0.5:
            currenttime = time.time()
            if timeleft == -1:
                numbers = [-2, -2, -2, -2]
            else:
                numbers = [-1, int(timeleft / 60), int(timeleft % 60 / 10), int(timeleft % 10)]
            for digit in range(0,4):
                for segment in range(0,7):
                    GPIO.output(pins[segments[segment]], NUMBERS[numbers[digit]][segment])

                GPIO.output(pins[digits[digit]], 0)
                time.sleep(0.001)
                GPIO.output(pins[digits[digit]], 1)

        time.sleep(0.5)

def stop():
    pause(-1)

def timer_main(state):
    starttime = time.time()
    currenttime = time.time()
    timerstart = 5 * 60 + 1
    timeleft = timerstart
    try:
        # while currenttime - starttime < 5:
        #     currenttime = time.time()
        #     timeleft = 5 - (currenttime - starttime)
        #     numbers = [-1, 5, 0, 0]
        #     for digit in range(0,4):
        #         for segment in range(0,7):
        #             GPIO.output(pins[segments[segment]], NUMBERS[numbers[digit]][segment])

        #         GPIO.output(pins[digits[digit]], 0)
        #         time.sleep(0.001)
        #         GPIO.output(pins[digits[digit]], 1)

        # starttime = time.time()
        # currenttime = time.time()
        # timeleft = 5

        while currenttime - starttime < timerstart:
            if state == 2:
                pause(timeleft)
            if state == 1:
                stop()
            currenttime = time.time()
            timeleft = timerstart - (currenttime - starttime)
            numbers = [-1, int(timeleft / 60), int(timeleft % 60 / 10), int(timeleft % 10)]
            for digit in range(0,4):
                for segment in range(0,7):
                    GPIO.output(pins[segments[segment]], NUMBERS[numbers[digit]][segment])

                GPIO.output(pins[digits[digit]], 0)
                time.sleep(0.001)
                GPIO.output(pins[digits[digit]], 1)

        pause(-1)

    finally:
        GPIO.cleanup()

# CONTROLLER

wires_index = 0
keypad_index = 1
simon_index = 2

status_array = [0, 0, 0]

#def run_wires():
#    status_array[wires_index] = subprocess.Popen(["python", "wires.py"])
#    print("Wires Completed:", status_array[wires_index])

#def run_keypad():
#    status_array[keypad_index] = subprocess.Popen(["python", "keypad.py"])
#    print("Keypad Completed:", status_array[keypad_index])

#def run_simon():
#    status_array[simon_index] = subprocess.Popen(["python", "simon.py"])
#    print("Simon Completed:", status_array[simon_index])


def main():

    timer_state = 0

    t1 = threading.Thread(target=wires.main, args=(status_array, wires_index))
    t2 = threading.Thread(target=keypad.main, args=(status_array, keypad_index))
    t3 = threading.Thread(target=simon.main, args=(status_array, simon_index))
    t4 = threading.Thread(target=timer_main, args=(lambda : timer_state, ))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    running = True
    victory = True
    while(running):
        for status in status_array:
            if status == 1:
                victory = False
                running = False
        if not status_array.__contains__(0):
            running = False

    if victory:
        timer_state = 2
    else:
        timer_state = 1

main()

