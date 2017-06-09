$(function() {
	$('submit').click(function() {
		var text = $('#text').val();
		$.ajax({
			url: '/announcement/',
			    data: $('form').serialize(),
			    type: 'POST',
			    success: function(response) {
			    console.log(response);
			},
			    error: function(error) {
			    console.log(error);
			}
		    });
	    });
    });