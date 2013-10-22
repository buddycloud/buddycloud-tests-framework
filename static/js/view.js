// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(domain_url){

	$("#test_launcher_status").html("Let's find out about <span class='domain_title'>"+domain_url+"</span>");
	$("#tests_output_table").html("");
}

// What to do in the page when a new test was issued just now
function handleTestCreation(test_name, test_source){

	$("#inspect_button").addClass("disabled");
	$("#inspect_button").attr("onclick", "");

	test_entry_html = "<div class='test_entry'>";
	test_entry_html += "<div style='display:table; width:100%;'>"
	test_entry_html += "<div style='display:table-row;'>";
	test_entry_html += "<div style='display:table-cell;'>";
	test_entry_html += "<span id='td_" + test_name + "' class='btn disabled test_name'>";
	test_entry_html += "<i id='ti_" + test_name + "' class='icon-random'></i>";
	test_entry_html += "<span>" + test_name + "</span>";
	test_entry_html += "</span>";
	test_entry_html += "</div>";
	test_entry_html += "<div style='display:table-cell;'>";
	test_entry_html += "<span id='ts_" + test_name + "' class='btn disabled test_source'>";
	test_entry_html += "<a href='https://" + test_source + "' target='_blank'>source</a></span>";
	test_entry_html += "</div>";
	test_entry_html += "</div>";
	test_entry_html += "</div>";	
	test_entry_html += "<span id='to_" + test_name + "' class='test_output input uneditable-input'>";
	test_entry_html += "Running this test...</span>";
	test_entry_html += "</div>";

	$("#tests_output_table").append(test_entry_html);
}

function handleTestRelaunch(test_name){

	$("#inspect_button").addClass("disabled");
	$("#inspect_button").attr("onclick", "");

	$("#td_"+test_name).attr("class", "btn disabled test_name");
	$("#td_"+test_name).attr("data-response", "");
	$("#td_"+test_name).attr("onclick", "");
	$("#ts_"+test_name).attr("class", "btn disabled test_source");
	$("#to_"+test_name).attr("class", "test_output uneditable-input");
	$("#to_"+test_name).html("Running this test again...");
	$("#ti_"+test_name).attr("class", "icon-random");
}

// What to do in the page once a test finishes running
function handleTestResponse(data){

	$("#td_"+data.name).addClass("btn-"+getExitStatusClass(data.exit_status));
	$("#td_"+data.name).removeClass("disabled");
	$("#td_"+data.name).attr("data-response", JSON.stringify(data));
	$("#td_"+data.name).attr("onclick", "focusOnTest('"+data.name+"');");
	$("#ts_"+data.name).addClass("btn-"+getExitStatusClass(data.exit_status));
	$("#ts_"+data.name).removeClass("disabled");
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

	var close = "<button href='#' data-dismiss='modal' class='btn btn-";
	close += situation + "'>Close</button>";	
	var retry = "<button id='retry_this_btn' href='#' data-dismiss='modal' class='btn btn-";
	retry += situation + "'>Retry this</button>" + close;
	var retryFails = "<button id='retry_all_failed_btn' href='#' data-dismiss='modal' class='btn";
	retryFails += " btn-" + situation + "'>Retry all that failed</button>" + retry;
	var retryAll = "<button id='retry_all_btn' href='#' data-dismiss='modal' class='btn btn-";
	retryAll += situation + "'>Retry all</button>" + retryFails;
	$("#message_buttons").html(retryAll);

	$("#retry_this_btn").attr("onclick", "runAgain('" + test_name + "', '" + domain_url + "');");
	$("#retry_all_failed_btn").attr("onclick", "retryTests('" + domain_url + "');");
	$("#retry_all_btn").attr("onclick", "startInspection();");
}


function finishLauncher(){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function finishRunningTestAgain(domain_url, data){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function focusOnTest(test_name){

	var exit_val = parseInt(JSON.parse($("#td_"+test_name).attr("data-response")).exit_status);
	var exit_status_class = getExitStatusClass(exit_val);
	createButtons(domain_url, test_name, exit_status_class);

	var msg = JSON.parse($("#td_" + test_name).attr("data-response"))['message'];
	showMessage(test_name, msg, exit_status_class);
}
