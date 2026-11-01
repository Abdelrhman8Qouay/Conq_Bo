# src/vision.py
import cv2
import numpy as np
import mss


class Vision:
    def __init__(self):
        self.sct = mss.mss()
        # Adjust these coordinates to match the center of YOUR game screen
        self.monitor = {"top": 240, "left": 460, "width": 1000, "height": 600}

    def capture_screen(self):
        img = np.array(self.sct.grab(self.monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def find_template(self, template_path, threshold=0.75):
        screen = self.capture_screen()
        template = cv2.imread(template_path)

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + (w // 2)
            center_y = max_loc[1] + (h // 2)

            abs_x = self.monitor["left"] + center_x
            abs_y = self.monitor["top"] + center_y
            return (abs_x, abs_y)

        return None
