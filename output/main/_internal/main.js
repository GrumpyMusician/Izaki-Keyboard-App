document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    window.pywebview.api.close();
});

function hideSpecial(hide){
    if (hide){
        document.querySelectorAll('.specialchars').forEach(element => {
            element.style.opacity = '0';  
        });
    } else {
        document.querySelectorAll('.specialchars').forEach(element => {
            element.style.opacity = '1';  
        });
    }
}

window.setLoad = function(hide){
    if (hide == 0){
        document.getElementById("loadingScreen").style.display = 'none'; 
    } else if (hide == 1) {
        document.getElementById("loadingScreen").style.display = 'flex'; 
    }
}

window.setIdle = function(hide){
    if (hide == 0){
        document.getElementById("idleScreen").style.display = 'none'; 
    } else if (hide == 1) {
        document.getElementById("idleScreen").style.display = 'flex'; 
    }
}

window.setMode = function(modeNum){
    if (modeNum === 0){
        hideSpecial(true)
        document.getElementById("systat").setAttribute("fill", "#86A788");
        document.getElementById("baistat").setAttribute("fill", "#3F72AF");
    } else if (modeNum === 1){
        hideSpecial(false)
        document.getElementById("latinstat").setAttribute("fill", "#86A788");
        document.getElementById("systat").setAttribute("fill", "#3F72AF");
    } else if (modeNum === 2){
        document.getElementById("askaozastat").setAttribute("fill", "#86A788");
        document.getElementById("latinstat").setAttribute("fill", "#3F72AF");
    } else if (modeNum === 3){
        hideSpecial(true)
        document.getElementById("baistat").setAttribute("fill", "#86A788");
        document.getElementById("askaozastat").setAttribute("fill", "#3F72AF");
    }
}

window.keyIn = function(key) {
    try {
        document.getElementById(removeLeadingPlus(key)).setAttribute("fill", "#86A788");
    } catch (error) {}
};

window.keyOut = function(key) {
    try {
        document.getElementById(removeLeadingPlus(key)).setAttribute("fill", "#3F72AF");
    } catch (error){}
};

window.updateMapping = function(keyMap){
    for (const key in keyMap) {
        try {
            if (key != "tab"){
                document.getElementById(key).nextElementSibling.textContent = keyMap[key].slice(0, -1);
            }
        } catch (error){}
    }
};

function removeLeadingPlus(key) {
    if (key.startsWith("+")) {
        return key.slice(1);
    }
    return key;
}