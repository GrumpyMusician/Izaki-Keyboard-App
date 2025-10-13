import requests
import csv
import json
from hotkeys import hotkeys
from plyer import notification
import webview
import threading
import keyboard
def main():
    try:
        importtojson("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=457897588", "master.json")
    except requests.exceptions.ConnectionError as e:
        notification.notify(title='Internet Connection Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.Timeout as e:
        notification.notify(title='Internet Timeout Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.RequestException as e:
        notification.notify(title='Internet Request Exception Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)

    threading.Thread(target = startHotkey, daemon = True).start()
    startWebview()

def importtojson(url, target):
    response = requests.get(url)
    response.raise_for_status()

    csv_text = response.content.decode('utf-8').splitlines()

    reader = csv.DictReader(csv_text)

    data = {}

    for row in reader:
        key = row[reader.fieldnames[0]]
        nested = {k: v for k, v in row.items() if k != reader.fieldnames[0]}
        data[key] = nested

    with open(target, "w", encoding = "utf-8") as file:
        file.write("{\n")
        items = list(data.items())
        for i, (key, value) in enumerate(items):
            json_value = json.dumps(value, ensure_ascii = False)
            if i < len(items) - 1:
                file.write(f'  "{key}": {json_value},\n')
            else:
                file.write(f'  "{key}": {json_value}\n')
        file.write('}\n')

def getfromjson(target):
    with open(target, "r", encoding = "utf-8") as file:
        data = json.load(file)

    return data

def startHotkey():
    hotkey = hotkeys(getfromjson("master.json"))

def startWebview():
    class API:
        def close(self):
            webview.windows[0].destroy()

    window = webview.create_window("Izaki Keyboard", "index.html", width=630, height=310, frameless=True, on_top=True, js_api=API())
    threading.Thread(target = keyboardListen, args = (window,), daemon = True).start()
    webview.start() 

def keyboardListen(window):
    def on_key_event(event):
        if event.event_type == keyboard.KEY_DOWN:
            #print("keyIn:", event.name.lower())
            window.evaluate_js(f"window.keyIn('{event.name.lower()}');")

        elif event.event_type == keyboard.KEY_UP:
            #print("keyOut:", event.name.lower())
            window.evaluate_js(f"window.keyOut('{event.name.lower()}');")

    keyboard.hook(on_key_event)
                                        
main()