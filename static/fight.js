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

var charSPD = (charAGI/charHP)*10;
var enemySPD = parseInt(document.getElementById("enemySPD").innerHTML);

//var nextRoom = document.getElementById("nextRoom").innerHTML;

var flag = 0;

var canAttack = false;
var canHeal  = false;
var canWait = false;
var mustWait = false;

var attackButton = document.getElementById("attackButton");
var healButton = document.getElementById("healButton");
var waitButton = document.getElementById("waitButton");

attackButton.onclick = function(){
    if(canAttack){
        flag = 1;
    }
};
healButton.onclick = function(){
    if(canHeal){
        flag = 2;
    }
};
waitButton.onclick = function(){
    if(canWait){
        flag = 3;
    }
};

document.onload = battle();

function click(){
    var toBreak = false;
    attackButton.onclick = function(){
        if(canAttack){
            flag = 1;
            toBreak = true;
        }
    };
    healButton.onclick = function(){
        if(canHeal){
            flag = 2;
            toBreak = true;
        }
    };
    waitButton.onclick = function(){
        if(canWait){
            flag = 3;
            toBreak = true;
        }
    };
    while(!toBreak){
        if(toBreak){
            break;
        }
    }
    return true;
}

async function battle(){
    var isCharTurn = charSPD>enemySPD;

    while(currentCharHP>0||currentEnemyHP>0){
        console.log("while loop");
        document.getElementById("enemyStatus").innerHTML=currentEnemyHP+" / "+enemyHP;
        document.getElementById("charStatus").innerHTML=currentCharHP+" / "+charHP;
        var toSendToLog = "<code>";
        if(isCharTurn){
            canWait = true;
            if(!mustWait){
                canAttack = true;
                canHeal = true;
            }

            var didHeal = false;
            console.log("outside of doTurn");
            //var test = await click();
            function doTurn(){
                console.log("inside of doTurn");
                if(flag==0){
                    setTimeout(doTurn(),100);
                }else if(flag==1){
                    if(charWepACC>=Math.random()){
                        var damage = charSTR*charWepSTR;
                        toSendToLog+="You do <b>"+damage+"</b> to "+enemyName;
                        currentEnemyHP = Math.max(currentEnemyHP-damage,0);
                    }else{
                        toSendToLog+="You miss your attack!";
                    }
                }else if(flag==2){
                    var heal = charWepSTR*0.2*charHP;
                    toSendToLog+="You heal yourself for <b>"+heal+"</b> health";
                    currentCharHP = Math.min(currentCharHP+heal,charHP);
                    didHeal = true;
                }else{
                    toSendToLog+="You wait."
                }
            }
            doTurn();
            mustWait=didHeal;

        }else{
            if(charEVA>=Math.random()){
                toSendToLog+="You dodge the attack!";
            }else{
                var damage = enemySTR;
                toSendToLog+=enemyName+" hits you for <b>"+damage+"</b> damage";
                currentCharHP = Math.max(currentCharHP-damage,0);
            }
        }

        isCharTurn = !isCharTurn;
        toSendToLog+="</code><br>";
        combatLog.innerHTML = toSendToLog+combatLog.innerHTML;
    }
    if(currentCharHP>0){
        combatLog.innerHTML = "You win!<br>"+combatLog.innerHTML;
        document.getElementById("nextRoomDiv").classList.remove("hidden");
    }else{
        combatLog.innerHTML = "You lose...<br>"+combatLog.innerHTML;
        document.getElementById("retry").classList.remove("hidden");
    }

    /*
    while(currentCharHP>0||currentEnemyHP>0){}
    if(currentCharHP>0){win}else{lose}

     */
}