# src/input.py
import pydirectinput
import random
import time
import math

pydirectinput.PAUSE = 0.01  # Add a tiny delay between actions


class Input:
    @staticmethod
    def human_click(x, y):
        """Moves to coordinates with slight variance, then clicks."""
        # Add slight random offset (miss the exact center by a few pixels)
        offset_x = random.randint(-8, 8)
        offset_y = random.randint(-8, 8)
        target_x = x + offset_x
        target_y = y + offset_y

        # Move mouse
        pydirectinput.moveTo(target_x, target_y)

        # Random human delay before clicking
        time.sleep(random.uniform(0.1, 0.3))

        # Click
        pydirectinput.click()

        # Random delay after clicking
        time.sleep(random.uniform(0.2, 0.5))
