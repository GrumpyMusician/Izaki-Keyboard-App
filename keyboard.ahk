#Requires AutoHotkey v2.0
#SingleInstance Force

; --- Load JSON as plain text ---
latinizedFile := A_ScriptDir "\latinized.json"
jsonText := FileRead(latinizedFile, "UTF-8")

; --- Parse "key": "value" pairs into a Map ---
latinized := Map()
matches := []
pos := 1
while (pos := RegExMatch(jsonText, '"(.*?)":\s*"(.*?)"', &m, pos)) {
    if (m[2] != "nan")
        latinized[m[1]] := m[2]
    pos += StrLen(m[0])
}

; --- Buffer for multi-character combos ---
inputBuffer := ""

; --- Register hotkeys for every single key in the mapping ---
for key, value in latinized {
    try Hotkey(key, KeyHandler.Bind(key), "On")
}

; --- Key handler ---
KeyHandler(key, hotkeyName) {
    global inputBuffer, latinized

    inputBuffer .= key

    ; If combo (like "aa") exists → send it
    if (latinized.Has(inputBuffer)) {
        SendText(latinized[inputBuffer])
        inputBuffer := ""
        return
    }

    ; Otherwise, check just this single key
    if (latinized.Has(key)) {
        SendText(latinized[key])
        inputBuffer := ""
    }
}
