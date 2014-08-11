$(document).ready(function() {
	$(document).scroll(navbar_ajust);
	navbar_ajust();
  
  $('#Proj_name').focus();
  $('#Proj_add').submit(insProj);
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

function insProj(evt) {
  evt.preventDefault();
  
  name = $('#Proj_name').val();
  remark = $('#Proj_remark').val();

	$.ajax({
		type: 'POST',
		url: '/admin/project/add',
		data: {
			'name': name,
			'remark': remark
		},
    timeout: 5000,
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				window.location.reload();
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
    error: function(data) {
      alert('操作超时');
    },
		dataType: 'json'
	});
}

function delProj(id) {
	if (!confirm("操作提示：即将删除所选项目")) {
		return false;
	}
  
	$.ajax({
		type: 'POST',
		url: '/admin/project/del',
		data: {
			'id': id,
		},
    timeout: 5000,
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				window.location.reload();
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
    error: function(data) {
      alert('操作超时');
    },
		dataType: 'json'
	});
}