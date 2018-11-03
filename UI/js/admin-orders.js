async function fetchAndDisplayOrders() {
    var request = createOrdersRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            // fetch and display response body
        } else if (response.status == 401) {
            window.location.href = "index.html";
        } else if (response.status == 404) {
            // display empty orders error
        } else {
            // unexpected error occurred, display message + status code
        }
    } catch (error) {
        alert(error);
    }
}

function createOrdersRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/orders",
        {method: "GET", headers: headers}
    );
    return request;
}