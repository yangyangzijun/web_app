$(function(){
	gouwucheIn()
	function gouwucheIn () {
		$(".nav_gouwuche").mouseenter(function () {
			$("#gouwuchebox").slideDown(200);
			$(".nav_whith_right").fadeOut(0);
		});
	}
	gouwucheOut()
	function gouwucheOut () {
		$(".nav_gouwuche").mouseleave(function () {
			$("#gouwuchebox").slideUp(200);
			$(".nav_whith_right").fadeIn(300);
		});
	}
	
	
	
	whiteNavShowBoxIn()
	function whiteNavShowBoxIn () {
		$(".nav_whith_llist").mouseenter(function () {
			$("#whiteNavShowBox").slideDown(200);
		});
	}
	
	whiteNavShowBoxOut()
	function whiteNavShowBoxOut () {
		$(".nav_whith_llist").mouseleave(function () {
			$("#whiteNavShowBox").slideUp(200);
		});
	}
// 	gouwuche()
// 	function gouwuche () {
// 	$(".nav_gouwuche").mouseenter(function () {
// 		$("#gouwuchebox").slideDown(200);
// 	}
})