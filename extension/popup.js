$(document).ready(function(){
	$("#whoDat").click(function(){
		$.ajax({
		  type: 'POST',
		  url: "http://localhost:5000",
		  data: {
		  			"url" : "http://www.google.com",
		  			"name" : $("#name").val()
		  		},
		  success: function(response) {
		  				alert(response);
		  			},
		  timeout: 1200000
		});
		// $.post(, {"url":"http://www.getwhodat.com/asdf", "name":"Dick Costello"}, function(response){
		// 	// $("#name").val()
		// 	alert("clicked");
  // 			alert( "Data Loaded: " + response);
		// }, timeout : 1200000);
	});
});