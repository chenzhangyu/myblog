$(document).ready(function(){
    replace();
    $('.replyComment').click(function(){
        $('#reply-form').attr('action', $(this).next().attr('value'))
    });
})

function replace()
{
    var x;
    a = document.getElementsByClassName('replies')
    for(x in a)
    {
        if(a[x].innerHTML == 'delete')
        {
            a[x].innerHTML = '被和谐'
            a[x].style.color = 'gray'
        }
    }
}