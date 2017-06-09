var complete = function( e ) {
    console.log("clicked");
    var obj_id = this.id;
    var description = $("label[for=" + this.id + "]");
    var input = { text : description.html() };
    $.ajax({
	url: '/todocomplete/',
	type: 'POST',
	data: JSON.stringify(input),
	contentType: 'application/json; charset=utf-8',
	success: function( d ) {
	    console.log(JSON.parse(d));
            $("#" + obj_id).parent().remove();
	    // description.remove();
	}
    });
}

var add = function( e ) {
    if ($.trim($('#task').html) !== "") {
	num_todos++;

	var input = {  text : $('#task').val() };
	$.ajax({
	    url: '/todoadd/',
	    type: 'POST',
	    data: JSON.stringify(input),
	    contentType: 'application/json; charset=utf-8',
	    success: function( d ) {
		console.log(JSON.parse(d))
		if (JSON.parse(d)["created"] == true) {
		    var input = document.createElement("input");
		    input.type = "checkbox";
		    input.id = num_todos.toString();
		    input.addEventListener('click', complete);

		    var li = document.createElement("li");
		    li.style= "list-style-type: none";
		    var label = document.createElement("label");
		    label.htmlFor = num_todos.toString();
		    label.innerHTML = JSON.parse(d)["text"];

		    li.appendChild(input);
		    li.appendChild(label);

		    $('.todos').append(li);
		} else {
		    alert("Todo already created!");
		}
	    }
	});
    }
};

var num_todos = 0;
var buttons = document.getElementsByClassName('initial_todos');
for (var i=0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', complete);
    num_todos++;
};


document.getElementById('add').addEventListener('click', add);
