$(document).ready(function(){
	$('#add-tag-btn').click(function(){
		$('#tag-list-input').parent().removeClass('has-error');
		$('#msg').text('');
		$('#addTagModal').modal('show');
	});
	// $('.glyphicon-fullscreen').click(function(){
	// 	var editor = document.createElement('textarea');
	// 	$(editor).attr('rows', 10);
	// 	$('#body-container').fadeOut(500);
	// 	$('body').append(editor);

	// });
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
	// $('#submit-passage').click(function(){
	// 	var title = $('#title').val();
	// 	var description = $('#description').val();
	// 	var tags = [];
	// 	$("input[type='checkbox']").each(function(i){
	// 		if ($(this).is(':checked')) {
	// 			tags.push($(this).val());
	// 		};
	// 	});
	// 	var content = $('#content').val();
	// 	var info = {
	// 		'title': title,
	// 		'description': description,
	// 		'tags': tags,
	// 		'content': marked(content)
	// 	};
	// 	if ($('#pid').length) {
	// 		info['pid'] = $('pid').val();
	// 	};
	// 	console.log(info);
	// 	for(key in info){
	// 		if (!info[key].length) {
	// 			alert('some info is null!');
	// 			return;
	// 		};
	// 	};
	// 	$.ajax({
	// 		url: $('#form').attr('url'),
	// 		type: 'post',
	// 		dataType: 'json',
	// 		data: info
	// 	}).done(function(data){
	// 		if (data.status === true) {
	// 			// window.location.href = '/admin/home';
	// 		}else{
	// 			alert('fail to operate!')
	// 		}
	// 	})

	// });
	$('#preview').click(function(){
		$('#preview-dialog').modal('show');
		$("#preview-content").html(marked($('#content').val()));
		$('#preview-content pre code').each(function(i, block){
			hljs.highlightBlock(block);
		});
	})
});

function failToCall () {
	if($('#tag-list-input').parent().hasClass('has-error') === false){
		$('#tag-list-input').parent().addClass('has-error');
	}
	$('#msg').text('网络错误或该标签已存在!');
}