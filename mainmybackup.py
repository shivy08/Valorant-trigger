import json, time, threading, keyboard, sys
import win32api
from ctypes import WinDLL
import numpy as np
from mss import mss as mss_module
import mouse
import mss
import random


def exiting():
    try:
        print("exiting")
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
        JJJ = 0
        # HELLO GUYS
    except:
        try:
            sys.exit()
        except:
            raise SystemExit
        
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


xxx={}
#hiel
ZONE_X = 2
ZONE_Y = 4
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE_X),
    int(HEIGHT / 2 - ZONE_Y),
    int(WIDTH / 2 + ZONE_X),
    int(HEIGHT / 2),
)
print(GRAB_ZONE)

def storeeeSct(self):
    sct_img=self.sct.grab(GRAB_ZONE)
    output = f"valoSct/sct-{self.i}.png"
    self.i=self.i+1
    print(self.i)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

class triggerbot:
    def __init__(self):
        self.sct = mss_module()
        self.triggerbot = False
        self.triggerbot_toggle = True
        self.exit_program = False 
        self.toggle_lock = threading.Lock()
        self.k = 0
        self.i = 0
        self.delays = [(0, 0), (20,50),(0, 200), (0,300)]
        self.gun_delay = self.delays[0]

        with open('config.json') as json_file:
            data = json.load(json_file)

        try:
            self.trigger_hotkey = int(data["trigger_hotkey"],16)
            self.always_enabled =  data["always_enabled"]
            self.trigger_delay = data["trigger_delay"]/1000.0
            self.base_delay = data["base_delay"]
            self.color_tolerance = data["color_tolerance"]
            self.delays = data.get("gun_delays", self.delays)
            self.R, self.G, self.B = (250, 100, 250)  # purple
            #self.R, self.G, self.B = (255, 255, 0)  # yellow
        except:
            exiting()

    def cooldown(self):
        time.sleep(0.3)
        with self.toggle_lock:
            self.triggerbot_toggle = True
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.triggerbot else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

   
        
    def searcherino(self):
        img = np.array(self.sct.grab(GRAB_ZONE))
        
        
    
        pmap = np.array(img)
        pixels = pmap.reshape(-1, 4)
        color_mask = (
            (pixels[:, 0] > self.R -  self.color_tolerance) & (pixels[:, 0] < self.R +  self.color_tolerance) &
            (pixels[:, 1] > self.G -  self.color_tolerance) & (pixels[:, 1] < self.G +  self.color_tolerance) &
            (pixels[:, 2] > self.B -  self.color_tolerance) & (pixels[:, 2] < self.B +  self.color_tolerance)
        )
        matching_pixels = pixels[color_mask]
        
        if self.triggerbot and len(matching_pixels) > 0:
#             delay_percentage = self.trigger_delay / 100.0 
#             actual_delay = self.base_delay + self.base_delay * delay_percentage
            actual_delay = self.base_delay + self.trigger_delay
            time.sleep(actual_delay)
            spray_delay = random.randint(self.gun_delay[0], self.gun_delay[1])
            
#             print(actual_delay)
            
            keyboard.press("h")
            time.sleep(spray_delay/1000)
            keyboard.release("h")
            time.sleep(actual_delay)
#             storeeeSct(self)
#             mouse.click()
#             self.k = self.k + 1
#             if(self.k%50==0):
#                 print(self.k)


    def toggle(self):
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.triggerbot_toggle:
                    self.triggerbot = not self.triggerbot
                    print(self.triggerbot)
                    self.triggerbot_toggle = False
                    threading.Thread(target=self.cooldown).start()

            if keyboard.is_pressed("ctrl+shift+x"):  # Check for the kkkkk keybind
                self.exit_program = True
                exiting()
        
    def hold(self):
        while True:
            keyboard.is_pressed("ctrl+shift+x")
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True
                self.searcherino()
            else:
                time.sleep(0.1)
            if keyboard.is_pressed("ctrl+shift+x"):  # Check for the exit keybind
                self.exit_program = True
                exiting()

    def starterino(self):
        while not self.exit_program:  # Keep running until the exit_program flag is True
            for i in range(0, len(self.delays)):
                if keyboard.is_pressed(f'ctrl+shift+{i+1}'):
                    self.gun_delay = self.delays[i]
                    kernel32.Beep(440 + i*100, 75)
            if self.always_enabled == True:
                self.toggle()
                self.searcherino() if self.triggerbot else time.sleep(0.1)
            else:
                self.hold()

triggerbot().starterino()