# src/dashboard.py
import tkinter as tk
from tkinter import ttk
import queue
import time
import keyboard
from input import Input

ACTIVE_TARGET = {"x": 0, "y": 0, "window": ""}


class Dashboard:
    def __init__(self, alert_queue, settings):
        self.root = tk.Tk()
        self.root.title("Conquer Multi-Box Radar")
        self.root.geometry("450x650+50+50")
        # self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e1e")

        self.alert_queue = alert_queue
        self.settings = settings

        # Shared settings to alter monitor speed dynamically
        self.scan_delay = tk.DoubleVar(value=0.4)
        self.ui_opacity = tk.DoubleVar(value=0.95)

        # --- Settings Panel ---
        settings_frame = tk.Frame(self.root, bg="#1e1e1e")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            settings_frame, text="Scan Delay (sec):", bg="#1e1e1e", fg="white"
        ).pack(side=tk.LEFT)
        delay_slider = ttk.Scale(
            settings_frame,
            from_=0.1,
            to=2.0,
            variable=self.scan_delay,
            orient=tk.HORIZONTAL,
            command=self.update_delay,
        )
        delay_slider.pack(side=tk.LEFT, padx=5)

        tk.Label(settings_frame, text="Opacity:", bg="#1e1e1e", fg="white").pack(
            side=tk.LEFT, padx=(10, 0)
        )
        opacity_slider = ttk.Scale(
            settings_frame,
            from_=0.3,
            to=1.0,
            variable=self.ui_opacity,
            orient=tk.HORIZONTAL,
            command=self.update_opacity,
        )
        opacity_slider.pack(side=tk.LEFT, padx=5)

        # --- Title ---
        title_label = tk.Label(
            self.root,
            text="Loot Radar (F9 to Loot)",
            font=("Arial", 14, "bold"),
            fg="cyan",
            bg="#1e1e1e",
        )
        title_label.pack(pady=5)

        self.account_frames = {}
        self.frame_container = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_container.pack(fill=tk.BOTH, expand=True, padx=10)

        self.check_queue()
        keyboard.on_press_key("F9", self.loot_active_target)

    def update_delay(self, val):
        # Update a global variable that main.py reads
        self.settings["scan_delay"] = float(val)

    def update_opacity(self, val):
        self.root.attributes("-alpha", float(val))

    def add_account_panel(self, window_title):
        if window_title in self.account_frames:
            return

        frame = tk.Frame(
            self.frame_container, bg="#2d2d2d", bd=2, relief=tk.RAISED, cursor="hand2"
        )
        frame.pack(fill=tk.X, pady=3)

        frame.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))

        lbl_name = tk.Label(
            frame,
            text=window_title,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#2d2d2d",
            anchor="w",
        )
        lbl_name.pack(fill=tk.X, padx=5, pady=1)

        lbl_status = tk.Label(
            frame,
            text="Scanning...",
            font=("Arial", 9),
            fg="gray",
            bg="#2d2d2d",
            anchor="w",
        )
        lbl_status.pack(fill=tk.X, padx=5, pady=1)

        lbl_name.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))
        lbl_status.bind("<Button-1>", lambda e, w=window_title: Input.focus_window(w))

        self.account_frames[window_title] = {
            "frame": frame,
            "lbl_status": lbl_status,
            "last_alert_time": 0,
        }

    def loot_active_target(self, e):
        if ACTIVE_TARGET["window"] != "":
            Input.focus_window(ACTIVE_TARGET["window"])
            time.sleep(0.1)
            Input.pickup_at(ACTIVE_TARGET["x"], ACTIVE_TARGET["y"])
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
                panel["lbl_status"].config(text="Scanning...", fg="gray", bg="#2d2d2d")
                panel["last_alert_time"] = 0
                if ACTIVE_TARGET["window"] == w_title:
                    ACTIVE_TARGET["window"] = ""

        self.root.after(100, self.check_queue)

    def run(self):
        self.root.mainloop()
