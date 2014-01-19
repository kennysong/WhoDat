$(document).ready(function(){
	$("#whoDat").click(function(){
		$.post( "http://getwhodat.herokuapp.com/", {'name': VARIABLE_HERE, 'link': VARIABLE_HERE}, function( data ) {
  			console.log( "Data Loaded: " + data );
		});
	});
});