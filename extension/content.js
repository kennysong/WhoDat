chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    if (request.greeting == 'whodatclick') {
        var name = window.getSelection().toString();

        if (name.split(/\s+/).length > 3) {
            console.log('Too long!')
        } else {
            var selection = window.getSelection().getRangeAt(0);
            var selectedText = selection.extractContents();

            var span = document.createElement("span");
            span.style.backgroundColor = "yellow";
            span.appendChild(selectedText);
            selection.insertNode(span);
            console.log($(span));
            $(span).popover({"content": "Finding email...", "placement":"top"})
            $(span).popover('show');

            sendResponse({"copied": window.getSelection().toString()});       
        }

    } else {
        var email = request.email;
        $('.popover-content').html('<form role="form"><div class="input-group input-group-sm"><span class="input-group-addon">To:</span><input class="form-control" style="width: 210px;" value="'+email+'"></div><div class="input-group input-group-sm" style="margin-top:3px;"><span class="input-group-addon">From:</span><input class="form-control" style="width: 196px;" placeholder="Your email"></div><div class="input-group input-group-sm" style="margin-top:3px;"><textarea class="form-control" style="width: 248px;height: 180px;" placeholder="Write email..."></textarea></div><button type="button" style="width: 250px;margin-top: 5px;" class="btn btn-success">Send!</button></form>');
        $('.popover-content').css({'width':'400px', 'height':'300px'});
        var top = parseInt($('.popover, .fade, .top, .in')[0].style.top);
        var left = parseInt($('.popover, .fade, .top, .in')[0].style.left);

        top -= 270;
        left -= 75;


        $('.popover').css({'top':String(top)+'px', 'left':String(left)+'px'});


    }
});



$(document).ready(function(){
	$("body").tooltip();
	$("body").popover();
});
