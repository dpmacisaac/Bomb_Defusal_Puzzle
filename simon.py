import random
from simon_button import simon_button
from gpiozero import Button
from gpiozero import LED
from signal import pause
from time import sleep
import time
random.seed(int(time.time()))



difficulty_chart = {
        'easy': {
            'max_level':6,
            'show_speed':1
                },
        'medium': {
            'max_level':1,
            'show_speed':0.75
                },
        'hard': {
            'max_level':7,
            'show_speed':0.75
                },
        'infinite': {
            'max_level':100000,
            'show_speed':0.75
                }
    }
last_press_time = 0
waiting = True
double_click_threshold = 0.25
class Simon:

    def __init__(self, buttons, difficulty,game_mode):
        '''
            buttons: list of simon_button objects
            difficulty: string with options: 'easy', 'medium', 'hard'
        '''
        self.pressed_list = []
        self.buttons = buttons
        self.difficulty = difficulty
        self.game_mode = game_mode
        self.turn_all_on()
            
    def button_pressed_start_game(self):
        global waiting
        print("press")
        waiting = False

    def button_pressed(self, i):
        global last_press_time
        current_time = time.time()
        diff = (current_time - last_press_time)
        if diff >= double_click_threshold:
            print(diff)
            print(f"PRESSSEd {i}")
            self.pressed_list.append(i)
        else:
            print("double, ignore")
        last_press_time = current_time

    def run_simon(self):
        for i, sm_button in enumerate(self.buttons):
            sm_button.button.when_pressed = lambda: self.button_pressed_start_game()

        while waiting:
            sleep(1)
            
        for i, sm_button in enumerate(self.buttons):
            sm_button.button.when_pressed = lambda i=i: self.button_pressed(i)

        for button in self.buttons:
            button.turn_light_on()
            sleep(0.2)
            button.turn_light_off()
        sleep(0.4)
        self.all_on_indicator()
        sleep(0.4)
        order = []
        for level in range(1,difficulty_chart[self.difficulty]['max_level']+1):
            print(f'level:{level}')
            # gets button order
            order = Simon.random_button_order(level,len(self.buttons),self.game_mode, order)
            print("order generated")
            # show button order
            
            print("showing simon order")
            self.show_order(order)
            self.pressed_list = []
            print("testing user")
            passed = self.check_user_input(order)
            print(f'TEST: {passed}')
            if not passed:
                if self.difficulty == 'infinite':
                    print(f"Your Score: {level-1}")
                self.flash_x(3)
                return 1
            self.all_on_indicator()
            self.turn_all_off()
        
        self.flash_x(0)
        self.buttons[1].led.off()
        return 2

    def flash_x(self,x):
        flash_inc= 0.2
        self.buttons[x].turn_light_off()
        for _ in range(5):
            self.buttons[x].turn_light_on()
            sleep(flash_inc)
            self.buttons[x].turn_light_off()
            sleep(flash_inc)

    def check_user_input(self,order):
        while len(self.pressed_list)<len(order):
            if self.pressed_list != order[:len(self.pressed_list)]:
                return False
            sleep(1)
        print(self.pressed_list)
        print(order)
        if self.pressed_list == order:
            return True
        else:
            return False

    def random_button_order(level:int, buttons_count:int, game_mode, order):
        '''
        input:
            level | int = amount of buttons needed to rbe pressed
            buttons_count | int = amount of buttons that can be in the level
        output:
            button_order_list | [int] = list of buttons
        '''
        if game_mode == 'continuous':
            order.append(random.randint(0,buttons_count-1))
            return order
        button_order_list = []
        for _ in range(level):
            button_order_list.append(random.randint(0,buttons_count-1))

        return button_order_list
    
    def show_order(self, order):
        for button in order:
            sm_button = self.buttons[button]
            sm_button.turn_light_on()
            sleep(difficulty_chart[self.difficulty]['show_speed'])
            sm_button.turn_light_off()
            sleep(0.25)
    
    def turn_all_on(self):
        for sm_button in self.buttons:
            sm_button.turn_light_on()
    def turn_all_off(self):
        for sm_button in self.buttons:
            sm_button.turn_light_off()
    def all_on_indicator(self):
        self.turn_all_on()
        sleep(0.75)
        self.turn_all_off()
        sleep(0.25)

def main():
    #green
    button1 = Button(17)
    led1 = LED(27)
    sm_button1 = simon_button(button1,led1,'green')
    #white
    button2 = Button(2)
    led2 = LED(3)
    sm_button2 = simon_button(button2,led2,'white')
    #blue
    button3 = Button(4)
    led3 = LED(14)
    sm_button3 = simon_button(button3,led3,'blue')
    #red
    button4 = Button(22)
    led4 = LED(23)
    sm_button4 = simon_button(button4,led4,'red')
    simon = Simon([sm_button1,sm_button2,sm_button3,sm_button4],'medium','continuous')
    exit(simon.run_simon())
    '''
    passed = 1
    while passed == 1:
        simon = Simon([sm_button1,sm_button2,sm_button3,sm_button4],'medium','continuous')
        passed = simon.run_simon()
        global waiting
        waiting = True'''
    
if __name__=='__main__':
    main()

