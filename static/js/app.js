$(document).ready(function() {
	$(document).scroll(navbar_ajust);
	navbar_ajust();

	//以下函数用于资产管理系统
	$('#asset_query_form').submit(qryAsset);
	$('#asset_add').hide();
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

/*
 * 管理操作 -- 冻结账号
 *
 */
function frzAccount(id) {	
	if (!confirm("操作提示：冻结账号后将不可登录")) {
		return false;
	}
	$.ajax({
		type: 'POST',
		url: './admin.php?module=account&action=frz',
		data: {
			'id': id
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				window.location.reload();
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}

function load_newAsset() {
	if ($('#asset_add').is(':hidden')) {
		$('#asset_add').show();
	} else {
		$('#asset_add').hide();
	}
}