var test_entries = null;
var current_test = null;

var failed_tests = [];

// Get tests from server and starts tests launcher
function startInspection(){

	domain_url = handleDomainURL();
	if ( domain_url == null ){
		return;
	}
	var msg = ("Inspecting domain '"+domain_url+"'...").split("");
	updateDisplay(msg, "info");
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
	failed_tests = [];
	handleTestCreation(test_entries[current_test].name);
	issueTest(test_entries[current_test].name, domain_url, decideNext, false);
}

// Issues a new test to be run
function issueTest(test_name, domain_url, decide_next, retry){

	$.get("/perform_test/"+test_name+"/"+domain_url, function(data){
		handleTestResponse(data, domain_url);
		decide_next(domain_url, data, retry);
	});
}

// Decides what to do once a test finishes running
function decideNext(domain_url, data, retry){

	data = JSON.parse(data);
	// If current test has failed and continue if fail is 'false':
	if ( data.exit_status != 0 && !test_entries[current_test].continue_if_fail ){
		failed_tests.push(test_entries[current_test]);
		finishLauncher();
	}
	else{ //Otherwise, the test has passed or failed but continue if fail is 'true'
		if ( data.exit_status == 1 ){
			failed_tests.push(test_entries[current_test]);
		}
		current_test++;
		if ( current_test == test_entries.length ){ //If there's no more tests to be issued
			finishLauncher();
		}
		else{ // Otherwise, there's a new test to be issued, do it.
			if ( retry ){
				handleTestRelaunch(test_entries[current_test].name, "danger"); //TODO: take this hardcoded thing out, sometimes can be 'warning' instead of 'danger'
			}
			else{
				handleTestCreation(test_entries[current_test].name);
			}
			issueTest(test_entries[current_test].name, domain_url, decideNext, retry);
		}
	}
}

function runAgain(test_name, domain_url, previous_status){

	var msg = ("Running test '"+test_name+"' again...").split("");
	updateDisplay(msg, "info");

	handleTestRelaunch(test_name, previous_status);
	issueTest(test_name, domain_url, finishRunningTestAgain, true);
}

function retryTests(domain_url){

	var msg = ("Retrying tests that failed for domain '"+domain_url+"'...").split("");
	updateDisplay(msg, "info");
	
	test_entries = [];
	for ( var i=0; i<failed_tests.length; i++ ){
		test_entries.push(failed_tests[i]);
	}
	failed_tests = [];
	current_test = 0;
	handleTestRelaunch(test_entries[current_test].name, "danger"); //TODO: take this hardcoded thing out, sometimes can be 'warning' instead of 'danger'
	issueTest(test_entries[current_test].name, domain_url, decideNext, true);
}

// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(){

	$("#tests_output_table").html("");
}

// What to do in the page when a new test was issued just now
function handleTestCreation(test_name){

	$("#tests_output_table").append("<div class='input-prepend' style='width:100%;'><button id='td_"+test_name+"' class='btn disabled' style='width:25%; padding-left:5px; text-align:left;'><i id='ti_"+test_name+"' class='icon-random'></i> <span class='text-left'>"+test_name+"</span> </button><span id='to_"+test_name+"' class='test_output input uneditable-input' style='width:73%;'><small></small></span></div>");
}

function handleTestRelaunch(test_name, previous_status){

	$("#td_"+test_name).removeClass("btn-"+previous_status);
	$("#td_"+test_name).addClass("disabled");
	$("#td_"+test_name).tooltip("destroy");
	$("#td_"+test_name).attr("onclick", "");
	$("#to_"+test_name).removeClass(previous_status);
	$("#to_"+test_name).html("");
	$("#ti_"+test_name).attr("class", "icon-random");
}

// What to do in the page once a test finishes running
function handleTestResponse(data, domain_url){

	data = JSON.parse(data);
	$("#td_"+data.name).addClass("btn-"+getExitStatusClass(data.exit_status));
	if ( data.exit_status == 1 ){
		$("#td_"+data.name).attr("data-toggle","tooltip");
		$("#td_"+data.name).attr("title","Click to run again");
		$("#td_"+data.name).tooltip({'animation' : true, 'delay' : 100});
		$("#td_"+data.name).removeClass("disabled");
		$("#td_"+data.name).attr("onclick", "runAgain('"+data.name+"', '"+domain_url+"', '"+getExitStatusClass(data.exit_status)+"');");
	}
	$("#to_"+data.name).addClass(getExitStatusClass(data.exit_status));
	$("#to_"+data.name).html("<small>"+data.output+"</small>");
	$("#ti_"+data.name).attr("class", getExitStatusIcon(data.exit_status) + " icon-white");
}

