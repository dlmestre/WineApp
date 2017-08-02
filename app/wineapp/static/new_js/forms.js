function insertForm(pos) {
    console.log(pos);
    divname = "#formdiv" + pos;
    hideIds();
    $(divname).show();
}

function hideId(pos) {
    divname = "#formdiv" + pos;
    $(divname).hide();
}

function hideIds() {
    console.log("hiding ids");
    var ids = $('[id^="formdiv"]');
    ids.hide();
}

function hideIdsCSS() {
    var ids = $('[id^="formdiv"]');
    ids.css("display","none")
}

$(function() {
    hideIds();
});
