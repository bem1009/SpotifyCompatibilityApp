var addProfileButton = document.getElementById("addProfiles");
var totalTextBoxes = 1;
var submitButton = document.getElementById("passDataToScript");

var textBoxIDs = ["fname1"];


submitButton.onclick = function processData(){
    
    //console.log("Input is " + profile );
    var profiles = [];
    for (var i = 0; i < textBoxIDs.length; i++ ) {
        console.log("Input is " + textBoxIDs[i] );

        profiles.push(document.getElementById(textBoxIDs[i]).value);
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
