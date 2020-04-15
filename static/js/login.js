
const error_1 = `<div class="notification is-danger is-light" id="tx_n_error_1">
<button class="delete" onclick="closenote('tx_n_error_1')" id="tx_b_closenote"></button>
Something went wrong. Please try again and contact us if you continue to have trouble.
</div>`;
const error_2 = `<div class="notification is-danger is-light" id="tx_n_error_1">
<button class="delete" onclick="closenote('tx_n_error_1')" id="tx_b_closenote"></button>
Incorrect email or password. Please try again.
</div>`;

function login() {
    console.log("LOGIN");
    // constants
    const url = 'http://' + hostname + ':' + port.toString() + "/login"
    console.log(url);
    const request = new XMLHttpRequest();
    // get elements
    var email = document.getElementById("tx_i_email");
    var pwd = document.getElementById("tx_i_password");
    var button = document.getElementById("tx_b_login");

    // update elements
    email.disabled = true;
    pwd.disabled = true;
    button.disabled = true;
    button.classList.add("is-loading");

    // collect data
    var data = {
        "email": email.value,
        "password": pwd.value
    };
    console.log(data);

    // send login request
    request.open("POST", url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(data));
    request.onreadystatechange = (e) => {
        if (request.readyState == 4) {
            if (request.status == 200) {
                console.log(request.responseText);
                resp_data = JSON.parse(request.response);
                if (resp_data['status'] == 0) {
                    console.log(resp_data['session']);
                    window.location.assign('http://' + hostname + ':' + port.toString() + "/home" + "?email=" + email.value + "&session=" + resp_data['session'])
                } else {
                    displaynote(error_2);
                    reset_login_fields();
                }
            } else {
                displaynote(error_1);
                reset_login_fields();
            }
        }
    }
}

function displaynote(noteText) {
    var parent = document.getElementById("tx_n_placeholder");
    var note = document.createElement("div");
    note.innerHTML = noteText;
    parent.appendChild(note);
}

function reset_login_fields() {
    var email = document.getElementById("tx_i_email");
    var pwd = document.getElementById("tx_i_password");
    var button = document.getElementById("tx_b_login");

    // update elements
    email.value = null;
    pwd.value = null;
    email.disabled = false;
    pwd.disabled = false;
    button.disabled = false;
    button.classList.remove("is-loading");
}

function closenote(id) {
    document.getElementById(id).remove();
}

function resetpwd() {
    console.log("RESETPWD");
}

function contactus() {
    console.log("CONTACTUS");
}