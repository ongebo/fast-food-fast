fetchAndDisplayAdminMenu();
var menu = [];
var itemToEdit;

window.addEventListener("click", event => {
    var modal = document.querySelector(".modal");
    if (event.target == modal) {
        modal.style.display = "none";
        removeErrorSignals();
    }
});
document.querySelector(".close").addEventListener("click", event => {
    document.querySelector(".modal").style.display = "none";
    removeErrorSignals();
});
document.querySelector(".add").addEventListener("click", event => {
    document.querySelector(".form-title").textContent = "Add Menu Item";
    document.querySelector("input[type=submit]").value = "Add";
    document.querySelector(".modal").style.display = "block";
});
document.querySelector(".modal-content > form").addEventListener("submit", submitFormData);

async function fetchAndDisplayAdminMenu() {
    var request = createRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 404) {
            displayEmptyMenuMessage();
        } else {
            var responseBody = await response.json();
            menu = responseBody.menu;
            displayAdminMenu(responseBody.menu);
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

function displayAdminMenu(menu) {
    var menuList = document.querySelector(".menu-list");
    for (var c = 0; c < menu.length; c++) {
        var item = document.createElement("td");
        var unit = document.createElement("td");
        var rate = document.createElement("td");
        item.textContent = menu[c].item;
        unit.textContent = menu[c].unit;
        rate.textContent = menu[c].rate;
        var tdsWithLinks = createTableDataWithLinks(c);
        var tableRow = document.createElement("tr");
        tableRow.appendChild(item);
        tableRow.appendChild(unit);
        tableRow.appendChild(rate);
        tableRow.appendChild(tdsWithLinks[0]);
        tableRow.appendChild(tdsWithLinks[1]);
        menuList.appendChild(tableRow);
    }
}

function createTableDataWithLinks(id) {
    var editLink = document.createElement("a");
    var deleteLink = document.createElement("a");
    editLink.setAttribute("class", "edit");
    editLink.href = "#";
    editLink.id = id;
    editLink.addEventListener("click", displayEditDialog);
    editLink.textContent = "Edit";
    deleteLink.setAttribute("class", "delete");
    deleteLink.href = "#";
    deleteLink.textContent = "Delete";
    var editTableData = document.createElement("td");
    var deleteTableData = document.createElement("td");
    editTableData.appendChild(editLink);
    deleteTableData.appendChild(deleteLink);
    return [editTableData, deleteTableData];
}

function displayEditDialog(event) {
    var linkId = parseInt(event.target.id);
    itemToEdit = menu[linkId].id;
    document.querySelector("input[name=item]").value = menu[linkId].item;
    document.querySelector("input[name=unit]").value = menu[linkId].unit;
    document.querySelector("input[name=rate]").value = menu[linkId].rate;
    document.querySelector(".form-title").textContent = "Edit Menu Item";
    document.querySelector("input[type=submit]").value = "Edit";
    document.querySelector(".modal").style.display = "block";
}

function submitFormData(event) {
    var submitButton = document.querySelector("input[type=submit]");
    var action = submitButton.value;
    submitButton.disabled = true;
    submitButton.value = "Submitting...";
    removeErrorSignals();
    if (action == "Edit") {
        editMenuItem();
    } else if (action == "Add") {
        addMenuItem();
    }
    submitButton.disabled = false;
    submitButton.value = action;
}

async function editMenuItem() {
    var request = createEditRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 200) {
            document.querySelector("input[type=submit]").value = "Update Successful!";
            location.reload(true);
        } else if (response.status == 401) {
            window.location.href = "index.html";
        } else if (response.status == 400) {
            var responseBody = await response.json();
            displayBadRequestError(responseBody);
        } else if (response.status == 404) {
            var item = document.querySelector("input[name=item]");
            item.classList.add("error");
            document.querySelector(".item-error").textContent = item.value +
            " doesn't exist in database!";
        }
    } catch (error) {
        alert(error);
    }
}

function createEditRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var requestBody = {
        item: document.querySelector("input[name=item]").value,
        unit: document.querySelector("input[name=unit]").value,
        rate: document.querySelector("input[name=rate]").value
    }
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/menu/" + itemToEdit,
        {method: "PUT", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

function displayBadRequestError(responseBody) {
    var errorMessage = responseBody.error;
    if (errorMessage.indexOf("item") != -1) {
        document.querySelector("input[name=item]").classList.add("error");
        document.querySelector(".item-error").textContent = errorMessage;
    } else if (errorMessage.indexOf("unit") != -1) {
        document.querySelector("input[name=unit]").classList.add("error");
        document.querySelector(".unit-error").textContent = errorMessage;
    } else {
        document.querySelector("input[name=rate]").classList.add("error");
        document.querySelector(".rate-error").textContent = errorMessage;
    }
}

async function addMenuItem() {
    var request = createAddRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 201) {
            document.querySelector("input[type=submit]").value = "Add Successful!";
            location.reload(true);
        } else if (response.status == 400) {
            var responseBody = await response.json();
            displayBadRequestError(responseBody);
        } else if (response.status == 401) {
            window.location.href = "index.html";
        }
    } catch (error) {
        alert(error);
    }
}

function createAddRequestObject() {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + sessionStorage.getItem("token"));
    var requestBody = {
        item: document.querySelector("input[name=item]").value,
        unit: document.querySelector("input[name=unit]").value,
        rate: document.querySelector("input[name=rate]").value
    }
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/menu",
        {method: "POST", headers: headers, body: JSON.stringify(requestBody)}
    );
    return request;
}

function removeErrorSignals() {
    document.querySelector(".item-error").textContent = "";
    document.querySelector(".unit-error").textContent = "";
    document.querySelector(".rate-error").textContent = "";
    var erroredFields = document.getElementsByClassName("error");
    for (var c = 0; c < erroredFields.length; c++) {
        erroredFields[c].classList.remove("error");
    }
}
