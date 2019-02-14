function coolSearchOn() {
    $("#cool-search").mousedown(function () {
        $(".cool-search").slideToggle("0.5s");
    });
}

function openMenu(){
    $(".open-personal-menu").mousedown(function () {
        $(".personal-menu-my").slideToggle("0.5s");
    })
}
openMenu();
coolSearchOn();
