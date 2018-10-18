var form = document.querySelector("form");
form.addEventListener("submit", register);

async function register(event) {
    var inputs = document.getElementsByTagName("input");
    var requestBody = {};
    for (var c = 0; c < inputs.length; c++) {
        if (inputs[c].name == "username" || inputs[c].name == "password") {
            requestBody[inputs[c].name] = inputs[c].value;
        }
    }
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/auth/signup",
        {method: "POST", cache: "reload", body: JSON.stringify(requestBody)}
    );
    try {
        var promise = fetch(request);
        var response = await promise;
        if (response.status == 201) {
            alert("You were successfully registered!!");
        } else {
            alert("You were not registered!!");
        }
    }
    catch(e) {
        console.log(e);
        alert(e);
    }
}
