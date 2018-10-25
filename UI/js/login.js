var userButton = document.querySelector("input[value=Login]");
var adminButton = document.querySelector("input[value='Login as Admin']");
userButton.addEventListener("click", function(event) {login();});
adminButton.addEventListener("click", function(event) {login(admin=true);});

async function login(admin=false) {
    removeErrorMessages();
    var request = createRequestObject();
    try {
        var response = await fetch(request);
        var responseBody = await response.json();
        if (response.status == 200) {
            sessionStorage.setItem("token", responseBody.token);
            if (admin) {
                window.location.href = "admin-menu.html";
            } else {
                window.location.href = "food-order.html";
            }
        } else {
            displayErrorMessage(responseBody);
        }
    } catch (error) {
        alert(error);
    }
}

function createRequestObject() {
    var username = document.querySelector("input[name=username]").value;
    var password = document.querySelector("input[name=password]").value;
    var requestBody = {username: username, password: password}
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/auth/login",
        {method: "POST", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

function displayErrorMessage(responseBody) {
    var errorMessage = responseBody.error;
    var errorOutputElement;
    if (errorMessage.indexOf("password") != -1) {
        errorOutputElement = document.querySelector(".password-error");
    } else {
        errorOutputElement = document.querySelector(".username-error");
    }
    errorOutputElement.innerHTML = errorMessage;
}

function removeErrorMessages() {
    var nameErrorElement = document.querySelector(".username-error");
    var passwordErrorElement = document.querySelector(".password-error");
    nameErrorElement.innerHTML = "";
    passwordErrorElement.innerHTML = "";
}
