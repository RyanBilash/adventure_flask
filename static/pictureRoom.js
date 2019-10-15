var cheeseButton = document.getElementById('cheeseButton');
var nothingButton = document.getElementById('nothingButton');
var canClick1 = true;

cheeseButton.onclick = function(){
    if(canClick1){
        document.getElementById('succeedDiv').classList.remove('hidden');
        canClick1 = false;
    }
}
nothingButton.onclick = function(){
    if(canClick1){
        document.getElementById('fallDiv').classList.remove('hidden');
        canClick1 = false;
    }
}

document.getElementById('continue').onclick = function(){
    location.href = "/game/skeleton/";
}

var stat = parseInt(document.getElementById('stats').innerText);

var canClimb = true;
var canSearch = true;
var climbButton = document.getElementById('climbButton');
var searchButton = document.getElementById('searchButton');

var climbSuccess = document.getElementById('climbSuccess');
var climbFail = document.getElementById('climbFail');

climbButton.onclick = function(){
    if(canClimb){
        if(stat*Math.random()>=0.5){
            climbSuccess.classList.remove('hidden');
            canClimb = false;
        }else{
            if(climbFail.classList.contains('hidden')){climbFail.classList.remove('hidden');}
        }
    }
}

searchButton.onclick = function(){
    if(canSearch){
        document.getElementById('searchDiv').classList.remove('hidden');
        canSearch = false;
    }
}

document.getElementById('continuePit').onclick = function(){
    if(!canSearch){
        location.href = "/game/skeletony/";
    }else{
        location.href = "/game/skeleton/";
    }
}




