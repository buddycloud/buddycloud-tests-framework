// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(domain_url){

	$("#tests_launcher_message").html("Let's find out about <span class='domain_title'>"+domain_url+"</span>");
	$("#tests_output").html("");
}

function doGetByCode(code, element){

	data = {
		 0: {
			'class' : 'test_success',
			'message' : '( This test was successful )'
		    },
		 1: {
			'class' : 'test_failure',
			'message' : '( This test failed )'
		    },
		 2: {
			'class' : 'test_warning',
			'message' : '( Something unexpected happened )'
		    }
		}
	return data[code][element]
}

// What to do in the page once a test finishes running
function handleTestCompletion(data){

	$("#td_"+data.name).attr("data-response", JSON.stringify(data));
	$(".test_entry > div > div > div:nth-child(1):has(#td_"+data.name+")").attr("onclick", "focusOnTest('"+data.name+"');");	
	$("#td_"+data.name).addClass(doGetByCode(data.exit_status, "class"));
	$("#td_"+data.name+"_content").html(doGetByCode(data.exit_status, "message"));
}

function handleResults(data, cancelling){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").addClass("active");
	$("#inspect_button").text("Stop");
	$("#inspect_button").attr("onclick", "stopInspection();");

	var template = $('#tests_output_template').html();
	Mustache.parse(template);
	var rendered = Mustache.render(template, data);
	$('#tests_output').html(rendered);

	for ( index in data.tests ){
		if (!cancelling){
			if ( data.tests[index].test_run_status == 1 ){
				$("#to_"+data.tests[index].name).html("Running this test...");
			}
			else if ( data.tests[index].test_run_status == 2 ){
				handleTestCompletion(data.tests[index].result);
			}
		}
		else{
			if ( data.tests[index].test_run_status == 2 ){
				handleTestCompletion(data.tests[index].result);
			}
			else{
				$("#to_"+data.tests[index].name).html("This test was cancelled.");
			}
		}
	}

	$(".test_entry > div > div:has(.test_success)")
		.css("background-color", "#F4F8FA");
	$(".test_entry > div > div:has(.test_success)")
		.css("color", "#5BC0DE");
	$(".test_entry > div > div > div:nth-child(1):has(.test_success)")
		.css("border-left-color", "#5BC0DE");
	$(".test_entry > div > div > div:nth-child(1):has(.test_success)")
		.hover(
			function(){
				$(this).css("cursor", "pointer");
				$(this).css("background", "linear-gradient(to right, #5BC0DE, transparent)");
				$(this).css("color", "white");
			},
			function(){
				$(this).css("cursor", "default");
				$(this).css("background", "none");
				$(this).css("color", "#5BC0DE");
			}
		);

	$(".test_entry > div > div:has(.test_failure)")
		.css("background-color", "#F2DEDE");
	$(".test_entry > div > div:has(.test_failure)")
		.css("color", "#D9534F");
	$(".test_entry > div > div > div:nth-child(1):has(.test_failure)")
		.css("border-left-color", "#D9534F");
	$(".test_entry > div > div > div:nth-child(1):has(.test_failure)")
		.hover(
			function(){
				$(this).css("cursor", "pointer");
				$(this).css("background", "linear-gradient(to right, #D9534F, transparent)");
				$(this).css("color", "white");
			},
			function(){
				$(this).css("cursor", "default");
				$(this).css("background", "none");
				$(this).css("color", "#D9534F");
			}
		);

	$(".test_entry > div > div:has(.test_warning)")
		.css("background-color", "#FCF8E3");
	$(".test_entry > div > div:has(.test_warning)")
		.css("color", "#F0AD4E");
	$(".test_entry > div > div > div:nth-child(1):has(.test_warning)")
		.css("border-left-color", "#F0AD4E");
	$(".test_entry > div > div > div:nth-child(1):has(.test_warning)")
		.hover(
			function(){
				$(this).css("cursor", "pointer");
				$(this).css("background", "linear-gradient(to right, #F0AD4E, transparent)");
				$(this).css("color", "white");
			},
			function(){
				$(this).css("cursor", "default");
				$(this).css("background", "none");
				$(this).css("color", "#F0AD4E");
			}
		);

	if ( data.run_status == 2){
		if (updaterId != null){
			clearInterval(updaterId);
		}
		finishLauncher();
	}
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
		$("#inspect_button").removeClass("disabled");
		$("#inspect_button").removeClass("active");
		$("#inspect_button").text("Check");
		$("#inspect_button").attr("onclick", "startInspection();");

		return null;
	}
}

var show_modal = true;

function showMessage(title, body, situation){

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

function createButtons(domain_url, test_name){

	var close = "<button href='#' data-dismiss='modal' class='btn'>Close</button>";	
	$("#message_buttons").html(close);
}


function finishLauncher(){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").removeClass("active");
	$("#inspect_button").text("Check");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function focusOnTest(test_name){

	var exit_val = parseInt(JSON.parse($("#td_"+test_name).attr("data-response")).exit_status);
	var exit_status_class = doGetByCode(exit_val, "class");
	createButtons(domain_url, test_name);

	var msg = JSON.parse($("#td_" + test_name).attr("data-response"))['message'];
	showMessage(test_name, msg, exit_status_class);
}
