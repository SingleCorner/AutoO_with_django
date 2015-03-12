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
  $('#Accnt_add').submit(insAccnt);

  $('#GetServer').click(GetServer);
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
  
	alias_name = $('#Proj_alias').val();
  name = $('#Proj_name').val();
  remark = $('#Proj_remark').val();
	
	$.ajax({
		type: 'POST',
		url: '/admin/project/add',
		data: {
			'alias_name': alias_name,
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
	ip_2 = $('#Asset_ip_2').val();
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
			'ip_2': ip_2,
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
/*
 * 帐号控制模块
 * Author: sinerwr
 * 帐号控制：添加
 * 
*/
function insAccnt(evt) {
  evt.preventDefault();
	
	account = $('#Accnt_id').val();
	name = $('#Accnt_name').val();
	passwd = $('#Accnt_pass').val();
	mgr = $('input[name="Accnt_mgr"]:checked').val();
	project = $('#Accnt_proj').val();
	
	$.ajax({
		type: 'POST',
		url: '/sys/account/add',
		data: {
			'account': account,
			'name': name,
			'passwd': passwd,
			'mgr': mgr,
			'project': project,
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
	})
}

/*
 * 帐号控制模块
 * Author: sinerwr
 * 帐号控制：状态变更
 * 		控制帐号登录，1为可登录，0为不可登录
 * 
*/
function accnt_op(id,ctrl) {	
	if (!confirm("操作提示：冻结/解冻帐号将影响此用户登录")) {
		return false;
	}
	
	$.ajax({
		type: 'POST',
		url: './',
		data: {
			'id': id,
			'ctrl': ctrl,
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

function GetServer(){
	ipaddr = $('#ipaddr').val();
	data_trans = 1;

	$.ajax({
		type: 'POST',
		url: './getinfo',
		data: {
			'ipaddr': ipaddr,
			'data_trans': data_trans,
		},
		success: function(data, status, xhr) {
			$('#Asset_hostname').val(data.host);
			$('#Asset_cpu').val(data.cpu);
			$('#Asset_mem').val(data.mem);
			$('#Asset_ip').val(data.ip);
			$('#Asset_ip').html(data.ip);
		}
	})
}
