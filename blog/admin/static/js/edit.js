$(document).ready(function(){
	$('#tag-submit').click(function(){
		var userInput = $('#tag-list-input').val().split(',');
		$.ajax({
			url: "{{url_for('.add_tag')}}",
			method: "post",
			dataType: "json",
			data: {
				tagList: userInput,
				from: 'editor'
			}
		}).done(function(data){
			if(data.status === true){
				console.log(data.result);
				$('#myModal').modal('hide');
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
}