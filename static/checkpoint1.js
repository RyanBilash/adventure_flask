var itemList = document.getElementById('itemList').innerHTML.split(' ');

var pictureRoomButton = document.getElementById('pictureRoomButton');
var fAndRButton = document.getElementById('fAndRButton');
var canPressSet1 = true;

var pictureRoomDiv = document.getElementById('pictureRoomDiv');

var outerFAndRDiv = document.getElementById('fAndRDiv');

var takeFAndR = document.getElementById('takeFAndR');
var leaveFAndR = document.getElementById('leaveFAndR');
var canPressSet2 = true;

var innerFAndRDiv = document.getElementById('takeFAndRDiv');

var dropdown = document.getElementById('dropdown');

function toggleSet(num){
    if(num==1){canPressSet1 = !canPressSet1;}
    else if(num==2){canPressSet2 = !canPressSet2;}
}

pictureRoomButton.onclick = function(){
    if(canPressSet1){
        pictureRoomDiv.classList.remove('hidden');
        toggleSet(1);
    }
}

fAndRButton.onclick = function(){
    if(canPressSet1){
        outerFAndRDiv.classList.remove('hidden');
        toggleSet(1)
    }
}

takeFAndR.onclick = function(){
    if(canPressSet2){
        innerFAndRDiv.classList.remove('hidden');
        toggleSet(2);
    }
}

leaveFAndR.onclick = function(){
    if(canPressSet2){
        outerFAndRDiv.classList.add('hidden');
        toggleSet(1);
    }
}

for (let i = 0; i < itemList.length; i++) {
    dropdown.innerHTML = dropdown.innerHTML+"<option value='"+itemList[i]+"'>"+
        itemList[i].replace("_",' ')+"</option>";
}

