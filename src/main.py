# src/main.py
import time
import threading
import queue
import os
import json
from vision import Vision
from dashboard import Dashboard

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    settings = json.load(f)
    WINDOWS = settings.get("windows", [])

alert_queue = queue.Queue()


def monitor_account(vision, window_title, alert_queue):
    print(f"[{window_title}] Monitor started.")

    while True:
        try:
            # CPU OPTIMIZATION 3: Scan once every 0.4 seconds
            # This is plenty fast for loot detection, but saves CPU.
            time.sleep(0.4)

            found_items = vision.scan_window(window_title)

            if found_items:
                # Sort by priority to grab the DB/CPS before the silver
                found_items.sort(key=lambda x: x["priority"], reverse=True)
                best_item = found_items[0]

                alert_queue.put(
                    {
                        "window": window_title,
                        "name": best_item["name"],
                        "x": best_item["x"],
                        "y": best_item["y"],
                    }
                )

                # Small cooldown so it doesn't spam the UI while the item is on the ground
                time.sleep(1.5)

        except Exception as e:
            time.sleep(1)


def main():
    print(f"--- V4.5: CPU Optimized Radar System ---")
    vision = Vision(CONFIG_PATH)
    dashboard = Dashboard(alert_queue)

    for window_title in WINDOWS:
        dashboard.add_account_panel(window_title)
        t = threading.Thread(
            target=monitor_account,
            args=(vision, window_title, alert_queue),
            daemon=True,
        )
        t.start()

    try:
        dashboard.run()
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()
