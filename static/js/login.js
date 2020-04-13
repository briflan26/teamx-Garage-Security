const error_1 = `<div class="notification is-danger is-light" id="tx_n_error_1">
<button class="delete" onclick="closenote('tx_n_error_1')" id="tx_b_closenote"></button>
Something went wrong. Please try again and contact us if you continue to have trouble.
</div>`;

function login() {
    console.log("LOGIN");
    // constants
    // const url = "http://teamx.ddns.net/login";
    const host = "http://localhost:8000"
    const url = host + "/login"
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
                window.location.assign(host + "/home")
            } else {
                var parent = document.getElementById("tx_n_placeholder");
                var note = document.createElement("div");
                note.innerHTML = error_1;
                parent.appendChild(note);

                // update elements
                email.value = null;
                pwd.value = null;
                email.disabled = false;
                pwd.disabled = false;
                button.disabled = false;
                button.classList.remove("is-loading");
            }
        }
    }
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