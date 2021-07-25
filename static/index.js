var addProfileButton = document.getElementById("addProfiles");
var totalTextBoxes = 1;
var submitButton = document.getElementById("passDataToScript");

var textBoxIDs = ["fname1"];

var clientID = "54b18b9335cf4489bbd682de84967d7f"

const AUTHORIZE = "https://accounts.spotify.com/authorize"

var redirect_uri = "http://127.0.0.1:5000/"

clientSecret = "d59f90b740604e9dbaf02b8e39e49ecf"


function requestAuthorization () {
    localStorage.setItem("client_id", clientID);
    
    let url = AUTHORIZE;

    url += "?client_id=" + clientID;
    url += "&response_type=code";
    url += "&redirect_uri=" + encodeURI(redirect_uri);
    url += "&show_dialog=true";
    url += "&scope=playlist-modify-public"

    window.location.href = url;

    print(url)

}


function onPageLoad() {
    // if window has query params on it
    if (window.location.search.length > 0) {
        handleRedirect();

    }
    
    
}


function handleRedirect() {
    let code = getCode();

}

// find code param in the redirect url
function getCode() {
    let code = null;
    const queryString = window.location.search;
    if (queryString.length > 0){
        const urlParams = new URLSearchParams(queryString);
        code = urlParams.get('code')

    }

    return code;
}

function fetchAccessToken(code){
    let body = "grant_type=authorization_code";
    body += "&code=" + code;
    body += "&redirect_uri=" + encodeURI(redirect_uri);
    body += "&client_id=" + clientID;
    body += "&client_secret=" + clientSecret;
    callAuthorizationApi(body);

}


// handle this in python later to keep things cleaner?
function callAuthorizationApi(body){
    let xhr = new XMLHttpRequest();
    xhr.open("POST",TOKEN,true)
    xhr.setRequestHeader("Content-Type", 'application/x-www-form-urlencoded')
    xhr.setRequestHeader("Authorization", "Basic" + btoa(client_id + ":" + clientSecret));
    xhr.send(body);
    xhr.onload = handleAuthorizationResponse;

}


// need to also add authorization response 








submitButton.onclick = function processData(){

    var content = document.getElementById('content')
    var slowwarning = document.getElementById('slow_warning')
    if (content.style.display !== 'none') {
        content.style.display = 'none';
        slowwarning.style.display = 'block';

    }
}

addProfileButton.onclick = function addTextBoxes(){

    if (totalTextBoxes == 4) {
        return
    }

    var ptag = document.createElement("p");
    // Create an input type dynamically
    var element = document.createElement("input");
    element.type = "text";
    totalTextBoxes += 1;
    element.id = "fname" + totalTextBoxes;
    element.name = "fname" + totalTextBoxes;
    textBoxIDs.push(element.id)
    //Create Labels
    var label = document.createElement("Label");
    label.innerHTML = "User-ID: ";   

    // 'foobar' is the div id, where new fields are to be added
    var foo = document.getElementById("inputProfiles");

    foo.appendChild(ptag);

    ptag.appendChild(label);
    ptag.appendChild(element);

};
