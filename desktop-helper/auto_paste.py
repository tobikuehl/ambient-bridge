import platform
import time
import pyautogui
import pyperclip

PASTE_KEY = "command" if platform.system() == "Darwin" else "ctrl"


def watch_and_paste():
    print("Desktop Auto-Paste Helper active (Press Ctrl+C to stop)...")
    last_value = pyperclip.paste()
    while True:
        time.sleep(0.3)
        current = pyperclip.paste()
        if current and current != last_value:
            last_value = current
            # Switch focus back to the previously active browser window (Web EHR)
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.25)
            pyautogui.hotkey(PASTE_KEY, "v")


if __name__ == "__main__":
    watch_and_paste()
