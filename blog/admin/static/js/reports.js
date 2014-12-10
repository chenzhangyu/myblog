$(document).ready(function(){
	$('.glyphicon-trash').click(function(){
		var mode = $(this).prev().attr('mode');
		if(mode === 'reply'){
			var info = {
				'mode': mode,
				'cid': $(this).prev().val()
			}
		} else if (mode === 'talk') {
			var info = {
				'mode': mode,
				'tid': $(this).prev().val()
			}
		} else {
			return;
		};
		console.log(info);
		$.ajax({
			url: '/admin/ignore_report',
			type: 'post',
			dataType: 'json',
			context: this,
			data: info
		}).done(function(data){
			$(this).parent().parent().fadeOut(1000);
		}).fail(function(){
			alert('fail to operate');
		})
	});
});