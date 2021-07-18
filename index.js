var button = document.getElementById("addProfiles");

button.onclick = function addTextBoxes(){
    console.log("Button Clicked!")

    // Create an input type dynamically
    var element = document.createElement("input");
    element.type = "text";

    //Create Labels
    var label = document.createElement("Label");
    label.innerHTML = "New Label";   

    // 'foobar' is the div id, where new fields are to be added
    var foo = document.getElementById("inputProfiles");

    foo.appendChild(label);
    foo.appendChild(element);

};
