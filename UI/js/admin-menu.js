fetchAndDisplayAdminMenu();

async function fetchAndDisplayAdminMenu() {
    var request = createRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 404) {
            displayEmptyMenuMessage();
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

function displayEmptyMenuMessage() {
    var messageElement = document.createElement("h2");
    messageElement.setAttribute("class", "title");
    messageElement.textContent = "The food menu is empty!";
    var table = document.querySelector(".menu-list");
    var menu = document.querySelector(".admin-menu");
    menu.replaceChild(messageElement, table);
}
