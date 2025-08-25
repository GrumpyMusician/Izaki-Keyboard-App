import os
import pandas as pd
import json
import webview
import threading
import subprocess
import socket
import signal
import psutil   # pip install psutil

# -------------------------
# 1. Fetch Latinized Mappings from Google Sheet
# -------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=1653244319"
latinized = dict(zip(
    pd.read_csv(sheet_url, header=None)[0].astype(str),
    pd.read_csv(sheet_url, header=None)[1].astype(str)
))

with open("latinized.json", "w", encoding="utf-8") as f:
    json.dump(latinized, f, ensure_ascii=False, indent=2)

# -------------------------
# 2. Shared state for AHK socket
# -------------------------
keyboard_state = {"mode": "System", "keys": []}

def socket_server(host="127.0.0.1", port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Socket listening on {host}:{port}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                msg = json.loads(data.decode())
                keyboard_state["mode"] = msg.get("mode", keyboard_state["mode"])
                keyboard_state["keys"] = msg.get("keys", keyboard_state["keys"])
                print("Updated keyboard state:", keyboard_state)
            except Exception as e:
                print("Error decoding message:", e)

threading.Thread(target=socket_server, daemon=True).start()

# -------------------------
# 3. Webview for live keyboard
# -------------------------
class API:
    def get_state(self):
        return keyboard_state
    
    def close(self):
        webview.windows[0].destroy()

api = API()
file_path = os.path.abspath("index.html")

window = webview.create_window(
    "Izaki Keyboard",
    f"file://{file_path}",
    width=630,
    height=310,
    frameless=True,
    on_top=True,
    js_api=api
)

# -------------------------
# 4. Launch AHK v2 script automatically
# -------------------------
ahk_exe = os.path.join(os.getcwd(), "AutoHotkey.exe")
ahk_script = os.path.join(os.getcwd(), "keyboard.ahk")
ahk_proc = subprocess.Popen([ahk_exe, ahk_script], shell=True)

# -------------------------
# 5. Ensure AHK is killed when Python exits
# -------------------------
def kill_ahk():
    try:
        # If we started it, kill that process
        ahk_proc.terminate()
    except Exception:
        pass

    # Extra safety: kill any stray AutoHotkey.exe processes
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] and "AutoHotkey.exe" in proc.info["name"]:
            try:
                os.kill(proc.info["pid"], signal.SIGTERM)
            except Exception:
                pass

import atexit
atexit.register(kill_ahk)

# -------------------------
# 6. Run the UI
# -------------------------
webview.start()
