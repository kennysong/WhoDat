function clicked(info, tab) {
  var url = tab.url;
  var name;

  console.log(url)

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {greeting: "whodatclick"}, function(response) {
      var name = response.copied;
      
      console.log(url);
      console.log(name);
      $.post("http://getwhodat.herokuapp.com/", {"url":url, "name":name}, function(response){
        var emails = response['emails'];
        console.log(response)
        console.log(emails)

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {greeting: "responseemail", 'emails': emails}, function(response) {
            console.log(response);

          });
        });



      })

    });
  });

}

var id = chrome.contextMenus.create({"title": "WhoDat?", "contexts":["all"],
                                     "onclick": clicked});

