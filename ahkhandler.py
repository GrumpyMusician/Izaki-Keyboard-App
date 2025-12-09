from ahk import AHK
import keyboard

class ahkhandler:
    def __init__(self, data, sendMode, sendMaps, keyIn, keyOut, setLoad):
        self.data = data
        self.sendMode = sendMode
        self.sendMaps = sendMaps
        self.keyIn = keyIn
        self.keyOut = keyOut
        self.setLoad = setLoad

        self.ahk = AHK()
        self.keyboard = keyboard
        self.refChar = "μ" # μ - System, λ - Latinized, δ - Askaoza, φ - Byakuzhi; Not all matter tho, some put in for fun ;)

        self.buffer = ""

        # Mode modifiers and whatnot
        self.mode = 0 # 0 = System Keyboard, 1 = Latinized, 2 = Askaoza, 3 = Byakuzhi
        
        self.keyboard.add_hotkey('left shift+right shift', self.incrementMode)
        self.keyboard.add_hotkey('backspace', self.keyboardBackspace)

        self.keyboard.on_press_key('backspace', lambda e: self.keyIn('backspace'))
        self.keyboard.on_release_key('backspace', lambda e: self.keyOut('backspace'))
        self.keyboard.on_press_key('caps lock', lambda e: self.keyIn('caps lock'))
        self.keyboard.on_release_key('caps lock', lambda e: self.keyOut('caps lock'))
        self.keyboard.on_press_key('enter', lambda e: self.keyIn('enter'))
        self.keyboard.on_release_key('enter', lambda e: self.keyOut('enter'))
        self.keyboard.on_press_key('left shift', lambda e: self.keyboardShift(True, True))
        self.keyboard.on_release_key('left shift', lambda e: self.keyboardShift(True, False))
        self.keyboard.on_press_key('right shift', lambda e: self.keyboardShift(False, True))
        self.keyboard.on_release_key('right shift', lambda e: self.keyboardShift(False, False))

        #print("start")

        self.setLoad(1)
        self.ahk.start_hotkeys()
        self.sendMode(0)
        self.setHotKeys()
        self.ahk.stop_hotkeys()
        self.setBopprehKeys()
        self.setLoad(0)

    def incrementMode(self):
        if self.mode == 3:
            self.mode = 0
        else:
            self.mode += 1
        if self.mode == 0:
            self.refChar = "μ"
            self.setBopprehKeys()
        elif self.mode == 1:
            self.clearBopprehKeys()
            self.ahk.start_hotkeys()
            self.refChar = "λ"
        elif self.mode == 2:
            self.refChar = "δ"
        elif self.mode == 3:
            self.setLoad(1)
            self.refChar = "φ"
            self.ahk.stop_hotkeys()
            self.setBopprehKeys()
            self.setLoad(0)

        self.setRefChar()
        #print(self.mode)

    def setRefChar(self):
        if not self.buffer:
            if self.mode == 0:
                self.refChar = "μ"
            elif self.mode == 3:
                self.refChar = "φ"
                
            else:
                if self.mode == 1:
                    self.refChar = "λ"
                elif self.mode == 2:
                    self.refChar = "δ"

                if self.ahk.key_state("LShift"):
                        self.keyboardShift(True, True)
                elif self.ahk.key_state("RShift"):
                    self.keyboardShift(False, True)
                else:
                    self.sendMaps(self.data[self.refChar])
        
        else:
            for key in self.data:
                if self.buffer.endswith(key):
                    self.refChar = key

                    if self.ahk.key_state("LShift"):
                        self.keyboardShift(True, True)
                    elif self.ahk.key_state("RShift"):
                        self.keyboardShift(False, True)
                    else:
                        self.sendMaps(self.data[self.refChar])
                    break

        self.sendMode(self.mode)

    def setBopprehKeys(self):
        for key in self.data["λ"]:
            if not key.strip():
                continue

            if key[0] != "+":
                self.keyboard.on_press_key(key, lambda e, k=key: self.keyIn(k))
                self.keyboard.on_release_key(key, lambda e, k=key: self.keyOut(k))

    def clearBopprehKeys(self): 
        for key in self.data["λ"]:
            if not key.strip():
                continue

            if key[0] != "+":
                self.keyboard.unhook_key(key)

    def setHotKeys(self):
        for key in self.data["λ"]:
            if not key.strip():
                continue

            if key == ";": #semicolon key being weird, so we have to modify it and it specifically:
                self.ahk.add_hotkey("`;", callback=lambda e=None, k=key: self.inject(k))
                self.ahk.add_hotkey("`; up", callback=lambda e=None, k=key: self.keyOut(k))
            else:
                self.ahk.add_hotkey(f"{key}", callback=lambda e=None, k=key: self.inject(k))
                self.ahk.add_hotkey(f"{key} up", callback=lambda e=None, k=key: self.keyOut(k))

    def inject(self, key):
        #print(key, "|", self.data[self.refChar][key], "|", self.buffer, "|", self.refChar)

        self.keyIn(key)        

        if self.mode == 1 or self.mode == 2:
            try:
                value = self.data[self.refChar][key]
            except:
                if self.mode == 1:
                    value = self.data["λ"][key]
                elif self.mode == 2:
                    value = self.data["δ"][key]
                

            self.keyboard.write('\b' * int(value[-1]))
            
            if int(value[-1]) != 0:
                self.buffer = self.buffer[:-int(value[-1])]

            self.keyboard.write(value[:-1])
            self.buffer += value[:-1]

            self.setRefChar()

    def keyboardBackspace(self):
        self.buffer = self.buffer[:-1]
        self.setRefChar()

    def keyboardShift(self, isLeftShift, isPressing):
        if self.mode == 0 or self.mode == 3:
            if isPressing:
                if isLeftShift:
                    self.keyIn('left shift')
                else:
                    self.keyIn('right shift')
            else:
                if isLeftShift:
                    self.keyOut('left shift')
                else:
                    self.keyOut('right shift')

            return

        if isPressing:
            if isLeftShift:
                self.keyIn('left shift')
            else:
                self.keyIn('right shift')

            d = self.data[self.refChar]
            keys = list(d.keys())
            new_map = {}

            for key in keys:
                if key.startswith("+"):
                    base = key[1:]
                    if base in d:
                        new_map["+" + base] = d[base]
                        new_map[base] = d[key]
                    else:
                        new_map[base] = d[key]
                elif "+" + key not in d:
                    new_map[key] = d[key]

            self.sendMaps(new_map)
        
        else:
            if isLeftShift:
                self.keyOut('left shift')
            else:
                self.keyOut('right shift')
            self.sendMaps(self.data[self.refChar])