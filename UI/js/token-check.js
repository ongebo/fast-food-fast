var token = sessionStorage.getItem("token");
if (token == null || tokenHasExpired(token))
    window.location.href = "index.html"; // redirect to login page

function tokenHasExpired(token) {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Bearer " + token);
    var request = new Request(
        "https://gbo-fff-with-db.herokuapp.com/api/v1/users/orders",
        {headers: headers}
    );
    
    try {
        fetch(request).then(
            res => {
                if (res.status == 401)
                    return true
                else
                    return false
            }
        );
    } catch (error) {
        alert(error);
    }
}
