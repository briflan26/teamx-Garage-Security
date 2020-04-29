var counter = 0;
var lastime = 0;

function closenote(id) {
    document.getElementById(id).remove();
}

function displayalert(ctr, ts, msg) {
    var camalert = `<div class="columns" id='notification_${ctr}'><div class="column is-narrow"><div class="notification">
    <button class="delete" onclick="closenote('notification_${ctr}')"></button><div class="columns"><div class="column is-narrow">${ts}</div>
    <div class="column is-narrow">${msg}</div></div></div></div></div>`;
    var parent = document.getElementById("tx_cam_alerts");
    var note = document.createElement("div");
    note.innerHTML = camalert;
    parent.appendChild(note);
}

function refresh() {
    console.log("REFRESH");
    // constants
    const ref_url = 'http://' + hostname + ':' + port.toString() + "/security/camera/refresh" + "?email=" +
        window.sessionStorage.getItem('email') + "&session=" + window.sessionStorage.getItem('key') + "&epoch=" +
        lastime.toString();
    console.log(ref_url);
    const request = new XMLHttpRequest();

    // get elements
    var button = document.getElementById("tx_b_refresh");
    var parent = document.getElementById("tx_cam_alerts");
    parent.innerHTML = '';

    // update elements
    button.classList.add("is-loading");

    // send login request
    request.open("GET", ref_url);
    request.send();
    request.onreadystatechange = (e) => {
        if (request.readyState == 4) {
            if (request.status == 200) {
                console.log(request.responseText);
                resp_data = JSON.parse(request.response);
                if (resp_data['status'] == 0) {
                    for (var k in resp_data['alerts']) {
                        displayalert(counter, resp_data['alerts'][k]['time'], resp_data['alerts'][k]['message']);
                        counter++;
                        if (Number(k) > lastime) lastime = Number(k);
                    }
                } else {
                    parent.innerHTML = "<h3 class='title is-5'>No new alerts</h3>"
                }
                button.classList.remove("is-loading");
            }
        }
    }
}

function gopen() {
    const ref_url = 'http://' + hostname + ':' + port.toString() + "/garage/status/change";
    const request = new XMLHttpRequest();
    var status = document.getElementById("tx_garage_status");
    var schange = document.getElementById("tx_b_change_status");

    schange.classList.add("is-loading");

    request.open("POST", ref_url);
    request.send(JSON.stringify({ "status": 0, "email": window.sessionStorage.getItem("email"), "session": window.sessionStorage.getItem("key") }));
    request.onreadystatechange = (e) => {
        if (request.readyState == 4) {
            if (request.status == 200) {
                console.log(request.responseText);
                status.innerHTML = "Opened";
                schange.onclick = function () { gclose(); };
                schange.innerHTML = "Close Your Garage";
                schange.classList.remove("is-loading");
            } else {
                alert("Unable to open your garage. Please contact your system administrator");
            }
        }
    }
}

function gclose() {
    console.log("Closing garage..")
    const ref_url = 'http://' + hostname + ':' + port.toString() + "/garage/status/change";
    const request = new XMLHttpRequest();
    var status = document.getElementById("tx_garage_status");
    var schange = document.getElementById("tx_b_change_status");

    schange.classList.add("is-loading");

    request.open("POST", ref_url);
    request.send(JSON.stringify({ "status": 1, "email": window.sessionStorage.getItem("email"), "session": window.sessionStorage.getItem("key") }));
    request.onreadystatechange = (e) => {
        if (request.readyState == 4) {
            if (request.status == 200) {
                console.log(request.responseText);
                status.innerHTML = "Closed";
                schange.onclick = function () { gopen(); };
                schange.innerHTML = "Open Your Garage";
                schange.classList.remove("is-loading");
            } else {
                schange.classList.remove("is-loading");
                alert("Unable to close your garage. Please contact your system administrator");
            }
        }
    }
}

function modalClose(id) {
    el = document.getElementById(id);
    el.classList.remove("is-active");
}

function modalOpen(id){
    el = document.getElementById(id);
    el.classList.add("is-active");
}