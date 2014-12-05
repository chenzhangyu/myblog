$(document).ready(function(){
	$('#add-box').click(function(){
		$('#op-name').text('增加链接');
		$('#submit-btn').attr('toggle', 'add');
		$('#operation').modal('show');
	});
	$('.edit-friend').click(function(){
		$('#op-name').text('修改信息');
		$('#submit-btn').attr({
			'toggle': 'update',
			'fid': $(this).parent().prev().prev().attr('fid')
		});
		$('#friend-input').val($(this).parent().prev().prev().text());
		$('#link-input').val($(this).parent().prev().attr('href'));
		$('#operation').modal('show');
	});
	$('.del-friend').click(function(){
		var fid = $(this).parent().prev().prev().attr('fid');
		var friend = $(this).parent().prev().prev().text();
		if(window.confirm('确认删除?')){
			$.ajax({
				'url': '/admin/del_friend',
				'type': 'post',
				'datatype': 'json',
				'data': {
					fid: fid
				}
			}).done(function(data){
				if (data.status === true) {
					window.location.href = '';
				}
			}).fail(function(){
				alert('fail to operate');
			});
		}
	});
	$('#submit-btn').click(function(){
		if ($(this).attr('toggle') === 'add') {
			var url = '/admin/add_friend';
			var info = {
				friend: $('#friend-input').val(),
				link: $('#link-input').val()
			};
		}else{
			var url = '/admin/update_friend';
			var info = {
				friend: $('#friend-input').val(),
				link: $('#link-input').val(),
				fid: $(this).attr('fid')
			};
		}
		$.ajax({
			'url': url,
			'type': 'post',
			'context': this,
			'datatype': 'json',
			'data': info
		}).done(function(data){
			if(data.status === true){
				window.location.href = '';
			}else{
				alert('fail to operate!');
			}
		}).fail(function(){
			alert('fail to operate!');
		});
	});
});