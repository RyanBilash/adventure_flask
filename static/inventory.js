var weapons = document.getElementById("weapons").innerHTML.split(" ");
var items = document.getElementById("items").innerHTML.split(" ");
var equipped = document.getElementById("equipped").innerHTML.split(" ");

var characterInfo = document.getElementById("equip");
var itemDiv = document.getElementById('itemList');

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

var dropdown = document.getElementById("dropdown");
dropdown.onchange = function(){
    if(dropdown.value!='null'){
        dropdown.form.submit();
    }
}

if(weapons[0]!=""){
    for (var i = 0; i < weapons.length; i++) {
        if(weapons[i]!=""){
            var temp = "";

            temp = "<option value='"+weapons[i]+"'>"+weapons[i].replace('_',' ')+"</option>"
            dropdown.innerHTML += temp;
        }
    }
}

if(items[0]!=""){
    for (let i = 0; i < items.length; i++) {
        if(items[i]!="") {
            var itemValues = items[i].split(",");
            var temp = "<b>";
            temp = itemValues[0].replace("_", " ") + "</b>: +";
            temp += itemValues[1] + " HP +" + itemValues[2] + " STR +" + itemValues[3] + " AGI<br>";
            itemDiv.innerHTML = itemDiv.innerHTML + temp;
        }
    }
}

document.getElementById("goBack").href = document.getElementById('referPage').innerText;