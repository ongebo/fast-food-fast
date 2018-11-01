var admin = sessionStorage.getItem("admin");
var token = sessionStorage.getItem("token");

if (token == null || admin == false) {
    window.location.href = "index.html";
}
redirectIfTokenHasExpired(token);

async function redirectIfTokenHasExpired(token) {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + token);
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/menu",
        {method: "GET", headers: headers}
    );
    
    try {
        var response = await fetch(request);
        console.log(response.status);
        if (response.status == 401) {
            window.location.href = "index.html";
        }
    } catch (error) {
        alert(error);
    }
}
