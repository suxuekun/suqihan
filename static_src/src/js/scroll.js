(function(_global){

	$(function(){
		_global.onscroll = function(){
			if (document.body.scrollTop > 0){
				$(document.body).addClass("ui-scroll");
			}else{
				$(document.body).removeClass("ui-scroll");
			}
			// if (document.body.scrollTop > 60){
			// 	$(document.body).addClass("ui-scroll-60");
			// }else{
			// 	$(document.body).removeClass("ui-scroll-60");
			// }
		};
	});
})(window);