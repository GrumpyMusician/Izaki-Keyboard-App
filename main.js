document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    window.pywebview.api.close();
});

window.keyIn = function(key) {
    document.getElementById(key).setAttribute("fill", "#86A788");
};

window.keyOut = function(key) {
    document.getElementById(key).setAttribute("fill", "#3F72AF");
};