var test_entries = null;
var current_test = null;

// Get tests from server and starts tests launcher
function startInspection(){
	
	domain_url = handleDomainURL();
	$.get("/test_names", function(data){
		testsLauncher(data, domain_url);
	});
}

// Configures environment and start to run test suite
function testsLauncher(data, domain_url){

	handleStartTestsLauncher();
	data = JSON.parse(data);
	test_entries = data;
	current_test = 0;
	issueTest(test_entries[current_test].name, domain_url, decideNext);
}

// Issues a new test to be run
function issueTest(test_name, domain_url, decide_next){

	handleTestCreation(test_name);
	$.get("/perform_test/"+test_name+"/"+domain_url, function(data){
		handleTestResponse(data);
		decideNext(domain_url, data);
	});
}

// Decides what to do once a test finishes running
function decideNext(domain_url, data){

	data = JSON.parse(data);
	// If current test has failed and continue if fail is 'false':
	if ( data.exit_status != 0 && !test_entries[current_test].continue_if_fail ){
		abortLauncher(data.name);
	}
	else{ //Otherwise, the test has passed or failed but continue if fail is 'true':
		current_test++;
		if ( current_test == test_entries.length ){ //If there's no more tests to be issued
			finishLauncher();
		}
		else{ // Otherwise, there's a new test to be issued, do it.
			issueTest(test_entries[current_test].name, domain_url, decideNext);
		}
	}
}

// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(){

	$("#tests_output_table").html("");
}

// What to do in the page when a new test was issued just now
function handleTestCreation(test_name){

	$("#tests_output_table").append("<tr id='tr_"+test_name+"'><td>"+test_name+"</td><td id='td_"+test_name+"'></td></tr>");
}

// What to do in the page once a test finishes running
function handleTestResponse(data){

	data = JSON.parse(data);
	$("#tr_"+data.name).attr("class", getExitStatusClass(data.exit_status));
	$("#td_"+data.name).text(data.output);
}

function handleDomainURL(){

	domain_url = $("#domain_url_box").val();
	if ( domain_url.search("://") != -1 ){
		domain_url = domain_url.substr(domain_url.search("://")+3, domain_url.length);
		$("#domain_url_box").val(domain_url);
	}
	return domain_url;
}

function getExitStatusClass(code){

	switch(code){
		case 0:
			return "success";
		case 1:
			return "error";
		default:
			return "warning";
	}
}

function abortLauncher(testName){
	window.alert("Test "+testName+" failed. Aborting...");
}

function finishLauncher(){
	window.alert("You've executed all tests...");
}
