var attackButton = document.getElementById("attack");
var sneakButton = document.getElementById("sneak");

var charAGI = parseInt(document.getElementById("charAGI").innerHTML);
var charHP = parseInt(document.getElementById("charHP").innerHTML);

var hadClicked = false;

attackButton.onclick = function(){
    if(!hadClicked){
       document.getElementById("attackDiv").classList.remove("hidden");
    }
    hadClicked = true;
}

sneakButton.onclick = function(){
    if(!hadClicked){
        sneakVal = getRandSneakVal(charAGI,charHP);
        if(sneakVal>=13.5){
            document.getElementById("sneakDiv").classList.remove("hidden");
        }else if(sneakVal>=8){
            document.getElementById("okSneakDiv").classList.remove("hidden");
        }else{
            document.getElementById("badSneakDiv").classList.remove("hidden");
        }

    }
    hadClicked = true;
}

function getRandSneakVal(agi,hp){
    return agi/hp*10*Math.random();
}