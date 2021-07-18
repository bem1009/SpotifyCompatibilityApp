var button = document.getElementById("addProfiles");
var totalTextBoxes = 1;



button.onclick = function addTextBoxes(){
    console.log("Button Clicked!");

    if (totalTextBoxes == 4) {
        return
    }

    totalTextBoxes += 1;
    var ptag = document.createElement("p");
    // Create an input type dynamically
    var element = document.createElement("input");
    element.type = "text";

    //Create Labels
    var label = document.createElement("Label");
    label.innerHTML = "New Label ";   

    // 'foobar' is the div id, where new fields are to be added
    var foo = document.getElementById("inputProfiles");

    foo.appendChild(ptag);

    ptag.appendChild(label);
    ptag.appendChild(element);

};
