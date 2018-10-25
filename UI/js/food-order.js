fetchAndDisplayMenu();

function fetchAndDisplayMenu() {
    var request = createRequestObject();
    try {
        fetch(request).then(
            response => {
                return response.json();
            }
        ).then(
            menuData => {
                displayMenu(menuData);
            }
        );
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
        var itemElement = createMenuItemElement(item);
        var itemDetails = createItemDetailsElement(item.unit, c);
        menu.appendChild(itemElement);
        menu.appendChild(itemDetails);
    }
    var orderButton = document.createElement("button");
    orderButton.setAttribute("class", "order");
    orderButton.innerHTML = "Place Order";
    menu.appendChild(orderButton);
    attachEventHandlersToMenuItems();
}

function createMenuItemElement(item) {
    var h3 = document.createElement("h3");
    h3.textContent = item.item;
    var rate = document.createTextNode("Ugx " + item.rate + " per " + item.unit);
    var itemElement = document.createElement("div");
    itemElement.setAttribute("class", "menu-item");
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
