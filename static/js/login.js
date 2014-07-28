$(document).ready(function() {
	$('#USER_login_form').submit(function(evt) {
		// 阻断默认提交过程
		evt.preventDefault();
		
		// 准备变量
		var user = $('#USER_login_user').val();
		var pswd = $('#USER_login_pswd').val();
		var time = $('#USER_login_timestamp').val();
		
		// 检查输入
		if (user.length != 4) {
			$('#USER_login_status').html("No No No,工号貌似错了>_< ");
			$('#USER_login_user').focus();
			return false;
		}
		
		if (pswd.length == 0) {
			$('#USER_login_status').html("乃不能丢掉密码君");
			$('#USER_login_pswd').focus();
			return false;
		}
		
		$('#USER_login_user').attr('disabled', true);
		$('#USER_login_pswd').attr('disabled', true);
		$('#USER_login_submit').attr('disabled', true);
		$('#USER_login_status').html('用力登录中，请稍等…');
		
		// 加密
		pswd = $.sha1($.sha1(pswd) + time);
		
		$.ajax({
			type: 'POST',
			url: './?a=login',
			data: {
				'username': user,
				'password': pswd,
				'encrypto': 'on'
			},
			timeout: 5000,
			success: function(data, status, xhr) {
				if (data.code == 0) {
					$('#USER_login_status').html('登录成功~！系统准备ing');
					setTimeout(function(){
							window.location = data.referer || './';
						},2000
					);					
				} else {
					$('#USER_login_user').attr('disabled', false);
					$('#USER_login_pswd').attr('disabled', false);
					$('#USER_login_submit').attr('disabled', false);
					if (data.code == -1 || data.code == -2) {
						$('#USER_login_pswd').val('');
						$('#USER_login_pswd').focus();
					}
					$('#USER_login_status').html(data.message);
				}
			},
			error: function(data) {
				$('#USER_login_user').attr('disabled', false);
				$('#USER_login_pswd').attr('disabled', false);
				$('#USER_login_submit').attr('disabled', false);
				$('#USER_login_user').focus();
				$('#USER_login_pswd').val('');
				$('#USER_login_status').html(data.responseText);

			},
			dataType: 'json'
		});
	});

	// 设置焦点
	$('#USER_login_user').focus();
	PressEnter();
});
function PressEnter() { 
var e = jQuery.Event("keypress");//模拟一个键盘事件 
e.keyCode = 122; 
$('body').trigger(e);
} 
