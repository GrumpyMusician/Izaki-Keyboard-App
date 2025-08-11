import pyperclip
import webview
import os
import keyboard
import threading
import ctypes
import pandas as pd

class API:
    def close_app(self):
        webview.windows[0].destroy()

def getprevchar():
    try:
        old_clip = pyperclip.paste()
    except Exception:
        old_clip = ''

    keyboard.press_and_release('shift+left')
    keyboard.press_and_release('ctrl+c')
    try:
        char = pyperclip.paste()
    except Exception:
        char = ''

    try:
        pyperclip.copy(old_clip)
    except Exception:
        pass

    keyboard.press_and_release('right')
    return char

def listen_keys():  
    mode = 0  # 0 = System, 1 = Latinzied, 2 = Askaoza, 3 = Bai
    pressed_keys = set()  # Track currently pressed keys
    
    #keyboard.write(char) #Injects character at caret

    def on_event(e):
        nonlocal mode

        if e.event_type == "down":
            pressed_keys.add(e.scan_code)
        elif e.event_type == "up":
            pressed_keys.discard(e.scan_code)

        print(pressed_keys, mode)

        if 42 in pressed_keys or 54 in pressed_keys:
            webview.windows[0].evaluate_js("window.shift(true)")
            
            if 42 in pressed_keys and 54 in pressed_keys:
                mode += 1
                if mode > 3:
                    mode = 0

            if mode == 2:
                mode = 3

            if bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1) and mode == 3:
                mode = 2

            webview.windows[0].evaluate_js(f"window.mode({mode})")            
        else:
            webview.windows[0].evaluate_js("window.shift(false)")

            if mode == 3:
                mode = 2

            if bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1) and mode == 2:
                mode = 3
            
            webview.windows[0].evaluate_js(f"window.mode({mode})")

        if bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1):
            webview.windows[0].evaluate_js("window.caps(true)")
        else:
            webview.windows[0].evaluate_js("window.caps(false)")

        # Mode Dependent Stuff -------------------------------------------------------------------------------------------------
        if mode == 0:
            webview.windows[0].evaluate_js("window.system(true)")
            webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[1]})")
            webview.windows[0].evaluate_js(f"window.keyboard({list(pressed_keys)})") # Make keyboard go blinky-blinky
        elif mode == 1:
            webview.windows[0].evaluate_js("window.system(false)")

            if not bool(ctypes.WinDLL("User32.dll").GetKeyState(0x10) & 0x8000) and not bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1):
                # No shift, no caps
                webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[2]})")
            elif bool(ctypes.WinDLL("User32.dll").GetKeyState(0x10) & 0x8000) and not bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1):
                # Shift, no caps
                webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[3]})")
            elif not bool(ctypes.WinDLL("User32.dll").GetKeyState(0x10) & 0x8000) and bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1):
                # No shift, caps
                webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[4]})")
            else:
                # Shift and caps
                webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[5]})")

            webview.windows[0].evaluate_js(f"window.keyboard({list(pressed_keys)})") # Make keyboard go blinky-blinky

        else:
            webview.windows[0].evaluate_js(f"text({latinized[0]}, {latinized[1]})")
            webview.windows[0].evaluate_js(f"window.keyboard({list(pressed_keys)})") # Make keyboard go blinky-blinky

    keyboard.hook(on_event)
    keyboard.wait()

api = API()

file_path = os.path.abspath("index.html")
webview.create_window(
    "Izaki Keyboard",
    f"file://{file_path}",
    width=630,
    height=310,
    frameless=True,
    on_top=True,
    js_api=api
)


latinized = pd.read_csv("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=1653244319").fillna('').values.tolist()
#doubled = pd.read_csv("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=1877749518", header=None).fillna('').values.tolist()
#askaoza = {row[0]: row[1:].tolist() for _, row in pd.read_csv("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=457897588").fillna('').iterrows()}

# Start keyboard listener in background thread
threading.Thread(target=listen_keys, daemon=True).start()

webview.start()

