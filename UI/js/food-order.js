fetchAndDisplayMenu();
var orderList = [];

function fetchAndDisplayMenu() {
    var request = createRequestObject();
    try {
        fetch(request).then(
            response => {
                return response.json();
            }
        ).then(displayMenu);
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
        {method: "GET", cache: "reload", headers: headers}
    );
    return request;
}

function displayMenu(menuData) {
    var menu = document.querySelector(".food-menu");
    var menuItems = menuData.menu;
    for (var c = 0; c < menuItems.length; c++) {
        var item = menuItems[c];
        var itemElement = createMenuItemElement(item, c);
        var itemDetails = createItemDetailsElement(item.unit, c);
        menu.appendChild(itemElement);
        menu.appendChild(itemDetails);
    }
    var orderButton = document.createElement("button");
    orderButton.setAttribute("class", "order");
    orderButton.innerHTML = "Place Order";
    orderButton.addEventListener("click", placeOrder);
    document.querySelector(".order-list > button").addEventListener("click", placeOrder);
    menu.appendChild(orderButton);
    attachEventHandlersToMenuItems();
}

function createMenuItemElement(item, id) {
    var h3 = document.createElement("h3");
    h3.id = "name" + id;
    h3.textContent = item.item;
    var rate = document.createTextNode("Ugx " + item.rate + " per " + item.unit);
    var itemElement = document.createElement("div");
    itemElement.setAttribute("class", "menu-item");
    itemElement.id = "item" + id;
    itemElement.appendChild(h3);
    itemElement.appendChild(rate);
    return itemElement;
}

function createItemDetailsElement(unit, id) {
    var input = document.createElement("input");
    input.type = "number";
    input.id = "input" + id;
    input.placeholder = "Enter number of " + unit + "s";
    var span = document.createElement("span");
    span.setAttribute("class", "quantity");
    span.appendChild(document.createTextNode("Quantity: "));
    span.appendChild(input);
    var button = document.createElement("button");
    button.innerHTML = "Add to List";
    button.id = "button" + id;
    button.addEventListener("click", addItemToList);

    var itemDetails = document.createElement("div");
    itemDetails.setAttribute("class", "menu-item-details");
    itemDetails.appendChild(span);
    itemDetails.appendChild(button);
    return itemDetails;
}

function attachEventHandlersToMenuItems() {
    var acc = document.getElementsByClassName("menu-item");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("selected");
            var panel = this.nextElementSibling;
            if (panel.style.display === "block"){
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }
}

function addItemToList(event) {
    var buttonId = event.target.id;
    var idSuffix = buttonId.match(/[0-9]+/);
    var orderItem = createOrderItem(idSuffix);
    var itemNotInList = true;
    for (var c = 0; c < orderList.length; c++) {
        if (orderList[c].item == orderItem.item) {
            orderList[c] = orderItem;
            itemNotInList = false;
        }
    }
    if (itemNotInList)
        orderList.push(orderItem);
    displayOrderList();
}

function createOrderItem(idSuffix) {
    var itemSelector = "#item" + idSuffix;
    var item = document.getElementById("name" + idSuffix).innerHTML;
    var quantity = document.querySelector("#input" + idSuffix).value;
    var rate = document.querySelector(itemSelector).innerHTML.match(/ [0-9]+ /);
    var rate = parseFloat(rate);
    var cost = quantity * rate;
    var orderItem = {item: item, quantity: quantity, cost: cost};
    return orderItem;
}

function displayOrderList() {
    var listElement = document.querySelector(".order-list");
    var orderButton = document.querySelector(".order-list > button");
    removeChildElements(listElement);
    for (var c = 0; c < orderList.length; c++) {
        var unit = getItemUnit(orderList[c].item);
        var content = orderList[c].quantity + " " + unit + "s of " + orderList[c].item +
        " @ Ugx " + orderList[c].cost;
        var p = document.createElement("p");
        p.setAttribute("class", "order-list-item");
        p.appendChild(document.createTextNode(content));
        listElement.insertBefore(p, orderButton);
    }
    listElement.insertBefore(createOrderTotalElement(), orderButton);
}

function removeChildElements(listElement) {
    var listLength = listElement.children.length;
    while (listLength > 2) {
        for (var c = 0; c < listLength; c++) {
            var child = listElement.children[c];
            if (child.className != "order" && child.className != "title") {
                listElement.removeChild(child);
                break;
            }
        }
        listLength = listElement.children.length;
    }
}

function getItemUnit(orderItem) {
    var menuItems = document.getElementsByClassName("menu-item");
    var unit;
    for (var c = 0; c < menuItems.length; c++) {
        if (menuItems[c].querySelector("h3").innerHTML == orderItem) {
            unit = menuItems[c].innerHTML.match(/per [a-zA-Z]+/).toString().substring(4);
            return unit;
        }
    }
}

function createOrderTotalElement() {
    var orderTotal = 0;
    for (var c = 0; c < orderList.length; c++) {
        orderTotal += orderList[c].cost;
    }
    var orderTotalElement = document.createElement("h2");
    orderTotalElement.setAttribute("class", "order-total");
    orderTotalElement.appendChild(document.createTextNode("Order Total: " + orderTotal));
    return orderTotalElement;
}

function placeOrder() {
    var request = createOrderRequestObject();
    try {
        fetch(request).then(
            response => {
                if (response.status == 201) {
                    showMessageAboutOrder("Your order was successful!");
                } else {
                    showMessageAboutOrder("Your order was not successful!");
                }
            }
        );
    } catch (error) {
        showMessageAboutOrder(error);
    }
}

function createOrderRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var requestBody = {items: orderList}
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/users/orders",
        {method: "POST", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

function showMessageAboutOrder(message) {
    var listElement = document.querySelector(".order-list");
    var orderButton = document.querySelector(".order-list > button");
    removeChildElements(listElement);
    var messageElement = document.createElement("h2");
    messageElement.textContent = message;
    listElement.insertBefore(messageElement, orderButton);
}
