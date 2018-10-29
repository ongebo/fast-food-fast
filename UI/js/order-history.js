fetchAndDisplayOrderHistory();

async function fetchAndDisplayOrderHistory() {
    var request = createHistoryRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            // display order history
            var orders = await response.json();
            displayOrderHistory(orders.orders);
        } else {
            // show error message
            showErrorMessage();
        }
    } catch (error) {
        alert(error);
    }
}

function createHistoryRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/users/orders",
        {method: "GET", headers: headers}
    );
    return request;
}

function displayOrderHistory(orders) {
    orders.reverse(); // latest order first
    var orderNumber = orders.length;
    var historyElement = document.querySelector(".history");
    removeHistoryChildElements(historyElement);
    for (var c = 0; c < orders.length; c++, orderNumber--) {
        var itemElements = createOrderItemElements(orders[c]);
        var totalCost = document.createElement("h2");
        totalCost.setAttribute("class", "order-total");
        totalCost.textContent = "Order Total: " + orders[c]["total-cost"];
        var label = document.createElement("h2");
        label.textContent = "Order #" + orderNumber;
        var historyDetail = document.createElement("div");
        historyDetail.setAttribute("class", "history-detail");
        historyDetail.appendChild(label);
        for (var i = 0; i < itemElements.length; i++) {
            historyDetail.appendChild(itemElements[i]);
        }
        historyDetail.appendChild(totalCost);
        historyElement.appendChild(historyDetail);
    }
}

function createOrderItemElements(order) {
    var itemElements = [];
    for (var c = 0; c < order.items.length; c++) {
        var item = order.items[c];
        var itemElement = document.createElement("p");
        itemElement.setAttribute("class", "order-list-item");
        var units = item.item;
        if (item.quantity > 1)
            units += "s";
        var content = item.quantity + " " + units + " @ Ugx " + item.cost;
        itemElement.appendChild(document.createTextNode(content));
        itemElements.push(itemElement);
    }
    return itemElements;
}

function removeHistoryChildElements(historyElement) {
    var listLength = historyElement.children.length;
    while (listLength > 1) {
        for (var c = 0; c < listLength; c++) {
            var child = historyElement.children[c];
            if (child.className != "title") {
                historyElement.removeChild(child);
                break;
            }
            listLength = historyElement.children.length;
        }
    }
}

function showErrorMessage() {
    var historyElement = document.querySelector(".history");
    removeHistoryChildElements(historyElement);
    var messageElement = document.createElement("h2");
    messageElement.textContent = "You have not made any orders!";
    historyElement.appendChild(messageElement);
}
