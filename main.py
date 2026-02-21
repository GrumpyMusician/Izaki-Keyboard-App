import requests
import csv
import json
from collections import defaultdict
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
    ahkhandler.ahkhandler(getCharacters(), getByakuzhi(), getCompounds(), sendMode, sendMaps, keyIn, keyOut, setLoad, setIdle)
    
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
    window.evaluate_js(f'keyIn("{keyName}")')

def keyOut(keyName):
    global window
    window.evaluate_js(f'keyOut("{keyName}")')

def setLoad(hide):
    global window
    window.evaluate_js(f'setLoad("{hide}")')

def setIdle(hide):
    global window
    window.evaluate_js(f'setIdle("{hide}")')

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

        with open("characters.json", "w", encoding = "utf-8") as file:
            file.write("{\n")
            items = list(data.items())
            for i, (key, value) in enumerate(items):
                json_value = json.dumps(value, ensure_ascii = False)
                if i < len(items) - 1:
                    file.write(f'  "{key}": {json_value},\n')
                else:
                    file.write(f'  "{key}": {json_value}\n')
            file.write('}\n') 

        response = requests.get("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=620421474")
        response.raise_for_status()

        csv_text = response.content.decode("utf-8").splitlines()
        reader = csv.DictReader(csv_text)

        data = {}
        count = 0
        for row in reader:
            if count > 1:
                key = row[reader.fieldnames[6]].strip()
                value = row[reader.fieldnames[4]].strip()

                if key: #ignore empty stuff
                    data[key] = value

            count += 1

        with open("byakuzhi.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        # Fetch the CSV
        response = requests.get("https://docs.google.com/spreadsheets/d/16X5QlpYoW5aToM6LoJlEZ8K0XvmlasJArD0vYzFOZ3Y/export?format=csv&gid=0")
        response.raise_for_status()

        csv_text = response.content.decode("utf-8").splitlines()
        reader = csv.DictReader(csv_text)

        data = defaultdict(lambda: {"byakuzhi": [], "latin": []})

        header = reader.fieldnames
        byakuzhi_cols = header[3:7]
        latin_cols = header[8:12]

        for row in reader:
            key = row[header[2]].strip()
            if not key or key == "#NUM!":
                continue

            byakuzhi_row = [row[col].strip() for col in byakuzhi_cols if row[col].strip() and row[col].strip() != "#NUM!"]
            latin_row = [row[col].strip() for col in latin_cols if row[col].strip() and row[col].strip() != "#NUM!"]

            if byakuzhi_row or latin_row:
                data[key]["byakuzhi"].append(byakuzhi_row)
                data[key]["latin"].append(latin_row)

        with open("compounds.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError as e:
        notification.notify(title='Internet Connection Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.Timeout as e:
        notification.notify(title='Internet Timeout Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)
    except requests.exceptions.RequestException as e:
        notification.notify(title='Internet Request Exception Error', message="Uh-oh! This program can not extract the latest set of keymappings due to an internet issue. Don't worry! It'll still run since the last set of keymappings.", app_icon= "icon.ico", timeout=10)

def getCharacters():
    with open("characters.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)

    return data

def getByakuzhi():
    with open("byakuzhi.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)

    return data

def getCompounds():
    with open("compounds.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)

    return data
    
main()