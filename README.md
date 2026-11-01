Let's build the foundation. For **Version 1**, we will focus strictly on the core loop: **Find Item -> Move Mouse -> Click -> Verify**.

We will completely ignore the puzzle, combat, and death for now. If the bot gets stuck, you press `F12` to kill it. This allows you to test your screen capture speed, OpenCV accuracy, and human-like mouse movement in isolation.

### 📁 Step 1: Project Setup

Create a new folder, open it in your IDE (like VS Code), and create the following files:

```text
conquer_bot/
├── config/
│   └── templates/
│       └── (You will save item_crop.png here)
├── src/
│   ├── vision.py
│   ├── input.py
│   └── main.py
└── requirements.txt
```

**`requirements.txt`** (Run `pip install -r requirements.txt`):

```text
opencv-python
numpy
mss
pydirectinput
keyboard
```

---

### 🛠️ Step 2: The Core Modules

#### 1. `src/vision.py` (The Eyes)

We use `mss` instead of `dxcam` for Version 1 because it's incredibly stable, requires zero complex setup, and is fast enough for basic gathering. We will use OpenCV to find your item template.

```python
# src/vision.py
import cv2
import numpy as np
import mss

class Vision:
    def __init__(self):
        self.sct = mss.mss()
        # Define the region you want to scan (e.g., the center of your screen)
        # Adjust these values based on your resolution.
        # For 1920x1080, this scans a 1000x600 box in the middle.
        self.monitor = {"top": 240, "left": 460, "width": 1000, "height": 600}

    def capture_screen(self):
        """Grabs the screen and returns it as an OpenCV image."""
        img = np.array(self.sct.grab(self.monitor))
        # Convert BGRA to BGR (OpenCV format)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def find_template(self, template_path, threshold=0.75):
        """
        Looks for the template on the screen.
        Returns the absolute screen (X, Y) center of the match, or None.
        """
        screen = self.capture_screen()
        template = cv2.imread(template_path)

        if template is None:
            raise FileNotFoundError(f"Template not found: {template_path}")

        # Perform template matching
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # Calculate the center of the bounding box
            h, w = template.shape[:2]
            center_x = max_loc[0] + (w // 2)
            center_y = max_loc[1] + (h // 2)

            # Convert relative coordinates back to absolute screen coordinates
            abs_x = self.monitor["left"] + center_x
            abs_y = self.monitor["top"] + center_y
            return (abs_x, abs_y)

        return None
```

#### 2. `src/input.py` (The Hands)

We use `pydirectinput` because standard `pyautogui` often fails to register clicks in DirectX games. We also add random variance to make the clicks imperfect.

```python
# src/input.py
import pydirectinput
import random
import time
import math

pydirectinput.PAUSE = 0.01 # Add a tiny delay between actions

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
```

#### 3. `src/main.py` (The Brain)

This is the main loop. It uses a very basic state check and relies on a "cooldown" so it doesn't spam click the same item 60 times a second.

```python
# src/main.py
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

    # Path to the item you want to collect (Cropped screenshot of the purple orb)
    ITEM_TEMPLATE = "../config/templates/item_crop.png"

    last_click_time = 0
    click_cooldown = 2.0 # Wait 2 seconds after clicking before clicking again

    while True:
        # PANIC BUTTON
        if keyboard.is_pressed('F12'):
            print("PANIC STOP TRIGGERED!")
            break

        current_time = time.time()

        # Only look for items if we aren't on cooldown
        if current_time - last_click_time > click_cooldown:

            # 1. Look for the item
            item_location = vision.find_template(ITEM_TEMPLATE, threshold=0.70)

            if item_location:
                print(f"Item found at {item_location}! Clicking...")

                # 2. Click the item
                action.human_click(item_location[0], item_location[1])

                # 3. Reset cooldown
                last_click_time = time.time()

                # Human reaction time before looking again
                time.sleep(random.uniform(0.5, 1.2))
            else:
                # If no item found, wait a bit before checking again to save CPU
                time.sleep(random.uniform(0.1, 0.3))
        else:
            # Waiting for cooldown to expire
            time.sleep(0.1)

if __name__ == "__main__":
    main()
```

---

### 🎯 Step 3: Your First Test Run

You need to create the template image. This is the most important part of Vision-based bots.

1. Run the game. Find the purple orb (or whatever mob/item you are targeting).
2. Take a screenshot of your screen.
3. Open the screenshot in Paint or Photoshop.
4. Crop **ONLY** the item. Do not include the ground, the text above it, or the health bars. Just the orb itself.
5. Save it as `item_crop.png` inside `config/templates/`.

**To test:**

1. Open your terminal, navigate to `src/`, and run `python main.py`.
2. Tab into the game.
3. Wait for a purple orb to drop.
4. Watch the mouse move to it, click with a slight offset, and wait.

### ⚠️ V1 Limitations (What to expect)

- **It will click through walls/UI:** Because it just looks at pixels, if your inventory covers where the orb is, it will click your inventory. (Don't worry, we fix this in V2 by detecting the UI).
- **It might get stuck:** If the item drops on a cliff you can't reach, the bot will keep clicking it. (The `click_cooldown` helps prevent instant bans, but you'll need to move manually if it happens).
- **The template must be perfect:** If the lighting changes or the item is partially covered by a monster, `find_template` might fail. You can lower the `threshold` in `main.py` to `0.60` if it's missing items, but don't lower it too much or it will click random rocks.

### 📝 Next Steps (For V2)

Once you confirm this loops perfectly and clicks at a human pace, we will add:

1.  **UI Masking:** Teach the bot to ignore the bottom half of the screen (where the chat and inventory are).
2.  **The Puzzle Handler:** Adding the web CAPTCHA solving logic.
3.  **Health checks:** Reading the HP orb.

Get V1 running smoothly first. Let me know when you have it clicking the item successfully, and we will move to the next phase!
