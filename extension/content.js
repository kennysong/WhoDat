chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
      sendResponse({"copied": window.getSelection().toString()});
});
