var weapons = document.getElementById("weapons").innerHTML.split(" ");
var items = document.getElementById("items").innerHTML.split(" ");
var equipped = document.getElementById("equipped").innerHTML.split(" ");

var characterInfo = document.getElementById("equip");
if(equipped.length>1) {
    var tempE = '';
    tempE += "<b>" + equipped[0].
    replace("replace_with_space", " ") + "</b>: a " + equipped[1]+" with " + equipped[2]+
        " STR, " + equipped[3]+" HP, and " + equipped[4]+" AGI";
    if (equipped.length >= 6) {
        tempE += "<br><b>" + equipped[5]+"</b>: " + equipped[6]+"x damage and " + equipped[7]+" accuracy";
    }
    characterInfo.innerHTML = tempE;
}

var dropdownButton = document.getElementById("dropdownButton");
var dropdownList = document.getElementById("dropdownList");

if(weapons[0]!=""){
    dropdownButton.innerHTML = weapons[0].replace("_", " ");
    for (var i = 0; i < weapons.length; i++) {
        var temp = "";
        temp = "<input class='dropdownItems' type='submit' name='equip' value='" + weapons[0].
        replace("_", " ") + "'>";
        dropdownList.innerHTML += temp;
    }
}

document.getElementById("goBack").href = document.referrer;

dropdownButton.onclick = function() {
    dropdownList.classList.toggle("show");
};

//.replace("<<","{").replace(">>","}").replace("╩","[").replace("╦","]")