var yesButton = document.getElementById("yesButton");
var noButton = document.getElementById("noButton");

yesButton.onclick= function(){
    document.getElementById("respondYes").classList.remove("hidden");
    document.getElementById("yesQuote").classList.remove("hidden");
    hideButtons();
};
noButton.onclick= function(){
    document.getElementById("respondNo").classList.remove("hidden");
    document.getElementById("noQuote").classList.remove("hidden");
    hideButtons();
};
function hideButtons(){
    yesButton.classList.add("hidden");
    noButton.classList.add("hidden");
}