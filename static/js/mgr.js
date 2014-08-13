/*
 * 后台管理控制js
 * Author： xingrz, SingleCorner[sinerwr], JasonWu
 * 
*/
$(document).ready(function() {
	$(document).scroll(navbar_ajust);
	navbar_ajust();
  
  $('#Proj_name').focus();
  $('#Proj_add').submit(insProj);
	$('#Asset_add').submit(insAsset);
	$('#Asset_upt').submit(uptAsset);
});

/*
 * 基础控制模块
 * Author: Xingrz
 * 控制页面滚动时仍然可操作导航条
 * 
 */
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
 * 项目控制模块
 * Author: sinerwr
 * 项目控制：添加
 * 
*/
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
/*
 * 项目控制模块
 * Author: sinerwr
 * 项目控制：删除
 * 
*/
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

/*
 * 资产控制模块
 * Author: sinerwr
 * 资产控制：添加
 * 
*/
function insAsset(evt) {
  evt.preventDefault();
	
	pid = $('#Asset_proj').val();
	ip = $('#Asset_ip').val();
	cpu = $('#Asset_cpu').val();
	mem = $('#Asset_mem').val();
	disk = $('#Asset_disk').val();
	type = $('#Asset_type').val();
	srv = $('#Asset_srv').val();
	desc = $('#Asset_desc').val();

	$.ajax({
		type: 'POST',
		url: '/admin/servers/add',
		data: {
			'pid': pid,
			'ip': ip,
			'cpu': cpu,
			'mem': mem,
			'disk': disk,
			'type': type,
			'srv': srv,
			'desc': desc,
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
/*
 * 资产控制模块
 * Author: sinerwr
 * 资产控制：更新
 * 
*/
function uptAsset(evt) {
  evt.preventDefault();
	id = $('#Asset_id').val();;
	pid = $('#Asset_proj').val();
	ip = $('#Asset_ip').val();
	cpu = $('#Asset_cpu').val();
	mem = $('#Asset_mem').val();
	disk = $('#Asset_disk').val();
	type = $('#Asset_type').val();
	srv = $('#Asset_srv').val();
	desc = $('#Asset_desc').val();
	status = $('#Asset_status').val();
	cacti = $('#Asset_cacti').val();
	nagios = $('#Asset_nagios').val();

	url = '/admin/servers/'+ id + '?update';
	//alert(url);
	$.ajax({
		type: 'POST',
		url: url,
		data: {
			'pid': pid,
			'ip': ip,
			'cpu': cpu,
			'mem': mem,
			'disk': disk,
			'type': type,
			'srv': srv,
			'desc': desc,
			'status': status,
			'cacti': cacti,
			'nagios': nagios,
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
/*
 * 资产控制模块
 * Author: sinerwr
 * 资产控制：删除
 * 
*/
function delAsset(id) {
	if (!confirm("操作提示：即将删除所选项目")) {
		return false;
	}
  
	$.ajax({
		type: 'POST',
		url: '/admin/servers/del',
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