function handleResults(data){
	for ( index in data.tests ){
		if ( $("#td_"+data.tests[index].name).length == 0 ){
			handleTestCreation(data.tests[index].name, data.tests[index].source);
		}
		if ( data.tests[index].test_run_status == 0 ){
			$("#to_"+data.tests[index].name).html("About to run this test. Please wait.");
		}
		else if ( data.tests[index].test_run_status == 1 ){
			$("#to_"+data.tests[index].name).html("Running this test...");
		}
		else if ( data.tests[index].test_run_status == 2 ){
			handleTestResponse(data.tests[index].result);
		}
	}
	if ( data.run_status == 2){
		clearInterval(updaterId);
		finishLauncher();
	}
}

function getUpdatedResults(){

	$.ajax({
		url: "/get_results",
		type: "get",
		dataType: "json",
		success: function(data){
			handleResults(data);
		},
		error: function(jqXHR){
			//window.alert("problem retrieving results: "+jqXHR);
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
	$.ajax({
		url: "/launch/" + domain_url,
		type: "get",
		dataType: "json",
		success: function(data){
			handleStartTestsLauncher(domain_url);
			getUpdatedResults();
			updaterId = window.setInterval(function(){
				getUpdatedResults();
			}, 800);
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
