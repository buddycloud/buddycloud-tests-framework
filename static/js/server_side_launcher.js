function handleResults(data, cancelling){
	for ( index in data.tests ){
		if (!cancelling){
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
		else{
			if ( data.tests[index].test_run_status == 2 ){
				handleTestResponse(data.tests[index].result);
			}
			else{
				$("#td_"+data.tests[index].name).attr("class", "btn test_name btn-warning");
				$("#ts_"+data.tests[index].name).attr("class", "btn test_source btn-warning");
				$("#to_"+data.tests[index].name).attr("class", "test_output input uneditable-input warning");
				$("#to_"+data.tests[index].name).html("This test was cancelled.");
				$("#ti_"+data.tests[index].name).attr("class", "icon-warning-sign icon-white");
			}
		}
	}
	if ( data.run_status == 2){
		if (updaterId != null){
			clearInterval(updaterId);
		}
		finishLauncher();
	}
}

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
	$("#inspect_button").addClass("disabled");
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
