import keyboard
import time
import ctypes
import PIL.ImageGrab
import requests
import datetime

print("*" * 25)
print("* {:^21} *".format("ION TRIGGER BOT V1"))
print("*" * 25)
print() 

def validate_key(k):
    # Retrieve keys from GitHub and Split the keys into list
    url = 'url'
    response = requests.get(url).text.splitlines()

    # Store all non expired keys
    keys = []

    for key in response:
        key, expiry = key.split(",")

        # Convert to datetime.date format
        expiry = datetime.date.fromisoformat(expiry)

        # Check if expired
        if expiry < datetime.date.today():
            continue

        # If not expired, add to non expired keys list
        keys.append(key)

    # Check if the key is in non expired keys list
    if k not in keys:
        return False

    # Return true if passed all checks
    return True

def validate_license_key():
    while True:
        key = input("Enter license key: ")
        if not validate_key(key):
            print("Invalid license key. Please try again.")
        else:
            print()
            print("Valid license key. You can now use ION TRIGGER BOT OFFICIAL V1.0")
            print()
            print("WARNING!!!")
            print()
            print()
            print("DISABLE RAW INPUT BUFFER (IN GENERAL SETTINGS)")
            print("SELECT ANY COLOR, BUT BE SURE TO SELECT LATER IN THE TRIGGER BOT")
            print("RECOMENDED IS PURPLE (AS IT DOESNT HAVE A LOT OF PURPLE IN GAME)")
            print("PUT IT IN WINDOWED FULLSCREEN! ONLY!")
            print()
            return

# Check if license key is valid before running the script
validate_license_key()
    
S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
YELLOW_R, YELLOW_G, YELLOW_B = (255, 255, 0)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
RED_R, RED_G, RED_B = (255, 0, 0)
TOLERANCE = 70

# Get user input for color choice
color_choice = input("Enter color choice (1 for yellow, 2 for purple, 3 for red): ")
if color_choice == "1":
    print("You choose yellow.")
    print()
elif color_choice == "2":
    print("You choose purple.")
    print()
elif color_choice == "3":
    print("You choose red.")
    print()
else:
    print("Invalid choice. Please enter either 1 for yellow or 2 for purple.")
    print()

# User input for sleep duration
print("SHOT DELAY, FOR EX: 0.1 IS THE FASTEST, AND BY ADDING MORE, DELAYS THE SHOTS.")
sleep_duration = float(input("Enter Shot Delay: "))
print("SHOT DELAY IS: ", sleep_duration)
    
# Get user input for TRIGGER_KEY
print()
print("TYPE A KEYBOARD KEY, EX: INSERT, F1, F2.")
TRIGGER_KEY = input("Enter TOGGLE_KEY choice: ")
print("USE TO TOGGLE ON AND OFF")
print()

# Get user input for HOLD_KEY
print("TYPE A KEYBOARD KEY, EX: INSERT, F1, F2.")
HOLD_KEY = input("Enter HOLD_KEY choice: ")
print("USE TO, HOLD TO ON, AND RELEASE TO OFF")
print()

class triggerBot():
    def __init__(self):
        self.toggled = False
        self.held = False

    def toggle(self):
        self.toggled = not self.toggled

    def set_hold(self, status):
        self.held = status

    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up

    def validate(self, r_list, g_list, b_list):
        found = False
        for pixel in  range(0, len(r_list)):
            if self.approx(r_list[pixel], g_list[pixel], b_list[pixel]):
                found = True
        return found

    def approx(self, r, g ,b):
        valid = 0
        if color_choice == "1":  # Yellow color
            if YELLOW_R - TOLERANCE < r < YELLOW_R + TOLERANCE:
                valid += 1
                if YELLOW_G - TOLERANCE < g < YELLOW_G + TOLERANCE:
                    valid += 1
                if YELLOW_B - TOLERANCE < b < YELLOW_B + TOLERANCE:
                    valid += 1
        elif color_choice == "2":  # Purple color
            if PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE:
                valid += 1
                if PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE:
                    valid += 1
                if PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE:
                    valid += 1
        elif color_choice == "3":  # red color
            if RED_R - TOLERANCE < r < RED_R + TOLERANCE:
                valid += 1
                if RED_G - TOLERANCE < g < RED_G + TOLERANCE:
                    valid += 1
                if RED_B - TOLERANCE < b < RED_B + TOLERANCE:
                    valid += 1
        return valid == 3

    def scan(self):
        start_time = time.time()
        r_list = []
        g_list = []
        b_list = []
        grabzone = 15
        pmap = PIL.ImageGrab.grab(bbox=(S_HEIGHT/2-grabzone, S_WIDTH/2-grabzone, S_HEIGHT/2+grabzone, S_WIDTH/2+grabzone))
        for x in range(0, grabzone*2):
            for y in range(0, grabzone*2):
                r, g, b = pmap.getpixel((x,y))
                r_list.append(r)
                g_list.append(g)
                b_list.append(b)
        if self.validate(r_list, g_list, b_list):
            self.click()
            time.sleep(sleep_duration) #user input delay

    def set_toggle(self, status):
        self.toggled = status

if __name__ == "__main__":
    print("WELCOME TO ION TRIGGER BOT OFFICIAL V1.0")
    print()
    print("TOGGLE_KEY IS: ", TRIGGER_KEY)
    print("HOLD_KEY IS: ", HOLD_KEY)
    print()

    bot = triggerBot()
    trigger_active = False  # Initialize trigger state to False
    while True:
        if keyboard.is_pressed(TRIGGER_KEY):
            if not bot.held:  # Check if hold is not active
                trigger_active = not trigger_active  # Toggle trigger state
                bot.toggle()  # Toggle triggerBot's state
                if trigger_active:
                    print("TOGGLE Activated")
                else:
                    print("TOGGLE Deactivated")
                time.sleep(0.1)  # Add delay to avoid multiple toggles in one key press
        if bot.toggled:  # Call bot.scan() while self.toggled is True
            bot.scan()
        if keyboard.is_pressed(HOLD_KEY):
            bot.set_hold(True)
            print("HOLD Activated")
            while keyboard.is_pressed(HOLD_KEY):
                if bot.held:
                    bot.scan()  # Call bot.scan() to perform trigger action
                time.sleep(0.1)
            bot.set_hold(False)
            print("HOLD Deactivated")
