var items = document.getElementsByClassName("item");
var points = document.getElementsByClassName("point");
var goPreBtn = document.getElementById("goPre");
var goNextBtn = document.getElementById('goNext');
var time = 30;
var	index = 0; 
var leftul1 = document.getElementById('leftUl');
var ull = document.querySelector('#shoujidianhua');



//alert("注意！这只是对小米商城网页模仿的模仿，仅学习用！目前只支持1336*768分辨率显示器！")
// ull.click = function(){
// 	leftul1.style.display = 'none';
// 	console.log("asdfasdf")
// }
function clearActive(){
	for(var i = 0;i < items.length;i ++){
		items[i].className =  'item';
	}
	for(var i = 0;i < points.length;i ++){
		points[i].className =  'point';
	}
}
var goIndex = function(){
	clearActive();
	items[index].className ='item active';
	points[index].className = 'point active';
}
var goPre = function(){
	if(index==0){
		index = 4;
	}
	else{
		index --;	
	}
	goIndex();
	time = 30;
}
var goNext = function(){
	if(index == 4){
		index = 0;
	}
	else{
		index++;
	}
	goIndex();
	time = 30;
	}
	
var point0 = function(){
	index = 0;
	goIndex();
	time = 0;
}
var point1 = function(){
	index = 1;
	goIndex();
	time = 0;
}
var point2 = function(){
	index = 2;
	goIndex();
	time = 0;
}
var point3 = function(){
	index = 3;
	goIndex();
	time = 0;
}
var point4 = function(){
	index = 4;
	goIndex();
	time = 0;
}
setInterval(function(){
	time++;
	if(time == 50){
		goNext();
		time = 30;
	}
}, 100)
