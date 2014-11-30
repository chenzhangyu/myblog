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
				for (x in data.result){
					var label = document.createElement('label');
					var input = document.createElement('input');
					$(input).attr({
						'type': 'checkbox', 
						'name': 'tags', 
						'value': data.result[x].tag,
						'checked': 'checked'
					});
					$(label).addClass('checkbox-inline').append(input).html($(label).html()+data.result[x].tag);
					console.log(label);
					$('#tag-list').append(label);
				}
				$('#addTagModal').modal('hide');
			}else{
				failToCall();
			}
		}).fail(failToCall);
	});
});

function failToCall () {
	if($('#tag-list-input').parent().hasClass('has-error') === false){
		$('#tag-list-input').parent().addClass('has-error');
	}
	$('#msg').text('网络错误或该标签已存在!');
}