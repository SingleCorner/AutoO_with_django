$(document).ready(function() {
	$(document).scroll(navbar_ajust);
	navbar_ajust();


	$('.rollbackWeb').bind('click',rollbackWeb);

	$('.delWeb').bind('click',delWeb);

	$('#addProjMain').submit(insProjMain);
	$('#addProjSub').submit(insProjSub);
	$('#addProjWeb').submit(insProjWeb);
	$('#Accnt_add').submit(insAccnt);

	//以下函数用于资产管理系统
	$('#asset_query_form').submit(qryAsset);
	$('#asset_add_form').submit(insAsset);
	$('#asset_mod_form').submit(uptAsset);


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
 * 刷新后不改变页面查询数据
 * 设置主项目ID
 */
function setMainID(id) {
	var mid = id;
	$.ajax({
		type: 'POST',
		url: './?module=set&action=mid',
		data: {
			'mid': mid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				window.location = "./";
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}
/*
 * 刷新后不改变页面查询数据
 * 设置子项目ID
 */
function setSubID(id) {
	var sid = id;
	$.ajax({
		type: 'POST',
		url: './?module=set&action=sid',
		data: {
			'sid': sid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				window.location = "./";
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}
/*
 * 项目操作 -- 更新
 */
function updateWeb(id) {
	if (!confirm("操作提示：即将进行更新，更新前确认做好备份")) {
		return false;
	}
	var wid = id;
	$.ajax({
		type: 'POST',
		url: './?module=web&action=update',
		data: {
			'wid': wid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				setTimeout(function(){
						window.location = data.referer || './';
					},1000
				);					
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}
/*
 * 项目操作 -- 备份
 */
function backupWeb(id) {
	if (!confirm("操作提示：备份")) {
		return false;
	}
	var wid = id;
	$.ajax({
		type: 'POST',
		url: './?module=web&action=backup',
		data: {
			'wid': wid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				setTimeout(function(){
						window.location.reload();
					},2000
				);					
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}
/*
 * 项目操作 -- 回滚
 */
function rollbackWeb() {
	if (!confirm("操作提示：即将进行回滚")) {
		return false;
	}
	var e = $(this).parent();
	var wid = e.children('input').val();
	var id = e.children('select').val();
	e.parent().children('td.proj_stat').html('正在执行');
	$.ajax({
		type: 'POST',
		url: './?module=web&action=rollback',
		data: {
			'id': id,
			'wid': wid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				e.parent().children('td.proj_stat').html(data.message);
				alert(data.alertmsg);
				setTimeout(function(){
						window.location.reload();
					},2000
				);					
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}
/*
 * 项目操作 -- 删除备份
 */
function delWeb(id) {
	if (!confirm("操作提示：即将删除备份")) {
		return false;
	}
	var e = $(this).parent();
	var wid = e.children('input').val();
	var id = e.children('select').val();
	e.parent().children('td.proj_stat').html('正在执行');
	$.ajax({
		type: 'POST',
		url: './?module=web&action=delbak',
		data: {
			'id': id,
			'wid': wid
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				e.parent().children('td.proj_stat').html(data.message);
				setTimeout(function(){
						window.location = data.referer || './';
					},2000
				);					
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}


/*
 * 以下函数仅供管理调用
 *
 * 管理页面带有权限控制，好奇宝宝可以尝试使用以下函数进行调用
 */



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
/*
 * 管理操作 -- 添加账号
 *
 */
function insAccnt(evt) {
	evt.preventDefault();
	var no = $('#Accnt_id').val();
	var name = $('#Accnt_name').val();
	var passwd = $('#Accnt_pass').val();
	var module = $('#Accnt_proj').val();
	var manage = $('#Accnt_add').children('input[name="Accnt_mgr"]:checked').val();
	
	$.ajax({
		type: 'POST',
		url: './admin.php?module=account&action=add',
		data: {
			'no': no,
			'name': name,
			'passwd': passwd,
			'module': module,
			'manage': manage
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
/*
 * 管理操作 -- 增加主项目
 *
 */
function insProjMain(evt) {
	evt.preventDefault();
	var name = $('#ProjMain_name').val();
	var alias = $('#ProjMain_alias').val();

	$.ajax({
		type: 'POST',
		url: './admin.php?module=proj&action=addMain',
		data: {
			'name': name,
			'alias': alias
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
/*
 * 管理操作 -- 删除主项目
 *
 */
function delProjMain(id) {
	if (!confirm("操作提示：删除主项目将删除关联子项目")) {
		return false;
	}
	$.ajax({
		type: 'POST',
		url: './admin.php?module=proj&action=delMain',
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


/*
 * 管理操作 -- 增加子项目
 *
 */
function insProjSub(evt) {
	evt.preventDefault();
	var name = $('#ProjSub_name').val();
	var mid = $('#ProjSub_mid').val();

	$.ajax({
		type: 'POST',
		url: './admin.php?module=proj&action=addSub',
		data: {
			'name': name,
			'mid': mid
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
/*
 * 管理操作 -- 删除子项目
 *
 */
function delProjSub(id) {
	if (!confirm("操作提示：删除子项目前请确定项目内无网站")) {
		return false;
	}
	$.ajax({
		type: 'POST',
		url: './admin.php?module=proj&action=delSub',
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
/*
 * 管理操作 -- 增加网站
 *
 */
function insProjWeb(evt) {
	evt.preventDefault();
	var sid = $('#ProjWeb_sid').val();
	var name = $('#ProjWeb_name').val();
	var addr = $('#ProjWeb_addr').val();
	var uld = $('#ProjWeb_uld').val();
	var bak = $('#ProjWeb_bak').val();
	var rls = $('#ProjWeb_rls').val();

	$.ajax({
		type: 'POST',
		url: './admin.php?module=web&action=add',
		data: {
			'sid': sid,
			'name': name,
			'addr': addr,
			'uld': uld,
			'bak': bak,
			'rls': rls
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
/*
 * 管理操作 -- 删除网站
 *
 */
function delProjWeb(id) {
	if (!confirm("操作提示：确认删除网站！")) {
		return false;
	}
	$.ajax({
		type: 'POST',
		url: './admin.php?module=web&action=del',
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







//以下函数用于资产管理系统
function qryAsset(evt) {
	evt.preventDefault();
	var pid = $('#proj_id').val();
	var addr = $('#proj_ip').val();
	var stat = $('#proj_stat').val();

	$.ajax({
		type: 'POST',
		url: '?module=asset&action=trans',
		data: {
			'pid': pid,
			'addr': addr,
			'stat': stat
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				window.location.href = data.message;
			} else if (data.code == 0) {
				alert(data.message);
			}
		},
		dataType: 'json'
	});
}

function delAsset(id) {
	if (!confirm("操作提示：确认删除")) {
		return false;
	}
	$.ajax({
		type: 'POST',
		url: 'admin.php?module=asset&action=del',
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

function insAsset(evt) {
	evt.preventDefault();

	var pid = $('#asset_add_pid').val();
	var ip = $('#asset_add_ip').val();
	var cpu = $('#asset_add_cpu').val();
	var ram = $('#asset_add_ram').val();
	var disk = $('#asset_add_disk').val();
	var desc = $('#asset_add_desc').val();
	var stat = $('input[name="asset_add_stat"]:checked').val();
	var catci =  $('input[name="asset_add_mon1"]:checked').val();
	var nagios =  $('input[name="asset_add_mon2"]:checked').val();

	$.ajax({
		type: 'POST',
		url: 'admin.php?module=asset&action=add',
		data: {
			'pid': pid,
			'ip': ip,
			'cpu': cpu,
			'ram': ram,
			'disk': disk,
			'desc': desc,
			'stat': stat,
			'cacti': catci,
			'nagios': nagios
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

function uptAsset(evt) {
	evt.preventDefault();

	var id = $('#asset_mod_id').val();
	var ip = $('#asset_mod_ip').val();
	var cpu = $('#asset_mod_cpu').val();
	var ram = $('#asset_mod_ram').val();
	var disk = $('#asset_mod_disk').val();
	var desc = $('#asset_mod_desc').val();
	var stat = $('input[name="asset_mod_stat"]:checked').val();
	var catci =  $('input[name="asset_mod_mon1"]:checked').val();
	var nagios =  $('input[name="asset_mod_mon2"]:checked').val();

	$.ajax({
		type: 'POST',
		url: 'admin.php?module=asset&action=modify',
		data: {
			'id': id,
			'ip': ip,
			'cpu': cpu,
			'ram': ram,
			'disk': disk,
			'desc': desc,
			'stat': stat,
			'cacti': catci,
			'nagios': nagios
		},
		success: function(data, status, xhr) {
			if (data.code == 1) {
				alert(data.message);
				history.go(-1);
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