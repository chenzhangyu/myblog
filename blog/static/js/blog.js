$(document).ready(function(){
    $('.replyComment').click(function(){
        $('#reply-form').attr('action', $(this).next().attr('value'))
    });
})

