$(document).ready(function(){
	$('.op').on('click', '.glyphicon-play', function(){
		$.ajax({
			url: '/admin/display_passage',
			dataType: 'json',
			type: 'post',
			context: this,
			data: {
				pid: $(this).parent().children().first().val()
			}
		}).done(function(data){
			if (data.status === true) {
				var span = document.createElement('span');
				$(span).addClass('glyphicon glyphicon-stop pointer').attr({
					'title': '暂停'
				});
				$(this).prev().after(span);
				$(this).remove();
			}
		});
	});
	$('.op').on('click', '.glyphicon-stop', function(){
		$.ajax({
			url: '/admin/rollback_passage',
			dataType: 'json',
			type: 'post',
			context: this,
			data: {
				pid: $(this).parent().children().first().val()
			}
		}).done(function(data){
			if (data.status === true) {
				var span = document.createElement('span');
				$(span).addClass('glyphicon glyphicon-play pointer').attr({
					'title': '展示'
				});
				$(this).prev().after(span);
				$(this).remove();
			}
		});
	});
	$('.glyphicon-edit').click(function(){
		window.location.href = '/admin/edit?pid=' + $(this).parent().children().first().val();
	});
	$('.glyphicon-trash').click(function(){
		$.ajax({
			url: '/admin/del_passage',
			dataType: 'json',
			type: 'post',
			context: this,
			data: {
				pid: $(this).parent().children().first().val()
			}
		}).done(function(data){
			if (data.status === true){
				$(this).parent().parent().remove();
			}
		});
	});
	$('.glyphicon-share-alt').click(function(){
		$.ajax({
			url: '/admin/recycle_passage',
			dataType: 'json',
			type: 'post',
			context: this,
			data: {
				pid: $(this).parent().children().first().val()
			}
		}).done(function(data){
			if (data.status === true){
				$(this).parent().parent().remove();
			}
		});
	});
});