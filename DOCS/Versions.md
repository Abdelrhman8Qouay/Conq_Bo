# Version 1

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

# Version 2

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

