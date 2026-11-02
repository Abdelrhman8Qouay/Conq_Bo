# src/main.py
import os
import time
import keyboard
from vision import Vision
from input import Input


def main():
    print("--- TEST MODE: Bypassing Window Focus ---")
    print("1. CLICK ON YOUR GAME WINDOW NOW.")
    print("2. Do not click back on the terminal.")
    print("Press 'F12' to stop.")

    vision = Vision()
    action = Input()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ITEM_TEMPLATE = os.path.join(BASE_DIR, "config", "templates", "item_crop.png")

    vision.load_template(ITEM_TEMPLATE)

    last_action_time = 0
    ACTION_COOLDOWN = 1.5

    while True:
        if keyboard.is_pressed("F12"):
            print("PANIC STOP TRIGGERED!")
            break

        current_time = time.time()

        if current_time - last_action_time > ACTION_COOLDOWN:
            item_location = vision.find_template(threshold=0.65)

            if item_location:
                print(f"Item detected at {item_location}! Clicking BLINDLY...")

                # Bypass focus_game() entirely!
                action.pickup_at(item_location[0], item_location[1])

                last_action_time = time.time()

            else:
                time.sleep(0.1)
        else:
            time.sleep(0.05)


if __name__ == "__main__":
    main()
