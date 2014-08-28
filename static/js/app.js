$(document).ready(function() {
	$(document).scroll(navbar_ajust);
	navbar_ajust();

});


function navbar_ajust() {
	if ($(document).scrollTop() > 60) {
		if (!$('body').hasClass('scroll')){
			$('body').addClass('scroll');
		}
	} else {
		$('body').removeClass('scroll');
	}
}