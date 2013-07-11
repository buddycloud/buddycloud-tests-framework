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
	$.get("/test_names", function(data){
		testsLauncher(data, domain_url);
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

// Issues a new test to be run
function issueTest(test_name, domain_url, decide_next, retry){

	$.ajax({
		url: "/perform_test/"+test_name+"/"+domain_url,
		type: "get",
		dataType: "json",
		success: function(data){
			handleTestResponse(data, domain_url);
			decide_next(domain_url, data, retry);
		},
		error: function(jqXHR) {
			data = {
				'name' : test_name,
				'exit_status' : 2,
				'briefing' : "A problem occurred while launching test " + test_name + ".",
				'message' : "A problem occurred while launching test " + test_name + ". <br/> This does not mean a problem with the actual test."
			};

			if ( jqXHR.status == 503 ){
				data['briefing'] = "Our server was busy and could not launch test " + test_name + " at the time. Retrying again in 5 seconds...";
				handleTestResponse(data, domain_url);
				window.setTimeout(function(){
					handleTestRelaunch(test_name);
					issueTest(test_name, domain_url, decide_next, retry);
				}, 5000);
			}
			else{
				data['message'] = "A problem occurred while launching test " + test_name + ".";
				data['message'] += "<br/> Server returned status (" + jqXHR.status + ").";
				data['message'] += "<br/> Be warned that this does not necessarily mean a problem with the actual test.";
				handleTestResponse(data, domain_url);
				decide_next(domain_url, data, retry);
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

function runAgain(test_name, domain_url, previous_status){


	handleTestRelaunch(test_name, previous_status);
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
