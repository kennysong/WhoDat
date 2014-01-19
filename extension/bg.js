function clicked(info, tab) {
  var url = tab.url;
  var name;

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {greeting: "whodatclick"}, function(response) {
      var name = response.copied;
      
      console.log(url);
      console.log(name);

      $.post("http://getwhodat.herokuapp.com", {"url":url, "name":name}, function(response){
        console.log(response);
        var email = response['email'];

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {greeting: "responseemail", 'email': email}, function(response) {
            


          });
        });



      })

    });
  });

}

var id = chrome.contextMenus.create({"title": "WhoDat?", "contexts":["all"],
                                     "onclick": clicked});

