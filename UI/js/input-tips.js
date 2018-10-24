function addInputTips() {
    var username = document.querySelector("input[name=username]");
    var telephone = document.querySelector("input[name=telephone]");

    var usernameTip = "Username can only contain letters. Each name (firstname/lastname)" +
    " must contain atleast three letters, names are separated by single spaces.";
    var telephoneTip = "Use the format: +xxx-xxx-xxxxxx e.g. +23-234-918719, +256-751-682390";
    
    username.title = usernameTip;
    telephone.title = telephoneTip;
}