function handleDomainURL(){

	$("#inspect_button").tooltip("destroy");
	domain_url = $("#domain_url_box").val();

	var valid = true;

	if ( domain_url == null || domain_url.trim() == "" || domain_url.charAt(0) == '/' ){
		valid = false;
	}
	else if ( domain_url.charAt(0) == '-' || domain_url.charAt(domain_url.length-1) == '-' ){
		valid = false;
	}
	else if ( domain_url.indexOf("!") != -1 || domain_url.indexOf("@") != -1 || domain_url.indexOf("#") != -1 ){
		valid = false;
	}
	else if ( domain_url.indexOf("$") != -1 || domain_url.indexOf("%") != -1 || domain_url.indexOf("^") != -1 ){
		valid = false;
	}
	else if ( domain_url.indexOf("&") != -1 || domain_url.indexOf("*") != -1 || domain_url.indexOf(" ") != -1 ){
		valid = false;
	}
	else if ( domain_url.indexOf("(") != -1 || domain_url.indexOf(")") != -1 || domain_url.indexOf("?") != -1 ){
		valid = false;
	}
	else if ( domain_url.indexOf("://") != -1 ){
		domain_url = domain_url.substr(domain_url.indexOf("://")+3, domain_url.length);
		$("#domain_url_box").val(domain_url);
	}
	if ( valid ){
		window.history.pushState({"html" :"", "pageTitle" : "state "+domain_url}, "", "/"+domain_url); 
		$("#inspect_button").addClass("disabled");
		$("#inspect_button").attr("onclick", "");
		return domain_url.toLowerCase();
	}
	else{
		if ( domain_url.charAt(0) == '/' ){
			domain_url = domain_url.replace("/", "");
		}
		window.history.pushState({"html" :"", "pageTitle" : "state "+domain_url}, "", "/"+domain_url); 
		$("#inspect_button").attr("data-toggle", "tooltip");
		$("#inspect_button").attr("title", "Please enter a valid domain!");
		$("#inspect_button").tooltip({
			'animation' : true,
			'placement' : 'bottom',
			'trigger' : 'manual',
			'delay' : 100
		});
		$("#inspect_button").tooltip('show');

		var msg = "Please enter a valid domain.".split("");
		updateDisplay(msg, "error");
		return null;
	}
}

function getExitStatusClass(code){

	switch(code){
		case 0:
			return "success";
		case 1:
			return "danger";
		default:
			return "warning";
	}
}

function getExitStatusIcon(code){

	switch(code){
		case 0:
			return "icon-ok-sign";
		case 1:
			return "icon-remove-sign";
		default:
			return "icon-warning-sign";
	}
}

var show_modal = true;

function showMessage(title, body, situation){

	$("#message_title").text(title);
	$("#message_body_area").attr("class", "modal-body "+situation);
	$("#message_body").text(body);
	if ( show_modal ){
		window.setTimeout(function(){
			$("#message").modal({'keyboard' : false, 'show' : true, 'backdrop' : true});
		}, 750);
	}
	$("message").on("hidden", function(){
		show_modal = true;
	});
	$("message").on("show", function(){
		show_modal = false;
	});
}

function composeButtons(domain_url, tests, situation){
	if ( tests == null ){
		$("#message_buttons").html("<button href='#' data-dismiss='modal' class='btn btn-"+situation+"'>Close</button>");
	}
	else{
		$("#message_buttons").html("<button id='retry_button' href='#' data-dismiss='modal' class='btn btn-danger'>Retry tests</button><button href='#' data-dismiss='modal' class='btn btn-"+situation+"'>Close</button>");
		$("#retry_button").attr("onclick", "retryTests('"+domain_url+"');");
	}
}


function finishLauncher(){

	var summary = "Inspection summary: ";
	if ( failed_tests.length == 0 ){
		var msg = "All tests were successful. Congratulations!".split("");
		updateDisplay(msg, "info");
		summary += "None of the tests failed! Congratulations!";
		composeButtons(domain_url, null, "success");
		showMessage("All tests finished properly!", summary, "success");
	}
	else{
		var msg =  " failed. Please fix these problems.";
		var summary_piece = " failed: "+failed_tests[0].name;
		for ( var i=1; i<failed_tests.length; i++ ){
			summary_piece += ", " + failed_tests[i].name;
		}
		summary_piece += ".";
		if ( failed_tests.length == 1 ){
			msg = ("One test"+msg).split("");
			summary_piece = ("One test"+summary_piece);
		}
		else{
			msg = (failed_tests.length+" tests"+msg).split("");
			summary_piece = (failed_tests.length+" tests"+summary_piece);
		}
		summary += summary_piece;
		updateDisplay(msg, "error");
		composeButtons(domain_url, failed_tests, "danger");
		showMessage("All tests finished!", summary, "danger");
	}
	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function finishRunningTestAgain(domain_url, data){

	data = JSON.parse(data);
	composeButtons(domain_url, null, getExitStatusClass(data.exit_status));
	if ( data.exit_status == 0 ){
		
		var msg = ("Test "+data.name+" was succesful!").split("");
		updateDisplay(msg, "info");
		showMessage(data.name+" passed!", data.output, getExitStatusClass(data.exit_status));
	}
	else{
		var msg = ("Test "+data.name+" failed!").split("");
		updateDisplay(msg, "error");
		showMessage(data.name+" failed!", data.output, getExitStatusClass(data.exit_status));
	}
	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}
