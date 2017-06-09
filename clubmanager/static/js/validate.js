var longerDes = function(){
    newDes = document.getElementById("description"); 
    msg = document.getElementById("secret");
    newDes.blur(function(){
	$.ajax({
		url: "length.txt",
		success: function(d){
		    $("#div1").html(result);
		    msg.innerHTML = 'Description too short'
		    // d = JSON.parse(d);
		    //if (d["type"] == "teacher"){
		    //	$("#" + id).remove();
		    //	makeCalendar(getMonth[0],getMonth[1]);
		    //};
		    //} 
	    })
    };
    
}

