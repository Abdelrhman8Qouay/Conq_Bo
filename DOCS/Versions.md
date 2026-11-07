# Version 1.1.0

You need to create the template image. This is the most important part of Vision-based bots.

- Run the game. Find the purple orb (or whatever mob/item you are targeting).
- Take a screenshot of your screen.
- Open the screenshot in Paint or Photoshop.
- Crop ONLY the item. Do not include the ground, the text above it, or the health bars. Just the orb itself.
- Save it as item_crop.png inside config/templates/.

To test:

- Open your terminal, navigate to src/, and run python main.py.
- Tab into the game.
- Wait for a purple orb to drop.
- Watch the terminal output.

# Version 1.3.0

we need to make the bot act like a real player:

- Stop spamming: Add a cooldown so it doesn't click the same item 20 times a second.
- Use the Pickup Key: Instead of clicking the ground, move the mouse near the item and press ~.
- Logging: Print exactly what the bot is doing so you can debug its behavior.

🔬 How to test this:

- Double-click Run_Bot.bat.
- Windows will pop up a User Account Control (UAC) prompt asking for permission. Click Yes.
- A new terminal window will open automatically, showing your Python prints.
- Click on your Conquer Online game window to make it the active window.
- Wait for the item to drop. Because the script is now running with Administrator privileges, pydirectinput will be able to send the click and the ~ key directly to the game, bypassing any focus issues!

# Version 1.3.0

## To address your weak CPU, we are abandoning "brute force" screen scanning. Instead of checking every pixel of the screen 10 times a second, we are implementing Three Major Optimizations:

Region of Interest (ROI) Locking: We only scan the bottom-middle area of the screen where monsters drop loot. We ignore the sky, UI, and chat.
Downscaling: We shrink the captured image by 50% before running OpenCV. This reduces CPU usage by 75% with almost zero loss in accuracy.
Dynamic Polling: We don't spam the CPU. The scanner runs once every 0.4 seconds, which is still incredibly fast (faster than human reaction time) but gives your CPU breathing room.

- We also added the UI Tricks: Clicking the dashboard instantly brings that specific game window to the front, and pressing F9 executes a smart pickup using the coordinates the radar already found.

### src/input.py (Added Window Focus)

We add a function to bring specific windows to the foreground when you click them on the dashboard.

### src/vision.py (CPU Optimized)

We downscale the image by 0.5 (50%) and crop the screen to a central rectangle. We also return the exact coordinates of the item so we can auto-pick it up later.

### src/dashboard.py (UI Tricks)

Added on_click events. When you click the flashing panel, it automatically brings that game window to the front. It also updates a global "Target Coordinates" so you can press F9 to loot.

### src/main.py (Dynamic Polling)

We adjust the sleep timer to prevent CPU maxing out.

### How the Workflow works now:

You leave your 3 Archers on auto-bot.
The radar scans them every 0.4 seconds in the background. Your CPU will sit at maybe 5-10% usage.
A DB drops on Account 2. The dashboard panel for Account 2 flashes Red and beeps.
You look at your 2nd monitor, see the red flash.
You click the red panel with your mouse. Python instantly brings Account 2 to the front of your screen.
You press F9. The bot automatically moves your mouse to the exact coordinates of the DB, holds Ctrl, and clicks it.
You Alt-Tab back to what you were doing.

# Version 1.3.1

- Improved the Monitor Radar.
