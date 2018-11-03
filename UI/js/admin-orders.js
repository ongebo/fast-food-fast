fetchAndDisplayOrders();

async function fetchAndDisplayOrders() {
    var request = createOrdersRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            var responseBody = await response.json();
            displayOrders(responseBody.orders);
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

function displayOrders(orders) {
    var newOrders = [], acceptedOrders = [], completeOrders = [];
    for (var c = 0; c < orders.length; c++) {
        var order = orders[c];
        if (order.status.toLowerCase() == "new")
            newOrders.push(order);
        else if (order.status.toLowerCase() == "processing")
            acceptedOrders.push(order);
        else if (order.status.toLowerCase() == "complete")
            completeOrders.push(order);
    }
    displayCompleteOrders(completeOrders);
    displayAcceptedOrders(acceptedOrders);
    displayNewOrders(newOrders);
}

function displayCompleteOrders(completeOrders) {
    var table = document.querySelector(".admin-orders .orders-list");
    for (var c = 0; c < completeOrders.length; c++) {
        order = completeOrders[c];
        var name = document.createElement("td");
        var identity = document.createElement("td");
        var cost = document.createElement("td");
        var detailsLink = createOrderDetailsLink();
        name.textContent = order.customer;
        identity.textContent = order["order-id"];
        cost.textContent = order["total-cost"];

        var tableRow = document.createElement("tr");
        tableRow.appendChild(name);
        tableRow.appendChild(identity);
        tableRow.appendChild(cost);
        tableRow.appendChild(detailsLink);
        table.appendChild(tableRow);
    }
}

function createOrderDetailsLink() {
    var td = document.createElement("td");
    var link = document.createElement("a");
    link.href = "#";
    link.setAttribute("class", "details");
    td.appendChild(link);
    return td;
}

function displayAcceptedOrders(acceptedOrders) {
    var container = document.querySelector(".accepted");
    for (var c = 0; c < acceptedOrders.length; c++) {
        var order = acceptedOrders[c];
        var customer = document.createElement("h3");
        var items = createOrderItemsElements(order.items);
        var total = document.createElement("h3");
        var optionLinks = createAcceptedOrderLinks();
        var orderElement = document.createElement("div");
        customer.textContent = order.customer + " #" + order["order-id"];
        total.textContent = "Total: Ugx " + order["total-cost"];
        orderElement.appendChild(customer);
        for (var i = 0; i < items.length; i++)
            orderElement.appendChild(items[i]);
        orderElement.appendChild(total);
        orderElement.appendChild(optionLinks);
        orderElement.setAttribute("class", "process-order");
        container.appendChild(orderElement);
    }
}

function createOrderItemsElements(orderItems) {
    var paragraphs = [];
    for (var c = 0; c < orderItems.length; c++) {
        var orderItem = orderItems[c];
        var paragraph = document.createElement("p");
        var name = orderItem.item;
        var unit;
        if (orderItem.quantity > 1 && name.charAt(name.length - 1) != "s")
            unit = name + "s";
        else
            unit = name;
        paragraph.textContent = orderItem.quantity + " " + unit + " @ Ugx" + orderItem.cost;
        paragraphs.push(paragraph);
    }
    return paragraphs;
}

function createAcceptedOrderLinks() {
    var span = document.createElement("span");
    var cancelLink = document.createElement("a");
    var completeLink = document.createElement("a");
    cancelLink.href = "#";
    cancelLink.setAttribute("class", "decline");
    cancelLink.textContent = "Cancel";
    completeLink.href = "#";
    completeLink.setAttribute("class", "complete");
    completeLink.textContent = "Complete";
    span.setAttribute("class", "admin-options");
    span.appendChild(cancelLink);
    span.appendChild(completeLink);
    return span;
}

function displayNewOrders(newOrders) {
    //
}
