var combatLog = "";

var charAGI = parseInt(document.getElementById("charAGI").innerHTML);
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

var nextRoom = document.getElementById("nextRoom").innerHTML;

function battle(){
    var isCharTurn = charSPD>enemySPD;
    /*
    while(currentCharHP>0||currentEnemyHP>0){}
    if(currentCharHP>0){win}else{lose}

     */
}