var lastResults = null;

function getUpdatedResults(cancelling){

	$.ajax({
		url: "/get_results",
		type: "get",
		dataType: "json",
		success: function(data){
			lastResults = data;
			handleResults(data, cancelling);
		},
		error: function(jqXHR){
			if (lastResults != null){
				handleResults(lastResults, true);
			}
			if (updaterId != null){
				clearInterval(updaterId);
			}
			finishLauncher();
		}
	});

}

var updaterId = null;

// Get tests from server and starts tests launcher
function startInspection(){

	domain_url = handleDomainURL();
	if ( domain_url == null ){
		return;
	}
	$("#inspect_button").addClass("active");
	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").text("Stop");
	$("#inspect_button").attr("onclick", "");
	$.ajax({
		url: "/launch/" + domain_url,
		type: "get",
		dataType: "json",
		success: function(data){
			handleStartTestsLauncher(domain_url);
			getUpdatedResults(false);
			updaterId = window.setInterval(function(){
				getUpdatedResults(false);
			}, 5000);
		},
		error: function(jqXHR){
			if ( jqXHR.status == 503 ){
				window.setTimeout(function(){
					startInspection();
				}, 5000);
			}
		}
	});
}

function stopInspection(){

	getUpdatedResults(true);
	$.ajax({
		url: "/stop_launcher",
		type: "get",
		success: function(data){
			if (updaterId != null){
				clearInterval(updaterId);
			}
			finishLauncher();
		},
		error: function(jqXHR){
			if ( jqXHR.status == 503 ){
				window.setTimeout(function(){
					stopInspection();
				}, 5000);
			}
		}
	});
}