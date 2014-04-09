// What to do in the page when a new test suite is about to run
function handleStartTestsLauncher(domain_url){

/*	var message = "Let's find out about <code>" + domain_url + "</code>";
	$("#tests_header_message").html(message);
	$("#tests_output").html("");*/
}

function doGetByCode(code, element){

	data = {
		 0: {
			'icon' : 'glyphicon-ok'
		    },
		 1: {
			'icon' : 'glyphicon-remove'
		    },
		 2: {
			'icon' : 'glyphicon-remove'
		    }
		}
	return data[code][element]
}

function handleResults(data, cancelling){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").addClass("active");
	$("#inspect_button").text("Stop");
	$("#inspect_button").attr("onclick", "stopInspection();");

	var domain_url = data.run_id;
	domain_url = domain_url.split("_")[0];
	data["domain_url"] = domain_url;

	for ( index in data.tests ){
		if ( data.tests[index].test_run_status == 2 ){
			var exit_status = data.tests[index].result.exit_status;
			var icon = doGetByCode(exit_status, "icon");
			data.tests[index].result["icon"] = icon;

			var briefing = data.tests[index].result.briefing;
			data.tests[index].result["heading"] = briefing;

			var message = data.tests[index].result.message;
			data.tests[index].result["information"] = message;

			data.tests[index].result["data"] = "";

		}
	}

	var template = $('#tests_output_template').html();
	Mustache.parse(template);
	var rendered = Mustache.render(template, data);
	$('#tests_output').html(rendered);

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

function showInformation(title, body){

	$("#message_title").text(title + " test results");
	$("#message_body_area").attr("class", "modal-body");
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

function finishLauncher(){

	$("#inspect_button").removeClass("disabled");
	$("#inspect_button").removeClass("active");
	$("#inspect_button").text("Check");
	$("#inspect_button").attr("onclick", "startInspection();");
}

function focusOnTest(test_name){

	var information = $("#"+test_name+" .result_information");
	information = information.attr("data-information");
	showInformation(test_name, information);
}
