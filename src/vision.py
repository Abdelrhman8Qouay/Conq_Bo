# src/vision.py
import cv2
import numpy as np
import mss
import win32gui
import os
import json


class Vision:
    def __init__(self, config_path):
        self.sct = mss.mss()
        self.loaded_templates = []
        self.scale = 0.5

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(config_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        templates_dir = os.path.join(BASE_DIR, "config", "templates")

        for item in settings.get("items", []):
            path = os.path.join(templates_dir, item["image"])

            # Load in COLOR (1) instead of Grayscale (0) to prevent phantom detections
            template = cv2.imread(path, 1)

            if template is not None:
                h, w = template.shape[:2]
                resized_template = cv2.resize(
                    template, (int(w * self.scale), int(h * self.scale))
                )

                self.loaded_templates.append(
                    {
                        "name": item["name"],
                        "priority": item.get("priority", 1),
                        # INCREASE THRESHOLD: Phantom detections usually happen below 0.8
                        "threshold": max(item.get("threshold", 0.8), 0.8),
                        "image": resized_template,
                    }
                )

    def get_game_rect(self, window_title):
        hwnd = None

        def enum_cb(h, results):
            if (
                win32gui.IsWindowVisible(h)
                and win32gui.GetWindowText(h) == window_title
            ):
                results.append(h)
            return True

        results = []
        win32gui.EnumWindows(enum_cb, results)
        if results:
            hwnd = results[0]
            rect = win32gui.GetClientRect(hwnd)
            pt = win32gui.ClientToScreen(hwnd, (0, 0))
            return (pt[0], pt[1], pt[0] + rect[2], pt[1] + rect[3])
        return None

    def scan_window(self, window_title):
        rect = self.get_game_rect(window_title)
        if not rect:
            return None

        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        roi_x = rect[0] + int(width * 0.2)
        roi_y = rect[1] + int(height * 0.3)
        roi_w = int(width * 0.6)
        roi_h = int(height * 0.5)

        monitor = {"top": roi_y, "left": roi_x, "width": roi_w, "height": roi_h}
        img = np.array(self.sct.grab(monitor))

        # Convert BGRA to BGR (remove alpha channel)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img_small = cv2.resize(img_bgr, (0, 0), fx=self.scale, fy=self.scale)

        found_items = []

        for item in self.loaded_templates:
            template = item["image"]

            # Use TM_CCOEFF_NORMED but on color images
            result = cv2.matchTemplate(img_small, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= item["threshold"])

            for pt in zip(*locations[::-1]):
                real_x = int(pt[0] / self.scale) + roi_x
                real_y = int(pt[1] / self.scale) + roi_y

                found_items.append(
                    {
                        "name": item["name"],
                        "priority": item["priority"],
                        "x": real_x,
                        "y": real_y,
                        "window": window_title,
                    }
                )

        return found_items if found_items else None
