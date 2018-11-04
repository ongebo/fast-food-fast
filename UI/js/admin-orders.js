fetchAndDisplayOrders();
attachEventHandlers();
var orders;

function attachEventHandlers() {
    document.querySelector(".no").addEventListener("click", e => {
        document.querySelector(".confirm-box").style.display = "none";
    });
    document.querySelector(".yes").addEventListener("click", updateOrderStatus);
    document.querySelector(".close").addEventListener("click", function() {
        document.querySelector(".order").style.display = "none";
    });
}

async function fetchAndDisplayOrders() {
    var request = createOrdersRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            var responseBody = await response.json();
            orders = responseBody.orders;
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
        var detailsLink = createOrderDetailsLink(order["order-id"]);
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

function createOrderDetailsLink(orderId) {
    var td = document.createElement("td");
    var link = document.createElement("a");
    link.href = "#";
    link.setAttribute("class", "details");
    link.textContent = "Details";
    link.id = orderId;
    link.addEventListener("click", showOrderDetails);
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
        var optionLinks = createAcceptedOrderLinks(order["order-id"]);
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
        paragraph.textContent = orderItem.quantity + " " + unit + " @ Ugx " + orderItem.cost;
        paragraphs.push(paragraph);
    }
    return paragraphs;
}

function createAcceptedOrderLinks(orderId) {
    var span = document.createElement("span");
    var cancelLink = document.createElement("a");
    var completeLink = document.createElement("a");
    
    cancelLink.href = "#";
    cancelLink.setAttribute("class", "decline");
    cancelLink.textContent = "Cancel";
    cancelLink.id = orderId;
    cancelLink.addEventListener("click", declineOrder)

    completeLink.href = "#";
    completeLink.setAttribute("class", "complete");
    completeLink.textContent = "Complete";
    completeLink.id = orderId;
    completeLink.addEventListener("click", completeOrder);
    
    span.setAttribute("class", "admin-options");
    span.appendChild(cancelLink);
    span.appendChild(completeLink);
    return span;
}

function displayNewOrders(newOrders) {
    var container = document.querySelector(".new");
    for (var c = 0; c < newOrders.length; c++) {
        var order = newOrders[c];
        var customer = document.createElement("h3");
        var items = createOrderItemsElements(order.items);
        var total = document.createElement("h3");
        var optionLinks = createNewOrderUpdateLinks(order["order-id"]);
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

function createNewOrderUpdateLinks(orderId) {
    var span = document.createElement("span");
    var acceptLink = document.createElement("a");
    var declineLink = document.createElement("a");
    var completeLink = document.createElement("a");

    acceptLink.href = "#";
    acceptLink.setAttribute("class", "accept");
    acceptLink.textContent = "Accept";
    acceptLink.id = orderId;
    acceptLink.addEventListener("click", acceptOrder);
    
    declineLink.href = "#";
    declineLink.setAttribute("class", "decline");
    declineLink.textContent = "Decline";
    declineLink.id = orderId;
    declineLink.addEventListener("click", declineOrder);
    
    completeLink.href = "#";
    completeLink.setAttribute("class", "complete");
    completeLink.textContent = "Complete";
    completeLink.id = orderId;
    completeLink.addEventListener("click", completeOrder);
    
    span.setAttribute("class", "admin-options");
    span.appendChild(acceptLink);
    span.appendChild(declineLink);
    span.appendChild(completeLink);
    return span;
}

function acceptOrder(event) {
    event.preventDefault();
    var yesButton = document.querySelector(".confirm-box .yes");
    var promptElement = document.querySelector(".prompt-message");
    yesButton.className = "yes processing";
    yesButton.id = event.target.id;
    promptElement.textContent = "Do you want to accept order #" + event.target.id + "?";
    document.querySelector(".confirm-box").style.display = "block";
}

function declineOrder(event) {
    event.preventDefault();
    var yesButton = document.querySelector(".confirm-box .yes");
    var promptElement = document.querySelector(".prompt-message");
    yesButton.className = "yes cancelled";
    yesButton.id = event.target.id;
    promptElement.textContent = "Do you want to decline order #" + event.target.id + "?";
    document.querySelector(".confirm-box").style.display = "block";
}

function completeOrder(event) {
    event.preventDefault();
    var yesButton = document.querySelector(".confirm-box .yes");
    var promptElement = document.querySelector(".prompt-message");
    yesButton.className = "yes complete";
    yesButton.id = event.target.id;
    promptElement.textContent = "Do you want to complete order #" + event.target.id + "?";
    document.querySelector(".confirm-box").style.display = "block";
}

async function updateOrderStatus(event) {
    var orderId = event.target.id;
    var status = event.target.className.substring(4);
    var request = createOrderUpdateRequestObject(status, orderId);
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            location.reload(true);
        } else if (response.status == 401) {
            location.href = "index.html";
        }
    } catch (error) {
        alert(error);
    }
}

function createOrderUpdateRequestObject(status, orderId) {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var requestBody = {status: status};
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/orders/" + orderId,
        {method: "PUT", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

function showOrderDetails(event) {
    event.preventDefault();
    var order;
    for (var c = 0; c < orders.length; c++)
        if (orders[c]["order-id"] == event.target.id)
            order = orders[c];
    var customer = document.createElement("h3");
    var items = createOrderItemsElements(order.items);
    var status = document.createElement("h3");
    var total = document.createElement("h3");
    var orderElement = document.createElement("div");

    customer.textContent = order.customer + " #" + order["order-id"];
    status.textContent = "Status: " + order.status;
    total.textContent = "Total: Ugx " + order["total-cost"];
    orderElement.appendChild(customer);
    for (var i = 0; i < items.length; i++)
        orderElement.appendChild(items[i]);
    orderElement.appendChild(status);
    orderElement.appendChild(total);
    orderElement.setAttribute("class", "process-order");

    var container = document.querySelector(".order-details");
    var oldChild = document.querySelector(".order-details .process-order");
    if (oldChild)
        container.replaceChild(orderElement, oldChild);
    else
        container.appendChild(orderElement);
    document.querySelector(".order").style.display = "block";
}
