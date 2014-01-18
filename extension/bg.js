// Copyright (c) 2010 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// A generic onclick callback function.
function clicked(info, tab) {
  var url = tab.url;
  var name;

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
      var name = response.copied;
      
      console.log(url);
      console.log(name);

      $.post("http://getwhodat.herokuapp.com", {"url":url, "name":name}, function(response){
        console.log(response);
      })

    });
  });

}

var id = chrome.contextMenus.create({"title": "Find email", "contexts":["all"],
                                     "onclick": clicked});
