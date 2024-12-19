let cards = document.querySelectorAll('.car');
let cmpt = 0;

document.getElementById('prevServiceGris').style.background = "#aaa";
document.getElementById('prevService').classList.add('d-none');
document.getElementById('prevServiceGris').classList.remove('d-none');
for(let i = 3; i < cards.length ; i++){
    cards[i].classList.add('d-none');
}
const next = function(){
    for(let i = cmpt; i < cmpt+3 ; i++){
        cards[i].classList.add('d-none');
    }
    cmpt +=3;
   
    for(let i = cmpt; i < cmpt+3 ; i++){
    cards[i].classList.remove('d-none');
    }
    if(cmpt >= (cards.length-3)){
        document.getElementById('nextServiceGris').style.background = "#aaa";
        document.getElementById('nextServiceGris').classList.remove('d-none');
        document.getElementById('nextService').classList.add('d-none');
    }
    if(cmpt >= 0){
        document.getElementById('prevService').classList.remove('d-none');
        document.getElementById('prevServiceGris').classList.add('d-none');
    }
}
document.getElementById('nextService').addEventListener('click', next)
const prev = function(){
    for(let i = cmpt; i < cmpt+3 ; i++){
        cards[i].classList.add('d-none');
    }
    cmpt -=3;
    for(let i = cmpt; i < cmpt+3 ; i++){
        cards[i].classList.remove('d-none');
    }
    if(cmpt <= cards.length){
        document.getElementById('nextService').classList.remove('d-none');
        document.getElementById('nextServiceGris').classList.add('d-none');
    }
    if(cmpt<= 2){
        document.getElementById('prevServiceGris').style.background = "#aaa";
        document.getElementById('prevServiceGris').classList.remove('d-none');
        document.getElementById('prevService').classList.add('d-none');
    }
}
document.getElementById('prevService').addEventListener('click',prev);
