function qs(key) {
    key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
    var match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));
    return match && decodeURIComponent(match[1].replace(/\+/g, " "));
}

function set_emoji(){
	$('#emoji').css('top', (-$('#emoji').height()-5)+'px');
}
$(document).ready(function(){
	set_emoji();

	$.ajax({
		url: '/blog/get_content',
		type: 'post',
		dataType: 'json',
		data: {
			pid: qs('pid')
		}
	}).done(function(data){
		if(data.status === true){
			$("#passage-content").html(marked(data.result));
			$('#passage-content pre code').each(function(i, block){
				hljs.highlightBlock(block);
			});
		}
	});
	$('#comment').click(function(){
		var content = $('#comment-input').val();
		if (!content) {
			alert('不能留空( ⊙ o ⊙ )啊！');
			return;
		}
		$.ajax({
			url: '/blog/comment',
			type: 'post',
			dataType: 'json',
			data: {
				pid: qs('pid'),
				comment: content
			}
		}).done(function(data){
			if (data.status === true) {
				window.location.href = '';
			}else{
				alert('请先微博账号登录!');
			}
		});
	});
	$('.reply').click(function(){
		$('#reply-box').text('回复 '+$(this).parent().children().first().text());
		$('#msg').text('');
		if ($(this).parent().attr('mode') === 'talk') {
			$('#reply-dialog').attr({
				'mode': 'talk',
				'cid': $(this).parent().attr('cid'),
				'tid': $(this).parent().attr('tid')
			}).modal('show');
		}else{
			$('#reply-dialog').attr({
				'mode': 'reply',
				'cid': $(this).parent().attr('cid')
			}).modal('show');
		}
	});
	$('.vote-up').click(function(){
		if ($(this).parent().attr('mode') === 'talk') {
			var info = {
				'mode': 'talk',
				'tid': $(this).parent().attr('tid')
			};
		}else{
			var info = {
				'mode': 'reply',
				'cid': $(this).parent().attr('cid')
			};
		}
		$.ajax({
			url: '/blog/vote',
			type: 'post',
			dataType: 'json',
			data: info,
			context: this
		}).done(function(data){
			if (data.status === true) {
				var votes = $(this).find('.votes')
				if (data.result === true) {
					if (votes.length) {
						var s = votes.text();
						votes.text('('+(parseInt(s.slice(1, -1))+1) + ')') ;
					}else{
						var span = document.createElement('span');
						$(span).addClass('votes').text('(1)');
						$(this).append(span);
					}
				}else{
					var s = votes.text().slice(1, -1);
					if (parseInt(s) !== 1) {
						votes.text('('+(parseInt(s)-1) +')');
					}else{
						votes.remove();
					}					
				}
			}else{
				alert('请先微博账号登录!');
			}
		})
	});
	$('.report').click(function(){
		$('#reply-box').text('简单说一下原因,请不要留空');
		if ($(this).parent().attr('mode') === 'talk') {
			$('#reply-dialog').attr({
				'mode': 'report_talk',
				'tid': $(this).parent().attr('tid')
			}).modal('show');
		}else{
			$('#reply-dialog').attr({
				'mode': 'report_reply',
				'cid': $(this).parent().attr('cid')
			}).modal('show');
		}
	});
	$('#submit-btn').click(function(){
		var mode = $('#reply-dialog').attr('mode');
		var content = $('#reply-input').val();
		if(!content) {
			$('#msg').text('不能留空( ⊙ o ⊙ )啊！');
			return;
		}
		if (mode === 'reply') {
			var info = {
				pid: qs('pid'),
				cid: $('#reply-dialog').attr('cid'),
			};
		} else if (mode === 'talk'){
			var info = {
				pid: qs('pid'),
				cid: $('#reply-dialog').attr('cid'),
				tid: $('#reply-dialog').attr('tid'),
			};
		} else if (mode === 'report_reply') {
			var info = {
				mode: mode,
				cid: $('#reply-dialog').attr('cid')
			}
		} else {
			var info = {
				mode: mode,
				tid: $('#reply-dialog').attr('tid')
			}
		};
		info.content = content;
		$.ajax({
			url: '/blog/' + mode,
			type: 'post',
			dataType: 'json',
			data: info
		}).done(function(data){
			if (data.status === true){
				if (data.refresh === true) {
					window.location.href = '';
				} else {
					$('#reply-dialog').modal('hide');
				};
			} else {
				$('#reply-dialog').modal('hide');
				alert('请先微博账号登录!');
			}
		}).fail(function(){
			alert('fail to operate!');
		});
	});

	$('.fa-smile-o').click(function(){
		if ($('#emoji').css('display') === 'none') {
			$('#emoji').css('display', 'inline-block');
		}else{
			$('#emoji').css('display', 'none');
		}
	});

	$('#emoji-list span').click(function(){
		var comment = $('#comment-input');
		var start = comment.prop('selectionStart');
		var end = comment.prop('selectionEnd');
		var content = comment.val();
		comment.val(content.substring(0, start)+$(this).text()+content.substring(end, content.length));
		$('#emoji').css('display', 'none');
		comment.focus();
		var pos = $(this).text().length + start;
		comment[0].setSelectionRange(pos, pos);
	});
});
