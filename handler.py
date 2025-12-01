from ahk import AHK
import keyboard
from functools import partial

class handler:
    def __init__(self, data):
        self.ahk = AHK()
        self.keyboard = keyboard
        self.data = data
        self.refChar = "μ" # μ - System, λ - Latinized, δ - Askaoza, φ - Byakuzhi; Not all matter tho, some put in for fun ;)

        self.buffer = ""

        # Mode modifiers and whatnot
        self.mode = 0 # 0 = System Keyboard, 1 = Latinized, 2 = Askaoza, 3 = Byakuzhi
        
        self.keyboard.add_hotkey('left shift+right shift', self.incrementMode)

        self.keyboard.add_hotkey('backspace', self.keyboardBackspace)

        print("start")

        self.ahk.start_hotkeys()
        self.ahk.block_forever()
        

    def incrementMode(self):
        if self.mode == 3:
            self.mode = 0
        else:
            self.mode += 1

        self.setRefChar()
        if self.mode == 1 or self.mode == 2:
            self.ahk.clear_hotkeys()
            self.setHotKeys()

        print(self.mode)

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
        
        else:
            for key in self.data:
                if self.buffer.endswith(key):
                    self.refChar = key
                    break

    def setHotKeys(self):
        for key in self.data["λ"]:
            if not key.strip():
                continue
            self.ahk.add_hotkey(key, callback=partial(self.inject, key))

    def inject(self, key):
        #print(key, "|", self.data[self.refChar][key], "|", self.buffer, "|", self.refChar)

        value = self.data[self.refChar][key]

        self.keyboard.write('\b' * int(value[-1]))
        
        if int(value[-1]) != 0:
            self.buffer = self.buffer[:-int(value[-1])]

        self.keyboard.write(value[:-1])
        self.buffer += value[:-1]

        self.setRefChar()
        

    def keyboardBackspace(self):
        self.buffer = self.buffer[:-1]
        self.setRefChar()