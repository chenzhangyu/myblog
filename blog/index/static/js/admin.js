$(document).ready(function(){
	$('.delete').click(function(){
		if (window.confirm('确认删除?')) {
			if ($(this).parent().attr('mode') === 'talk') {
				var info = {
					'mode': 'talk',
					'tid': $(this).parent().attr('tid')
				};
			} else {
				var info = {
					'mode': 'reply',
					'cid': $(this).parent().attr('cid')
				};
			}
			$.ajax({
				url: '/admin/del_comment',
				type: 'post',
				dataType: 'json',
				data: info
			}).done(function(data){
				if (data.status === true) {
					window.location.href = '';
				};
			});	
		};
	});
});