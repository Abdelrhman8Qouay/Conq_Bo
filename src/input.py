# src/input.py
import ctypes
import ctypes.wintypes
import time
import random
import math
import win32gui
import win32con
import threading

# --- Windows API Constants ---
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]

    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.wintypes.DWORD), ("_input", _INPUT)]


def send_mouse_input(flags, x=0, y=0):
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT()
    ii_.mi = MOUSEINPUT(x, y, 0, flags, 0, ctypes.pointer(extra))
    x_input = INPUT(INPUT_MOUSE, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x_input), ctypes.sizeof(x_input))


def send_keyboard_input(vk_code, flags=0):
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT()
    ii_.ki = KEYBDINPUT(vk_code, 0, flags, 0, ctypes.pointer(extra))
    x_input = INPUT(INPUT_KEYBOARD, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x_input), ctypes.sizeof(x_input))


def get_cursor_pos():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


class Input:
    @staticmethod
    def focus_window(window_title):
        """Brings the specific game window to the front."""

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
            # Restore if minimized
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        return False

    @staticmethod
    def hold_ctrl():
        send_keyboard_input(VK_CONTROL)

    @staticmethod
    def release_ctrl():
        send_keyboard_input(VK_CONTROL, KEYEVENTF_KEYUP)

    @staticmethod
    def move_to_human(target_x, target_y):
        start_x, start_y = get_cursor_pos()
        dist = math.hypot(target_x - start_x, target_y - start_y)

        if dist < 15:
            send_mouse_input(MOUSEEVENTF_MOVE, target_x - start_x, target_y - start_y)
            time.sleep(random.uniform(0.005, 0.015))
            return

        steps = random.randint(3, 5)
        for i in range(1, steps + 1):
            t = i / steps
            ease_t = 1 - (1 - t) ** 1.5
            current_x, current_y = get_cursor_pos()
            next_x = start_x + (target_x - start_x) * ease_t
            next_y = start_y + (target_y - start_y) * ease_t
            dx = int(next_x - current_x)
            dy = int(next_y - current_y)
            if dx != 0 or dy != 0:
                send_mouse_input(MOUSEEVENTF_MOVE, dx, dy)
            time.sleep(random.uniform(0.002, 0.006))

        current_x, current_y = get_cursor_pos()
        send_mouse_input(MOUSEEVENTF_MOVE, target_x - current_x, target_y - current_y)
        time.sleep(random.uniform(0.02, 0.06))

    @staticmethod
    def pickup_at(x, y):
        target_x = x + int(random.gauss(0, 2))
        target_y = y + int(random.gauss(0, 2))
        Input.hold_ctrl()
        Input.move_to_human(target_x, target_y)
        Input.release_ctrl()
        time.sleep(random.uniform(0.01, 0.03))
        send_mouse_input(MOUSEEVENTF_LEFTDOWN)
        time.sleep(random.uniform(0.03, 0.06))
        send_mouse_input(MOUSEEVENTF_LEFTUP)
        time.sleep(random.uniform(0.1, 0.2))
