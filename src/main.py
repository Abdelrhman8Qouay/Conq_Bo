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
    settings_data = json.load(f)
    WINDOWS = settings_data.get("windows", [])

# Create a shared settings dictionary for live updates
live_settings = {"scan_delay": 0.4}
alert_queue = queue.Queue()


def monitor_account(vision, window_title, alert_queue, live_settings):
    while True:
        try:
            # Read dynamic delay set by the UI
            time.sleep(live_settings["scan_delay"])

            found_items = vision.scan_window(window_title)

            if found_items:
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
                time.sleep(1.5)  # Cooldown to prevent spam
        except Exception as e:
            time.sleep(1)


def main():
    vision = Vision(CONFIG_PATH)
    dashboard = Dashboard(alert_queue, live_settings)

    for window_title in WINDOWS:
        dashboard.add_account_panel(window_title)
        t = threading.Thread(
            target=monitor_account,
            args=(vision, window_title, alert_queue, live_settings),
            daemon=True,
        )
        t.start()

    try:
        dashboard.run()
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()
