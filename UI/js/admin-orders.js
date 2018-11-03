async function fetchAndDisplayOrders() {
    var request = createOrdersRequestObject();
    try {
        //
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