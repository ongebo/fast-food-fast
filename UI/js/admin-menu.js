fetchAndDisplayAdminMenu();
window.addEventListener("click", event => {
    var modal = document.querySelector(".modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
});
document.querySelector(".close").addEventListener("click", event => {
    document.querySelector(".modal").style.display = "none";
});
document.querySelector(".add").addEventListener("click", event => {
    document.querySelector(".form-title").textContent = "Add Menu Item";
    document.querySelector("input[type=submit]").value = "Add";
    document.querySelector(".modal").style.display = "block";
});

async function fetchAndDisplayAdminMenu() {
    var request = createRequestObject();
    try {
        var response = await fetch(request);
        if (response.status == 404) {
            displayEmptyMenuMessage();
        } else {
            var responseBody = await response.json();
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
