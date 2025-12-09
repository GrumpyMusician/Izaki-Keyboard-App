import requests
import csv
import json
from plyer import notification
import ahkhandler
import threading
import webview

window = None

def main():
    updateJSON()

    ahkthread = threading.Thread(target = runhandler, daemon = True)

    ahkthread.start()

    runwebview()

def runhandler():
    ahkhandler.ahkhandler(getJSON(), sendMode, sendMaps, keyIn, keyOut)
    
def runwebview():
    global window
    class API:
        def close(self):
            webview.windows[0].destroy()

    window = webview.create_window("Izaki Keyboard", "index.html", width=630, height=320, frameless=True, on_top=True, js_api = API())
    webview.start() 

def sendMode(modeNum):
    global window
    window.evaluate_js(f'setMode({modeNum})')

def sendMaps(mapList):
    global window
    window.evaluate_js(f'updateMapping({mapList})')

def keyIn(keyName):
    global window
    print("in", keyName)
    window.evaluate_js(f'keyIn("{keyName}")')

def keyOut(keyName):
    global window
    print("out", keyName)
    window.evaluate_js(f'keyOut("{keyName}")')

def updateJSON():
    try:
        response = requests.get("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=457897588")
        response.raise_for_status()

        csv_text = response.content.decode('utf-8').splitlines()

        reader = csv.DictReader(csv_text)

        data = {}

        for row in reader:
            key = row[reader.fieldnames[0]]
            nested = {k: v for k, v in row.items() if k != reader.fieldnames[0]}
            data[key] = nested

        with open("master.json", "w", encoding = "utf-8") as file:
            file.write("{\n")
            items = list(data.items())
            for i, (key, value) in enumerate(items):
                json_value = json.dumps(value, ensure_ascii = False)
                if i < len(items) - 1:
                    file.write(f'  "{key}": {json_value},\n')
                else:
                    file.write(f'  "{key}": {json_value}\n')
            file.write('}\n') 

    except requests.exceptions.ConnectionError as e:
        notification.notify(title='Internet Connection Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.Timeout as e:
        notification.notify(title='Internet Timeout Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.RequestException as e:
        notification.notify(title='Internet Request Exception Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)

def getJSON():
    with open("master.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)

    return data
    
main()