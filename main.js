document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    window.pywebview.api.close();
});

window.keyIn = function(key) {
    try {
        document.getElementById(key).setAttribute("fill", "#86A788");
    } catch (error) {}
};

window.keyOut = function(key) {
    try {
        document.getElementById(key).setAttribute("fill", "#3F72AF");
    } catch (error){}
};

window.updateMapping = function(keyMap){
    for (const key in keyMap) {
        try {
            document.getElementById(key).nextElementSibling.textContent = keyMap[key].slice(0, -1);
        } catch (error){}
    }
};

function flattenExtraneousKey(name) {
    const shiftMap = {
        '!': '1',
        '@': '2',
        '#': '3',
        '$': '4',
        '%': '5',
        '^': '6',
        '&': '7',
        '*': '8',
        '(': '9',
        ')': '0',
        "?": "/"
    };

  return shiftMap[name] || name;
}