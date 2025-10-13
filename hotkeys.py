from ahk import AHK
import keyboard
import mouse

class hotkeys:
    def __init__(self, dictionary):
        self.ahk = AHK()
        self.keyboard = keyboard
        self.mouse = mouse

        self.refs = dictionary
        self.buffer = ""
        self.refchar = ""
        self.setrefchar()
        self.keys = list(dictionary.keys())

        self.initAHK() 

    def getCurrentMap(self):
        return self.refs[self.refchar]

    def setrefchar(self):
        if self.buffer == "":
            self.refchar = "δ"
        else:
            self.refchar = "δ"
            for key in self.keys:
                if self.buffer.endswith(key):
                    self.refchar = key
                    break

        print(self.refchar)

    def keyboardtype(self, character, infLoopRisk = False):

        for i in range(int(character[-1])):
            self.ahk.key_press('backspace')
            self.buffer = self.buffer[:-1]

        if infLoopRisk:
            self.keyboard.write(character[:-1])
            self.buffer += character[:-1]

        else: 
            self.ahk.send_input(character[:-1])
            self.buffer += character[:-1]

        self.setrefchar()

    def initAHK(self):
        self.setrefchar()

        self.ahk.add_hotkey('+4', callback = self.ahkDollar)

        self.ahk.add_hotkey('q', callback = self.ahkq)
        self.ahk.add_hotkey('+q', callback = self.ahkQ)

        self.ahk.add_hotkey('w', callback = self.ahkw)
        self.ahk.add_hotkey('+w', callback = self.ahkpW)

        self.ahk.add_hotkey('e', callback = self.ahke)
        self.ahk.add_hotkey('+e', callback = self.ahkE)

        self.ahk.add_hotkey('r', callback = self.ahkr)
        self.ahk.add_hotkey('+r', callback = self.ahkR)

        self.ahk.add_hotkey('t', callback = self.ahkt)
        self.ahk.add_hotkey('+t', callback = self.ahkT)

        self.ahk.add_hotkey('y', callback = self.ahky)
        self.ahk.add_hotkey('+y', callback = self.ahkY)

        self.ahk.add_hotkey('u', callback = self.ahku)
        self.ahk.add_hotkey('+u', callback = self.ahkU)

        self.ahk.add_hotkey('i', callback = self.ahki)
        self.ahk.add_hotkey('+i', callback = self.ahkI)

        self.ahk.add_hotkey('o', callback = self.ahko)
        self.ahk.add_hotkey('+o', callback = self.ahkO)

        self.ahk.add_hotkey('p', callback = self.ahkp)
        self.ahk.add_hotkey('+p', callback = self.ahkP)

        self.ahk.add_hotkey('a', callback = self.ahka)
        self.ahk.add_hotkey('+a', callback = self.ahkA)

        self.ahk.add_hotkey('s', callback = self.ahks)
        self.ahk.add_hotkey('+s', callback = self.ahkS)

        self.ahk.add_hotkey('d', callback = self.ahkd)
        self.ahk.add_hotkey('+d', callback = self.ahkD)

        self.ahk.add_hotkey('f', callback = self.ahkf)
        self.ahk.add_hotkey('+f', callback = self.ahkF)

        self.ahk.add_hotkey('g', callback = self.ahkg)
        self.ahk.add_hotkey('+g', callback = self.ahkG)

        self.ahk.add_hotkey('h', callback = self.ahkh)
        self.ahk.add_hotkey('+h', callback = self.ahkH)

        self.ahk.add_hotkey('j', callback = self.ahkj)
        self.ahk.add_hotkey('+j', callback = self.ahkJ)

        self.ahk.add_hotkey('k', callback = self.ahkk)
        self.ahk.add_hotkey('+k', callback = self.ahkK)

        self.ahk.add_hotkey('l', callback = self.ahkl)
        self.ahk.add_hotkey('+l', callback = self.ahkL)

        self.ahk.add_hotkey('z', callback = self.ahkz)
        self.ahk.add_hotkey('+z', callback = self.ahkZ)

        self.ahk.add_hotkey('x', callback = self.ahkx)
        self.ahk.add_hotkey('+x', callback = self.ahkX)

        self.ahk.add_hotkey('c', callback = self.ahkc)
        self.ahk.add_hotkey('+c', callback = self.ahkC)

        self.ahk.add_hotkey('v', callback = self.ahkv)
        self.ahk.add_hotkey('+v', callback = self.ahkV)

        self.ahk.add_hotkey('b', callback = self.ahkb)
        self.ahk.add_hotkey('+b', callback = self.ahkB)

        self.ahk.add_hotkey('n', callback = self.ahkn)
        self.ahk.add_hotkey('+n', callback = self.ahkN)

        self.ahk.add_hotkey('m', callback = self.ahkm)
        self.ahk.add_hotkey('+m', callback = self.ahkM)

        self.ahk.add_hotkey(',', callback = self.ahkComma)
        self.ahk.add_hotkey('.', callback = self.ahkPeriod)
        self.ahk.add_hotkey('!', callback = self.ahkExclamation)
        self.ahk.add_hotkey('?', callback = self.ahkQuestion)

        self.ahk.add_hotkey('space', callback = self.keyboardSpace)

        self.keyboard.add_hotkey('backspace', self.keyboardBackspace)
        
        self.mouse.on_click(self.mouseMouse)

        self.ahk.start_hotkeys()
        self.ahk.block_forever()

    def ahkDollar(self):
        self.keyboardtype(self.refs[self.refchar]["$"])

    def ahkq(self):
        self.keyboardtype(self.refs[self.refchar]["q"])

    def ahkQ(self):
        self.keyboardtype(self.refs[self.refchar]["Q"])

    def ahkw(self):
        self.keyboardtype(self.refs[self.refchar]["w"])

    def ahkpW(self):
        self.keyboardtype(self.refs[self.refchar]["W"])

    def ahke(self):
        self.keyboardtype(self.refs[self.refchar]["e"])

    def ahkE(self):
        self.keyboardtype(self.refs[self.refchar]["E"])

    def ahkr(self):
        self.keyboardtype(self.refs[self.refchar]["r"])

    def ahkR(self):
        self.keyboardtype(self.refs[self.refchar]["R"])

    def ahkt(self):
        self.keyboardtype(self.refs[self.refchar]["t"])

    def ahkT(self):
        self.keyboardtype(self.refs[self.refchar]["T"])

    def ahky(self):
        self.keyboardtype(self.refs[self.refchar]["y"])

    def ahkY(self):
        self.keyboardtype(self.refs[self.refchar]["Y"])

    def ahku(self):
        self.keyboardtype(self.refs[self.refchar]["u"])

    def ahkU(self):
        self.keyboardtype(self.refs[self.refchar]["U"])

    def ahki(self):
        self.keyboardtype(self.refs[self.refchar]["i"])

    def ahkI(self):
        self.keyboardtype(self.refs[self.refchar]["I"])

    def ahko(self):
        self.keyboardtype(self.refs[self.refchar]["o"])

    def ahkO(self):
        self.keyboardtype(self.refs[self.refchar]["O"])

    def ahkp(self):
        self.keyboardtype(self.refs[self.refchar]["p"])

    def ahkP(self):
        self.keyboardtype(self.refs[self.refchar]["P"])

    def ahka(self):
        self.keyboardtype(self.refs[self.refchar]["a"])

    def ahkA(self):
        self.keyboardtype(self.refs[self.refchar]["A"])

    def ahks(self):
        self.keyboardtype(self.refs[self.refchar]["s"])

    def ahkS(self):
        self.keyboardtype(self.refs[self.refchar]["S"])

    def ahkd(self):
        self.keyboardtype(self.refs[self.refchar]["d"])

    def ahkD(self):
        self.keyboardtype(self.refs[self.refchar]["D"])

    def ahkf(self):
        self.keyboardtype(self.refs[self.refchar]["f"])

    def ahkF(self):
        self.keyboardtype(self.refs[self.refchar]["F"])

    def ahkg(self):
        self.keyboardtype(self.refs[self.refchar]["g"])

    def ahkG(self):
        self.keyboardtype(self.refs[self.refchar]["G"])

    def ahkh(self):
        self.keyboardtype(self.refs[self.refchar]["h"])

    def ahkH(self):
        self.keyboardtype(self.refs[self.refchar]["H"])

    def ahkj(self):
        self.keyboardtype(self.refs[self.refchar]["j"])

    def ahkJ(self):
        self.keyboardtype(self.refs[self.refchar]["J"])

    def ahkk(self):
        self.keyboardtype(self.refs[self.refchar]["k"])

    def ahkK(self):
        self.keyboardtype(self.refs[self.refchar]["K"])

    def ahkl(self):
        self.keyboardtype(self.refs[self.refchar]["l"])

    def ahkL(self):
        self.keyboardtype(self.refs[self.refchar]["L"])

    def ahkz(self):
        self.keyboardtype(self.refs[self.refchar]["z"])

    def ahkZ(self):
        self.keyboardtype(self.refs[self.refchar]["Z"])

    def ahkx(self):
        self.keyboardtype(self.refs[self.refchar]["x"])

    def ahkX(self):
        self.keyboardtype(self.refs[self.refchar]["X"])

    def ahkc(self):
        self.keyboardtype(self.refs[self.refchar]["c"])

    def ahkC(self):
        self.keyboardtype(self.refs[self.refchar]["C"])

    def ahkv(self):
        self.keyboardtype(self.refs[self.refchar]["v"])

    def ahkV(self):
        self.keyboardtype(self.refs[self.refchar]["V"])

    def ahkb(self):
        self.keyboardtype(self.refs[self.refchar]["b"])

    def ahkB(self):
        self.keyboardtype(self.refs[self.refchar]["B"])

    def ahkn(self):
        self.keyboardtype(self.refs[self.refchar]["n"])

    def ahkN(self):
        self.keyboardtype(self.refs[self.refchar]["N"])

    def ahkm(self):
        self.keyboardtype(self.refs[self.refchar]["m"])

    def ahkM(self):
        self.keyboardtype(self.refs[self.refchar]["M"])

    def ahkComma(self):
        self.keyboardtype(self.refs[self.refchar][","])

    def ahkPeriod(self):
        self.keyboardtype(self.refs[self.refchar]["."])

    def ahkExclamation(self):
        self.keyboardtype(self.refs[self.refchar]["!"], infLoopRisk = True)

    def ahkQuestion(self):
        self.keyboardtype(self.refs[self.refchar]["?"])

    def keyboardSpace(self):
        self.keyboardtype(self.refs[self.refchar][" "], infLoopRisk = True)

    def keyboardBackspace(self):
        self.buffer = self.buffer[:-1]
        self.setrefchar()

    def mouseMouse(self):
        self.buffer = ""
        self.setrefchar()

