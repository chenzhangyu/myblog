$(document).ready(function(){
	$('#tag-submit').click(function(){
		$.ajax({
			url: '/admin/add_tag',
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'tagList': $('#tag-list-input').val().split(',')})
		}).done(function(data){
			if(data.status === true){
				console.log(data.result);
				$('#addTagModal').modal('hide');
			}else{
				failToCall();
			}
		}).fail(failToCall);
	});
	$('.glyphicon-trash').click(function(){
		var tag_name = 'asdf';
		$.ajax({
			url: '/admin/del_tag',
			dataType: 'json',
			type: 'post',
			data: {
				tag: tag_name
			}
		}).done(function(data){
			console.log(data.status);
		}).fail(function(){
			alert('fail to operate');
		})
	})
});

function failToCall() {
	if($('#tag-list-input').parent().hasClass('has-error') === false){
		$('#tag-list-input').parent().addClass('has-error');
	}
}

function test () {
	$.ajax({
		url: '/admin/add_tag',
		dataType: 'json',
		type: 'POST',
		contentType: 'application/json;charset=UTF-8',
		data: JSON.stringify({'tagList': $('#tag-list-input').val().split(',')}),
		success: function(data){
			console.log(data.result);
		}
	});
}