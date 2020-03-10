function aboutLoaded() {
    set_zcu_logo();
    set_state_logo("ok_icon_frame","ok");
    set_state_logo("value_error_icon_frame","value_error");
    set_state_logo("error_icon_frame","error");
}

function startTime() {
    var d = new Date();
    var h = d.getHours();
    var m = d.getMinutes();
    var s = d.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    var weekday = new Array(7);
        weekday[0] = "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";
    document.getElementsByTagName("set_actual_time")[0].innerHTML = h + ":" + m + ":" + s;
    document.getElementsByTagName("set_actual_date")[0].innerHTML = weekday[d.getDay()] +" \u00A0 " +  d.toLocaleDateString();
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

function set_zcu_logo() {
    var img = document.createElement("IMG");
    img.setAttribute("src", "../frontend/img/fav_en.png");
    img.setAttribute("width", "400");
    document.getElementsByTagName("zcu_logo")[0].appendChild(img);
}

function set_state_logo(frame,state) {
    switch (state) {
        case "ok":
            document.getElementsByTagName(frame)[0].innerHTML = "<img src='../frontend/img/state/ok.png' width='25'/>";
            break;
        case "value_error":
            document.getElementsByTagName(frame)[0].innerHTML = "<img src='../frontend/img/state/value_error.png' width='25'/>";
            break;
        case "error":
            document.getElementsByTagName(frame)[0].innerHTML = "<img src='../frontend/img/state/error.png' width='25'/>";
            break;
    }
}

function formatValue(value) {
    if (value == 1) {
        return "open";
    }
    else if (value == 0) {
        return "close";
    }
}

function load_json_file() {
    var request = new XMLHttpRequest();
    request.open("GET", "../backend/webpage_data.json", false);
    request.send(null);
    return JSON.parse(request.responseText);
}   