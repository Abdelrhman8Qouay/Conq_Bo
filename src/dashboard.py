# src/dashboard.py
import tkinter as tk
import queue
import time
import keyboard
from input import Input

# Global storage for the last detected item coordinates
# So pressing F9 knows where to click
ACTIVE_TARGET = {"x": 0, "y": 0, "window": ""}


class Dashboard:
    def __init__(self, alert_queue):
        self.root = tk.Tk()
        self.root.title("Conquer Multi-Box Radar")
        self.root.geometry("450x500+50+50")
        # self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e1e")

        self.alert_queue = alert_queue

        title_label = tk.Label(
            self.root,
            text="Loot Radar (F9 to Loot)",
            font=("Arial", 14, "bold"),
            fg="cyan",
            bg="#1e1e1e",
        )
        title_label.pack(pady=10)

        self.account_frames = {}
        self.frame_container = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_container.pack(fill=tk.BOTH, expand=True, padx=10)

        self.check_queue()

        # Start a background listener for the F9 key
        self.listener_thread = keyboard.on_press_key("F9", self.loot_active_target)

    def add_account_panel(self, window_title):
        if window_title in self.account_frames:
            return

        frame = tk.Frame(
            self.frame_container, bg="#2d2d2d", bd=2, relief=tk.RAISED, cursor="hand2"
        )
        frame.pack(fill=tk.X, pady=5)

        # UI TRICK: Clicking the panel brings the window to the front
        frame.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))

        lbl_name = tk.Label(
            frame,
            text=window_title,
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2d2d2d",
            anchor="w",
        )
        lbl_name.pack(fill=tk.X, padx=5, pady=2)

        lbl_status = tk.Label(
            frame,
            text="Scanning... (Safe)",
            font=("Arial", 10),
            fg="gray",
            bg="#2d2d2d",
            anchor="w",
        )
        lbl_status.pack(fill=tk.X, padx=5, pady=2)

        # Bind labels too so clicking anywhere on the panel works
        lbl_name.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))
        lbl_status.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))

        self.account_frames[window_title] = {
            "frame": frame,
            "lbl_status": lbl_status,
            "last_alert_time": 0,
        }

    def loot_active_target(self, e):
        """Triggers when you press F9. Clicks the target if one exists."""
        if ACTIVE_TARGET["window"] != "":
            # Bring window to front (just in case)
            Input.focus_window(ACTIVE_TARGET["window"])
            time.sleep(0.1)  # Tiny delay to let window focus
            # Trigger the auto-clicker
            Input.pickup_at(ACTIVE_TARGET["x"], ACTIVE_TARGET["y"])
            # Clear target to prevent double-clicking
            ACTIVE_TARGET["window"] = ""

    def check_queue(self):
        try:
            while True:
                alert = self.alert_queue.get_nowait()
                w_title = alert["window"]
                item_name = alert["name"]

                if w_title in self.account_frames:
                    panel = self.account_frames[w_title]
                    panel["frame"].config(bg="#8b0000")
                    panel["lbl_status"].config(
                        text=f"DETECTED: {item_name}!", fg="yellow", bg="#8b0000"
                    )
                    panel["last_alert_time"] = time.time()

                    # Update global target for F9
                    ACTIVE_TARGET["x"] = alert["x"]
                    ACTIVE_TARGET["y"] = alert["y"]
                    ACTIVE_TARGET["window"] = w_title

                    self.root.bell()
        except queue.Empty:
            pass

        current_time = time.time()
        for w_title, panel in self.account_frames.items():
            if (
                panel["last_alert_time"] > 0
                and (current_time - panel["last_alert_time"]) > 4.0
            ):
                panel["frame"].config(bg="#2d2d2d")
                panel["lbl_status"].config(
                    text="Scanning... (Safe)", fg="gray", bg="#2d2d2d"
                )
                panel["last_alert_time"] = 0

                # Clear target if it timed out (the item probably despawned)
                if ACTIVE_TARGET["window"] == w_title:
                    ACTIVE_TARGET["window"] = ""

        self.root.after(100, self.check_queue)

    def run(self):
        self.root.mainloop()
