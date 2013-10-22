var test_entries = null;
var current_test = null;

var failed_tests = [];

var started_tests = false;

// Get tests from server and starts tests launcher
function startInspection(){

	started_tests = true;

	domain_url = handleDomainURL();
	if ( domain_url == null ){
		return;
	}
	$.ajax({
		url: "/test_names",
		type: "get",
		dataType: "json",
		success: function(data){
			testsLauncher(data, domain_url);
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

// Configures environment and start to run test suite
function testsLauncher(data, domain_url){

	handleStartTestsLauncher(domain_url);
	test_entries = data;
	current_test = 0;
	failed_tests = [];
	handleTestCreation(test_entries[current_test].name, test_entries[current_test].source);
	issueTest(test_entries[current_test].name, domain_url, decideNext, false);
}

var reattempted_issuing_test = false;
// Issues a new test to be run
function issueTest(test_name, domain_url, decide_next, retry){

	$.ajax({
		url: "/perform_test/"+test_name+"/"+domain_url,
		type: "get",
		dataType: "json",
		success: function(data){
			handleTestResponse(data);
			decide_next(domain_url, data, retry);
		},
		error: function(jqXHR) {
			data = {
				'name' : test_name,
				'exit_status' : 2,
				'briefing' : "A problem occurred while launching test " + test_name + ".",
				'message' : "A problem occurred while launching test " + test_name + ". <br/> This does not mean a problem with the actual test."
			};

			if ( jqXHR.status == 503 && !reattempted_issuing_test ){
				data['briefing'] = "Server busy. Could not launch test " + test_name + ". Retrying again in 5 seconds...";
				handleTestResponse(data);
				window.setTimeout(function(){
					handleTestRelaunch(test_name);
					issueTest(test_name, domain_url, decide_next, retry);
					reattempted_issuing_test = true;
				}, 5000);
			}
			else{
				data['message'] = "A problem (" + jqXHR.status + " " + jqXHR.statusText + ") occurred while launching test " + test_name + ".";
				data['message'] += "<br/> Server returned status (" + jqXHR.status + " " + jqXHR.statusText + ").";
				data['message'] += "<br/> Be warned that this does not necessarily mean a problem with the actual test.";
				handleTestResponse(data);
				decide_next(domain_url, data, retry);
				reattempted_issuing_test = false;
			}
		}
	});

}

// Decides what to do once a test finishes running
function decideNext(domain_url, data, retry){

	// If current test has failed and 'continue if fail' is 'false'; then stop launcher
	if ( data.exit_status != 0 && !test_entries[current_test].continue_if_fail ){
		failed_tests.push({ 'test' : test_entries[current_test], 'output' : data });
		finishLauncher();
	}
	else{ //Otherwise, the test has passed or failed but 'continue if fail' is 'true'; then see if should stop launcher of issue a new test
		if ( data.exit_status != 0 ){
			failed_tests.push({ 'test' : test_entries[current_test], 'output' : data });
		}
		current_test++;
		if ( current_test == test_entries.length ){ //If there's no more tests to be issued; stop launcher
			finishLauncher();
		}
		else{ // Otherwise, there's a new test to be issued, do it
			if ( retry ){
				handleTestRelaunch(test_entries[current_test].name);
			}
			else{
				handleTestCreation(test_entries[current_test].name, test_entries[current_test].source);
			}
			issueTest(test_entries[current_test].name, domain_url, decideNext, retry);
		}
	}
}

function runAgain(test_name, domain_url){

	handleTestRelaunch(test_name);
	issueTest(test_name, domain_url, finishRunningTestAgain, true);
}

function retryTests(domain_url){

	
	test_entries = [];
	for ( var i=0; i<failed_tests.length; i++ ){
		test_entries.push(failed_tests[i].test);
	}
	failed_tests = [];
	current_test = 0;
	handleTestRelaunch(test_entries[current_test].name);
	issueTest(test_entries[current_test].name, domain_url, decideNext, true);
}
