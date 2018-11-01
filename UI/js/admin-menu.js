fetchAndDisplayAdminMenu();

async function fetchAndDisplayAdminMenu() {
    var request = createRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 404) {
            // display error message
        } else {
            // fetch and display response body
        }
    } catch (error) {
        alert(error);
    }
}

function createRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/menu",
        {method: "GET", headers: headers}
    );
    return request;
}
