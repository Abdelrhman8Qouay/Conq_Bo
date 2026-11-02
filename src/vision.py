# src/vision.py
import cv2
import numpy as np
import mss


class Vision:
    def __init__(self):
        self.sct = mss.mss()
        # Keep the region you have been using
        self.monitor = {"top": 240, "left": 460, "width": 1000, "height": 600}
        self.template = None

    def load_template(self, path):
        # Load as grayscale (0) to ignore color variations
        self.template = cv2.imread(path, 0)
        if self.template is None:
            raise Exception(f"Could not load template at {path}")

    def find_template(self, threshold=0.65):
        # Capture screen
        img = np.array(self.sct.grab(self.monitor))

        # Convert screen to grayscale
        screen_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

        # Match template
        result = cv2.matchTemplate(screen_gray, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Convert BGRA to BGR for debug display
        debug_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        if max_val >= threshold:
            h, w = self.template.shape[:2]
            center_x = max_loc[0] + (w // 2)
            center_y = max_loc[1] + (h // 2)

            abs_x = self.monitor["left"] + center_x
            abs_y = self.monitor["top"] + center_y

            # Draw a green box around what it found
            cv2.rectangle(
                debug_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2
            )
            cv2.imshow("Bot Vision", debug_img)
            cv2.waitKey(1)

            return (abs_x, abs_y)

        # Show empty vision box if nothing found
        cv2.imshow("Bot Vision", debug_img)
        cv2.waitKey(1)
        return None
