chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

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
});

$(document).ready(function(){
	$("body").tooltip();
	$("body").popover();
});
