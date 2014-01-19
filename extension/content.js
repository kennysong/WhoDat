chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    if (request.greeting == 'whodatclick') {
        console.log('whodatclick')
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


            console.log(name)

            sendResponse({"copied": name});       

            console.log(name)
        }

    } else {
        console.log('else');
        // emails = request.emails;
        // html = '<form role="form"><h4>Potential Emails</h4>';

        // for (var i=0; i<emails.length; i++) {
        //     html += '<a href="#" class="email">%s</a>'%emails[i];
        // }
        // html += "</form>";

        // $('.popover-content').html(html);


        var emails = request.emails;
        console.log(emails)
        var email;

        if (emails.length == 0) {
            email = 'test@gmail.com';
        } else {
            email = emails[0]
        }

        $('.popover-content').html('<form role="form"><div class="input-group input-group-sm"><span class="input-group-addon">To: </span><input class="form-control" style="width: 210px;border-radius: 3px;border-color: gray;border: 1px gray solid;" id="to" value="'+email+'"></div><div class="input-group input-group-sm" style="margin-top:3px;border-radius: 3px;border-color: gray;"><span class="input-group-addon">From: </span><input class="form-control" id="from" style="width: 196px;border-radius: 3px;border-color: gray;border: 1px gray solid;" placeholder="Your email"></div><div class="input-group input-group-sm" style="margin-top:3px;"><textarea class="form-control" style="width: 248px;height: 180px;border-radius: 3px;border-color: gray;" id="message" placeholder="Write email..."></textarea></div><button type="button" style="width: 250px;margin-top: 5px;width: 250px;margin-top: 5px;background: #2ecc71;border-color: green;border-bottom-color: green;border-top-color: green;margin: 0;border-radius: 3px;box-shadow: none;border: none;color: white;padding: 10px;" class="btn btn-success" id="send_btn">Send!</button></form>');
        
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

$(document).on('click', '#send_btn', function(e){ 
    e.preventDefault();
    var to = $('#to').val();
    var from = $('#from').val();
    var message = $('#message').val();
    $.post('http://getwhodat.herokuapp.com/sendgrid', {'to':to, 'from':from, 'message':message}, function(data){
        console.log(data);
    })
});

$(document).on('click', '.emails', function(e){ 
    e.preventDefault();
    $(this);

});
