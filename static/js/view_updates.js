// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(domain_url){

	$("#test_launcher_status").html("Let's find out about <span class='domain_title'>"+domain_url+"</span>");
	$("#tests_output_table").html("");
}

// What to do in the page when a new test was issued just now
function handleTestCreation(test_name, test_source){

	test_entry_html = "<div class='test_entry'>";
	test_entry_html += "<span id='td_" + test_name + "' class='btn disabled test_name'>";
	test_entry_html += "<i id='ti_" + test_name + "' class='icon-random' style='padding:0px; margin:0px;'></i>";
	test_entry_html += "<span style='padding:0px; margin:0px; margin-left: 10px;'>" + test_name + "</span>";
	test_entry_html += "<a href='https://" + test_source + "' target='_blank' style='padding:0px; margin:0px; margin-left: 10px;'>source</a>";
	test_entry_html += "</span>";
	test_entry_html += "<span id='to_" + test_name + "' class='test_output input uneditable-input'>Running this test...</span>";
	test_entry_html += "</div>";

	$("#tests_output_table").append(test_entry_html);
/*	$("#td_"+test_name).popover({
		'title' : "Test ("+test_name+") Info",
		'content' : "<br/>Test source: <a href='https://"+test_source+"' target='_blank'>on github</a>",
		'trigger' : 'hover',
		'html' : true,
		'placement' : 'top',
		'delay' : { 'show' : 100, 'hide' : 3500 }
	});*/
}

function handleTestRelaunch(test_name){

	$("#td_"+test_name).attr("class", "btn disabled test_name");
	$("#td_"+data.name).attr("data-response", "");
	$("#td_"+test_name).attr("onclick", "");
	$("#to_"+test_name).attr("class", "test_output uneditable-input");
	$("#to_"+test_name).html("Running this test again...");
	$("#ti_"+test_name).attr("class", "icon-random");
}

// What to do in the page once a test finishes running
function handleTestResponse(data, domain_url){

	$("#td_"+data.name).addClass("btn-"+getExitStatusClass(data.exit_status));
	$("#td_"+data.name).attr("data-response", JSON.stringify(data));
/*	if ( data.exit_status == 1 ){
		$("#td_"+data.name).removeClass("disabled");
		//$("#td_"+data.name).attr("onclick", "runAgain('"+data.name+"', '"+domain_url+"', '"+getExitStatusClass(data.exit_status)+"');");
	}*/
	$("#td_"+data.name).removeClass("disabled");
	$("#td_"+data.name).attr("onclick", "focusOnTest('"+data.name+"');");
	$("#to_"+data.name).addClass(getExitStatusClass(data.exit_status));
	$("#to_"+data.name).html(data.briefing);
	$("#ti_"+data.name).attr("class", getExitStatusIcon(data.exit_status) + " icon-white");
}

function handleDomainURL(){

	$("#domain_url_box").tooltip("destroy");
	domain_url = $("#domain_url_box").val();
	domain_url = domain_url.trim();
	
	if ( domain_url.indexOf("://") != -1 ){
		domain_url = domain_url.substr(domain_url.indexOf("://")+3, domain_url.length);
		$("#domain_url_box").val(domain_url);
	}

	var valid_domain_regex = /^[a-z0-9]+([-.]{1}[a-z0-9]+)*.[a-z]{2,5}$/;

	var valid_domain = true;

	if ( domain_url == null ){

		valid_domain = false;
	}
	else {

		valid_domain = valid_domain_regex.test(domain_url);
	}

	if ( valid_domain ){
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
		$("#domain_url_box").attr("data-toggle", "tooltip");
		$("#domain_url_box").attr("title", "Please enter a valid domain!");
		$("#domain_url_box").tooltip({
			'animation' : true,
			'placement' : 'bottom',
			'trigger' : 'manual',
			'delay' : 100
		});
		$("#domain_url_box").tooltip('show');

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

	$("#message_title_wrap").attr("class", "modal-header btn btn-"+situation);
	$("#message_title").text(title);
	$("#message_body_area").attr("class", "modal-body "+situation);
	$("#message_body").html(body);
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

function createButtons(domain_url, test_name, situation){

	var buttons_html = "<button href='#' data-dismiss='modal' class='btn btn-" + situation + "'>Close</button>";	
	buttons_html = "<button id='retry_this_btn' href='#' data-dismiss='modal' class='btn btn-" + situation + "'>Retry this test</button>" + buttons_html;
	buttons_html = "<button id='retry_all_failed_btn' href='#' data-dismiss='modal' class='btn btn-" + situation + "'>Retry all failed tests</button>" + buttons_html;
	buttons_html = "<button id='retry_all_btn' href='#' data-dismiss='modal' class='btn btn-" + situation + "'>Retry all tests</button>" + buttons_html;
	$("#message_buttons").html(buttons_html);

	$("#retry_this_btn").attr("onclick", "runAgain('" + test_name + "', '" + domain_url + "');");
	$("#retry_all_failed_btn").attr("onclick", "retryTests('" + domain_url + "');");
	$("#retry_all_btn").attr("onclick", "startInspection();");
}


function finishLauncher(){

/*	var summary = "Inspection summary: ";
	if ( failed_tests.length == 0 ){
		
		summary += "None of the tests failed! Congratulations!";
		createButtons(domain_url, null, "success");
		showMessage("All tests finished properly!", summary, "success");
	}
	else{
		
		var summary_piece = " failed: "+failed_tests[0].test.name;
		
		for ( var i=1; i<failed_tests.length; i++ ){
		
			summary_piece += ", " + failed_tests[i].test.name;
		}
		
		summary_piece += ".";
		
		if ( failed_tests.length == 1 ){
			
			summary_piece = ("One test"+summary_piece);
		}
		else{

			summary_piece = (failed_tests.length+" tests"+summary_piece);
		}
		
		summary += summary_piece;

		var message = "<br/><br/>These tests failed because of the following reasons: ";

		for ( var i=0; i<failed_tests.length; i++ ){

			message += "<br/><strong>" + failed_tests[i].test.name + "</strong>: " + failed_tests[i].output.message
		}

		createButtons(domain_url, failed_tests.test, "danger");

		showMessage("All tests finished!", summary + message, "danger");
	}*/
	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function finishRunningTestAgain(domain_url, data){

/*	createButtons(domain_url, null, getExitStatusClass(data.exit_status));
	if ( data.exit_status == 0 ){
		
		showMessage(data.name+" passed!", data.message, getExitStatusClass(data.exit_status));
	}
	else{
		showMessage(data.name+" failed!", data.message, getExitStatusClass(data.exit_status));
	}*/
	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function focusOnTest(test_name){

	var exit_status_class = getExitStatusClass(parseInt(JSON.parse($("#td_"+test_name).attr("data-response")).exit_status));
	createButtons(domain_url, test_name, exit_status_class);

	var msg = JSON.parse($("#td_api_server_lookup").attr("data-response"))['message'];
	showMessage(test_name, msg, exit_status_class);
}
