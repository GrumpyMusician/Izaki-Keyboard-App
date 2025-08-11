document.addEventListener('contextmenu', function (e) {
    e.preventDefault(); // Optional: prevent default right-click menu
    window.pywebview.api.close_app();
});

askbai = false
window.mode = function(mode) { //0 = System, 1 = Latinized, 2 = Askaoza, 3 = Bai
    if (mode === 0){
        askbai = false;
        document.getElementById("systemstat").setAttribute("fill", "#86A788");
        document.getElementById("latinstat").setAttribute("fill", "#3F72AF");
        document.getElementById("askaozastat").setAttribute("fill", "#3F72AF");
        document.getElementById("baistat").setAttribute("fill", "#3F72AF");
    }
    else if (mode === 1){
        document.getElementById("systemstat").setAttribute("fill", "#3F72AF");
        document.getElementById("latinstat").setAttribute("fill", "#86A788");
        document.getElementById("askaozastat").setAttribute("fill", "#3F72AF");
        document.getElementById("baistat").setAttribute("fill", "#3F72AF");
    }
    else if (mode === 2){
        askbai = true;
        document.getElementById("systemstat").setAttribute("fill", "#3F72AF");
        document.getElementById("latinstat").setAttribute("fill", "#3F72AF");
        document.getElementById("askaozastat").setAttribute("fill", "#86A788");
        document.getElementById("baistat").setAttribute("fill", "#3F72AF");
    }
    else if (mode === 3){
        askbai = true;
        document.getElementById("systemstat").setAttribute("fill", "#3F72AF");
        document.getElementById("latinstat").setAttribute("fill", "#3F72AF");
        document.getElementById("askaozastat").setAttribute("fill", "#3F72AF");
        document.getElementById("baistat").setAttribute("fill", "#86A788");
    }
};

window.shift = function(status){
    if (status){
        document.getElementById("shiftstat").setAttribute("fill", "#86A788")
    } else {
        document.getElementById("shiftstat").setAttribute("fill", "#3F72AF")
    }
}

window.caps = function(status){
    if (status){
        document.getElementById("capsstat").setAttribute("fill", "#86A788")
    } else {
        document.getElementById("capsstat").setAttribute("fill", "#3F72AF")
    }
}

window.keyboard = function(keys){
    // Highlight keys whose id is in keys, else reset
    const rects = document.querySelectorAll('rect[id]');
    rects.forEach(rect => {
        const id = rect.id;
        // Only process numeric ids (keyboard keys)
        if (!isNaN(Number(id))) {
            if (keys.includes(Number(id))) {
                rect.setAttribute("fill", "#86A788");
            } else {
                rect.setAttribute("fill", "#3F72AF");
            }
        }
    });
}

window.system = function(status){
    if (status){
        document.getElementById("svg").setAttribute("style", "margin: -7.5zpx; opacity: 0.2;")
    }
    else {
        document.getElementById("svg").setAttribute("style", "margin: -7.5zpx;")
    }

}

window.text = function(key, value){
    for (let i = 0; i < key.length; i++){
        if (key[i] === "15"){
            document.getElementById("15").nextElementSibling.textContent = "TAB";
        } else {
            document.getElementById(key[i]).nextElementSibling.textContent = value[i];
        }
    }
}

const inputField = document.getElementById('liveInput');
document.getElementById("systemstat").setAttribute("fill", "#86A788");