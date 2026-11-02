# src/input.py
import pydirectinput
import random
import time
import ctypes
import pygetwindow as gw
import math
import json
import os

pydirectinput.PAUSE = 0.01

# Load settings from config folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")

with open(CONFIG_PATH, "r") as f:
    settings = json.load(f)
    GAME_WINDOW_TITLE = settings.get("window_title", "")


class Input:
    @staticmethod
    def focus_game():
        """Finds the game window by exact title and brings it to the front."""
        try:
            if not GAME_WINDOW_TITLE:
                print("ERROR: 'window_title' is empty in config/settings.json!")
                return False

            # Get window by the exact title from config
            windows = gw.getWindowsWithTitle(GAME_WINDOW_TITLE)

            if windows:
                win = windows[0]
                if not win.isActive:
                    ctypes.windll.user32.SetForegroundWindow(win._hWnd)
                    time.sleep(0.3)  # Wait for Windows to switch
                return win.isActive
            else:
                print(f"Could not find a window titled: '{GAME_WINDOW_TITLE}'")
                return False

        except Exception as e:
            print(f"Focus window error: {e}")
        return False

    @staticmethod
    def move_to_human(target_x, target_y):
        """WindMouse algorithm for human-like curved mouse movement."""
        start_x, start_y = pydirectinput.position()
        dist = math.hypot(target_x - start_x, target_y - start_y)

        if dist < 5:
            pydirectinput.moveTo(target_x, target_y)
            return

        gravity = 9.0
        wind = 3.0
        max_step = 15.0
        target_area = 10.0

        current_x, current_y = start_x, start_y
        velo_x, velo_y = 0.0, 0.0
        wind_x, wind_y = 0.0, 0.0

        while dist >= 1.0:
            wind = min(wind, 3.0)
            wind_x = wind_x / math.sqrt(3) + (
                random.random() * 2 - 1
            ) * wind / math.sqrt(5)
            wind_y = wind_y / math.sqrt(3) + (
                random.random() * 2 - 1
            ) * wind / math.sqrt(5)

            velo_x += wind_x + (gravity * (target_x - current_x) / dist)
            velo_y += wind_y + (gravity * (target_y - current_y) / dist)

            velo_mag = math.hypot(velo_x, velo_y)
            if velo_mag > max_step:
                random_dist = max_step / 2.0 + (random.random() * max_step / 2.0)
                velo_x = (velo_x / velo_mag) * random_dist
                velo_y = (velo_y / velo_mag) * random_dist

            current_x += velo_x
            current_y += velo_y

            pydirectinput.moveTo(int(current_x), int(current_y))
            time.sleep(random.uniform(0.005, 0.015))
            dist = math.hypot(target_x - current_x, target_y - current_y)

            if dist < target_area:
                max_step = 8.0

    @staticmethod
    def pickup_at(x, y):
        """Moves to item with human movement, then clicks and presses pickup key."""
        target_x = x + random.randint(-4, 4)
        target_y = y + random.randint(-4, 4)

        Input.move_to_human(target_x, target_y)
        time.sleep(random.uniform(0.1, 0.2))

        # In Conquer, clicking the item directly usually picks it up,
        # but if you want to use the hotkey, uncomment the press line:
        pydirectinput.click()
        # pydirectinput.press('`')

        time.sleep(random.uniform(0.3, 0.5))
