# src/main.py
import os
import time
import random
import keyboard
from vision import Vision
from input import Input


def main():
    print("Starting Conquer Bot V1...")
    print("Press 'F12' at any time to PANIC STOP.")

    vision = Vision()
    action = Input()

    # --- PATH FIX ---
    # Dynamically locate the root directory and templates folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ITEM_TEMPLATE = os.path.join(BASE_DIR, "config", "templates", "item_crop.png")

    print(f"Looking for template at: {ITEM_TEMPLATE}")
    if not os.path.exists(ITEM_TEMPLATE):
        print("ERROR: Image file not found! Check the path above.")
        return

    last_click_time = 0
    click_cooldown = 2.0

    while True:
        if keyboard.is_pressed("F12"):
            print("PANIC STOP TRIGGERED!")
            break

        current_time = time.time()

        if current_time - last_click_time > click_cooldown:

            # 1. Look for the item
            item_location = vision.find_template(ITEM_TEMPLATE, threshold=0.70)

            if item_location:
                print(f"Item found at {item_location}! Clicking...")

                # 2. Click the item
                action.human_click(item_location[0], item_location[1])

                # 3. Reset cooldown
                last_click_time = time.time()

                time.sleep(random.uniform(0.5, 1.2))
            else:
                time.sleep(random.uniform(0.1, 0.3))
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
