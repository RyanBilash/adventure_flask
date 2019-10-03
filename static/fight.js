var combatLog = document.getElementById("combatLog");

var charAGI = parseInt(document.getElementById("charAGI").innerHTML);
var charEVA = charAGI/25.0;
var charHP = parseInt(document.getElementById("charHP").innerHTML);
var currentCharHP = charHP+0.0;
var charSTR = parseInt(document.getElementById("charSTR").innerHTML);
var charWepSTR = parseFloat(document.getElementById("charWepSTR").innerHTML);
var charWepACC = parseFloat(document.getElementById("charWepACC").innerHTML);

var enemyName = document.getElementById("enemyName").innerHTML;
var enemyHP = parseInt(document.getElementById("enemyHP").innerHTML);
var currentEnemyHP = parseFloat(document.getElementById("currentEnemyHP").innerHTML);
var enemySTR = parseFloat(document.getElementById("enemySTR").innerHTML);

var canAttack = false;
var canHeal  = false;
var canWait = false;
var mustWait = false;

var attackButton = document.getElementById("attackButton");
var healButton = document.getElementById("healButton");
var waitButton = document.getElementById("waitButton");

attackButton.onclick = function(){
    if(canAttack){
        doTurn("attack");
    }else if(mustWait){
        alert("You must wait after healing");
    }
};
healButton.onclick = function(){
    if(canHeal){
        doTurn("heal")
    }else if(mustWait){
        alert("You must wait after healing");
    }
};
waitButton.onclick = function(){
    if(canWait){
        doTurn("wait");
    }
};

var toSendToLog = "";
function doTurn(type){
    canAttack = false;
    canHeal = false;
    canWait = false;
    didHeal = false;
    if(type=="attack"){
        if(charWepACC>=Math.random()){
            var damage = charSTR*charWepSTR;
            toSendToLog+="You do <b>"+damage.toFixed(2)+"</b> to "+enemyName;
            currentEnemyHP = Math.max(currentEnemyHP-damage,0);
        }else{
            toSendToLog+="You miss your attack!";
        }
    }else if(type=="heal"){
        var heal = charWepSTR*0.2*charHP;
        toSendToLog+="You heal yourself for <b>"+heal.toFixed(2)+"</b> health";
        currentCharHP = Math.min(currentCharHP+heal,charHP);
        didHeal = true;
        mustWait = true;
    }else{
        toSendToLog+="You wait.";
    }
    if(mustWait && !didHeal){
        mustWait = false;
    }
    update();
    if(canContinue()){
        enemyTurn();
    }
}

function enemyTurn(){
    if(charEVA>=Math.random()){
        toSendToLog+="You dodge the attack!";
    }else{
        var damage = enemySTR;
        toSendToLog+=enemyName+" hits you for <b>"+damage.toFixed(2)+"</b> damage";
        currentCharHP = Math.max(currentCharHP-damage,0);
    }
    if(canContinue()){
        canWait = true;
        if(!mustWait){
            canAttack = true;
            canHeal = true;
        }
    }

    update();
}

function update(){
    toSendToLog+="</code><br>";
    combatLog.innerHTML = toSendToLog+combatLog.innerHTML;

    document.getElementById("enemyStatus").innerHTML=currentEnemyHP.toFixed(2)+" / "+enemyHP;
    document.getElementById("charStatus").innerHTML=currentCharHP.toFixed(2)+" / "+charHP;
    if(currentCharHP>0&&currentEnemyHP<=0){
        combatLog.innerHTML = "You win!<br>"+combatLog.innerHTML;
        document.getElementById("nextRoomDiv").classList.remove("hidden");
    }else if(currentEnemyHP>0&&currentCharHP<=0){
        combatLog.innerHTML = "You lose...<br>"+combatLog.innerHTML;
        document.getElementById("retry").classList.remove("hidden");
    }
    toSendToLog = "";
}

function canContinue(){
    return currentCharHP>0&&currentEnemyHP>0;
}

var charSPD = (charAGI/charHP)*10;
var enemySPD = parseInt(document.getElementById("enemySPD").innerHTML);
if(charSPD>enemySPD){
    canAttack = true;
    canHeal = true;
    canWait = true;
}else{
    enemyTurn();
}