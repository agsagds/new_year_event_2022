const HOST_URL = document.location.origin;
const HOUSE_SIZE=64;
const PLAYER_SIZE=32;
const UP=0;
const DOWN=1;
const LEFT=2;
const RIGHT=3;

const c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
const img_elf = new Image();
img_elf.src = '../static/img/elf.png'
const img_house = new Image();
img_house.src = '../static/img/house.png'
const img_gifted_house = new Image();
img_gifted_house.src = '../static/img/gifted_house.png';

const update = () => {
	fetch(`${HOST_URL}/map`)
	.then((response)=>response.json())
	.then((data)=>{
		//console.log(data);
		//console.log('redraw');
		
		ctx.clearRect(0,0, c.width, c.height);
		for(var i of data.houses){
			ctx.drawImage((i.gifted === true ? img_gifted_house: img_house), i.x-HOUSE_SIZE, i.y-HOUSE_SIZE, HOUSE_SIZE, HOUSE_SIZE);
		}
		for(var i of data.players){
			ctx.drawImage(img_elf, i.x-PLAYER_SIZE, i.y-PLAYER_SIZE,PLAYER_SIZE, PLAYER_SIZE);
			ctx.font = "12px Arial";
			ctx.fillText(i.name, i.x-PLAYER_SIZE, i.y-PLAYER_SIZE-10);
		}
	});
}
setInterval(update, 1000);


let myId;
fetch(`${HOST_URL}/reg/DEFAULT_NAME`)
	.then((response)=>response.json())
	.then((data)=>{
		//console.log(data);
		myId = data;
	});

let stage=0;

const action=async ()=>{
	const map = await fetch(`${HOST_URL}/map`)
	.then((response)=>response.json());
	//console.log(map);
	const me = await fetch(`${HOST_URL}/about_me/${myId}`)
	.then((response)=>response.json());
	//console.log(me);

	setTimeout( async ()=>{
		if(stage%2==0 && me.x==map.width || stage%2==1 && me.x==0){
			await fetch(`${HOST_URL}/move/${myId}/${DOWN}`)//.then((response)=>response.json()).then((data)=>{console.log(data)});
			stage++;
		}else{
			await fetch(`${HOST_URL}/place_gift/${myId}`)//.then((response)=>response.json()).then((data)=>{console.log(data)});
			setTimeout(async ()=>{
				if(stage%2==0){
					await fetch(`${HOST_URL}/move/${myId}/${RIGHT}`)//.then((response)=>response.json()).then((data)=>{console.log(data)});
				}else{
					await fetch(`${HOST_URL}/move/${myId}/${LEFT}`)//.then((response)=>response.json()).then((data)=>{console.log(data)});
				}
			},2000);
			
		}
	}, 2000);
}

setInterval(action, 4000);