var form = document.querySelector("form");
form.addEventListener("submit", register);

async function register(event) {
    removeErrorMessages();
    ensurePasswordsEqual();
    var request = createRequestObject();
    displayWaitingSignal();
    try {
        var promise = fetch(request);
        var response = await promise;
        if (response.status == 201) {
            window.location.href = "index.html";
        } else {
            displayErrorMessage(response);
        }
    } catch (e) {
        console.log(e);
    }
}

function ensurePasswordsEqual() {
    var password1 = document.querySelector("input[name=password1]").value;
    var password2 = document.querySelector("input[name=password2]").value;
    if (password1 != password2) {
        var errorMessage = document.querySelector(".password-error");
        var passwordInputs = document.querySelectorAll("input[type=password]");
        errorMessage.innerHTML = "Passwords don't match!";
        for (var c = 0; c < passwordInputs.length; c++) {
            passwordInputs[c].style.border = "1px solid red";
        }
        throw "Passwords not matching"; // prevent registration from proceeding
    }
}

function createRequestObject() {
    var username = document.querySelector("input[name=username]").value;
    var email = document.querySelector("input[name=email-address]").value;
    var tel = document.querySelector("input[name=telephone]").value;
    var password = document.querySelector("input[name=password2]").value;
    var requestBody = {
        username: username, email: email,
        telephone: tel, password: password
    }
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/auth/signup",
        {method: "POST", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

async function displayErrorMessage(response) {
    var responseBody = await response.json();
    if (responseBody["error"].indexOf("exists!") !== -1) {
        var errorOutput = document.querySelector(".username-error");
        errorOutput.innerHTML = responseBody["error"];
    } else {
        var errorOutput = document.querySelector(".password-error");
        errorOutput.innerHTML = responseBody["error"];
    }
    removeWaitingSignal();
}

function displayWaitingSignal() {
    var submitButton = document.querySelector("input[type=submit]");
    submitButton.value = "Registering...";
    submitButton.disabled = true;
}

function removeWaitingSignal() {
    var submitButton = document.querySelector("input[type=submit]");
    submitButton.value = "Sign Up";
    submitButton.disabled = false;
}

function removeErrorMessages() {
    var nameError = document.querySelector(".username-error");
    var passwordError = document.querySelector(".password-error");
    nameError.innerHTML = "";
    passwordError.innerHTML = "";
}
