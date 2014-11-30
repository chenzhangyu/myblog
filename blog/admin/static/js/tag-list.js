$(document).ready(function(){
	$('#add-tag-btn').click(function(){
		$('#tag-list-input').parent().removeClass('has-error');
		$('#msg').text('');
		$('#addTagModal').modal('show');
	});
	$('#tag-submit').click(function(){
		$.ajax({
			url: '/admin/add_tag',
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'tagList': $('#tag-list-input').val().split(',')})
		}).done(function(data){
			if(data.status === true){
				location.reload();
			}else{
				failToCall();
			}
		}).fail(failToCall);
	});
	$('.glyphicon-trash').click(function(){
		var tag_name = $(this).parent().prev().children().first().text();
		console.log(tag_name);
		$.ajax({
			context: this,
			url: '/admin/del_tag',
			dataType: 'json',
			type: 'post',
			data: {
				tag: tag_name
			}
		}).done(function(data){
			$(this).parent().parent().css('display', 'none');
			// $(this).parent().parent().parent().remove($(this).parent().parent());
		}).fail(function(){
			alert('fail to operate');
		});
	});
	$('.glyphicon-edit').click(function(){
		var origin = $(this).parent().prev().children().first().text();
		$('#tag-input').val(origin);
		$('#updateTagModal').modal('show');
		$('#tag-update-submit').click(function(){
			$.ajax({
				url: '/admin/update_tag',
				dataType: 'json',
				type: 'post',
				data: {
					origin: origin,
					newTag: $('#tag-input').val()
				}
			}).done(function(data){
				if (data.status) {
					location.reload();
				}else{
					alert('( ⊙ o ⊙ ),标签名和已有的冲突啦!');
				}
			}).fail(function(){
				alert('fail to update');
			});
		});
	});
});

function failToCall () {
	if($('#tag-list-input').parent().hasClass('has-error') === false){
		$('#tag-list-input').parent().addClass('has-error');
	}
	$('#msg').text('网络错误或该标签已存在!');
}