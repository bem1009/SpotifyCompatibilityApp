/* 
 
 File Name: index.js
 Author: Benjamin Miller
 
 This file is used to process button input from the user and 
 pass them off into application.py 

*/  

var addProfileButton = document.getElementById("addProfiles");
var totalTextBoxes = 1;
var submitButton = document.getElementById("passDataToScript");

var textBoxIDs = ["fname1"];

var form = document.getElementById("buttons")

const AUTHORIZE = "https://accounts.spotify.com/authorize"

var redirect_uri = "http://127.0.0.1:5000/"

var authButton = document.getElementById('Authorization')

authButton.onclick = function requestAccess(){
    var currentLocation = window.location;
    location.href = currentLocation + "/reqAccess"

}


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
    access_token = localStorage.getItem("access_token");
    console.log(access_token)
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
    label.innerHTML = "Username: ";   

    // 'foobar' is the div id, where new fields are to be added
    var foo = document.getElementById("inputProfiles");

    foo.appendChild(ptag);

    ptag.appendChild(label);
    ptag.appendChild(element);

};
